# 数据挖掘课程实训（分类 / 聚类 / 关联规则）

分别覆盖**有监督分类**、**无监督聚类**与**关联规则挖掘**三类任务。

| 实验 | 任务 | 算法 | 数据规模 |
| --- | --- | --- | --- |
| 实训 5-1 | 客户流失预测 | 决策树分类 | — |
| 实训 5-2 | 超市客户聚类分析 | K-Means + 雷达图 | 469 条 |
| 实训 5-3 | 网址关联规则挖掘 | Apriori | 10527 条访问记录 |

---

## 实训 5-1：使用分类算法实现客户流失预测

### 数据

通信行业客户数据 `1communication.xlsx`，字段含 `educational_level`（教育水平）、`months`（在网月数）、`electronic_payment`（是否使用电子支付）、`type`（是否流失，标签）。

### 方法

1. **数据预处理**：将 `electronic_payment`、`type` 两个布尔型字段映射为 1 / 0。
2. **特征与标签**：特征取 `educational_level`、`months`、`electronic_payment` 三列，标签取 `type`。
3. **划分数据集**：`train_test_split(test_size=0.2, random_state=42)`，训练集与测试集 8:2。
4. **建模**：`DecisionTreeClassifier(criterion='entropy')`，以信息熵作为划分准则。
5. **评估**：`accuracy_score` 计算测试集准确率。
6. **预测**：构造新客户样本送入模型，输出「未流失 / 已流失」。

### 结果

测试集准确率 **0.745**。

---

## 实训 5-2：使用 K-Means 聚类算法实现超市客户聚类分析

### 数据

超市顾客购买行为数据 `2Supermarket-customers.xlsx`，以 `user_ID` 为索引，特征为 RFM 三维：`recency`、`frequence`、`monetary`。

### 方法

1. **导入数据**：以 `user_ID` 作为索引读取。
2. **数据标准化**：`(x - mean) / std`。
3. **聚类**：`KMeans(n_clusters=3, random_state=3)`。
4. **结果整理**：`value_counts()` 统计各类别数目，`cluster_centers_` 取出聚类中心，两者横向拼接后重命名表头输出。
5. **可视化**：绘制顾客特征聚类雷达图，三个维度为 recency / frequence / monetary，图例标注每个聚类的规模。

### 结果

将 **469** 名顾客聚为 3 类：

| 聚类 | 规模 | recency | frequence | monetary | 特征 |
| --- | --- | --- | --- | --- | --- |
| 聚类 0 | 204 | 0.957 | -0.553 | -0.510 | 近期有购买，频次与金额偏低 |
| 聚类 1 | 96 | -1.226 | 1.708 | 1.629 | 高频高额，但久未购买 |
| 聚类 2 | 169 | -0.459 | -0.303 | -0.310 | 三项指标均偏低 |

（表中数值为标准化后的聚类中心）

---

## 实训 5-3：使用 Apriori 算法挖掘网址间的相关关系

### 数据

用户访问记录 `3acc_records.csv`，含用户 IP 与访问 URL，共 10527 条。

### 方法

1. **读取与清洗**：按 `gb2312` 编码读取，列名规范为 `用户IP`、`URL`。
2. **会话聚合**：按用户 IP 分组，`agg(list)` 把同一用户的访问记录聚合为一个事务（即按 IP 去重后取浏览网址集合）。
3. **事务编码**：`mlxtend.preprocessing.TransactionEncoder` 将事务列表转为布尔矩阵。
4. **频繁项集**：`apriori(min_support=0.01)`，最小支持度取 1%（即至少 1% 的用户访问过）。
5. **关联规则**：`association_rules(metric="lift", min_threshold=1.0)`，以提升度大于 1.0 生成规则。

### 结果

挖掘出频繁项集与关联规则，用于识别网址之间的共访关系。支持度区间约 0.010 ~ 0.049。

---

## 环境要求

```bash
pip install -r requirements.txt
```

每个实验的文件放到对应子目录，按各目录内 README 或脚本注释运行。

## 目录结构

```
data-mining-coursework/
├── README.md
├── requirements.txt
├── .gitignore
├── lab5-1_churn_prediction/
│   └── churn_decision_tree.py
├── lab5-2_customer_clustering/
│   └── kmeans_radar.py
└── lab5-3_url_association/
    └── apriori_urls.py
```

> 三个实验的数据集（`1communication.xlsx`、`2Supermarket-customers.xlsx`、`3acc_records.csv`）未包含在本仓库中，字段说明见各实验的「数据」一节。

## 说明

- 课程实训项目，按实验指导书给定的实验任务独立完成编码、运行与结果整理。
- 雷达图中文标签依赖 `SimHei` 字体。
- 原始数据集未上传。
