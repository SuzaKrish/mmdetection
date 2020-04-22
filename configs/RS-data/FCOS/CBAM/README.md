## CBAM at FCOS in bbox_head 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | cls-Reduction | reg-reduction | cls-Bias | reg-Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|---------------|---------------|----------|----------|---------|--------|--------|----------|
| R-50     | 4             | 4             | True     | True     | 3422    | 70.5   | 70.8   | 63.1     |
| R-50     | 16            | 16            | True     | True     | 3421    | 70.9   | 70.8   | 63.1     |


## CBAM at FCOS in FPN 
Train Method = trainval,  Seed = 1,   Determinitic = False 

| Backbone | Reduction | Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|-----------|------|---------|--------|--------|----------|



## CBAM at FCOS in Backbone
Train Method = trainval,  Seed = 1,   Determinitic = False 


| Backbone | Reduction | Bias | Mem(MB) | box AP | Ours   | Baseline |
|----------|-----------|------|---------|--------|--------|----------|
