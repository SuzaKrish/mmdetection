import argparse
import os, sys
import os.path as osp
import pickle
import shutil
import tempfile
import time

import mmcv
import torch
from mmdet import __version__
from mmdet import datasets

import torch.distributed as dist
from mmcv.parallel import MMDataParallel, MMDistributedDataParallel
from mmcv.runner import get_dist_info, init_dist, load_checkpoint

from mmdet.core import coco_eval, results2json, wrap_fp16_model
from mmdet.datasets import build_dataloader, build_dataset
from mmdet.models import build_detector

from mmdet.apis import get_root_logger
from tools.custom_eval import voc_eval


def check_fileDir(filePath, cover=0):
    import os
    out_file_dir = os.path.split(filePath)[0]
    if not os.path.isdir(out_file_dir):
        os.makedirs(out_file_dir)
    elif cover:
        shutil.rmtree(out_file_dir)
        os.makedirs(out_file_dir)


def get_valFilePath(saveDir, imgPath):
    imgPathList = imgPath.split('/')
    if imgPath.find('DeepMoon'):
        return os.path.join(saveDir, '/'.join(imgPathList[-3:-1]), imgPathList[-1].split('.')[0] + '.txt')
    else:
        return os.path.join(saveDir, imgPathList[-1].split('.')[0] + '.txt')


def keep_out(results, data_loader, saveDir):
    prog_bar = mmcv.ProgressBar(len(data_loader))
    for i, data in enumerate(data_loader):
        imgPath = data['img_meta'][0].data[0][0]['filename']
        im_save_path = get_valFilePath(saveDir, imgPath)
        check_fileDir(im_save_path)
        resultFile = open(im_save_path, 'w')
        resultFile.write('{}\n'.format(imgPath))
        dets = results[i][0]
        for det in dets:
            bbox = det[:4]
            score = det[4]
            resultFile.write('{:.1f} {:.1f} {:.1f} {:.1f} {:.3f}\n'.
                             format(bbox[0], bbox[1],
                                    bbox[2], bbox[3],
                                    score))
        resultFile.close()
        prog_bar.update()

def single_gpu_test(model, data_loader, show=False):
    model.eval()
    results = []
    dataset = data_loader.dataset
    prog_bar = mmcv.ProgressBar(len(dataset))
    for i, data in enumerate(data_loader):
        with torch.no_grad():
            result = model(return_loss=False, rescale=not show, **data)
        results.append(result)

        if show:
            model.module.show_result(data, result)

        batch_size = data['img'][0].size(0)
        for _ in range(batch_size):
            prog_bar.update()
    return results


def multi_gpu_test(model, data_loader, tmpdir=None, gpu_collect=False):
    """Test model with multiple gpus.

    This method tests model with multiple gpus and collects the results
    under two different modes: gpu and cpu modes. By setting 'gpu_collect=True'
    it encodes results to gpu tensors and use gpu communication for results
    collection. On cpu mode it saves the results on different gpus to 'tmpdir'
    and collects them by the rank 0 worker.

    Args:
        model (nn.Module): Model to be tested.
        data_loader (nn.Dataloader): Pytorch data loader.
        tmpdir (str): Path of directory to save the temporary results from
            different gpus under cpu mode.
        gpu_collect (bool): Option to use either gpu or cpu to collect results.

    Returns:
        list: The prediction results.
    """
    model.eval()
    results = []
    dataset = data_loader.dataset
    rank, world_size = get_dist_info()
    if rank == 0:
        prog_bar = mmcv.ProgressBar(len(dataset))
    for i, data in enumerate(data_loader):
        with torch.no_grad():
            result = model(return_loss=False, rescale=True, **data)
        results.append(result)

        if rank == 0:
            batch_size = data['img'][0].size(0)
            for _ in range(batch_size * world_size):
                prog_bar.update()

    # collect results from all ranks
    if gpu_collect:
        results = collect_results_gpu(results, len(dataset))
    else:
        results = collect_results_cpu(results, len(dataset), tmpdir)
    return results


def collect_results_cpu(result_part, size, tmpdir=None):
    rank, world_size = get_dist_info()
    # create a tmp dir if it is not specified
    if tmpdir is None:
        MAX_LEN = 512
        # 32 is whitespace
        dir_tensor = torch.full((MAX_LEN, ),
                                32,
                                dtype=torch.uint8,
                                device='cuda')
        if rank == 0:
            tmpdir = tempfile.mkdtemp()
            tmpdir = torch.tensor(
                bytearray(tmpdir.encode()), dtype=torch.uint8, device='cuda')
            dir_tensor[:len(tmpdir)] = tmpdir
        dist.broadcast(dir_tensor, 0)
        tmpdir = dir_tensor.cpu().numpy().tobytes().decode().rstrip()
    else:
        mmcv.mkdir_or_exist(tmpdir)
    # dump the part result to the dir
    mmcv.dump(result_part, osp.join(tmpdir, 'part_{}.pkl'.format(rank)))
    dist.barrier()
    # collect all parts
    if rank != 0:
        return None
    else:
        # load results of all parts from tmp dir
        part_list = []
        for i in range(world_size):
            part_file = osp.join(tmpdir, 'part_{}.pkl'.format(i))
            part_list.append(mmcv.load(part_file))
        # sort the results
        ordered_results = []
        for res in zip(*part_list):
            ordered_results.extend(list(res))
        # the dataloader may pad some samples
        ordered_results = ordered_results[:size]
        # remove tmp dir
        shutil.rmtree(tmpdir)
        return ordered_results


def collect_results_gpu(result_part, size):
    rank, world_size = get_dist_info()
    # dump result part to tensor with pickle
    part_tensor = torch.tensor(
        bytearray(pickle.dumps(result_part)), dtype=torch.uint8, device='cuda')
    # gather all result part tensor shape
    shape_tensor = torch.tensor(part_tensor.shape, device='cuda')
    shape_list = [shape_tensor.clone() for _ in range(world_size)]
    dist.all_gather(shape_list, shape_tensor)
    # padding result part tensor to max length
    shape_max = torch.tensor(shape_list).max()
    part_send = torch.zeros(shape_max, dtype=torch.uint8, device='cuda')
    part_send[:shape_tensor[0]] = part_tensor
    part_recv_list = [
        part_tensor.new_zeros(shape_max) for _ in range(world_size)
    ]
    # gather all result part
    dist.all_gather(part_recv_list, part_send)

    if rank == 0:
        part_list = []
        for recv, shape in zip(part_recv_list, shape_list):
            part_list.append(
                pickle.loads(recv[:shape[0]].cpu().numpy().tobytes()))
        # sort the results
        ordered_results = []
        for res in zip(*part_list):
            ordered_results.extend(list(res))
        # the dataloader may pad some samples
        ordered_results = ordered_results[:size]
        return ordered_results


def parse_args():
    parser = argparse.ArgumentParser(description='MMDet test detector')
    parser.add_argument('config', help='test config file path')
    parser.add_argument('checkpoint', help='checkpoint file')
    parser.add_argument(
        '--use_cache',
        action='store_true',
        help='use cache of outputs for testing')
    parser.add_argument('--out', help='output result file')
    parser.add_argument(
        '--keep_out',
        action='store_true',
        help='keep output result in original file format')
    parser.add_argument(
        '--json_out',
        help='output result file name without extension',
        type=str)
    parser.add_argument(
        '--metric',
        choices=['coco', 'voc'],
        default='voc',
        help='metric types')
    parser.add_argument(
        '--eval',
        type=str,
        nargs='+',
        choices=['proposal', 'proposal_fast', 'bbox', 'segm', 'keypoints'],
        help='eval types')
    parser.add_argument('--show', action='store_true', help='show results')
    parser.add_argument(
        '--gpu_collect',
        action='store_true',
        help='whether to use gpu to collect results')
    parser.add_argument('--tmpdir', help='tmp dir for writing some results')
    parser.add_argument(
        '--launcher',
        choices=['none', 'pytorch', 'slurm', 'mpi'],
        default='none',
        help='job launcher')
    parser.add_argument('--local_rank', type=int, default=0)
    args = parser.parse_args()
    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)
    return args


def main():
    args = parse_args()

    # assert args.out or args.show or args.json_out, \
    #     ('Please specify at least one operation (save or show the results) '
    #      'with the argument "--show" or "--json_out"')

    if args.out is not None and not args.out.endswith(('.pkl', '.pickle')):
        raise ValueError('The output file must be a pkl file.')

    if args.json_out is not None and args.json_out.endswith('.json'):
        args.json_out = args.json_out[:-5]

    cfg = mmcv.Config.fromfile(args.config)
    # set cudnn_benchmark
    if cfg.get('cudnn_benchmark', False):
        torch.backends.cudnn.benchmark = True
    cfg.model.pretrained = None
    cfg.data.test.test_mode = True

    # init distributed env first, since logger depends on the dist info.
    if args.launcher == 'none':
        distributed = False
    else:
        distributed = True
        init_dist(args.launcher, **cfg.dist_params)

    # create work_dir with timestamp tag
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    cfg.work_dir = osp.dirname(args.checkpoint)
    if args.out is None:
        args.out = osp.join(cfg.work_dir, '{}_{}'.format(timestamp, osp.basename(args.checkpoint).replace('pth', 'pkl')))

    mmcv.mkdir_or_exist(osp.abspath(cfg.work_dir))
    # init the logger before other steps
    log_file = osp.join(cfg.work_dir, '{}_test.log'.format(timestamp))
    logger = get_root_logger(log_file=log_file, log_level=cfg.log_level)

    # log some basic info
    logger.info('Command-line argument:\n{}'.format(' '.join(sys.argv[1:])))
    logger.info('Distributed training: {}'.format(distributed))
    logger.info('MMDetection Version: {}'.format(__version__))
    logger.info('Config:\n{}'.format(cfg.text))

    # build the dataloader
    # TODO: support multiple images per gpu (only minor changes are needed)
    dataset = build_dataset(cfg.data.test)
    data_loader = build_dataloader(
        dataset,
        imgs_per_gpu=1,
        workers_per_gpu=cfg.data.workers_per_gpu,
        dist=distributed,
        shuffle=False)

    # build the model and load checkpoint
    model = build_detector(cfg.model, train_cfg=None, test_cfg=cfg.test_cfg)
    fp16_cfg = cfg.get('fp16', None)
    if fp16_cfg is not None:
        wrap_fp16_model(model)
    checkpoint = load_checkpoint(model, args.checkpoint, map_location='cpu')
    # old versions did not save class info in checkpoints, this walkaround is
    # for backward compatibility
    if 'CLASSES' in checkpoint['meta']:
        model.CLASSES = checkpoint['meta']['CLASSES']
    else:
        model.CLASSES = dataset.CLASSES

    if args.use_cache and osp.exists(args.out):
        print('\nreuse results from {}'.format(args.out))
        outputs = mmcv.load(args.out)
    else:
        if not distributed:
            model = MMDataParallel(model, device_ids=[0])
            outputs = single_gpu_test(model, data_loader, args.show)
        else:
            model = MMDistributedDataParallel(model.cuda())
            outputs = multi_gpu_test(model, data_loader, args.tmpdir,
                                     args.gpu_collect)
        print('\nwriting results to {}'.format(args.out))
        mmcv.dump(outputs, args.out)

    if args.keep_out:
        saveDir = osp.join(cfg.work_dir, osp.basename(args.out).split('.')[0] + '_out')
        print('\nsaving results to {}'.format(saveDir))
        keep_out(outputs, data_loader, saveDir)

    rank, _ = get_dist_info()
    if rank == 0:
        metric_type = args.metric
        eval_types = args.eval
        if metric_type == 'coco' and eval_types:
            print('Starting evaluate {}'.format(' and '.join(eval_types)))
            if eval_types == ['proposal_fast']:
                result_file = args.out
                coco_eval(result_file, eval_types, dataset.coco)
            else:
                if not isinstance(outputs[0], dict):
                    result_files = results2json(dataset, outputs, args.out)
                    coco_eval(result_files, eval_types, dataset.coco)
                else:
                    for name in outputs[0]:
                        print('\nEvaluating {}'.format(name))
                        outputs_ = [out[name] for out in outputs]
                        result_file = args.out + '.{}'.format(name)
                        result_files = results2json(dataset, outputs_,
                                                    result_file)
                        coco_eval(result_files, eval_types, dataset.coco)

            # Save predictions in the COCO json format
            if args.json_out:
                if not isinstance(outputs[0], dict):
                    results2json(dataset, outputs, args.json_out)
                else:
                    for name in outputs[0]:
                        outputs_ = [out[name] for out in outputs]
                        result_file = args.json_out + '.{}'.format(name)
                        results2json(dataset, outputs_, result_file)

        elif metric_type == 'voc':
            # test_dataset = mmcv.runner.obj_from_dict(cfg.data.test, datasets)
            test_dataset = dataset
            voc_eval(args.out, test_dataset, logger=logger)


if __name__ == '__main__':
    main()
