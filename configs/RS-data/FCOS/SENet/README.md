## SE at FCOS in bbox_head 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | cls-Reduction | reg-reduction | cls-Bias | reg-Bias | Mem(MB) | box AP | Non-SE | Baseline |
|----------|---------------|---------------|----------|----------|---------|--------|--------|----------|


## SE at FCOS in FPN 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|-----------|------|---------|--------|--------|----------|
| R-50     | 4         | True | 3340    | 72.0   | 70.8   | 63.1     |
| R-50     | 4         | True | 3339    | 70.9   | 70.8   | 63.1     |

