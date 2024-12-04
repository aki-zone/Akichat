import pandas as pd

####################################################################
#########################  修正CSV文件的表单  ########################
####################################################################


# 读取CSV文件
df = pd.read_csv("E:\\PC_Desktop\\AAAAATEST\\时差统计单.csv", encoding="gbk")

# 计算每100行的平均值
num_rows = len(df)
df_100 = df['延迟差(ms)'].iloc[0:num_rows].rolling(window=100).mean()[99::100]  # 每100行的平均值
df_1000 = df['延迟差(ms)'].iloc[0:num_rows].rolling(window=1000).mean()[999::1000]  # 每1000行的平均值
df_10000 = df['延迟差(ms)'].iloc[0:num_rows].rolling(window=10000).mean()[9999::10000]  # 每10000行的平均值

# 计算全部行的平均值
all_rows_mean = df['延迟差(ms)'].mean()

# 新建一个DataFrame用于保存这些统计数据
result_df = pd.DataFrame({
    '每100条平均值(ms)': df_100,
    '每1000条平均值(ms)': df_1000,
    '每10000条平均值(ms)': df_10000,
    '全部条平均值(ms)': [all_rows_mean] * len(df_100)  # 确保'全部行平均值'在每行都显示相同的均值
})

# 保存新的CSV文件
result_df.to_csv("E:\\PC_Desktop\\AAAAATEST\\时差统计单_总结.csv", index=False)
