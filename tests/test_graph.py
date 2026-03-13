"""
Graph 图类测试
"""

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aco.graph import Graph


class TestGraph(unittest.TestCase):
    """Graph 测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.cities = [(0, 0), (3, 0), (3, 4), (0, 4)]
        self.graph = Graph(self.cities)
    
    def test_init_with_cities(self):
        """测试带城市初始化"""
        self.assertEqual(self.graph.num_cities, 4)
        self.assertEqual(len(self.graph.cities), 4)
    
    def test_init_empty(self):
        """测试空初始化"""
        graph = Graph()
        self.assertEqual(graph.num_cities, 0)
        self.assertEqual(len(graph.cities), 0)
    
    def test_add_city(self):
        """测试添加城市"""
        graph = Graph()
        graph.add_city(0, 0)
        graph.add_city(10, 10)
        self.assertEqual(graph.num_cities, 2)
    
    def test_set_cities(self):
        """测试设置城市列表"""
        graph = Graph()
        cities = [(0, 0), (5, 5), (10, 0)]
        graph.set_cities(cities)
        self.assertEqual(graph.num_cities, 3)
    
    def test_euclidean_distance(self):
        """测试欧几里得距离计算"""
        # 3-4-5 直角三角形
        dist = Graph._euclidean_distance((0, 0), (3, 4))
        self.assertAlmostEqual(dist, 5.0, places=5)
        
        # 水平距离
        dist = Graph._euclidean_distance((0, 0), (10, 0))
        self.assertAlmostEqual(dist, 10.0, places=5)
        
        # 垂直距离
        dist = Graph._euclidean_distance((0, 0), (0, 7))
        self.assertAlmostEqual(dist, 7.0, places=5)
        
        # 同一点
        dist = Graph._euclidean_distance((5, 5), (5, 5))
        self.assertAlmostEqual(dist, 0.0, places=5)
    
    def test_distance_matrix(self):
        """测试距离矩阵"""
        # 检查矩阵大小
        self.assertEqual(len(self.graph.distance_matrix), 4)
        self.assertEqual(len(self.graph.distance_matrix[0]), 4)
        
        # 对角线应为 0
        for i in range(4):
            self.assertEqual(self.graph.distance_matrix[i][i], 0)
        
        # 检查对称性
        for i in range(4):
            for j in range(4):
                self.assertEqual(
                    self.graph.distance_matrix[i][j],
                    self.graph.distance_matrix[j][i]
                )
    
    def test_get_distance(self):
        """测试获取距离"""
        # (0,0) 到 (3,0) 距离为 3
        self.assertAlmostEqual(self.graph.get_distance(0, 1), 3.0, places=5)
        
        # (3,0) 到 (3,4) 距离为 4
        self.assertAlmostEqual(self.graph.get_distance(1, 2), 4.0, places=5)
        
        # (0,0) 到 (3,4) 距离为 5
        self.assertAlmostEqual(self.graph.get_distance(0, 2), 5.0, places=5)
    
    def test_initialize_pheromone(self):
        """测试初始化信息素"""
        self.graph.initialize_pheromone(1.5)
        
        self.assertEqual(len(self.graph.pheromone_matrix), 4)
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.graph.pheromone_matrix[i][j], 1.5)
    
    def test_get_pheromone(self):
        """测试获取信息素"""
        self.graph.initialize_pheromone(2.0)
        self.assertEqual(self.graph.get_pheromone(0, 1), 2.0)
        self.assertEqual(self.graph.get_pheromone(2, 3), 2.0)
    
    def test_update_pheromone(self):
        """测试更新信息素"""
        self.graph.initialize_pheromone(1.0)
        self.graph.update_pheromone(0, 1, 0.5)
        
        # 检查双向更新
        self.assertEqual(self.graph.get_pheromone(0, 1), 1.5)
        self.assertEqual(self.graph.get_pheromone(1, 0), 1.5)
        
        # 其他边不受影响
        self.assertEqual(self.graph.get_pheromone(2, 3), 1.0)
    
    def test_evaporate_pheromone(self):
        """测试信息素挥发"""
        self.graph.initialize_pheromone(1.0)
        self.graph.evaporate_pheromone(0.5)  # 挥发 50%
        
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(
                    self.graph.pheromone_matrix[i][j], 0.5, places=5
                )
    
    def test_calculate_path_distance(self):
        """测试计算路径距离"""
        # 路径 0 -> 1 -> 2 -> 3 -> 0
        # 距离: 3 + 4 + 3 + 4 = 14
        path = [0, 1, 2, 3]
        distance = self.graph.calculate_path_distance(path)
        self.assertAlmostEqual(distance, 14.0, places=5)
    
    def test_repr(self):
        """测试字符串表示"""
        repr_str = repr(self.graph)
        self.assertIn("Graph", repr_str)
        self.assertIn("num_cities=4", repr_str)


class TestGraphEdgeCases(unittest.TestCase):
    """Graph 边界情况测试"""
    
    def test_single_city(self):
        """测试单个城市"""
        graph = Graph([(0, 0)])
        self.assertEqual(graph.num_cities, 1)
        self.assertEqual(graph.get_distance(0, 0), 0)
    
    def test_two_cities(self):
        """测试两个城市"""
        graph = Graph([(0, 0), (10, 0)])
        self.assertEqual(graph.num_cities, 2)
        self.assertAlmostEqual(graph.get_distance(0, 1), 10.0, places=5)
    
    def test_collinear_cities(self):
        """测试共线城市"""
        cities = [(0, 0), (5, 0), (10, 0), (15, 0)]
        graph = Graph(cities)
        
        self.assertAlmostEqual(graph.get_distance(0, 1), 5.0, places=5)
        self.assertAlmostEqual(graph.get_distance(0, 3), 15.0, places=5)
    
    def test_negative_coordinates(self):
        """测试负坐标"""
        cities = [(-5, -5), (5, 5)]
        graph = Graph(cities)
        
        expected = math.sqrt(200)  # sqrt((10)^2 + (10)^2)
        self.assertAlmostEqual(graph.get_distance(0, 1), expected, places=5)
    
    def test_float_coordinates(self):
        """测试浮点坐标"""
        cities = [(0.5, 0.5), (1.5, 1.5)]
        graph = Graph(cities)
        
        expected = math.sqrt(2)
        self.assertAlmostEqual(graph.get_distance(0, 1), expected, places=5)


if __name__ == '__main__':
    unittest.main()
