"""实训 5-1：使用分类算法实现客户流失预测（决策树）"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = pd.read_excel('1communication.xlsx')

# 数据预处理：将文本特征转换为二进制数值
data['electronic_payment'] = data['electronic_payment'].map({True: 1, False: 0})
data['type'] = data['type'].map({True: 1, False: 0})

# 提取特征和标签
X = data[['educational_level', 'months', 'electronic_payment']]
y = data['type']

# 划分训练集和测试集（8:2）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 创建决策树分类器，以信息熵为划分准则
clf = DecisionTreeClassifier(criterion='entropy')

# 在训练集上训练模型
clf.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = clf.predict(X_test)

# 计算模型的准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"模型的准确率: {accuracy}")

# 新客户数据
new_data = pd.DataFrame({'educational_level': [5], 'months': [89], 'electronic_payment': [1]})

# 对新客户进行预测
prediction = clf.predict(new_data)
if prediction[0] == 0:
    print("销售预测数量结果: 未流失")
else:
    print("销售预测数量结果: 已流失")
