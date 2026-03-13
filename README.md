# 蚁群算法 (Ant Colony Optimization)

纯 Python 实现的蚁群算法，用于解决旅行商问题（TSP）。

## How to Run

### 使用 Docker（推荐）

```bash
cd ant-colony-algorithm

# 运行主程序
docker-compose up --build -d

# 查看运行日志
docker logs aco-algorithm

# 运行测试
docker-compose --profile test run --rm aco-test
```

### 本地运行

```bash
cd ant-colony-algorithm
python main.py
```

### 命令行参数

```bash
# 查看帮助
python main.py --help

# 运行所有测试实例
python main.py

# 只运行小规模实例
python main.py -i small

# 运行中等实例，50次迭代，30只蚂蚁
python main.py -i medium -n 50 -a 30

# 随机生成20个城市
python main.py -i random --cities 20

# 自定义算法参数
python main.py -i large --alpha 1.5 --beta 3.0 --rho 0.3

# 安静模式，不显示图表
python main.py -i small -q --no-chart

# 列出所有可用实例
python main.py --list

# 运行参数敏感性对比测试
python main.py -i medium --compare
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-i, --instance` | 测试实例 (small/medium/large/circle/grid/cluster/random/all) | all |
| `-n, --iterations` | 最大迭代次数 | 100 |
| `-a, --ants` | 蚂蚁数量 | 自动 |
| `--alpha` | 信息素重要程度因子 | 1.0 |
| `--beta` | 启发式信息重要程度因子 | 2.0 |
| `--rho` | 信息素挥发系数 | 0.5 |
| `--cities` | 随机实例的城市数量 | 15 |
| `--seed` | 随机种子 | None |
| `-q, --quiet` | 安静模式 | False |
| `--no-chart` | 不显示 ASCII 图表 | False |
| `--compare` | 运行参数敏感性对比测试 | False |

## Services

| 服务 | 命令 | 说明 |
|------|------|------|
| aco-algorithm | `docker-compose up --build -d` | 运行蚁群算法主程序 |
| aco-test | `docker-compose --profile test run --rm aco-test` | 运行测试套件 |

## 测试账号

无需账号，直接运行即可。

## 题目内容

帮我创作一个蚁群算法，纯python，不许用numpy

---

## 如何运行测试

### 使用 Docker 测试（推荐）

```bash
cd ant-colony-algorithm
docker-compose --profile test run --rm aco-test
```

测试结果：
```
======================================================================
  测试总结
======================================================================
  运行测试: 109
  成功: 109
  失败: 0
  错误: 0
  跳过: 0
  耗时: 0.280 秒
======================================================================
```

### 本地运行测试

```bash
cd ant-colony-algorithm
python run_tests.py
```

### 测试套件概览

项目包含 109 个测试用例，覆盖以下模块：

| 测试文件 | 测试数量 | 测试内容 |
|----------|----------|----------|
| test_config.py | 12 | ACOConfig 配置参数验证 |
| test_graph.py | 18 | Graph 图结构与距离矩阵 |
| test_ant.py | 16 | Ant 蚂蚁行为模拟 |
| test_colony.py | 17 | AntColony 蚁群管理 |
| test_math_utils.py | 12 | MathUtils 数学工具 |
| test_visualizer.py | 14 | Visualizer 可视化工具 |
| test_tsp_instances.py | 13 | TSPInstances 测试实例 |
| test_integration.py | 7 | 集成测试 |

### 运行特定测试模块

```bash
# 运行配置测试
python run_tests.py test_config

# 运行图结构测试
python run_tests.py test_graph

# 运行蚂蚁行为测试
python run_tests.py test_ant

# 运行蚁群测试
python run_tests.py test_colony

# 运行集成测试
python run_tests.py test_integration
```

### 使用 unittest 直接运行

```bash
# 运行所有测试
python -m unittest discover tests -v

# 运行单个测试文件
python -m unittest tests.test_config -v

# 运行单个测试类
python -m unittest tests.test_colony.TestAntColony -v

# 运行单个测试方法
python -m unittest tests.test_colony.TestAntColony.test_run_returns_valid_path -v
```

### 测试详细说明

#### 1. 配置测试 (test_config.py)

测试 ACOConfig 类的参数验证：

- 默认配置值验证
- 自定义配置值验证
- 无效参数异常处理（alpha、beta、rho、q、num_ants、max_iterations）
- 边界值测试

```python
# 示例：测试无效的 rho 值
def test_invalid_rho_too_high(self):
    with self.assertRaises(ValueError):
        ACOConfig(rho=1.5)  # rho 必须在 [0, 1] 范围内
```

#### 2. 图结构测试 (test_graph.py)

测试 Graph 类的核心功能：

- 距离矩阵构建
- 欧几里得距离计算
- 信息素初始化、更新、挥发
- 路径距离计算
- 边界情况（单城市、两城市、负坐标、浮点坐标）

```python
# 示例：测试距离矩阵对称性
def test_distance_matrix(self):
    for i in range(4):
        for j in range(4):
            self.assertEqual(
                self.graph.distance_matrix[i][j],
                self.graph.distance_matrix[j][i]
            )
```

#### 3. 蚂蚁行为测试 (test_ant.py)

测试 Ant 类的行为模拟：

- 初始化与重置
- 城市选择（轮盘赌算法）
- 移动与路径记录
- 完整旅行
- 信息素增量计算
- 概率计算验证

```python
# 示例：测试概率倾向于更近的城市
def test_probability_favors_closer_city(self):
    selections = {1: 0, 2: 0}
    for _ in range(1000):
        self.ant.reset(start_city=0)
        next_city = self.ant.select_next_city()
        selections[next_city] += 1
    # 城市 1 (距离 10) 应该比城市 2 (距离 20) 更常被选中
    self.assertGreater(selections[1], selections[2])
```

#### 4. 蚁群测试 (test_colony.py)

测试 AntColony 类的算法执行：

- 初始化与重置
- 运行返回有效路径
- 解的改进验证
- 收敛性测试
- 回调函数支持
- 边界情况（单蚂蚁、单迭代、两城市）

```python
# 示例：测试正方形城市找到最优解
def test_finds_optimal_for_square(self):
    cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
    graph = Graph(cities)
    config = ACOConfig(num_ants=20, max_iterations=100)
    colony = AntColony(graph, config)
    _, best_distance = colony.run(verbose=False)
    # 最优解应该是 40 (正方形周长)
    self.assertAlmostEqual(best_distance, 40.0, places=1)
```

#### 5. 集成测试 (test_integration.py)

测试完整工作流程：

- 小/中/大规模实例完整流程
- 随机实例测试
- 多次运行一致性
- 重置后重新运行
- 所有预设实例可解性
- 性能稳定性

```python
# 示例：测试完整工作流程
def test_full_workflow_small(self):
    cities, name = TSPInstances.get_small_instance()
    graph = Graph(cities)
    config = ACOConfig(num_ants=10, max_iterations=50)
    colony = AntColony(graph, config)
    best_path, best_distance = colony.run(verbose=False)
    
    self.assertEqual(len(best_path), len(cities))
    self.assertEqual(set(best_path), set(range(len(cities))))
```

### 测试输出示例

```
======================================================================
  蚁群算法测试套件
  Ant Colony Optimization Test Suite
======================================================================

发现 109 个测试用例
----------------------------------------------------------------------

test_default_config (test_config.TestACOConfig.test_default_config)
测试默认配置 ... ok
test_custom_config (test_config.TestACOConfig.test_custom_config)
测试自定义配置 ... ok
...

----------------------------------------------------------------------
Ran 109 tests in 0.323s

OK

======================================================================
  测试总结
======================================================================
  运行测试: 109
  成功: 109
  失败: 0
  错误: 0
  跳过: 0
  耗时: 0.323 秒
======================================================================
```

### 测试覆盖的核心功能

1. **参数验证**：确保所有配置参数在有效范围内
2. **距离计算**：验证欧几里得距离计算正确性
3. **信息素机制**：测试初始化、更新、挥发过程
4. **概率选择**：验证轮盘赌选择算法
5. **路径构建**：确保蚂蚁能完成有效旅行
6. **优化效果**：验证算法能找到好的解
7. **收敛性**：确保最优解单调不增
8. **可视化**：测试 ASCII 图表生成

---

## 项目介绍

### 什么是蚁群算法？

蚁群算法（Ant Colony Optimization, ACO）是一种模拟蚂蚁觅食行为的元启发式优化算法。蚂蚁在寻找食物时会释放信息素，其他蚂蚁会倾向于跟随信息素浓度高的路径，从而逐渐找到最短路径。

### 核心特性

- **纯 Python 实现**：不依赖 numpy 或其他科学计算库
- **模块化设计**：清晰的类结构，易于理解和扩展
- **可视化输出**：ASCII 图形展示收敛过程
- **参数可配置**：支持自定义蚂蚁数量、迭代次数、信息素参数等
- **多种测试用例**：内置多个 TSP 问题实例

### 算法参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| alpha | 1.0 | 信息素重要程度因子 |
| beta | 2.0 | 启发式信息重要程度因子 |
| rho | 0.5 | 信息素挥发系数 |
| Q | 100 | 信息素增量常数 |
| num_ants | 20 | 蚂蚁数量 |
| max_iterations | 100 | 最大迭代次数 |

### 项目结构

```
ant-colony-algorithm/
├── main.py              # 主程序入口
├── aco/
│   ├── __init__.py
│   ├── ant.py           # 蚂蚁类
│   ├── colony.py        # 蚁群类
│   ├── graph.py         # 图/距离矩阵
│   └── config.py        # 配置参数
├── utils/
│   ├── __init__.py
│   ├── math_utils.py    # 数学工具函数
│   └── visualizer.py    # 可视化工具
├── examples/
│   ├── __init__.py
│   └── tsp_instances.py # TSP 测试实例
├── Dockerfile
├── docker-compose.yml
└── README.md
```
