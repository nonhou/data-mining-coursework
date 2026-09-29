"""实训 5-3：使用 Apriori 算法挖掘网址间的相关关系"""
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# 读取 CSV 文件
df = pd.read_csv('3acc_records.csv', encoding='gb2312')

# 清理列名
df.columns = ['用户IP', 'URL']

# 对用户 IP 进行去重并聚合访问记录
user_visits = df.groupby('用户IP')['URL'].agg(list).reset_index()

# 转换为事务列表
transactions = user_visits['URL'].tolist()

# 使用 Apriori 算法挖掘关联规则
te = TransactionEncoder()
te_ary = te.fit_transform(transactions)
trans_df = pd.DataFrame(te_ary, columns=te.columns_)

# 计算频繁项集（根据数据量调整最小支持度）：1% 的用户访问过
min_support = 0.01
frequent_itemsets = apriori(trans_df, min_support=min_support, use_colnames=True)

print(trans_df)
print(frequent_itemsets)

# 生成关联规则：提升度大于 1.0
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
print(rules)
