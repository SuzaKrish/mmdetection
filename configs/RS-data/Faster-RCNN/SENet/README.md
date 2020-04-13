## SE at Faster-RCNN after roi align 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias  | Mem(MB) | box AP | Ours   | Baseline |
|----------|-----------|-------|---------|--------|--------|----------|
| R-50     | 4         | True  | 5052    | 71.3   | 70.8   | 63.1     |
| R-50     | 4         | True  | 5052    | 71.1   | 70.8   | 63.1     |
| R-50     | 16        | True  | 5051    | 71.2   | 70.8   | 63.1     |
| R-50     | 32        | True  | 5051    | 70.7   | 70.8   | 63.1     |



## SE at Faster-RCNN after FPN 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias  | Mem(MB) | box AP | Non-SE | Baseline |
|----------|-----------|-------|---------|--------|--------|----------|
| R-50     | 4         | TRUE  | 4992    | 71.1   | 70.8   | 63.1     |
