```
数据 → 正态性检验(Shapiro-Wilk) → 
  ├─ 非正态 → 非参数检验（Mann-Whitney/Kruskal-Wallis）
  └─ 正态 → 方差齐性检验 (F检验/Levene检验) → 
      ├─ 方差齐 → 参数检验（t 检验/ANOVA）
      └─ 方差不齐 → 稳健参数检验（Welch t 检验/Welch ANOVA）
```