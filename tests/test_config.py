"""
ACOConfig 配置类测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aco.config import ACOConfig


class TestACOConfig(unittest.TestCase):
    """ACOConfig 测试类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ACOConfig()
        self.assertEqual(config.alpha, 1.0)
        self.assertEqual(config.beta, 2.0)
        self.assertEqual(config.rho, 0.5)
        self.assertEqual(config.q, 100.0)
        self.assertEqual(config.num_ants, 20)
        self.assertEqual(config.max_iterations, 100)
        self.assertEqual(config.initial_pheromone, 1.0)
    
    def test_custom_config(self):
        """测试自定义配置"""
        config = ACOConfig(
            alpha=2.0,
            beta=3.0,
            rho=0.3,
            q=200.0,
            num_ants=30,
            max_iterations=150,
            initial_pheromone=2.0
        )
        self.assertEqual(config.alpha, 2.0)
        self.assertEqual(config.beta, 3.0)
        self.assertEqual(config.rho, 0.3)
        self.assertEqual(config.q, 200.0)
        self.assertEqual(config.num_ants, 30)
        self.assertEqual(config.max_iterations, 150)
        self.assertEqual(config.initial_pheromone, 2.0)
    
    def test_invalid_alpha(self):
        """测试无效的 alpha 值"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(alpha=-1.0)
        self.assertIn("alpha", str(context.exception))
    
    def test_invalid_beta(self):
        """测试无效的 beta 值"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(beta=-1.0)
        self.assertIn("beta", str(context.exception))
    
    def test_invalid_rho_too_low(self):
        """测试 rho 值过低"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(rho=-0.1)
        self.assertIn("rho", str(context.exception))
    
    def test_invalid_rho_too_high(self):
        """测试 rho 值过高"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(rho=1.5)
        self.assertIn("rho", str(context.exception))
    
    def test_invalid_q(self):
        """测试无效的 q 值"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(q=0)
        self.assertIn("q", str(context.exception))
    
    def test_invalid_num_ants(self):
        """测试无效的蚂蚁数量"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(num_ants=0)
        self.assertIn("num_ants", str(context.exception))
    
    def test_invalid_max_iterations(self):
        """测试无效的最大迭代次数"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(max_iterations=-10)
        self.assertIn("max_iterations", str(context.exception))
    
    def test_invalid_initial_pheromone(self):
        """测试无效的初始信息素"""
        with self.assertRaises(ValueError) as context:
            ACOConfig(initial_pheromone=0)
        self.assertIn("initial_pheromone", str(context.exception))
    
    def test_boundary_rho_values(self):
        """测试 rho 边界值"""
        config_zero = ACOConfig(rho=0)
        self.assertEqual(config_zero.rho, 0)
        
        config_one = ACOConfig(rho=1)
        self.assertEqual(config_one.rho, 1)
    
    def test_repr(self):
        """测试字符串表示"""
        config = ACOConfig()
        repr_str = repr(config)
        self.assertIn("ACOConfig", repr_str)
        self.assertIn("alpha=1.0", repr_str)


if __name__ == '__main__':
    unittest.main()
