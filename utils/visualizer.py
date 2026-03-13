"""
可视化工具
Visualization Utilities
"""

from typing import List, Tuple


class Visualizer:
    """ASCII 可视化工具类"""
    
    @staticmethod
    def draw_convergence_chart(
        iterations: List[int],
        best_distances: List[float],
        width: int = 60,
        height: int = 15
    ) -> str:
        """
        绘制收敛曲线（ASCII 图）
        
        Args:
            iterations: 迭代次数列表
            best_distances: 最优距离列表
            width: 图表宽度
            height: 图表高度
            
        Returns:
            ASCII 图表字符串
        """
        if not best_distances:
            return "无数据"
        
        min_dist = min(best_distances)
        max_dist = max(best_distances)
        dist_range = max_dist - min_dist if max_dist != min_dist else 1
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 绘制边框
        for i in range(height):
            canvas[i][0] = '│'
        for j in range(width):
            canvas[height - 1][j] = '─'
        canvas[height - 1][0] = '└'
        
        # 绘制数据点
        step = max(1, len(best_distances) // (width - 2))
        for i in range(0, len(best_distances), step):
            x = min(1 + i * (width - 2) // len(best_distances), width - 1)
            y = int((max_dist - best_distances[i]) / dist_range * (height - 2))
            y = max(0, min(height - 2, y))
            canvas[y][x] = '●'
        
        # 转换为字符串
        lines = [''.join(row) for row in canvas]
        
        # 添加标签
        result = []
        result.append(f"  收敛曲线 (迭代次数: {len(iterations)})")
        result.append(f"  {max_dist:.1f} ┐")
        result.extend(['  ' + line for line in lines])
        result.append(f"  {min_dist:.1f} ┘")
        result.append(f"  {'0':^{width//2}}{'迭代次数':^{width//2}}{len(iterations)}")
        
        return '\n'.join(result)
    
    @staticmethod
    def draw_path(
        cities: List[Tuple[float, float]],
        path: List[int],
        width: int = 50,
        height: int = 25
    ) -> str:
        """
        绘制路径图（ASCII 图）
        
        Args:
            cities: 城市坐标列表
            path: 路径
            width: 图表宽度
            height: 图表高度
            
        Returns:
            ASCII 图表字符串
        """
        if not cities or not path:
            return "无数据"
        
        # 计算坐标范围
        x_coords = [c[0] for c in cities]
        y_coords = [c[1] for c in cities]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        x_range = max_x - min_x if max_x != min_x else 1
        y_range = max_y - min_y if max_y != min_y else 1
        
        # 创建画布
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # 绘制边框
        for i in range(height):
            canvas[i][0] = '│'
            canvas[i][width - 1] = '│'
        for j in range(width):
            canvas[0][j] = '─'
            canvas[height - 1][j] = '─'
        canvas[0][0] = '┌'
        canvas[0][width - 1] = '┐'
        canvas[height - 1][0] = '└'
        canvas[height - 1][width - 1] = '┘'
        
        # 映射城市到画布坐标
        def map_to_canvas(city_idx: int) -> Tuple[int, int]:
            x, y = cities[city_idx]
            cx = int((x - min_x) / x_range * (width - 4)) + 2
            cy = int((max_y - y) / y_range * (height - 4)) + 2
            return cx, cy
        
        # 绘制城市
        for i, city_idx in enumerate(path):
            cx, cy = map_to_canvas(city_idx)
            if 0 <= cy < height and 0 <= cx < width:
                # 起点用 ★ 标记
                if i == 0:
                    canvas[cy][cx] = '★'
                else:
                    canvas[cy][cx] = '○'
        
        # 转换为字符串
        lines = [''.join(row) for row in canvas]
        
        result = []
        result.append("  路径图 (★=起点, ○=城市)")
        result.extend(['  ' + line for line in lines])
        result.append(f"  路径: {' → '.join(str(p) for p in path[:8])}{'...' if len(path) > 8 else ''} → {path[0]}")
        
        return '\n'.join(result)
    
    @staticmethod
    def print_statistics(
        best_distance: float,
        best_path: List[int],
        history: List[Tuple[int, float, float]]
    ) -> str:
        """
        打印统计信息
        
        Args:
            best_distance: 最优距离
            best_path: 最优路径
            history: 历史记录
            
        Returns:
            统计信息字符串
        """
        lines = []
        lines.append("=" * 50)
        lines.append("  蚁群算法运行结果")
        lines.append("=" * 50)
        lines.append(f"  最优距离: {best_distance:.4f}")
        lines.append(f"  路径长度: {len(best_path)} 个城市")
        
        if history:
            initial_best = history[0][1]
            final_best = history[-1][1]
            improvement = (initial_best - final_best) / initial_best * 100 if initial_best > 0 else 0
            
            lines.append(f"  初始最优: {initial_best:.4f}")
            lines.append(f"  最终最优: {final_best:.4f}")
            lines.append(f"  改进幅度: {improvement:.2f}%")
            lines.append(f"  迭代次数: {len(history)}")
        
        lines.append("=" * 50)
        
        # 打印路径
        lines.append("  最优路径:")
        path_str = " → ".join(str(p) for p in best_path)
        path_str += f" → {best_path[0]}"
        
        # 分行显示
        max_line_len = 45
        while len(path_str) > max_line_len:
            split_idx = path_str.rfind(' → ', 0, max_line_len)
            if split_idx == -1:
                split_idx = max_line_len
            lines.append(f"    {path_str[:split_idx]}")
            path_str = path_str[split_idx + 3:]
        lines.append(f"    {path_str}")
        
        lines.append("=" * 50)
        
        return '\n'.join(lines)
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 40) -> str:
        """
        生成进度条
        
        Args:
            current: 当前进度
            total: 总数
            width: 进度条宽度
            
        Returns:
            进度条字符串
        """
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percent * 100:.1f}%"
