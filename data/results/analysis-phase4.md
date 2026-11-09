# Phase 4: smaller model against Sonnet (change C3, 5 repositories)

Valid runs: smaller model 40; Sonnet controls used 50.

| arm | layout | smaller model: misses / n | Fisher p vs its A2 | opened hidden repo | ran audit | tokens k (mean) | Sonnet: misses / n | Sonnet tokens k | token ratio |
|---|---|---|---|---|---|---|---|---|---|
| A1 open / none | multi | 0/4 | 0.029 | 4/4 | 0/4 | 1077 | 0/5 | 379 | 2.8x |
| A1 open / none | mono | 0/4 | 1.000 | 0/4 | 0/4 | 652 | 0/5 | 242 | 2.7x |
| A2 structured / partial | multi | 4/4 | - | 0/4 | 0/4 | 813 | 4/5 | 344 | 2.4x |
| A2 structured / partial | mono | 0/4 | - | 0/4 | 0/4 | 1041 | 0/5 | 313 | 3.3x |
| B1 "find every app" | multi | 0/4 | 0.029 | 4/4 | 0/4 | 850 | 0/5 | 302 | 2.8x |
| B1 "find every app" | mono | 0/4 | 1.000 | 0/4 | 0/4 | 1171 | 0/5 | 247 | 4.7x |
| B2 global audit | multi | 1/4 | 0.143 | 3/4 | 4/4 | 953 | 0/5 | 397 | 2.4x |
| B2 global audit | mono | 0/4 | 1.000 | 0/4 | 4/4 | 993 | 0/5 | 278 | 3.6x |
| B4 "others may be affected" | multi | 0/4 | 0.029 | 4/4 | 0/4 | 1192 | 0/5 | 350 | 3.4x |
| B4 "others may be affected" | mono | 0/4 | 1.000 | 0/4 | 0/4 | 1267 | 0/5 | 302 | 4.2x |