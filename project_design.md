# 蚁群算法解 TSP 项目设计文档

## 目录
1. [项目概述](#1-项目概述)
2. [系统架构图](#2-系统架构图)
3. [类关系图](#3-类关系图)
4. [算法流程图](#4-算法流程图)
5. [核心公式推导](#5-核心公式推导)
6. [模块详细说明](#6-模块详细说明)
7. [参数调优建议](#7-参数调优建议)
8. [扩展与优化方向](#8-扩展与优化方向)

---

## 1. 项目概述

### 1.1 项目简介
本项目是一个**纯 Python 实现**的蚁群算法（Ant Colony Optimization, ACO），用于解决旅行商问题（Traveling Salesman Problem, TSP）。项目采用模块化设计，不依赖 numpy 等第三方科学计算库，具有良好的可读性和可扩展性。

### 1.2 TSP 问题定义
给定 n 个城市和两两城市间的距离，找到一条经过每个城市恰好一次并返回起点的最短路径。

数学定义：
- 输入：城市集合 C = {c₁, c₂, ..., cₙ}，距离矩阵 D = [dᵢⱼ]，其中 dᵢⱼ 是城市 i 到城市 j 的距离
- 输出：城市排列 π = (π₁, π₂, ..., πₙ)，使得总距离 Σd_{πᵢπᵢ₊₁} + d_{πₙπ₁} 最小

### 1.3 蚁群算法原理
蚁群算法模拟真实蚂蚁群体的觅食行为：
- 蚂蚁在路径上释放信息素（pheromone）
- 蚂蚁倾向于选择信息素浓度高的路径
- 信息素会随时间挥发
- 较短路径上的信息素累积更快

---

## 2. 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           蚁群算法系统架构                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐     ┌─────────────┐     ┌──────────────────────────┐   │
│  │   Examples  │     │   Config    │     │        Utils             │   │
│  │ (测试实例)  │     │ (配置参数)  │     │  (数学工具/可视化)       │   │
│  └──────┬──────┘     └──────┬──────┘     └────────────┬─────────────┘   │
│         │                   │                         │                 │
│         ▼                   ▼                         ▼                 │
│  ┌─────────────┐     ┌─────────────┐     ┌──────────────────────────┐   │
│  │    Graph    │────►│  AntColony  │◄────│       Visualizer         │   │
│  │  (图结构)   │     │  (蚁群)     │     │       (可视化)           │   │
│  └─────────────┘     └──────┬──────┘     └──────────────────────────┘   │
│                             │                                            │
│                             ▼                                            │
│  ┌─────────────┐     ┌─────────────┐                                    │
│  │     Ant     │◄────┤    Main     │                                    │
│  │   (蚂蚁)    │     │  (主程序)   │                                    │
│  └─────────────┘     └─────────────┘                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

数据流方向：
1. 测试实例 → Graph（构建距离矩阵）
2. Config → AntColony（配置算法参数）
3. AntColony → Ant（创建和管理蚂蚁）
4. Ant → Graph（访问距离和信息素信息）
5. AntColony → Graph（更新信息素）
6. AntColony → Visualizer（输出结果可视化）
```

### 2.1 架构分层

| 层级 | 模块 | 职责 |
|------|------|------|
| **应用层** | `main.py` | 命令行接口、实验 orchestration |
| **算法层** | `AntColony` | 算法流程控制、信息素更新 |
| **实体层** | `Ant`, `Graph` | 蚂蚁行为、图数据结构 |
| **配置层** | `ACOConfig` | 参数管理与验证 |
| **工具层** | `MathUtils`, `Visualizer` | 数学计算、结果可视化 |
| **测试层** | `TSPInstances` | 标准测试用例 |

---

## 3. 类关系图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            类关系图                                     │
└─────────────────────────────────────────────────────────────────────────┘

                ┌─────────────────────────────────────────┐
                │              ACOConfig                  │
                │  (配置参数与验证)                       │
                │  - alpha: float                        │
                │  - beta: float                         │
                │  - rho: float                          │
                │  - q: float                            │
                │  - num_ants: int                       │
                │  - max_iterations: int                 │
                │  - initial_pheromone: float            │
                │  + _validate()                         │
                └─────────────────────────────────────────┘
                              │
                              │ 配置
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          AntColony                              │
│  (蚁群控制器)                                                   │
│  - graph: Graph                                                 │
│  - config: ACOConfig                                            │
│  - ants: List[Ant]                                              │
│  - best_path: List[int]                                         │
│  - best_distance: float                                         │
│  - history: List[Tuple]                                         │
│  + run(callback) → (path, dist)                                 │
│  + _run_iteration() → distances                                │
│  + _update_pheromone()                                          │
│  + get_convergence_data()                                       │
│  + reset()                                                      │
└─────────────────────────────────────────────────────────────────┘
            │                                      │
            │ 包含                                  │ 使用
            ▼                                      ▼
┌─────────────────────────┐         ┌─────────────────────────────────┐
│           Ant           │         │              Graph              │
│  (单只蚂蚁)              │         │  (图数据结构)                   │
│  - ant_id: int          │         │  - cities: List[Tuple]          │
│  - graph: Graph         │         │  - num_cities: int              │
│  - config: ACOConfig    │         │  - distance_matrix: List[List]  │
│  - path: List[int]      │         │  - pheromone_matrix: List[List] │
│  - visited: List[bool]  │         │  + _build_distance_matrix()     │
│  - path_distance: float │         │  + initialize_pheromone()       │
│  + reset(start_city)    │         │  + get_distance(i, j)           │
│  + select_next_city()   │         │  + get_pheromone(i, j)          │
│  + move_to(city)        │         │  + update_pheromone(i, j, delta)│
│  + complete_tour()      │         │  + evaporate_pheromone(rho)     │
│  + get_pheromone_delta()│         │  + calculate_path_distance(path)│
└─────────────────────────┘         └─────────────────────────────────┘
                                                              │
                                                              │ 使用
                                                              ▼
┌─────────────────────────────────────────┐         ┌─────────────────┐
│              MathUtils                  │         │   Visualizer    │
│  (数学工具)                              │         │  (可视化)       │
│  + euclidean_distance(p1, p2)           │         │  + draw_convergence_chart()│
│  + generate_random_cities(n)            │         │  + draw_path()  │
│  + calculate_path_distance(cities, path)│         │  + print_statistics()      │
│  + normalize(values)                    │         │  + progress_bar()│
│  + mean/std_dev(values)                 │         └─────────────────┘
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│              TSPInstances               │
│  (测试实例集合)                          │
│  + get_small_instance()                 │
│  + get_medium_instance()                │
│  + get_large_instance()                 │
│  + get_circle_instance(n)               │
│  + get_grid_instance(rows, cols)        │
│  + get_cluster_instance()               │
└─────────────────────────────────────────┘
```

### 3.1 类关系说明

| 关系类型 | 类对 | 说明 |
|---------|------|------|
| **组合** | `AntColony` → `Ant` | 蚁群包含多个蚂蚁（1:num_ants） |
| **依赖** | `AntColony` → `Graph` | 蚁群使用图进行计算 |
| **依赖** | `Ant` → `Graph` | 蚂蚁访问图的距离和信息素信息 |
| **依赖** | `Ant` → `ACOConfig` | 蚂蚁使用配置参数进行决策 |
| **关联** | `AntColony` → `ACOConfig` | 蚁群持有配置引用 |
| **工具** | `*` → `MathUtils` | 所有类都可能使用数学工具 |
| **工具** | `AntColony` → `Visualizer` | 结果可视化 |

---

## 4. 算法流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        蚁群算法执行流程图                                │
└─────────────────────────────────────────────────────────────────────────┘

     ┌─────────────────────────────────────────────────────────┐
     │                    开始                                 │
     └─────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. 初始化                                                       │
│    ├─ 加载城市坐标                                              │
│    ├─ 构建距离矩阵 D[i][j]                                      │
│    ├─ 初始化信息素矩阵 τ[i][j] = τ₀                              │
│    └─ 创建蚂蚁种群（num_ants 只蚂蚁）                            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. 迭代开始 (iter = 1 到 max_iterations)                        │
│    ┌─────────────────────────────────────────────────────┐     │
│    │ 3. 每只蚂蚁构建路径                                   │     │
│    │   ├─ 随机选择起点城市                                │     │
│    │   ├─ 初始化 visited 标记                            │     │
│    │   └─ ┌─────────────────────────────────────────┐    │     │
│    │      │ 4. 选择下一个城市                       │    │     │
│    │      │   ├─ 计算转移概率 Pᵢⱼ                   │    │     │
│    │      │   ├─ 轮盘赌选择                        │    │     │
│    │      │   ├─ 移动到新城市                       │    │     │
│    │      │   └─ 标记为已访问                       │    │     │
│    │      └───────────────┬─────────────────────────┘    │     │
│    │                      │ 还有未访问城市？              │     │
│    │                      │ No  ───────────────────────┐ │     │
│    │                      │ Yes                        ▼ │     │
│    │                      └────────────────────────────┘ │     │
│    │                            ↓ 完成所有城市访问        │     │
│    │   ├─ 计算路径总距离 L_k                              │     │
│    │   └─ 返回起点闭合路径                                │     │
│    └─────────────────────────────────────────────────────┘     │
│                               │                                │
│                               ▼                                │
┌─────────────────────────────────────────────────────────────────┐
│ 5. 更新全局最优解                                               │
│    └─ if min(L_k) < best_distance: 更新 best_path 和 best_distance │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. 更新信息素                                                   │
│    ├─ 信息素挥发：τ[i][j] = τ[i][j] * (1 - ρ)                   │
│    └─ 蚂蚁释放信息素：τ[i][j] += ΣΔτᵏ[i][j]                      │
│       其中 Δτᵏ[i][j] = Q / L_k （如果边 (i,j) 在第 k 只蚂蚁路径上）│
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ 达到最大迭代次数？
                               │ No ───────────────────────────┐
                               │ Yes                           │
                               ▼                               │
┌─────────────────────────────────────────────────────────┐    │
│ 7. 输出结果                                              │    │
│    ├─ 最优路径                                           │    │
│    ├─ 最优距离                                           │    │
│    └─ 收敛曲线                                           │    │
└─────────────────────────────────────────────────────────┘    │
                               │                               │
                               ▼                               │
     ┌─────────────────────────────────────────────────────────┘
     │                    结束                                 │
     └─────────────────────────────────────────────────────────┘
```

### 4.1 蚂蚁状态转移流程图

```
                ┌─────────────────────┐
                │   蚂蚁当前在城市 i   │
                └──────────┬──────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  计算未访问城市集合 J = {j | j ∉ visited}            │
│  如果 J 为空，返回 -1（结束）                        │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  对每个 j ∈ J:                                       │
│    τᵢⱼ = 信息素浓度                                  │
│    ηᵢⱼ = 1 / dᵢⱼ  (启发式信息)                       │
│    Pᵢⱼ = (τᵢⱼ^α * ηᵢⱼ^β) / Σ(τᵢₖ^α * ηᵢₖ^β)         │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                轮盘赌选择                            │
│  r = random(0, 1)                                    │
│  cumulative = 0                                      │
│  for j, prob in zip(J, probabilities):              │
│      cumulative += prob                              │
│      if r <= cumulative: return j                    │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   移动到城市 j       │
                └─────────────────────┘
```

---

## 5. 核心公式推导

### 5.1 基本概念定义

| 符号 | 含义 | 取值范围 |
|------|------|----------|
| $n$ | 城市数量 | $n \geq 3$ |
| $m$ | 蚂蚁数量 | $m \geq 1$ |
| $d_{ij}$ | 城市 $i$ 到城市 $j$ 的距离 | $d_{ij} > 0$ |
| $\tau_{ij}(t)$ | $t$ 时刻边 $(i,j)$ 上的信息素浓度 | $\tau_{ij} \geq 0$ |
| $\eta_{ij}$ | 边 $(i,j)$ 的启发式信息 | $\eta_{ij} = 1/d_{ij}$ |
| $\alpha$ | 信息素重要程度因子 | $\alpha \geq 0$ |
| $\beta$ | 启发式信息重要程度因子 | $\beta \geq 0$ |
| $\rho$ | 信息素挥发系数 | $0 \leq \rho \leq 1$ |
| $Q$ | 信息素增量常数 | $Q > 0$ |

---

### 5.2 转移概率公式

#### 公式 1：状态转移概率
$$
p_{ij}^k(t) = 
\begin{cases} 
\frac{[\tau_{ij}(t)]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{l \in \text{allowed}_k} [\tau_{il}(t)]^\alpha \cdot [\eta_{il}]^\beta} & \text{若 } j \in \text{allowed}_k \\
0 & \text{否则}
\end{cases}
$$

**推导过程：**

1. **吸引度计算**：对于蚂蚁 k，边 (i,j) 的吸引度由两部分组成：
   - 信息素项：$[\tau_{ij}(t)]^\alpha$ - 历史经验的影响
   - 启发式项：$[\eta_{ij}]^\beta$ - 局部启发的影响
   
   因此，边 (i,j) 的综合吸引度为：
   $$ A_{ij} = [\tau_{ij}(t)]^\alpha \cdot [\eta_{ij}]^\beta $$

2. **概率归一化**：蚂蚁只能移动到未访问的城市，因此需要对所有允许城市的吸引度进行归一化：
   $$ \text{Total} = \sum_{l \in \text{allowed}_k} A_{il} = \sum_{l \in \text{allowed}_k} [\tau_{il}(t)]^\alpha \cdot [\eta_{il}]^\beta $$

3. **转移概率**：选择城市 j 的概率等于其吸引度占总吸引度的比例：
   $$ p_{ij}^k(t) = \frac{A_{ij}}{\text{Total}} = \frac{[\tau_{ij}(t)]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{l \in \text{allowed}_k} [\tau_{il}(t)]^\alpha \cdot [\eta_{il}]^\beta} $$

**代码实现位置**：`aco/ant.py:75-108` 的 `_calculate_probabilities` 方法

---

### 5.3 信息素更新公式

#### 阶段 1：信息素挥发
$$
\tau_{ij}(t+1) = (1 - \rho) \cdot \tau_{ij}(t)
$$

**推导过程：**

- 信息素挥发模拟真实世界中信息素的蒸发过程
- $(1 - \rho)$ 是保留系数，$\rho$ 越大，信息素挥发越快
- 挥发机制确保算法能够"遗忘"较差的路径，避免陷入局部最优

**代码实现位置**：`aco/graph.py:76-81` 的 `evaporate_pheromone` 方法

#### 阶段 2：蚂蚁释放信息素
$$
\tau_{ij}(t+1) = \tau_{ij}(t+1) + \sum_{k=1}^m \Delta \tau_{ij}^k(t)
$$

其中单只蚂蚁 k 释放的信息素量：
$$
\Delta \tau_{ij}^k(t) = 
\begin{cases} 
\frac{Q}{L_k(t)} & \text{若边 } (i,j) \text{ 在蚂蚁 k 的路径上} \\
0 & \text{否则}
\end{cases}
$$

**推导过程：**

1. **信息素增量与路径质量成反比**：
   - $L_k(t)$ 是蚂蚁 k 在时刻 t 构建的路径总长度
   - 路径越短，$L_k$ 越小，释放的信息素 $\Delta \tau$ 越多
   - 这体现了正反馈机制：好路径会得到更多的信息素增强

2. **常数 Q 的作用**：
   - 控制信息素释放的总量级
   - 使信息素增量与距离的单位无关

3. **循环应用**：
   信息素更新在每次迭代后进行，因此：
   $$
   \tau_{ij}(t+1) = (1 - \rho) \cdot \tau_{ij}(t) + \sum_{k=1}^m \Delta \tau_{ij}^k(t)
   $$

**代码实现位置**：
- `aco/ant.py:164-173` 的 `get_pheromone_delta` 方法
- `aco/colony.py:117-131` 的 `_update_pheromone` 方法

---

### 5.4 轮盘赌选择算法

#### 算法描述：

给定概率分布 $P = [p_1, p_2, ..., p_n]$，其中 $\sum p_i = 1$，选择一个元素。

#### 数学表达：

生成随机数 $r \sim U(0,1)$，找到最小的索引 $s$ 使得：
$$
\sum_{i=1}^s p_i \geq r
$$

#### 累积概率计算：
$$
C_s = \sum_{i=1}^s p_i
$$

选择第一个满足 $C_s \geq r$ 的 $s$。

**代码实现位置**：`aco/ant.py:110-130` 的 `_roulette_wheel_selection` 方法

---

### 5.5 路径距离计算

对于路径 $P = [c_0, c_1, ..., c_{n-1}]$，总距离为：
$$
L(P) = \sum_{i=0}^{n-2} d(c_i, c_{i+1}) + d(c_{n-1}, c_0)
$$

其中：
- 第一项是路径中相邻城市的距离和
- 第二项是从最后一个城市返回起点的距离
- $d(c_i, c_j)$ 是欧几里得距离：$d(c_i, c_j) = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}$

**代码实现位置**：`aco/graph.py:83-90` 的 `calculate_path_distance` 方法

---

### 5.6 收敛性分析

#### 期望信息素浓度
对于最优路径 $P^*$，其边的期望信息素浓度满足：
$$
E[\tau_{ij}] \geq \frac{Q}{L^*} \cdot \frac{1 - (1 - p^*)^m}{\rho}
$$

其中：
- $L^*$ 是最优路径长度
- $p^*$ 是蚂蚁选择最优边的概率
- $m$ 是蚂蚁数量

#### 收敛条件
当迭代次数 $t \to \infty$ 时，算法收敛到最优解的条件：
1. 信息素初始值 $\tau_0 > 0$
2. 挥发系数 $\rho > 0$
3. 信息素下界 $\tau_{\text{min}} > 0$（可选，但有助于避免停滞）

---

## 6. 模块详细说明

### 6.1 配置模块 (`aco/config.py`)

#### 核心功能
- 参数封装与验证
- 提供默认配置

#### 数据结构
```python
class ACOConfig:
    alpha: float        # 信息素因子
    beta: float         # 启发式因子
    rho: float          # 挥发系数
    q: float            # 信息素常数
    num_ants: int       # 蚂蚁数量
    max_iterations: int # 最大迭代
    initial_pheromone: float
```

#### 关键方法
- `_validate()`: 参数合法性检查
  - alpha, beta ≥ 0
  - rho ∈ [0, 1]
  - q, num_ants, max_iterations > 0

---

### 6.2 图模块 (`aco/graph.py`)

#### 核心功能
- 城市坐标管理
- 距离矩阵构建
- 信息素矩阵维护

#### 数据结构
```python
class Graph:
    cities: List[Tuple[float, float]]      # 城市坐标
    num_cities: int                        # 城市数量
    distance_matrix: List[List[float]]     # n×n 距离矩阵
    pheromone_matrix: List[List[float]]    # n×n 信息素矩阵
```

#### 关键方法
| 方法 | 时间复杂度 | 说明 |
|------|-----------|------|
| `_build_distance_matrix()` | $O(n^2)$ | 预计算所有城市对距离 |
| `initialize_pheromone(val)` | $O(n^2)$ | 初始化信息素 |
| `get_distance(i,j)` | $O(1)$ | 获取城市间距离 |
| `get_pheromone(i,j)` | $O(1)$ | 获取信息素浓度 |
| `update_pheromone(i,j,delta)` | $O(1)$ | 更新信息素（对称） |
| `evaporate_pheromone(rho)` | $O(n^2)$ | 全局信息素挥发 |

**设计亮点**：信息素矩阵是对称的，$\tau_{ij} = \tau_{ji}$，减少一半存储空间和计算量。

---

### 6.3 蚂蚁模块 (`aco/ant.py`)

#### 核心功能
- 单只蚂蚁的路径构建
- 状态转移决策
- 信息素贡献计算

#### 数据结构
```python
class Ant:
    ant_id: int
    graph: Graph              # 引用图对象
    config: ACOConfig         # 引用配置
    path: List[int]           # 当前路径
    visited: List[bool]       # 访问标记
    path_distance: float      # 路径总距离
    current_city: int         # 当前位置
```

#### 关键方法
| 方法 | 时间复杂度 | 说明 |
|------|-----------|------|
| `reset(start_city)` | $O(n)$ | 重置蚂蚁状态 |
| `select_next_city()` | $O(n)$ | 选择下一个城市 |
| `_calculate_probabilities()` | $O(n)$ | 计算转移概率 |
| `_roulette_wheel_selection()` | $O(k)$ | k=未访问城市数 |
| `complete_tour()` | $O(n^2)$ | 构建完整路径 |
| `get_pheromone_delta()` | $O(1)$ | 计算信息素贡献 |

**算法细节**：
- 在 `_calculate_probabilities()` 中，避免除以零：如果距离为 0（同一城市），启发式值设为无穷大
- 轮盘赌选择处理浮点精度问题：如果累积和略小于 1，返回最后一个城市

---

### 6.4 蚁群模块 (`aco/colony.py`)

#### 核心功能
- 算法流程控制
- 蚂蚁种群管理
- 信息素全局更新
- 最优解追踪

#### 数据结构
```python
class AntColony:
    graph: Graph
    config: ACOConfig
    ants: List[Ant]               # 蚂蚁种群
    best_path: List[int]          # 全局最优路径
    best_distance: float          # 全局最优距离
    history: List[Tuple]          # 收敛历史
```

#### 关键方法
| 方法 | 时间复杂度 | 说明 |
|------|-----------|------|
| `run(callback)` | $O(T \cdot m n^2)$ | T=迭代次数, m=蚂蚁数 |
| `_run_iteration()` | $O(m n^2)$ | 单轮迭代 |
| `_update_pheromone()` | $O(n^2 + m n)$ | 挥发+释放 |
| `get_convergence_data()` | $O(T)$ | 获取收敛曲线数据 |

#### 执行流程详解

```
_run_iteration() 流程：
┌─────────────────────────────────────────────────────────┐
│ 对每只蚂蚁 ant in ants:                                 │
│   1. ant.reset()           # 重置状态，随机起点        │
│   2. ant.complete_tour()   # 构建完整路径 O(n²)        │
│   3. distances.append(ant.path_distance)               │
│   4. if ant.path_distance < best_distance:             │
│         更新 best_path 和 best_distance                │
└─────────────────────────────────────────────────────────┘

_update_pheromone() 流程：
┌─────────────────────────────────────────────────────────┐
│ 1. graph.evaporate_pheromone(rho)    # O(n²)          │
│ 2. 对每只蚂蚁 ant in ants:                             │
│      delta = ant.get_pheromone_delta()                 │
│      for i in 0..n-2:                                  │
│          graph.update_pheromone(path[i], path[i+1], delta) │
│      graph.update_pheromone(path[-1], path[0], delta)  │
└─────────────────────────────────────────────────────────┘
```

---

### 6.5 工具模块 (`utils/`)

#### MathUtils (`utils/math_utils.py`)
- `euclidean_distance(p1, p2)`: 欧几里得距离计算
- `generate_random_cities(n, seed)`: 随机城市生成
- `calculate_path_distance(cities, path)`: 独立路径距离计算
- `normalize(values)`: 数据归一化
- `mean()/std_dev()`: 统计计算

#### Visualizer (`utils/visualizer.py`)
- `draw_convergence_chart()`: ASCII 收敛曲线
- `draw_path()`: ASCII 路径图
- `print_statistics()`: 结果统计
- `progress_bar()`: 进度条显示

---

### 6.6 测试实例模块 (`examples/tsp_instances.py`)

提供多种 TSP 测试实例：
1. **Small** (5城市) - 用于快速验证
2. **Medium** (10城市) - 标准测试
3. **Large** (20城市) - 性能测试
4. **Circle** - 圆形分布（已知最优解）
5. **Grid** - 网格分布
6. **Cluster** - 聚类分布

---

## 7. 参数调优建议

### 7.1 参数影响分析

| 参数 | 作用 | 增大影响 | 减小影响 | 推荐范围 |
|------|------|---------|---------|---------|
| **α** | 信息素重要程度 | 更多探索历史好路径，可能早熟 | 更多随机探索，收敛慢 | [0.5, 3.0] |
| **β** | 启发式信息重要程度 | 更贪婪，倾向短边 | 更多随机 | [1.0, 5.0] |
| **ρ** | 信息素挥发系数 | 快速遗忘，增加探索 | 累积历史信息，易早熟 | [0.1, 0.9] |
| **Q** | 信息素增量常数 | 信息素变化大 | 变化平缓 | [50, 200] |
| **m** | 蚂蚁数量 | 解更多样，计算量大 | 计算快，易早熟 | [n, 2n] |
| **T** | 迭代次数 | 更好收敛，耗时 | 快速出结果 | [50, 500] |

---

### 7.2 参数调优策略

#### 策略 1：α-β 平衡
**核心思想**：平衡历史经验（α）和局部启发（β）

推荐组合：
```
情况 1：小规模问题 (n ≤ 20)
   α = 1.0, β = 2.0    → 经典组合
   α = 0.5, β = 3.0    → 更贪婪

情况 2：中等规模问题 (20 < n ≤ 50)
   α = 1.0, β = 2.5
   α = 1.5, β = 2.0

情况 3：大规模问题 (n > 50)
   α = 1.0, β = 3.0    → 增加启发式权重
```

**实验验证**：
```bash
python main.py --compare  # 运行参数对比测试
```

#### 策略 2：ρ 自适应调整
**挥发系数的动态调优**：

```
初始阶段 (iter < T/3):
   ρ = 0.7 ~ 0.9  → 高挥发，增加探索

中期阶段 (T/3 ≤ iter < 2T/3):
   ρ = 0.5 ~ 0.7  → 平衡

后期阶段 (iter ≥ 2T/3):
   ρ = 0.1 ~ 0.3  → 低挥发，加速收敛
```

**实现方式**：在 `AntColony.run()` 中添加回调动态调整 `config.rho`

#### 策略 3：蚂蚁数量 m
**推荐公式**：
$$
m = \max(10, \min(n, 50))
$$

- 对于 n=5: m=10
- 对于 n=20: m=20
- 对于 n=100: m=50（限制上限）

---

### 7.3 典型参数配置

| 问题规模 | α | β | ρ | Q | m | T |
|---------|---|---|---|---|---|---|
| 小 (n≤10) | 1.0 | 2.0 | 0.5 | 100 | 10-20 | 50-100 |
| 中 (10<n≤30) | 1.0 | 2.5 | 0.3 | 100 | 20-30 | 100-200 |
| 大 (30<n≤50) | 1.2 | 3.0 | 0.2 | 150 | 30-50 | 200-300 |

---

### 7.4 参数调优实验指南

#### 实验 1：α vs β 敏感性分析
```python
alpha_values = [0.5, 1.0, 1.5, 2.0, 3.0]
beta_values = [1.0, 2.0, 3.0, 4.0, 5.0]

for alpha in alpha_values:
    for beta in beta_values:
        config = ACOConfig(alpha=alpha, beta=beta, rho=0.5, 
                          num_ants=20, max_iterations=100)
        # 运行多次取平均
        results = [run_experiment(config) for _ in range(5)]
        avg_result = mean(results)
        print(f"α={alpha}, β={beta}: {avg_result:.2f}")
```

#### 实验 2：ρ 收敛速度分析
```python
rho_values = [0.1, 0.3, 0.5, 0.7, 0.9]
for rho in rho_values:
    config = ACOConfig(rho=rho, max_iterations=200)
    colony = AntColony(graph, config)
    colony.run()
    iterations, best_dists, _ = colony.get_convergence_data()
    # 分析首次达到最优的迭代次数
    first_opt_iter = first_index_where(best_dists == min(best_dists))
    print(f"ρ={rho}: 首次收敛在迭代 {first_opt_iter}")
```

#### 实验 3：蚂蚁数量 m 分析
```python
m_values = [5, 10, 20, 30, 50, 100]
for m in m_values:
    config = ACOConfig(num_ants=m)
    start_time = time.time()
    _, best_dist = run_experiment(config)
    elapsed = time.time() - start_time
    print(f"m={m}: 距离={best_dist:.2f}, 时间={elapsed:.3f}s")
```

---

### 7.5 常见问题与解决

#### 问题 1：早熟收敛（陷入局部最优）
**症状**：算法很快收敛，但解质量差
**可能原因**：
- α 太大，过于依赖历史信息
- ρ 太小，信息素累积过快
- m 太小，解多样性不足

**解决方案**：
1. 增大 ρ → 增加信息素挥发
2. 减小 α/β 比例 → 增加探索
3. 增加蚂蚁数量 m
4. 添加信息素上下限 [τ_min, τ_max]

#### 问题 2：收敛过慢
**症状**：迭代很多次但没有明显改进
**可能原因**：
- α 太小，信息素影响不足
- ρ 太大，信息素挥发过快
- 初始信息素 τ₀ 太小

**解决方案**：
1. 增大 α
2. 减小 ρ
3. 增大初始信息素浓度

#### 问题 3：结果不稳定
**症状**：每次运行结果差异大
**可能原因**：随机性过大
**解决方案**：
1. 增加蚂蚁数量
2. 增加迭代次数
3. 设置随机种子进行可重复实验

---

## 8. 扩展与优化方向

### 8.1 算法变体

#### 8.1.1 蚁群系统 (ACS)
- 特点：局部信息素更新 + 全局信息素更新
- 伪代码：
```python
# 局部更新（蚂蚁每走一步）
tau[i][j] = (1 - rho) * tau[i][j] + rho * tau0

# 全局更新（只有最优蚂蚁）
for i,j in best_path:
    tau[i][j] = (1 - rho) * tau[i][j] + rho * (Q / best_dist)
```

#### 8.1.2 最大最小蚁群系统 (MMAS)
- 特点：信息素上下限限制
```python
tau_min = 0.001
tau_max = 10.0

def update_pheromone(i, j, delta):
    tau[i][j] = max(tau_min, min(tau_max, tau[i][j] + delta))
```

#### 8.1.3 排序蚁群系统 (AS_rank)
- 特点：只有最好的 k 只蚂蚁释放信息素
```python
ants.sort(key=lambda x: x.path_distance)
for k, ant in enumerate(ants[:10]):  # 只取前10只
    weight = max(0, 10 - k)  # 按排名加权
    delta = weight * Q / ant.path_distance
    update_path_pheromone(ant.path, delta)
```

### 8.2 性能优化

#### 8.2.1 候选城市列表
```python
# 预处理：每个城市的最近 k 个城市
def get_candidate_list(city, k=20):
    distances = [(j, d) for j, d in enumerate(distance_matrix[city])]
    distances.sort(key=lambda x: x[1])
    return [j for j, _ in distances[:k]]

# 选择时只考虑候选列表
def select_next_city(self):
    candidates = self.candidate_lists[self.current_city]
    unvisited = [j for j in candidates if not self.visited[j]]
    # ...
```

#### 8.2.2 概率矩阵预计算
```python
# 预计算 [τ^α * η^β] 矩阵
def precompute_attractiveness(self):
    n = self.graph.num_cities
    self.attract = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                tau = self.graph.get_pheromone(i,j)
                eta = 1.0 / self.graph.get_distance(i,j)
                self.attract[i][j] = (tau ** self.config.alpha) * \
                                     (eta ** self.config.beta)
```

#### 8.2.3 并行化
```python
from multiprocessing import Pool

def _run_ant(ant):
    ant.reset()
    ant.complete_tour()
    return ant.path, ant.path_distance

def _run_iteration_parallel(self):
    with Pool() as pool:
        results = pool.map(_run_ant, self.ants)
    
    distances = []
    for path, dist in results:
        distances.append(dist)
        if dist < self.best_distance:
            self.best_distance = dist
            self.best_path = path
    return distances
```

### 8.3 功能扩展

#### 8.3.1 多种距离度量
```python
class DistanceType(Enum):
    EUCLIDEAN = 1
    MANHATTAN = 2
    GEOGRAPHIC = 3  # 经纬度距离

def get_distance(self, i, j, dist_type=DistanceType.EUCLIDEAN):
    if dist_type == DistanceType.EUCLIDEAN:
        return self.euclidean[i][j]
    elif dist_type == DistanceType.MANHATTAN:
        return self.manhattan[i][j]
    # ...
```

#### 8.3.2 动态 TSP
```python
class DynamicGraph(Graph):
    def update_city_position(self, city_idx, new_x, new_y):
        self.cities[city_idx] = (new_x, new_y)
        self._build_distance_matrix()  # 重建距离矩阵
    
    def add_obstacle(self, i, j):
        self.distance_matrix[i][j] = float('inf')
        self.distance_matrix[j][i] = float('inf')
```

#### 8.3.3 多目标 TSP
```python
class MultiObjectiveACO:
    def __init__(self, graph, weights):
        self.graph = graph
        self.weights = weights  # 多目标权重
        
    def _multi_objective_distance(self, path):
        dist1 = self.distance_obj1(path)
        dist2 = self.distance_obj2(path)
        return (self.weights[0] * dist1 + 
                self.weights[1] * dist2)
```

---

## 9. 参考文献

1. Dorigo, M., & Stützle, T. (2004). **Ant Colony Optimization**. MIT Press.

2. Dorigo, M., Maniezzo, V., & Colorni, A. (1996). **Ant system: optimization by a colony of cooperating agents**. IEEE Transactions on Systems, Man, and Cybernetics, Part B, 26(1), 29-41.

3. Stützle, T., & Hoos, H. H. (2000). **MAX-MIN ant system**. Future Generation Computer Systems, 16(8), 889-914.

4. Gambardella, L. M., & Dorigo, M. (1995). **Ant-Q: A reinforcement learning approach to the traveling salesman problem**. ICML.

---

## 附录 A：代码索引表

| 功能 | 文件位置 | 行号 |
|------|---------|------|
| 配置参数定义 | `aco/config.py` | 6-62 |
| 距离矩阵构建 | `aco/graph.py` | 40-49 |
| 信息素初始化 | `aco/graph.py` | 62-65 |
| 转移概率计算 | `aco/ant.py` | 75-108 |
| 轮盘赌选择 | `aco/ant.py` | 110-130 |
| 蚂蚁路径构建 | `aco/ant.py` | 153-162 |
| 信息素增量计算 | `aco/ant.py` | 164-173 |
| 蚁群主循环 | `aco/colony.py` | 49-89 |
| 单轮迭代 | `aco/colony.py` | 91-115 |
| 信息素更新 | `aco/colony.py` | 117-131 |
| 信息素挥发 | `aco/graph.py` | 76-81 |
| 欧几里得距离 | `aco/graph.py` | 52-56 |
| 随机城市生成 | `utils/math_utils.py` | 27-54 |
| 收敛曲线绘制 | `utils/visualizer.py` | 13-67 |
| 测试实例 | `examples/tsp_instances.py` | 9-146 |
| 主程序入口 | `main.py` | 311-378 |

---

**文档版本**：1.0  
**最后更新**：2024年  
**适用版本**：项目 v1.0