"""
MathUtils 数学工具测试
"""

import unittest
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.math_utils import MathUtils


class TestMathUtils(unittest.TestCase):
    """MathUtils 测试类"""
    
    def test_euclidean_distance(self):
        """测试欧几里得距离"""
        # 3-4-5 三角形
        dist = MathUtils.euclidean_distance((0, 0), (3, 4))
        self.assertAlmostEqual(dist, 5.0, places=5)
        
        # 水平距离
        dist = MathUtils.euclidean_distance((0, 0), (10, 0))
        self.assertAlmostEqual(dist, 10.0, places=5)
        
        # 同一点
        dist = MathUtils.euclidean_distance((5, 5), (5, 5))
        self.assertAlmostEqual(dist, 0.0, places=5)
    
    def test_manhattan_distance(self):
        """测试曼哈顿距离"""
        dist = MathUtils.manhattan_distance((0, 0), (3, 4))
        self.assertEqual(dist, 7)
        
        dist = MathUtils.manhattan_distance((1, 1), (4, 5))
        self.assertEqual(dist, 7)
    
    def test_generate_random_cities(self):
        """测试生成随机城市"""
        cities = MathUtils.generate_random_cities(10)
        
        self.assertEqual(len(cities), 10)
        for x, y in cities:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)
    
    def test_generate_random_cities_custom_range(self):
        """测试自定义范围生成随机城市"""
        cities = MathUtils.generate_random_cities(
            5, 
            x_range=(-50, 50), 
            y_range=(0, 200)
        )
        
        self.assertEqual(len(cities), 5)
        for x, y in cities:
            self.assertGreaterEqual(x, -50)
            self.assertLessEqual(x, 50)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 200)
    
    def test_generate_random_cities_with_seed(self):
        """测试带种子生成随机城市"""
        cities1 = MathUtils.generate_random_cities(5, seed=42)
        cities2 = MathUtils.generate_random_cities(5, seed=42)
        
        self.assertEqual(cities1, cities2)
    
    def test_calculate_path_distance(self):
        """测试计算路径距离"""
        cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        path = [0, 1, 2, 3]
        
        distance = MathUtils.calculate_path_distance(cities, path)
        self.assertAlmostEqual(distance, 40.0, places=5)
    
    def test_normalize(self):
        """测试归一化"""
        values = [0, 50, 100]
        normalized = MathUtils.normalize(values)
        
        self.assertAlmostEqual(normalized[0], 0.0, places=5)
        self.assertAlmostEqual(normalized[1], 0.5, places=5)
        self.assertAlmostEqual(normalized[2], 1.0, places=5)
    
    def test_normalize_same_values(self):
        """测试相同值归一化"""
        values = [5, 5, 5]
        normalized = MathUtils.normalize(values)
        
        # 相同值应该均匀分布
        for n in normalized:
            self.assertAlmostEqual(n, 1/3, places=5)
    
    def test_mean(self):
        """测试平均值"""
        values = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(MathUtils.mean(values), 3.0, places=5)
        
        # 空列表
        self.assertEqual(MathUtils.mean([]), 0.0)
    
    def test_std_dev(self):
        """测试标准差"""
        values = [2, 4, 4, 4, 5, 5, 7, 9]
        std = MathUtils.std_dev(values)
        self.assertAlmostEqual(std, 2.0, places=5)
        
        # 单个值
        self.assertEqual(MathUtils.std_dev([5]), 0.0)
        
        # 空列表
        self.assertEqual(MathUtils.std_dev([]), 0.0)
    
    def test_std_dev_uniform(self):
        """测试均匀值的标准差"""
        values = [5, 5, 5, 5]
        self.assertAlmostEqual(MathUtils.std_dev(values), 0.0, places=5)


if __name__ == '__main__':
    unittest.main()
