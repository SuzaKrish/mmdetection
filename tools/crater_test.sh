#!/usr/bin/env bash

name="faster_rcnn_r50_fpn_1x_divide3_1gpu"

timestamp="20200108_174857"
#timestamp="20200109_000232"

model="${name}"
checkpoint="latest"

python test.py ../configs/moon_crater/$model.py \
../results/moon_crater/$name/$timestamp/$checkpoint.pth \
--out ../results/moon_crater/$name/$timestamp/$checkpoint.pkl

python voc_eval.py ../results/moon_crater/$name/$timestamp/$checkpoint.pkl \
../configs/moon_crater/$model.py