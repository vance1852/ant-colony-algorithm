"""
蚁群类
Ant Colony Class
"""

import logging
from typing import List, Tuple, Optional, Callable

from .ant import Ant
from .graph import Graph
from .config import ACOConfig

# 配置日志
logger = logging.getLogger(__name__)


class AntColony:
    """蚁群类，管理整个蚁群算法的执行"""
    
    def __init__(self, graph: Graph, config: Optional[ACOConfig] = None):
        """
        初始化蚁群
        
        Args:
            graph: 图对象
            config: 配置参数，如果为 None 则使用默认配置
        """
        self.graph = graph
        self.config = config or ACOConfig()
        
        # 初始化蚂蚁
        self.ants: List[Ant] = [
            Ant(i, graph, self.config) 
            for i in range(self.config.num_ants)
        ]
        
        # 最优解记录
        self.best_path: List[int] = []
        self.best_distance: float = float('inf')
        
        # 迭代历史记录
        self.history: List[Tuple[int, float, float]] = []  # (iteration, best, average)
        
        # 初始化信息素
        self.graph.initialize_pheromone(self.config.initial_pheromone)
        
        logger.info(f"蚁群初始化完成: {self.config}")
    
    def run(
        self, 
        callback: Optional[Callable[[int, float, float], None]] = None,
        verbose: bool = True
    ) -> Tuple[List[int], float]:
        """
        运行蚁群算法
        
        Args:
            callback: 每次迭代后的回调函数，参数为 (iteration, best_distance, avg_distance)
            verbose: 是否输出详细信息
            
        Returns:
            (最优路径, 最优距离)
        """
        logger.info("开始运行蚁群算法...")
        
        for iteration in range(self.config.max_iterations):
            # 所有蚂蚁完成一次旅行
            iteration_distances = self._run_iteration()
            
            # 更新信息素
            self._update_pheromone()
            
            # 记录本次迭代结果
            avg_distance = sum(iteration_distances) / len(iteration_distances)
            self.history.append((iteration, self.best_distance, avg_distance))
            
            # 回调
            if callback:
                callback(iteration, self.best_distance, avg_distance)
            
            # 输出进度
            if verbose and (iteration + 1) % 10 == 0:
                logger.info(
                    f"迭代 {iteration + 1}/{self.config.max_iterations}: "
                    f"最优距离 = {self.best_distance:.2f}, 平均距离 = {avg_distance:.2f}"
                )
        
        logger.info(f"算法完成! 最优距离: {self.best_distance:.2f}")
        return self.best_path.copy(), self.best_distance
    
    def _run_iteration(self) -> List[float]:
        """
        执行一次迭代
        
        Returns:
            本次迭代所有蚂蚁的路径距离列表
        """
        distances = []
        
        for ant in self.ants:
            # 重置蚂蚁
            ant.reset()
            
            # 完成旅行
            ant.complete_tour()
            
            distances.append(ant.path_distance)
            
            # 更新全局最优
            if ant.path_distance < self.best_distance:
                self.best_distance = ant.path_distance
                self.best_path = ant.path.copy()
                logger.debug(f"发现更优解: {self.best_distance:.2f}")
        
        return distances
    
    def _update_pheromone(self):
        """更新信息素"""
        # 信息素挥发
        self.graph.evaporate_pheromone(self.config.rho)
        
        # 蚂蚁释放信息素
        for ant in self.ants:
            delta = ant.get_pheromone_delta()
            path = ant.path
            
            for i in range(len(path) - 1):
                self.graph.update_pheromone(path[i], path[i + 1], delta)
            
            # 回到起点的边
            self.graph.update_pheromone(path[-1], path[0], delta)
    
    def get_convergence_data(self) -> Tuple[List[int], List[float], List[float]]:
        """
        获取收敛数据
        
        Returns:
            (迭代次数列表, 最优距离列表, 平均距离列表)
        """
        iterations = [h[0] for h in self.history]
        best_distances = [h[1] for h in self.history]
        avg_distances = [h[2] for h in self.history]
        return iterations, best_distances, avg_distances
    
    def reset(self):
        """重置蚁群状态"""
        self.best_path = []
        self.best_distance = float('inf')
        self.history = []
        self.graph.initialize_pheromone(self.config.initial_pheromone)
        logger.info("蚁群状态已重置")
    
    def __repr__(self) -> str:
        return (
            f"AntColony(num_ants={len(self.ants)}, "
            f"best_distance={self.best_distance:.2f})"
        )
