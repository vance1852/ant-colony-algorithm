"""
蚁群算法配置参数
ACO Configuration Parameters
"""

class ACOConfig:
    """蚁群算法配置类"""
    
    def __init__(
        self,
        alpha: float = 1.0,
        beta: float = 2.0,
        rho: float = 0.5,
        q: float = 100.0,
        num_ants: int = 20,
        max_iterations: int = 100,
        initial_pheromone: float = 1.0
    ):
        """
        初始化配置参数
        
        Args:
            alpha: 信息素重要程度因子，值越大蚂蚁越倾向于选择信息素浓度高的路径
            beta: 启发式信息重要程度因子，值越大蚂蚁越倾向于选择距离短的路径
            rho: 信息素挥发系数，范围 [0, 1]，值越大信息素挥发越快
            q: 信息素增量常数，用于计算蚂蚁释放的信息素量
            num_ants: 蚂蚁数量
            max_iterations: 最大迭代次数
            initial_pheromone: 初始信息素浓度
        """
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.num_ants = num_ants
        self.max_iterations = max_iterations
        self.initial_pheromone = initial_pheromone
        
        self._validate()
    
    def _validate(self):
        """验证参数有效性"""
        if self.alpha < 0:
            raise ValueError("alpha 必须为非负数")
        if self.beta < 0:
            raise ValueError("beta 必须为非负数")
        if not 0 <= self.rho <= 1:
            raise ValueError("rho 必须在 [0, 1] 范围内")
        if self.q <= 0:
            raise ValueError("q 必须为正数")
        if self.num_ants <= 0:
            raise ValueError("num_ants 必须为正整数")
        if self.max_iterations <= 0:
            raise ValueError("max_iterations 必须为正整数")
        if self.initial_pheromone <= 0:
            raise ValueError("initial_pheromone 必须为正数")
    
    def __repr__(self) -> str:
        return (
            f"ACOConfig(alpha={self.alpha}, beta={self.beta}, rho={self.rho}, "
            f"q={self.q}, num_ants={self.num_ants}, max_iterations={self.max_iterations})"
        )
