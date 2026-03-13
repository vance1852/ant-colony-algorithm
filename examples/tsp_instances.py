"""
TSP 测试实例
TSP Test Instances
"""

from typing import List, Tuple


class TSPInstances:
    """TSP 测试实例集合"""
    
    @staticmethod
    def get_small_instance() -> Tuple[List[Tuple[float, float]], str]:
        """
        小规模测试实例（5个城市）
        
        Returns:
            (城市坐标列表, 实例名称)
        """
        cities = [
            (0, 0),
            (10, 0),
            (10, 10),
            (5, 15),
            (0, 10)
        ]
        return cities, "Small Instance (5 cities)"
    
    @staticmethod
    def get_medium_instance() -> Tuple[List[Tuple[float, float]], str]:
        """
        中等规模测试实例（10个城市）
        
        Returns:
            (城市坐标列表, 实例名称)
        """
        cities = [
            (0, 0),
            (20, 0),
            (40, 0),
            (40, 20),
            (40, 40),
            (20, 40),
            (0, 40),
            (0, 20),
            (20, 20),
            (30, 30)
        ]
        return cities, "Medium Instance (10 cities)"
    
    @staticmethod
    def get_large_instance() -> Tuple[List[Tuple[float, float]], str]:
        """
        大规模测试实例（20个城市）
        
        Returns:
            (城市坐标列表, 实例名称)
        """
        cities = [
            (60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
            (100, 160), (200, 160), (140, 140), (40, 120), (100, 120),
            (180, 100), (60, 80), (120, 80), (180, 60), (20, 40),
            (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)
        ]
        return cities, "Large Instance (20 cities)"
    
    @staticmethod
    def get_circle_instance(num_cities: int = 12) -> Tuple[List[Tuple[float, float]], str]:
        """
        圆形分布测试实例
        
        Args:
            num_cities: 城市数量
            
        Returns:
            (城市坐标列表, 实例名称)
        """
        import math
        
        radius = 50
        center = (50, 50)
        cities = []
        
        for i in range(num_cities):
            angle = 2 * math.pi * i / num_cities
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            cities.append((x, y))
        
        return cities, f"Circle Instance ({num_cities} cities)"
    
    @staticmethod
    def get_grid_instance(rows: int = 4, cols: int = 4) -> Tuple[List[Tuple[float, float]], str]:
        """
        网格分布测试实例
        
        Args:
            rows: 行数
            cols: 列数
            
        Returns:
            (城市坐标列表, 实例名称)
        """
        cities = []
        spacing = 20
        
        for i in range(rows):
            for j in range(cols):
                cities.append((j * spacing, i * spacing))
        
        return cities, f"Grid Instance ({rows}x{cols} = {rows * cols} cities)"
    
    @staticmethod
    def get_cluster_instance() -> Tuple[List[Tuple[float, float]], str]:
        """
        聚类分布测试实例（3个聚类）
        
        Returns:
            (城市坐标列表, 实例名称)
        """
        cities = [
            # 聚类 1 (左下)
            (10, 10), (15, 12), (12, 18), (8, 15), (18, 8),
            # 聚类 2 (右上)
            (80, 80), (85, 82), (82, 88), (78, 85), (88, 78),
            # 聚类 3 (中间)
            (45, 45), (50, 48), (48, 52), (42, 50), (52, 42)
        ]
        return cities, "Cluster Instance (15 cities, 3 clusters)"
    
    @staticmethod
    def get_all_instances() -> List[Tuple[List[Tuple[float, float]], str]]:
        """
        获取所有测试实例
        
        Returns:
            所有测试实例列表
        """
        return [
            TSPInstances.get_small_instance(),
            TSPInstances.get_medium_instance(),
            TSPInstances.get_large_instance(),
            TSPInstances.get_circle_instance(),
            TSPInstances.get_grid_instance(),
            TSPInstances.get_cluster_instance()
        ]
