#!/usr/bin/env bash

name="faster_rcnn_r50_fpn_1x_voc07_1gpu"

#timestamp="20200106_142452"
#timestamp="20200107_163527"
timestamp="20200108_102109"

model="${name}_${timestamp}"
checkpoint="latest"

python test.py ../configs/pascal_voc/$model.py \
../results/pascal_voc/$name/$timestamp/$checkpoint.pth \
--out ../results/pascal_voc/$name/$timestamp/$checkpoint.pkl

python voc_eval.py ../results/pascal_voc/$name/$timestamp/$checkpoint.pkl \
../configs/pascal_voc/$model.py