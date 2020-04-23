## SE at FCOS in bbox_head 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | cls-Reduction | reg-reduction | cls-Bias | reg-Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|---------------|---------------|----------|----------|---------|--------|--------|----------|
| R-50     | 4             | 4             | True     | True     | 3368    | 71.2   | 70.8   | 63.1     |
| R-50     | 16            | 16            | True     | True     | 3367    | 71.2   | 70.8   | 63.1     |
| R-50     | 32            | 32            | True     | True     | 3367    | 70.2   | 70.8   | 63.1     |
| R-101    | 4             | 4             | True     | True     | 4677    | 71.5   | 72.3   | 63.1     |
| R-101    | 16            | 16            | True     | True     | 4677    | 72.0   | 72.3   | 63.1     |

## SE at FCOS in FPN 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|-----------|------|---------|--------|--------|----------|
| R-50     | 4         | True | 3340    | 72.0   | 70.8   | 63.1     |
| R-50     | 16        | True | 3339    | 70.9   | 70.8   | 63.1     |
| R-50     | 32        | True | 3339    | 71.8   | 70.8   | 63.1     |



## SE at FCOS in Backbone
Train Method = trainval,  Seed = 1,   Determinitic = False 


| Backbone | Reduction | Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|-----------|------|---------|--------|--------|----------|
| R-50     | 4         | True | 3778    | 70.8   | 70.8   | 63.1     |
| R-50     | 16        | True | 3662    | 71.3   | 70.8   | 63.1     |
