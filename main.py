#!/usr/bin/env python3
"""
蚁群算法主程序
Ant Colony Optimization Main Program

纯 Python 实现，不使用 numpy
Pure Python implementation without numpy
"""

import argparse
import logging
import sys
import time
from typing import List, Tuple

from aco import ACOConfig, Graph, AntColony
from utils import MathUtils, Visualizer
from examples import TSPInstances


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='蚁群算法 (ACO) - 纯 Python 实现',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python main.py                          # 运行所有测试
  python main.py -i small                 # 只运行小规模实例
  python main.py -i medium -n 50 -a 30    # 中等实例，50次迭代，30只蚂蚁
  python main.py -i random --cities 20    # 随机生成20个城市
  python main.py --list                   # 列出所有可用实例
        '''
    )
    
    parser.add_argument(
        '-i', '--instance',
        choices=['small', 'medium', 'large', 'circle', 'grid', 'cluster', 'random', 'all'],
        default='all',
        help='选择测试实例 (默认: all)'
    )
    
    parser.add_argument(
        '-n', '--iterations',
        type=int,
        default=100,
        help='最大迭代次数 (默认: 100)'
    )
    
    parser.add_argument(
        '-a', '--ants',
        type=int,
        default=None,
        help='蚂蚁数量 (默认: 自动根据城市数量)'
    )
    
    parser.add_argument(
        '--alpha',
        type=float,
        default=1.0,
        help='信息素重要程度因子 (默认: 1.0)'
    )
    
    parser.add_argument(
        '--beta',
        type=float,
        default=2.0,
        help='启发式信息重要程度因子 (默认: 2.0)'
    )
    
    parser.add_argument(
        '--rho',
        type=float,
        default=0.5,
        help='信息素挥发系数 (默认: 0.5)'
    )
    
    parser.add_argument(
        '--cities',
        type=int,
        default=15,
        help='随机实例的城市数量 (默认: 15)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='随机种子 (用于可重复实验)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='列出所有可用实例'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='安静模式，减少输出'
    )
    
    parser.add_argument(
        '--no-chart',
        action='store_true',
        help='不显示 ASCII 图表'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='运行参数敏感性对比测试'
    )
    
    return parser.parse_args()


def run_single_instance(
    cities: List[Tuple[float, float]],
    instance_name: str,
    config: ACOConfig = None,
    show_chart: bool = True,
    quiet: bool = False
) -> Tuple[List[int], float]:
    """
    运行单个 TSP 实例
    
    Args:
        cities: 城市坐标列表
        instance_name: 实例名称
        config: 算法配置
        show_chart: 是否显示图表
        quiet: 安静模式
        
    Returns:
        (最优路径, 最优距离)
    """
    if not quiet:
        print("\n" + "=" * 60)
        print(f"  测试实例: {instance_name}")
        print(f"  城市数量: {len(cities)}")
        print("=" * 60)
    
    # 创建图
    graph = Graph(cities)
    
    # 使用默认配置或自定义配置
    if config is None:
        config = ACOConfig(
            alpha=1.0,
            beta=2.0,
            rho=0.5,
            q=100.0,
            num_ants=max(10, len(cities)),
            max_iterations=100
        )
    
    if not quiet:
        print(f"\n算法参数:")
        print(f"  - alpha (信息素因子): {config.alpha}")
        print(f"  - beta (启发式因子): {config.beta}")
        print(f"  - rho (挥发系数): {config.rho}")
        print(f"  - Q (信息素常数): {config.q}")
        print(f"  - 蚂蚁数量: {config.num_ants}")
        print(f"  - 最大迭代: {config.max_iterations}")
    
    # 创建蚁群
    colony = AntColony(graph, config)
    
    # 记录开始时间
    start_time = time.time()
    
    # 运行算法
    if not quiet:
        print("\n开始优化...")
    
    def progress_callback(iteration: int, best: float, avg: float):
        if not quiet and (iteration + 1) % 20 == 0:
            bar = Visualizer.progress_bar(iteration + 1, config.max_iterations)
            print(f"  {bar} 最优: {best:.2f}")
    
    best_path, best_distance = colony.run(callback=progress_callback, verbose=False)
    
    # 记录结束时间
    elapsed_time = time.time() - start_time
    
    # 打印结果
    print(Visualizer.print_statistics(best_distance, best_path, colony.history))
    
    # 绘制图表
    if show_chart:
        iterations, best_dists, avg_dists = colony.get_convergence_data()
        print("\n" + Visualizer.draw_convergence_chart(iterations, best_dists))
        print("\n" + Visualizer.draw_path(cities, best_path))
    
    print(f"\n运行时间: {elapsed_time:.3f} 秒")
    
    return best_path, best_distance


def run_comparison_test(quiet: bool = False):
    """运行参数对比测试"""
    print("\n" + "=" * 60)
    print("  参数敏感性测试")
    print("=" * 60)
    
    # 使用中等规模实例
    cities, name = TSPInstances.get_medium_instance()
    graph = Graph(cities)
    
    # 测试不同的 alpha 值
    print("\n测试不同的 alpha 值 (信息素重要程度):")
    print("-" * 40)
    
    alpha_values = [0.5, 1.0, 2.0, 3.0]
    
    for alpha in alpha_values:
        config = ACOConfig(alpha=alpha, beta=2.0, num_ants=10, max_iterations=50)
        colony = AntColony(Graph(cities), config)
        _, best_dist = colony.run(verbose=False)
        print(f"  alpha = {alpha}: 最优距离 = {best_dist:.2f}")
    
    # 测试不同的 beta 值
    print("\n测试不同的 beta 值 (启发式信息重要程度):")
    print("-" * 40)
    
    beta_values = [1.0, 2.0, 3.0, 5.0]
    
    for beta in beta_values:
        config = ACOConfig(alpha=1.0, beta=beta, num_ants=10, max_iterations=50)
        colony = AntColony(Graph(cities), config)
        _, best_dist = colony.run(verbose=False)
        print(f"  beta = {beta}: 最优距离 = {best_dist:.2f}")
    
    # 测试不同的 rho 值
    print("\n测试不同的 rho 值 (信息素挥发系数):")
    print("-" * 40)
    
    rho_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for rho in rho_values:
        config = ACOConfig(alpha=1.0, beta=2.0, rho=rho, num_ants=10, max_iterations=50)
        colony = AntColony(Graph(cities), config)
        _, best_dist = colony.run(verbose=False)
        print(f"  rho = {rho}: 最优距离 = {best_dist:.2f}")


def run_random_instance_test(num_cities: int = 15, seed: int = None, config: ACOConfig = None, 
                             show_chart: bool = True, quiet: bool = False):
    """运行随机实例测试"""
    if not quiet:
        print("\n" + "=" * 60)
        print("  随机实例测试")
        print("=" * 60)
    
    # 生成随机城市
    cities = MathUtils.generate_random_cities(num_cities, seed=seed or 42)
    
    if not quiet:
        print(f"\n生成 {num_cities} 个随机城市:")
        for i, (x, y) in enumerate(cities):
            print(f"  城市 {i}: ({x:.2f}, {y:.2f})")
    
    # 运行算法
    return run_single_instance(cities, f"Random Instance ({num_cities} cities)", 
                               config, show_chart, quiet)


def get_instance_by_name(name: str) -> Tuple[List[Tuple[float, float]], str]:
    """根据名称获取实例"""
    instances = {
        'small': TSPInstances.get_small_instance,
        'medium': TSPInstances.get_medium_instance,
        'large': TSPInstances.get_large_instance,
        'circle': lambda: TSPInstances.get_circle_instance(12),
        'grid': lambda: TSPInstances.get_grid_instance(4, 4),
        'cluster': TSPInstances.get_cluster_instance,
    }
    return instances[name]()


def list_instances():
    """列出所有可用实例"""
    print("\n可用的测试实例:")
    print("-" * 50)
    print(f"  {'名称':<12} {'城市数':<10} {'描述'}")
    print("-" * 50)
    print(f"  {'small':<12} {'5':<10} 小规模测试实例")
    print(f"  {'medium':<12} {'10':<10} 中等规模测试实例")
    print(f"  {'large':<12} {'20':<10} 大规模测试实例")
    print(f"  {'circle':<12} {'12':<10} 圆形分布实例")
    print(f"  {'grid':<12} {'16':<10} 网格分布实例 (4x4)")
    print(f"  {'cluster':<12} {'15':<10} 聚类分布实例 (3个聚类)")
    print(f"  {'random':<12} {'可配置':<10} 随机生成实例 (--cities)")
    print(f"  {'all':<12} {'-':<10} 运行所有预设实例")
    print("-" * 50)


def main():
    """主函数"""
    args = parse_args()
    
    # 列出实例
    if args.list:
        list_instances()
        return
    
    # 设置随机种子
    if args.seed is not None:
        import random
        random.seed(args.seed)
    
    print("\n" + "=" * 60)
    print("  蚁群算法 (Ant Colony Optimization)")
    print("  纯 Python 实现 - 无 numpy 依赖")
    print("=" * 60)
    
    # 构建配置
    def make_config(num_cities: int) -> ACOConfig:
        return ACOConfig(
            alpha=args.alpha,
            beta=args.beta,
            rho=args.rho,
            q=100.0,
            num_ants=args.ants or max(10, num_cities),
            max_iterations=args.iterations
        )
    
    show_chart = not args.no_chart
    quiet = args.quiet
    
    if args.instance == 'all':
        # 运行所有预设实例
        for name in ['small', 'medium', 'circle', 'cluster']:
            cities, instance_name = get_instance_by_name(name)
            config = make_config(len(cities))
            run_single_instance(cities, instance_name, config, show_chart, quiet)
        
        # 参数对比测试
        if args.compare:
            run_comparison_test(quiet)
        
        # 随机实例
        run_random_instance_test(args.cities, args.seed, make_config(args.cities), show_chart, quiet)
    
    elif args.instance == 'random':
        # 只运行随机实例
        config = make_config(args.cities)
        run_random_instance_test(args.cities, args.seed, config, show_chart, quiet)
    
    else:
        # 运行指定实例
        cities, instance_name = get_instance_by_name(args.instance)
        config = make_config(len(cities))
        run_single_instance(cities, instance_name, config, show_chart, quiet)
        
        if args.compare:
            run_comparison_test(quiet)
    
    print("\n" + "=" * 60)
    print("  完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
