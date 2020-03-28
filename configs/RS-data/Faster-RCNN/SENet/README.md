### Faster-RCNN at 20200223

| Backbone |Train Method | Seed | Deterministic | Mem(MB) | Train time (s/iter) | Test time (task/s) | box AP | Baseline |
|----------|-------------|------|---------------|---------|---------------------|--------------------|--------|----------|
| R-50     |train+val    | 1    | FALSE         | 2593    | 0.2                 | 27                 | 55.1   | 63.1     |
| R-50     |trainval     | 1    | FALSE         | 2928    | 0.22                | 27                 | 64.2   | 63.1     |
| R-50     |train+val    | 2    | FALSE         | 2593    | 0.2                 | 27                 | 55.4   | 63.1     |
| R-50     |trainval     | 2    | FALSE         | 2926    | 0.2                 | 27                 | 64.7   | 63.1     |
| R-50     |train+val    | 3    | FALSE         | 2751    | 0.16                | 28                 | 54.8   | 63.1     |
| R-50     |trainval     | 3    | FALSE         | 2927    | 0.2                 | 27                 | 64.2   | 63.1     |
| R-101    |train+val    | 1    | FALSE         | 5744    | 0.27                | 18                 | 60.6   | 65.1     |
| R-101    |trainval     | 1    | FALSE         | 6129    | 0.28                | 18                 | 70     | 65.1     |
| R-101    |train+val    | 2    | FALSE         | 5743    | 0.27                | 18                 | 59.3   | 65.1     |
| R-101    |trainval     | 2    | FALSE         | 6363    | 0.28                | 18                 | 70.1   | 65.1     |
| R-101    |train+val    | 3    | FALSE         | 5509    | 0.39                | 18                 | 60     | 65.1     |
| R-101    |trainval     | 3    | FALSE         | 6364    | 0.28                | 18                 | 69.7   | 65.1     |
