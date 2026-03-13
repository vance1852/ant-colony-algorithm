"""
图结构与距离矩阵
Graph Structure and Distance Matrix
"""

from typing import List, Tuple, Optional
import math


class Graph:
    """图类，用于表示 TSP 问题中的城市和距离"""
    
    def __init__(self, cities: Optional[List[Tuple[float, float]]] = None):
        """
        初始化图
        
        Args:
            cities: 城市坐标列表，每个元素为 (x, y) 坐标
        """
        self.cities: List[Tuple[float, float]] = cities or []
        self.num_cities: int = len(self.cities)
        self.distance_matrix: List[List[float]] = []
        self.pheromone_matrix: List[List[float]] = []
        
        if self.cities:
            self._build_distance_matrix()
    
    def add_city(self, x: float, y: float):
        """添加城市"""
        self.cities.append((x, y))
        self.num_cities = len(self.cities)
        self._build_distance_matrix()
    
    def set_cities(self, cities: List[Tuple[float, float]]):
        """设置城市列表"""
        self.cities = cities
        self.num_cities = len(cities)
        self._build_distance_matrix()
    
    def _build_distance_matrix(self):
        """构建距离矩阵"""
        n = self.num_cities
        self.distance_matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = self._euclidean_distance(self.cities[i], self.cities[j])
                self.distance_matrix[i][j] = dist
                self.distance_matrix[j][i] = dist
    
    @staticmethod
    def _euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """计算欧几里得距离"""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def get_distance(self, city_i: int, city_j: int) -> float:
        """获取两城市间的距离"""
        return self.distance_matrix[city_i][city_j]
    
    def initialize_pheromone(self, initial_value: float):
        """初始化信息素矩阵"""
        n = self.num_cities
        self.pheromone_matrix = [[initial_value] * n for _ in range(n)]
    
    def get_pheromone(self, city_i: int, city_j: int) -> float:
        """获取两城市间的信息素浓度"""
        return self.pheromone_matrix[city_i][city_j]
    
    def update_pheromone(self, city_i: int, city_j: int, delta: float):
        """更新信息素"""
        self.pheromone_matrix[city_i][city_j] += delta
        self.pheromone_matrix[city_j][city_i] += delta
    
    def evaporate_pheromone(self, rho: float):
        """信息素挥发"""
        n = self.num_cities
        for i in range(n):
            for j in range(n):
                self.pheromone_matrix[i][j] *= (1 - rho)
    
    def calculate_path_distance(self, path: List[int]) -> float:
        """计算路径总距离"""
        total = 0.0
        for i in range(len(path) - 1):
            total += self.get_distance(path[i], path[i + 1])
        # 回到起点
        total += self.get_distance(path[-1], path[0])
        return total
    
    def __repr__(self) -> str:
        return f"Graph(num_cities={self.num_cities})"
