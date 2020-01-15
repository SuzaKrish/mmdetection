# Latest 

### FCOS at 20191223


| Backbone | Style | GN | MS train | Lr schd | Mem(GB) | Train time(s/iter) | Inf time(fps) | box AP |
|----------|-------|----|----------|---------|---------|--------------------|---------------|--------|
| R-50     | caffe | N  | N        | 1x      | 7.0+    | -                  | -             | 62.11  |
| R-101    | caffe | N  | Y        | 2x      | 11.5    | -                  | -             | 67.79  |
| X101     | caffe | N  | Y        | 2x      | 11.6    | -                  | -             | 63.15  |

### Faster-RCNN at 20191223

| Backbone | Seed | Deterministic | Mem(GB) | Train time(s/iter) | Inf time(fps) | box AP |
|----------|------|---------------|---------|--------------------|---------------|--------|
| R-50     | 1    | TRUE          | -       | -                  | -             | 64.55  |
| R-101    | 2    | TRUE          | -       | -                  | -             | 69.82  |
| X101     | 3    | TRUE          | -       | -                  | -             | 60.37  |
