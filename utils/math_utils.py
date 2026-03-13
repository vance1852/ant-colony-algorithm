"""
数学工具函数
Math Utility Functions
"""

import math
import random
from typing import List, Tuple


class MathUtils:
    """数学工具类"""
    
    @staticmethod
    def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """计算欧几里得距离"""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    @staticmethod
    def manhattan_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """计算曼哈顿距离"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    @staticmethod
    def generate_random_cities(
        num_cities: int, 
        x_range: Tuple[float, float] = (0, 100),
        y_range: Tuple[float, float] = (0, 100),
        seed: int = None
    ) -> List[Tuple[float, float]]:
        """
        生成随机城市坐标
        
        Args:
            num_cities: 城市数量
            x_range: x 坐标范围
            y_range: y 坐标范围
            seed: 随机种子
            
        Returns:
            城市坐标列表
        """
        if seed is not None:
            random.seed(seed)
        
        cities = []
        for _ in range(num_cities):
            x = random.uniform(x_range[0], x_range[1])
            y = random.uniform(y_range[0], y_range[1])
            cities.append((x, y))
        
        return cities
    
    @staticmethod
    def calculate_path_distance(
        cities: List[Tuple[float, float]], 
        path: List[int]
    ) -> float:
        """
        计算路径总距离
        
        Args:
            cities: 城市坐标列表
            path: 路径（城市索引列表）
            
        Returns:
            路径总距离
        """
        total = 0.0
        for i in range(len(path) - 1):
            total += MathUtils.euclidean_distance(cities[path[i]], cities[path[i + 1]])
        # 回到起点
        total += MathUtils.euclidean_distance(cities[path[-1]], cities[path[0]])
        return total
    
    @staticmethod
    def normalize(values: List[float]) -> List[float]:
        """
        归一化列表
        
        Args:
            values: 数值列表
            
        Returns:
            归一化后的列表
        """
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            return [1.0 / len(values)] * len(values)
        
        return [(v - min_val) / (max_val - min_val) for v in values]
    
    @staticmethod
    def mean(values: List[float]) -> float:
        """计算平均值"""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    @staticmethod
    def std_dev(values: List[float]) -> float:
        """计算标准差"""
        if len(values) < 2:
            return 0.0
        
        avg = MathUtils.mean(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
