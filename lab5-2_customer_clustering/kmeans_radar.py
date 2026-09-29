"""实训 5-2：使用 K-Means 聚类算法实现超市客户聚类分析（RFM 三维 + 雷达图）"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 导入数据，并以 user_ID 作为索引
features = pd.read_excel('2Supermarket-customers.xlsx', index_col='user_ID')

# 数据标准化
features_scaler = 1.0 * (features - features.mean()) / features.std()

# 开始聚类，限定聚类中心数为 3
model = KMeans(n_clusters=3, random_state=3)
model.fit(features_scaler)

# 统计各个类别的数目
r1 = pd.Series(model.labels_).value_counts()
# 找出聚类中心
r2 = pd.DataFrame(model.cluster_centers_)
# 横向连接，得到聚类中心对应的类别下的数目（0 是纵向）
r = pd.concat([r2, r1], axis=1)
r.columns = list(features.columns) + ['类别数目']
print(r)

# 详细输出原始数据及对应的类别
r = pd.concat([features, pd.Series(model.labels_, index=features.index)], axis=1)
r.columns = list(features.columns) + ['聚类类别']


# 2. 雷达图可视化 ==============================================
def plot_radar_chart(cluster_centers, feature_names, title="顾客特征聚类雷达图"):
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    n_features = len(feature_names)
    angles = np.linspace(0, 2 * np.pi, n_features, endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # 设置雷达图的坐标：起始位置在顶部，顺时针方向
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # 绘制每个聚类的雷达图
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i in range(len(cluster_centers)):
        values = cluster_centers[i].tolist()
        values += values[:1]  # 闭合图形
        ax.plot(angles, values, color=colors[i], linewidth=2, linestyle='solid',
                label=f'聚类 {i} (n={r1[i]})')
        ax.fill(angles, values, color=colors[i], alpha=0.25)

    # 添加特征标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_names, fontsize=10)

    # 添加标题和图例
    plt.title(title, fontsize=14, y=1.08)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))


# 调用雷达图绘制函数
plot_radar_chart(model.cluster_centers_, features.columns.tolist())
plt.show()
