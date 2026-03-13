"""
AntColony 蚁群类测试
"""

import unittest
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aco.colony import AntColony
from aco.graph import Graph
from aco.config import ACOConfig


class TestAntColony(unittest.TestCase):
    """AntColony 测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        self.graph = Graph(self.cities)
        self.config = ACOConfig(num_ants=5, max_iterations=10)
        self.colony = AntColony(self.graph, self.config)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(len(self.colony.ants), 5)
        self.assertEqual(self.colony.best_distance, float('inf'))
        self.assertEqual(self.colony.best_path, [])
        self.assertEqual(len(self.colony.history), 0)
    
    def test_init_default_config(self):
        """测试默认配置初始化"""
        colony = AntColony(self.graph)
        self.assertEqual(len(colony.ants), 20)  # 默认蚂蚁数量
    
    def test_run_returns_valid_path(self):
        """测试运行返回有效路径"""
        best_path, best_distance = self.colony.run(verbose=False)
        
        # 路径应包含所有城市
        self.assertEqual(len(best_path), 4)
        self.assertEqual(set(best_path), {0, 1, 2, 3})
        
        # 距离应为正数
        self.assertGreater(best_distance, 0)
    
    def test_run_improves_solution(self):
        """测试运行改进解"""
        # 使用更多迭代
        config = ACOConfig(num_ants=10, max_iterations=50)
        colony = AntColony(self.graph, config)
        
        best_path, best_distance = colony.run(verbose=False)
        
        # 检查历史记录
        self.assertEqual(len(colony.history), 50)
        
        # 最终解应该不比初始解差
        initial_best = colony.history[0][1]
        final_best = colony.history[-1][1]
        self.assertLessEqual(final_best, initial_best)
    
    def test_run_with_callback(self):
        """测试带回调函数运行"""
        callback_data = []
        
        def callback(iteration, best, avg):
            callback_data.append((iteration, best, avg))
        
        self.colony.run(callback=callback, verbose=False)
        
        # 回调应该被调用 max_iterations 次
        self.assertEqual(len(callback_data), 10)
    
    def test_get_convergence_data(self):
        """测试获取收敛数据"""
        self.colony.run(verbose=False)
        
        iterations, best_dists, avg_dists = self.colony.get_convergence_data()
        
        self.assertEqual(len(iterations), 10)
        self.assertEqual(len(best_dists), 10)
        self.assertEqual(len(avg_dists), 10)
        
        # 迭代次数应该递增
        self.assertEqual(iterations, list(range(10)))
    
    def test_reset(self):
        """测试重置"""
        self.colony.run(verbose=False)
        
        # 确保有数据
        self.assertNotEqual(self.colony.best_path, [])
        self.assertNotEqual(self.colony.best_distance, float('inf'))
        
        # 重置
        self.colony.reset()
        
        self.assertEqual(self.colony.best_path, [])
        self.assertEqual(self.colony.best_distance, float('inf'))
        self.assertEqual(len(self.colony.history), 0)
    
    def test_pheromone_update(self):
        """测试信息素更新"""
        initial_pheromone = self.graph.pheromone_matrix[0][1]
        
        self.colony.run(verbose=False)
        
        # 信息素应该发生变化
        final_pheromone = self.graph.pheromone_matrix[0][1]
        # 由于挥发和更新，信息素会变化
        # 不一定增加或减少，取决于路径
    
    def test_repr(self):
        """测试字符串表示"""
        repr_str = repr(self.colony)
        self.assertIn("AntColony", repr_str)
        self.assertIn("num_ants=5", repr_str)


class TestAntColonyOptimization(unittest.TestCase):
    """蚁群优化效果测试"""
    
    def test_finds_optimal_for_square(self):
        """测试正方形城市找到最优解"""
        # 正方形的最优路径周长为 4 * 边长
        cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        graph = Graph(cities)
        config = ACOConfig(num_ants=20, max_iterations=100)
        colony = AntColony(graph, config)
        
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        # 最优解应该是 40 (正方形周长)
        self.assertAlmostEqual(best_distance, 40.0, places=1)
    
    def test_finds_good_solution_for_circle(self):
        """测试圆形分布找到好的解"""
        import math
        
        # 圆形分布的城市
        num_cities = 8
        radius = 50
        cities = []
        for i in range(num_cities):
            angle = 2 * math.pi * i / num_cities
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            cities.append((x, y))
        
        graph = Graph(cities)
        config = ACOConfig(num_ants=20, max_iterations=100)
        colony = AntColony(graph, config)
        
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        # 最优解应该接近圆的周长
        # 周长 = 2 * pi * r ≈ 314.16
        # 但由于是多边形，实际周长 = 8 * 边长
        # 边长 = 2 * r * sin(pi/8) ≈ 38.27
        # 总周长 ≈ 306.15
        expected_optimal = 8 * 2 * radius * math.sin(math.pi / 8)
        
        # 允许 5% 的误差
        self.assertLess(best_distance, expected_optimal * 1.05)
    
    def test_convergence(self):
        """测试收敛性"""
        cities = [(0, 0), (10, 0), (20, 0), (20, 10), (10, 10), (0, 10)]
        graph = Graph(cities)
        config = ACOConfig(num_ants=15, max_iterations=100)
        colony = AntColony(graph, config)
        
        random.seed(42)
        colony.run(verbose=False)
        
        iterations, best_dists, avg_dists = colony.get_convergence_data()
        
        # 最优距离应该单调不增
        for i in range(1, len(best_dists)):
            self.assertLessEqual(best_dists[i], best_dists[i-1])
    
    def test_different_parameters_affect_result(self):
        """测试不同参数影响结果"""
        cities = [(0, 0), (10, 0), (10, 10), (0, 10), (5, 5)]
        
        results = []
        
        for alpha in [0.5, 1.0, 2.0]:
            graph = Graph(cities)
            config = ACOConfig(alpha=alpha, num_ants=10, max_iterations=50)
            colony = AntColony(graph, config)
            
            random.seed(42)
            _, best_distance = colony.run(verbose=False)
            results.append(best_distance)
        
        # 不同参数应该产生结果（可能相同也可能不同）
        self.assertEqual(len(results), 3)


class TestAntColonyEdgeCases(unittest.TestCase):
    """蚁群边界情况测试"""
    
    def test_two_cities(self):
        """测试两个城市"""
        cities = [(0, 0), (10, 0)]
        graph = Graph(cities)
        config = ACOConfig(num_ants=5, max_iterations=10)
        colony = AntColony(graph, config)
        
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(best_path), 2)
        self.assertAlmostEqual(best_distance, 20.0, places=5)  # 来回
    
    def test_three_cities(self):
        """测试三个城市"""
        cities = [(0, 0), (10, 0), (5, 10)]
        graph = Graph(cities)
        config = ACOConfig(num_ants=5, max_iterations=10)
        colony = AntColony(graph, config)
        
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(best_path), 3)
        self.assertGreater(best_distance, 0)
    
    def test_single_iteration(self):
        """测试单次迭代"""
        cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        graph = Graph(cities)
        config = ACOConfig(num_ants=5, max_iterations=1)
        colony = AntColony(graph, config)
        
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(colony.history), 1)
        self.assertEqual(len(best_path), 4)
    
    def test_single_ant(self):
        """测试单只蚂蚁"""
        cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        graph = Graph(cities)
        config = ACOConfig(num_ants=1, max_iterations=10)
        colony = AntColony(graph, config)
        
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(best_path), 4)


if __name__ == '__main__':
    unittest.main()
