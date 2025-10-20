import numpy as np
from scipy.optimize import minimize

# 定义目标函数（这里以最大化 w1 + w2 为例，可根据实际需求调整）
def objective(x):
    x1, y1, x2, y2 = x
    z1 = 400 * x1 + 200 * y1
    z2 = 400 * x2 + 200 * y2

    # 分段函数 w1
    w1 = 200 * z1 if z1 <= 50000 else 10000000 + 140 * z1
    # 分段函数 w2
    w2 = 200 * z2 if z2 <= 50000 else 10000000 + 140 * z2

    return -(w1 + w2)  # 最大化 w1 + w2，转换为最小化问题

# 定义约束条件
def constraint_sum_x(x):
    return (x[0] + x[1]) - 230  # x1 + x2 >= 230

def constraint_sum_x_max(x):
    return 1030 - (x[0] + x[1])  # x1 + x2 <= 1030

def constraint_sum_y(x):
    return (x[2] + x[3]) - 0  # y1 + y2 > 0（实际有效约束）

def constraint_sum_y_max(x):
    return 90 - (x[2] + x[3])  # y1 + y2 <= 90

# 初始猜测值
x0 = [100, 50, 100, 50]  # 可根据实际情况调整

# 约束条件
con_sum_x = {'type': 'ineq', 'fun': constraint_sum_x}
con_sum_x_max = {'type': 'ineq', 'fun': constraint_sum_x_max}
con_sum_y = {'type': 'ineq', 'fun': constraint_sum_y}
con_sum_y_max = {'type': 'ineq', 'fun': constraint_sum_y_max}

# 约束列表
constraints = [con_sum_x, con_sum_x_max, con_sum_y, con_sum_y_max]

# 变量边界（精简后的约束）
bounds = [(0, 150), (0, 90), (0, 150), (0, 90)]

# 求解优化问题
solution = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# 提取结果
x_opt = solution.x
x1_opt, y1_opt, x2_opt, y2_opt = x_opt

# 计算 z1, z2, w1, w2
z1_opt = 400 * x1_opt + 200 * y1_opt
z2_opt = 400 * x2_opt + 200 * y2_opt

w1_opt = 200 * z1_opt if z1_opt <= 50000 else 10000000 + 140 * z1_opt
w2_opt = 200 * z2_opt if z2_opt <= 50000 else 10000000 + 140 * z2_opt

# 输出结果
print("优化结果：")
print(f"x1 = {x1_opt:.2f}, y1 = {y1_opt:.2f}, x2 = {x2_opt:.2f}, y2 = {y2_opt:.2f}")
print(f"z1 = {z1_opt:.2f}, z2 = {z2_opt:.2f}")
print(f"w1 = {w1_opt:.2f}, w2 = {w2_opt:.2f}")
print(f"目标函数值（最大化 w1 + w2）：{-solution.fun:.2f}")
