## CBAM at Faster-RCNN after roi align 
Spatial kernel size= 7 Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | C_Bias  | s_Bias  | Mem(MB) | box AP | ours   | Baseline |
|----------|-----------|---------|---------|---------|--------|--------|----------|
| R-50     | 4         | TRUE    | TRUE    | 5262    | 70.8   | 70.8   | 63.1     |
| R-50     | 16        | TRUE    | TRUE    | 5261    | 71.0   | 70.8   | 63.1     |
| R-50     | 32        | TRUE    | TRUE    | 5260    | 70.8   | 70.8   | 63.1     |
| R-101    | 4         | TRUE    | TRUE    | 6574    | 72.8   | 72.3   | 65.1     |
| R-101    | 16        | TRUE    | TRUE    | 6575    | 72.6   | 72.3   | 65.1     |




## CBAM at Faster-RCNN after FPN
Spatial kernel size= 7 Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | C_Bias  | s_Bias  | Mem(MB) | box AP | ours   | Baseline |
|----------|-----------|---------|---------|---------|--------|--------|----------|
| R-50     | 4         | TRUE    | TRUE    | 5261    | 70.7   | 70.8   | 63.1     |
| R-50     | 16        | TRUE    | TRUE    | 5262    | 71.4   | 70.8   | 63.1     |
| R-50     | 32        | TRUE    | TRUE    | 5261    | 71.3   | 70.8   | 63.1     |





