## CBAM at Faster-RCNN after roi align 
Spatial kernel size= 7 Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | C_Bias  | s_Bias  | Mem(MB) | box AP | Non-SE | Baseline | GPU     |
|----------|-----------|---------|---------|---------|--------|--------|----------|---------|
| R-50     | 1         | TRUE    | TRUE    | 5053    | 70.5   | 68.3   | 63.1     | V100    |
| R-50     | 4         | TRUE    | TRUE    | 5052    | 70.9   | 68.3   | 63.1     | TITAN V |
| R-50     | 8         | TRUE    | TRUE    | 5052    | 70.9   | 68.3   | 63.1     | V100    |
| R-50     | 16        | TRUE    | TRUE    | 4888    | 70.8   | 68.3   | 63.1     | TITAN V |
| R-50     | 32        | TRUE    | TRUE    | 5051    | 71.1   | 68.3   | 63.1     | V100    |
| R-50     | 64        | TRUE    | TRUE    | 4888    | 69.5   | 68.3   | 63.1     | TITAN V |
| R-101    | 4         | TRUE    | TRUE    | 5051    | 72.7   | 68.3   | 63.1     | V100    |
| R-101    | 16        | TRUE    | TRUE    | 5051    | 72.3   | 68.3   | 63.1     | V100    |
| R-101    | 32        | TRUE    | TRUE    | 5051    | 72.8   | 68.3   | 63.1     | V100    |


## CBAM at Faster-RCNN after FPN
Spatial kernel size= 7 Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | C_Bias  | s_Bias  | Mem(MB) | box AP | Non-SE | Baseline | GPU     |
|----------|-----------|---------|---------|---------|--------|--------|----------|---------|
| R-50     | 4         | TRUE    | TRUE    | 5052    | 70.4   | 68.3   | 63.1     | TITAN V |
| R-50     | 8         | TRUE    | TRUE    | 5052    | 70.3   | 68.3   | 63.1     | V100    |
| R-50     | 16        | TRUE    | TRUE    | 4888    | 70.3   | 68.3   | 63.1     | TITAN V |
| R-50     | 32        | TRUE    | TRUE    | 5051    | 70.2   | 68.3   | 63.1     | V100    |


