import numpy as np

# 输入时间矩阵
cost_matrix = np.array([
    [15, 18, 21, 24],
    [19, 23, 22, 18],
    [26, 18, 16, 19],
    [19, 21, 23, 17]
])

# 使用 Scipy 求解
from scipy.optimize import linear_sum_assignment
row_ind, col_ind = linear_sum_assignment(cost_matrix)
total_cost = cost_matrix[row_ind, col_ind].sum()

# 输出结果
print("最优分配方案:")
for i, j in zip(row_ind, col_ind):
    print(f"工人{i+1} → 任务{j+1}")
print(f"总完成时间: {total_cost} 分钟")
