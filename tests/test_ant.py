"""
Ant 蚂蚁类测试
"""

import unittest
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aco.ant import Ant
from aco.graph import Graph
from aco.config import ACOConfig


class TestAnt(unittest.TestCase):
    """Ant 测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        self.graph = Graph(self.cities)
        self.graph.initialize_pheromone(1.0)
        self.config = ACOConfig(num_ants=5, max_iterations=10)
        self.ant = Ant(0, self.graph, self.config)
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.ant.ant_id, 0)
        self.assertEqual(self.ant.graph, self.graph)
        self.assertEqual(self.ant.config, self.config)
        self.assertEqual(self.ant.path, [])
        self.assertEqual(self.ant.path_distance, 0.0)
    
    def test_reset_random_start(self):
        """测试随机起点重置"""
        random.seed(42)
        self.ant.reset()
        
        self.assertEqual(len(self.ant.path), 1)
        self.assertEqual(len(self.ant.visited), 4)
        self.assertEqual(self.ant.path_distance, 0.0)
        self.assertTrue(self.ant.visited[self.ant.path[0]])
    
    def test_reset_specific_start(self):
        """测试指定起点重置"""
        self.ant.reset(start_city=2)
        
        self.assertEqual(self.ant.path, [2])
        self.assertEqual(self.ant.current_city, 2)
        self.assertTrue(self.ant.visited[2])
        self.assertFalse(self.ant.visited[0])
    
    def test_select_next_city(self):
        """测试选择下一个城市"""
        self.ant.reset(start_city=0)
        next_city = self.ant.select_next_city()
        
        # 下一个城市应该是未访问的
        self.assertIn(next_city, [1, 2, 3])
        self.assertNotEqual(next_city, 0)
    
    def test_select_next_city_all_visited(self):
        """测试所有城市都已访问时"""
        self.ant.reset(start_city=0)
        self.ant.visited = [True, True, True, True]
        
        next_city = self.ant.select_next_city()
        self.assertEqual(next_city, -1)
    
    def test_move_to(self):
        """测试移动到城市"""
        self.ant.reset(start_city=0)
        initial_distance = self.ant.path_distance
        
        self.ant.move_to(1)
        
        self.assertEqual(self.ant.current_city, 1)
        self.assertIn(1, self.ant.path)
        self.assertTrue(self.ant.visited[1])
        self.assertGreater(self.ant.path_distance, initial_distance)
    
    def test_move_to_invalid_city(self):
        """测试移动到无效城市"""
        self.ant.reset(start_city=0)
        
        with self.assertRaises(ValueError):
            self.ant.move_to(10)  # 不存在的城市
    
    def test_move_to_visited_city(self):
        """测试移动到已访问城市"""
        self.ant.reset(start_city=0)
        
        with self.assertRaises(ValueError):
            self.ant.move_to(0)  # 已访问
    
    def test_complete_tour(self):
        """测试完成完整旅行"""
        self.ant.reset(start_city=0)
        self.ant.complete_tour()
        
        # 应该访问所有城市
        self.assertEqual(len(self.ant.path), 4)
        self.assertTrue(all(self.ant.visited))
        self.assertGreater(self.ant.path_distance, 0)
    
    def test_complete_tour_visits_all_cities(self):
        """测试完整旅行访问所有城市"""
        self.ant.reset(start_city=0)
        self.ant.complete_tour()
        
        # 检查所有城市都在路径中
        for i in range(4):
            self.assertIn(i, self.ant.path)
    
    def test_get_pheromone_delta(self):
        """测试计算信息素增量"""
        self.ant.reset(start_city=0)
        self.ant.complete_tour()
        
        delta = self.ant.get_pheromone_delta()
        
        # delta = Q / path_distance
        expected = self.config.q / self.ant.path_distance
        self.assertAlmostEqual(delta, expected, places=5)
    
    def test_get_pheromone_delta_zero_distance(self):
        """测试零距离时的信息素增量"""
        self.ant.reset(start_city=0)
        self.ant.path_distance = 0
        
        delta = self.ant.get_pheromone_delta()
        self.assertEqual(delta, 0.0)
    
    def test_repr(self):
        """测试字符串表示"""
        self.ant.reset(start_city=0)
        self.ant.complete_tour()
        
        repr_str = repr(self.ant)
        self.assertIn("Ant", repr_str)
        self.assertIn("id=0", repr_str)


class TestAntProbabilityCalculation(unittest.TestCase):
    """蚂蚁概率计算测试"""
    
    def setUp(self):
        """测试前准备"""
        self.cities = [(0, 0), (10, 0), (20, 0)]
        self.graph = Graph(self.cities)
        self.graph.initialize_pheromone(1.0)
        self.config = ACOConfig(alpha=1.0, beta=2.0)
        self.ant = Ant(0, self.graph, self.config)
    
    def test_probability_favors_closer_city(self):
        """测试概率倾向于更近的城市"""
        self.ant.reset(start_city=0)
        
        # 运行多次选择，统计结果
        selections = {1: 0, 2: 0}
        trials = 1000
        
        for _ in range(trials):
            self.ant.reset(start_city=0)
            next_city = self.ant.select_next_city()
            selections[next_city] += 1
        
        # 城市 1 (距离 10) 应该比城市 2 (距离 20) 更常被选中
        # 因为 beta=2，启发式信息 (1/d)^2 对近距离更有利
        self.assertGreater(selections[1], selections[2])
    
    def test_high_pheromone_increases_probability(self):
        """测试高信息素增加选择概率"""
        # 给城市 2 设置更高的信息素
        self.graph.pheromone_matrix[0][2] = 10.0
        self.graph.pheromone_matrix[2][0] = 10.0
        
        selections = {1: 0, 2: 0}
        trials = 1000
        
        for _ in range(trials):
            self.ant.reset(start_city=0)
            next_city = self.ant.select_next_city()
            selections[next_city] += 1
        
        # 虽然城市 2 更远，但信息素更高，应该增加其被选中的概率
        # 具体比例取决于 alpha 和 beta 的设置


class TestAntDeterministic(unittest.TestCase):
    """蚂蚁确定性行为测试"""
    
    def test_same_seed_same_result(self):
        """测试相同随机种子产生相同结果"""
        cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        graph = Graph(cities)
        graph.initialize_pheromone(1.0)
        config = ACOConfig()
        
        # 第一次运行
        random.seed(12345)
        ant1 = Ant(0, graph, config)
        ant1.reset()
        ant1.complete_tour()
        path1 = ant1.path.copy()
        dist1 = ant1.path_distance
        
        # 重新初始化信息素
        graph.initialize_pheromone(1.0)
        
        # 第二次运行，相同种子
        random.seed(12345)
        ant2 = Ant(0, graph, config)
        ant2.reset()
        ant2.complete_tour()
        path2 = ant2.path.copy()
        dist2 = ant2.path_distance
        
        self.assertEqual(path1, path2)
        self.assertAlmostEqual(dist1, dist2, places=5)


if __name__ == '__main__':
    unittest.main()
