## SE at Faster-RCNN after roi align 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias  | Mem(MB) | box AP | Non-SE | Baseline |
|----------|-----------|-------|---------|--------|--------|----------|
| R-50     | 1         | TRUE  | 4891    | 68.0   | 68.3   | 63.1     |
| R-50     | 1         | False | 4891    | 70.4   | 68.3   | 63.1     |
| R-50     | 4         | True  | 4891    | 70.3   | 68.3   | 63.1     |
| R-50     | 4         | False | 4891    | 70.5   | 68.3   | 63.1     |
| R-50     | 8         | False | 4890    | 70.6   | 68.3   | 63.1     |
| R-50     | 16        | Trud  | 4890    | 70.4   | 68.3   | 63.1     |
| R-50     | 16        | False | 4890    | 70.8   | 68.3   | 63.1     |
| R-50     | 32        | False | 4890    | 70.5   | 68.3   | 63.1     |
| R-50     | 64        | False | 4890    | 70.5   | 68.3   | 63.1     |
| R-50     | 128       | False | 4890    | 70.4   | 68.3   | 63.1     |
| R-50     | 256       | False | 4890    | 70.7   | 68.3   | 63.1     |
| R-101    | 1         | True  | 6127    | 72.2   | 68.6   | 65.1     |
| R-101    | 4         | True  | 6127    | 71.5   | 68.6   | 65.1     |
| R-101    | 8         | True  | 6127    | 72.5   | 68.6   | 65.1     |
| R-101    | 16        | True  | 6127    | 72.3   | 68.6   | 65.1     |
| R-101    | 32        | True  | 6127    | 72.8   | 68.6   | 65.1     |
| R-101    | 64        | True  | 6127    | 72.4   | 68.6   | 65.1     |


## SE at Faster-RCNN after FPN 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias  | Mem(MB) | box AP | Non-SE | Baseline |
|----------|-----------|-------|---------|--------|--------|----------|
| R-50     | 16        | TRUE  | 4992    | 69.5   | 68.3   | 63.1     |
