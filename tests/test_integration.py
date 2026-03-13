"""
集成测试
Integration Tests
"""

import unittest
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aco import ACOConfig, Graph, AntColony
from utils import MathUtils, Visualizer
from examples import TSPInstances


class TestIntegration(unittest.TestCase):
    """集成测试类"""
    
    def test_full_workflow_small(self):
        """测试完整工作流程 - 小规模"""
        # 1. 获取测试实例
        cities, name = TSPInstances.get_small_instance()
        
        # 2. 创建图
        graph = Graph(cities)
        
        # 3. 配置算法
        config = ACOConfig(
            alpha=1.0,
            beta=2.0,
            rho=0.5,
            num_ants=10,
            max_iterations=50
        )
        
        # 4. 创建蚁群
        colony = AntColony(graph, config)
        
        # 5. 运行算法
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        # 6. 验证结果
        self.assertEqual(len(best_path), len(cities))
        self.assertEqual(set(best_path), set(range(len(cities))))
        self.assertGreater(best_distance, 0)
        
        # 7. 获取收敛数据
        iterations, best_dists, avg_dists = colony.get_convergence_data()
        self.assertEqual(len(iterations), 50)
        
        # 8. 生成可视化
        chart = Visualizer.draw_convergence_chart(iterations, best_dists)
        self.assertIsInstance(chart, str)
        
        stats = Visualizer.print_statistics(best_distance, best_path, colony.history)
        self.assertIsInstance(stats, str)
    
    def test_full_workflow_medium(self):
        """测试完整工作流程 - 中等规模"""
        cities, name = TSPInstances.get_medium_instance()
        graph = Graph(cities)
        config = ACOConfig(num_ants=15, max_iterations=100)
        colony = AntColony(graph, config)
        
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(best_path), 10)
        self.assertGreater(best_distance, 0)
    
    def test_full_workflow_random(self):
        """测试完整工作流程 - 随机实例"""
        # 生成随机城市
        cities = MathUtils.generate_random_cities(15, seed=42)
        
        graph = Graph(cities)
        config = ACOConfig(num_ants=15, max_iterations=50)
        colony = AntColony(graph, config)
        
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(best_path), 15)
        
        # 验证路径距离计算一致
        calculated_distance = graph.calculate_path_distance(best_path)
        self.assertAlmostEqual(best_distance, calculated_distance, places=5)
    
    def test_multiple_runs_consistency(self):
        """测试多次运行一致性"""
        cities, _ = TSPInstances.get_small_instance()
        
        results = []
        for _ in range(3):
            graph = Graph(cities)
            config = ACOConfig(num_ants=10, max_iterations=30)
            colony = AntColony(graph, config)
            
            random.seed(12345)
            _, best_distance = colony.run(verbose=False)
            results.append(best_distance)
        
        # 相同种子应该产生相同结果
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])
    
    def test_reset_and_rerun(self):
        """测试重置后重新运行"""
        cities, _ = TSPInstances.get_small_instance()
        graph = Graph(cities)
        config = ACOConfig(num_ants=10, max_iterations=30)
        colony = AntColony(graph, config)
        
        # 第一次运行
        random.seed(42)
        path1, dist1 = colony.run(verbose=False)
        
        # 重置
        colony.reset()
        
        # 第二次运行
        random.seed(42)
        path2, dist2 = colony.run(verbose=False)
        
        # 结果应该相同
        self.assertEqual(path1, path2)
        self.assertAlmostEqual(dist1, dist2, places=5)


class TestIntegrationAllInstances(unittest.TestCase):
    """所有实例集成测试"""
    
    def test_all_instances_solvable(self):
        """测试所有实例都可解"""
        instances = TSPInstances.get_all_instances()
        
        for cities, name in instances:
            with self.subTest(instance=name):
                graph = Graph(cities)
                config = ACOConfig(
                    num_ants=max(5, len(cities) // 2),
                    max_iterations=30
                )
                colony = AntColony(graph, config)
                
                random.seed(42)
                best_path, best_distance = colony.run(verbose=False)
                
                # 验证解的有效性
                self.assertEqual(len(best_path), len(cities))
                self.assertEqual(set(best_path), set(range(len(cities))))
                self.assertGreater(best_distance, 0)
                self.assertTrue(best_distance < float('inf'))


class TestIntegrationPerformance(unittest.TestCase):
    """性能集成测试"""
    
    def test_large_instance_completes(self):
        """测试大规模实例能完成"""
        cities, _ = TSPInstances.get_large_instance()
        graph = Graph(cities)
        config = ACOConfig(num_ants=20, max_iterations=50)
        colony = AntColony(graph, config)
        
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        self.assertEqual(len(best_path), 20)
    
    def test_many_iterations_stable(self):
        """测试多次迭代稳定"""
        cities, _ = TSPInstances.get_medium_instance()
        graph = Graph(cities)
        config = ACOConfig(num_ants=10, max_iterations=200)
        colony = AntColony(graph, config)
        
        random.seed(42)
        best_path, best_distance = colony.run(verbose=False)
        
        # 检查没有异常值
        self.assertTrue(best_distance < float('inf'))
        self.assertFalse(best_distance != best_distance)  # 检查 NaN


if __name__ == '__main__':
    unittest.main()
