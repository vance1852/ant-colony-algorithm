"""
蚂蚁类
Ant Class
"""

import random
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph
    from .config import ACOConfig


class Ant:
    """蚂蚁类，模拟单只蚂蚁的行为"""
    
    def __init__(self, ant_id: int, graph: 'Graph', config: 'ACOConfig'):
        """
        初始化蚂蚁
        
        Args:
            ant_id: 蚂蚁编号
            graph: 图对象
            config: 配置参数
        """
        self.ant_id = ant_id
        self.graph = graph
        self.config = config
        
        self.path: List[int] = []
        self.visited: List[bool] = []
        self.path_distance: float = 0.0
        self.current_city: int = -1
    
    def reset(self, start_city: Optional[int] = None):
        """
        重置蚂蚁状态
        
        Args:
            start_city: 起始城市，如果为 None 则随机选择
        """
        self.path = []
        self.visited = [False] * self.graph.num_cities
        self.path_distance = 0.0
        
        if start_city is None:
            start_city = random.randint(0, self.graph.num_cities - 1)
        
        self.current_city = start_city
        self.path.append(start_city)
        self.visited[start_city] = True
    
    def select_next_city(self) -> int:
        """
        选择下一个城市（轮盘赌选择）
        
        Returns:
            下一个城市的索引
        """
        unvisited = self._get_unvisited_cities()
        
        if not unvisited:
            return -1
        
        # 计算转移概率
        probabilities = self._calculate_probabilities(unvisited)
        
        # 轮盘赌选择
        return self._roulette_wheel_selection(unvisited, probabilities)
    
    def _get_unvisited_cities(self) -> List[int]:
        """获取未访问的城市列表"""
        return [i for i in range(self.graph.num_cities) if not self.visited[i]]
    
    def _calculate_probabilities(self, unvisited: List[int]) -> List[float]:
        """
        计算转移概率
        
        Args:
            unvisited: 未访问城市列表
            
        Returns:
            各城市的转移概率
        """
        alpha = self.config.alpha
        beta = self.config.beta
        current = self.current_city
        
        # 计算分子（信息素^alpha * 启发式信息^beta）
        numerators = []
        for city in unvisited:
            pheromone = self.graph.get_pheromone(current, city)
            distance = self.graph.get_distance(current, city)
            
            # 启发式信息 = 1 / 距离
            heuristic = 1.0 / distance if distance > 0 else float('inf')
            
            # 计算吸引度
            attractiveness = (pheromone ** alpha) * (heuristic ** beta)
            numerators.append(attractiveness)
        
        # 计算概率
        total = sum(numerators)
        if total == 0:
            # 如果总和为0，均匀分布
            return [1.0 / len(unvisited)] * len(unvisited)
        
        return [n / total for n in numerators]
    
    def _roulette_wheel_selection(self, cities: List[int], probabilities: List[float]) -> int:
        """
        轮盘赌选择
        
        Args:
            cities: 候选城市列表
            probabilities: 对应的概率列表
            
        Returns:
            选中的城市
        """
        r = random.random()
        cumulative = 0.0
        
        for city, prob in zip(cities, probabilities):
            cumulative += prob
            if r <= cumulative:
                return city
        
        # 防止浮点误差，返回最后一个城市
        return cities[-1]
    
    def move_to(self, city: int):
        """
        移动到指定城市
        
        Args:
            city: 目标城市
        """
        if city < 0 or city >= self.graph.num_cities:
            raise ValueError(f"无效的城市索引: {city}")
        
        if self.visited[city]:
            raise ValueError(f"城市 {city} 已被访问")
        
        # 更新路径距离
        self.path_distance += self.graph.get_distance(self.current_city, city)
        
        # 更新状态
        self.current_city = city
        self.path.append(city)
        self.visited[city] = True
    
    def complete_tour(self):
        """完成一次完整的旅行"""
        while True:
            next_city = self.select_next_city()
            if next_city == -1:
                break
            self.move_to(next_city)
        
        # 加上返回起点的距离
        self.path_distance += self.graph.get_distance(self.current_city, self.path[0])
    
    def get_pheromone_delta(self) -> float:
        """
        计算该蚂蚁释放的信息素量
        
        Returns:
            信息素增量
        """
        if self.path_distance == 0:
            return 0.0
        return self.config.q / self.path_distance
    
    def __repr__(self) -> str:
        return f"Ant(id={self.ant_id}, path_distance={self.path_distance:.2f})"
