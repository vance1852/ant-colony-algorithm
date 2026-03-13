"""
TSPInstances 测试实例测试
"""

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.tsp_instances import TSPInstances


class TestTSPInstances(unittest.TestCase):
    """TSPInstances 测试类"""
    
    def test_get_small_instance(self):
        """测试小规模实例"""
        cities, name = TSPInstances.get_small_instance()
        
        self.assertEqual(len(cities), 5)
        self.assertIn("5 cities", name)
        
        # 检查坐标格式
        for city in cities:
            self.assertEqual(len(city), 2)
            self.assertIsInstance(city[0], (int, float))
            self.assertIsInstance(city[1], (int, float))
    
    def test_get_medium_instance(self):
        """测试中等规模实例"""
        cities, name = TSPInstances.get_medium_instance()
        
        self.assertEqual(len(cities), 10)
        self.assertIn("10 cities", name)
    
    def test_get_large_instance(self):
        """测试大规模实例"""
        cities, name = TSPInstances.get_large_instance()
        
        self.assertEqual(len(cities), 20)
        self.assertIn("20 cities", name)
    
    def test_get_circle_instance(self):
        """测试圆形分布实例"""
        cities, name = TSPInstances.get_circle_instance(12)
        
        self.assertEqual(len(cities), 12)
        self.assertIn("12 cities", name)
        
        # 验证城市在圆上
        center = (50, 50)
        radius = 50
        for x, y in cities:
            dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            self.assertAlmostEqual(dist, radius, places=5)
    
    def test_get_circle_instance_custom_size(self):
        """测试自定义大小圆形实例"""
        for n in [4, 8, 16, 32]:
            cities, name = TSPInstances.get_circle_instance(n)
            self.assertEqual(len(cities), n)
    
    def test_get_grid_instance(self):
        """测试网格分布实例"""
        cities, name = TSPInstances.get_grid_instance(4, 4)
        
        self.assertEqual(len(cities), 16)
        self.assertIn("16 cities", name)
    
    def test_get_grid_instance_custom_size(self):
        """测试自定义大小网格实例"""
        cities, name = TSPInstances.get_grid_instance(3, 5)
        
        self.assertEqual(len(cities), 15)
        self.assertIn("3x5", name)
    
    def test_get_cluster_instance(self):
        """测试聚类分布实例"""
        cities, name = TSPInstances.get_cluster_instance()
        
        self.assertEqual(len(cities), 15)
        self.assertIn("3 clusters", name)
        
        # 验证有三个聚类
        # 聚类 1: 左下 (约 10, 10)
        # 聚类 2: 右上 (约 80, 80)
        # 聚类 3: 中间 (约 45, 45)
    
    def test_get_all_instances(self):
        """测试获取所有实例"""
        instances = TSPInstances.get_all_instances()
        
        self.assertGreaterEqual(len(instances), 5)
        
        for cities, name in instances:
            self.assertIsInstance(cities, list)
            self.assertIsInstance(name, str)
            self.assertGreater(len(cities), 0)


class TestTSPInstancesValidity(unittest.TestCase):
    """TSP 实例有效性测试"""
    
    def test_no_duplicate_cities(self):
        """测试没有重复城市"""
        instances = TSPInstances.get_all_instances()
        
        for cities, name in instances:
            unique_cities = set(cities)
            self.assertEqual(
                len(unique_cities), 
                len(cities), 
                f"{name} 包含重复城市"
            )
    
    def test_all_coordinates_finite(self):
        """测试所有坐标都是有限数"""
        instances = TSPInstances.get_all_instances()
        
        for cities, name in instances:
            for x, y in cities:
                self.assertTrue(
                    math.isfinite(x) and math.isfinite(y),
                    f"{name} 包含无限坐标"
                )
    
    def test_circle_instance_symmetry(self):
        """测试圆形实例对称性"""
        cities, _ = TSPInstances.get_circle_instance(8)
        
        # 计算质心
        cx = sum(c[0] for c in cities) / len(cities)
        cy = sum(c[1] for c in cities) / len(cities)
        
        # 质心应该接近圆心 (50, 50)
        self.assertAlmostEqual(cx, 50, places=3)
        self.assertAlmostEqual(cy, 50, places=3)
    
    def test_grid_instance_spacing(self):
        """测试网格实例间距"""
        cities, _ = TSPInstances.get_grid_instance(3, 3)
        
        # 检查相邻城市间距一致
        spacing = 20  # 默认间距
        
        # 第一行的城市
        self.assertAlmostEqual(cities[1][0] - cities[0][0], spacing, places=5)


if __name__ == '__main__':
    unittest.main()
