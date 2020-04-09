## SE at FCOS in bbox_head 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | cls-Reduction | reg-reduction | cls-Bias | reg-Bias | Mem(MB) | box AP | Non-SE | Baseline |
|----------|---------------|---------------|----------|----------|---------|--------|--------|----------|
| R-50     | 4             | 4             | TRUE     | TRUE     | 3367    | 71.0   | 68.3   | 63.1     |
| R-50     | 16            | 16            | TRUE     | TRUE     | 3367    | 71.6   | 68.3   | 63.1     |
| R-101    | 4             | 4             | TRUE     | TRUE     | 4676    | 72.5   | 68.3   | 63.1     |
| R-101    | 16            | 16            | TRUE     | TRUE     | 4676    | 72.4   | 68.3   | 63.1     |

## SE at FCOS in FPN 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias | Mem(MB) | box AP | Non-SE | Baseline |
|----------|-----------|------|---------|--------|--------|----------|
| R-50     | 4         | TRUE | 3314    | 72.1   | 68.3   | 63.1     |
| R-50     | 16        | TRUE | 3312    | 71.2   | 68.3   | 63.1     |
