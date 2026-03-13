"""
Visualizer 可视化工具测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.visualizer import Visualizer


class TestVisualizer(unittest.TestCase):
    """Visualizer 测试类"""
    
    def test_draw_convergence_chart(self):
        """测试绘制收敛曲线"""
        iterations = list(range(10))
        best_distances = [100, 95, 90, 85, 80, 78, 76, 75, 74, 74]
        
        chart = Visualizer.draw_convergence_chart(iterations, best_distances)
        
        self.assertIsInstance(chart, str)
        self.assertIn("收敛曲线", chart)
        self.assertIn("●", chart)
    
    def test_draw_convergence_chart_empty(self):
        """测试空数据绘制"""
        chart = Visualizer.draw_convergence_chart([], [])
        self.assertEqual(chart, "无数据")
    
    def test_draw_convergence_chart_single_value(self):
        """测试单个值绘制"""
        chart = Visualizer.draw_convergence_chart([0], [100])
        self.assertIsInstance(chart, str)
    
    def test_draw_path(self):
        """测试绘制路径图"""
        cities = [(0, 0), (10, 0), (10, 10), (0, 10)]
        path = [0, 1, 2, 3]
        
        chart = Visualizer.draw_path(cities, path)
        
        self.assertIsInstance(chart, str)
        self.assertIn("路径图", chart)
        self.assertIn("★", chart)  # 起点标记
    
    def test_draw_path_empty(self):
        """测试空数据绘制路径"""
        chart = Visualizer.draw_path([], [])
        self.assertEqual(chart, "无数据")
    
    def test_print_statistics(self):
        """测试打印统计信息"""
        best_distance = 100.5
        best_path = [0, 1, 2, 3]
        history = [(0, 120, 150), (1, 110, 140), (2, 100.5, 130)]
        
        stats = Visualizer.print_statistics(best_distance, best_path, history)
        
        self.assertIsInstance(stats, str)
        self.assertIn("100.5", stats)
        self.assertIn("蚁群算法运行结果", stats)
    
    def test_print_statistics_empty_history(self):
        """测试空历史记录"""
        stats = Visualizer.print_statistics(100, [0, 1], [])
        self.assertIsInstance(stats, str)
    
    def test_progress_bar(self):
        """测试进度条"""
        bar = Visualizer.progress_bar(50, 100)
        
        self.assertIn("50.0%", bar)
        self.assertIn("█", bar)
        self.assertIn("░", bar)
    
    def test_progress_bar_zero(self):
        """测试零进度"""
        bar = Visualizer.progress_bar(0, 100)
        self.assertIn("0.0%", bar)
    
    def test_progress_bar_complete(self):
        """测试完成进度"""
        bar = Visualizer.progress_bar(100, 100)
        self.assertIn("100.0%", bar)
    
    def test_progress_bar_zero_total(self):
        """测试总数为零"""
        bar = Visualizer.progress_bar(0, 0)
        self.assertIn("0.0%", bar)


class TestVisualizerOutput(unittest.TestCase):
    """可视化输出格式测试"""
    
    def test_convergence_chart_dimensions(self):
        """测试收敛曲线尺寸"""
        iterations = list(range(100))
        best_distances = [100 - i * 0.5 for i in range(100)]
        
        chart = Visualizer.draw_convergence_chart(
            iterations, best_distances, width=80, height=20
        )
        
        lines = chart.split('\n')
        # 检查输出有多行
        self.assertGreater(len(lines), 10)
    
    def test_path_chart_dimensions(self):
        """测试路径图尺寸"""
        cities = [(0, 0), (50, 0), (50, 50), (0, 50)]
        path = [0, 1, 2, 3]
        
        chart = Visualizer.draw_path(cities, path, width=60, height=30)
        
        lines = chart.split('\n')
        self.assertGreater(len(lines), 20)
    
    def test_statistics_improvement_calculation(self):
        """测试改进幅度计算"""
        history = [(0, 200, 250), (1, 150, 200), (2, 100, 150)]
        
        stats = Visualizer.print_statistics(100, [0, 1, 2], history)
        
        # 改进幅度 = (200 - 100) / 200 * 100 = 50%
        self.assertIn("50.00%", stats)


if __name__ == '__main__':
    unittest.main()
