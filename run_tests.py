#!/usr/bin/env python3
"""
测试运行脚本
Test Runner Script
"""

import unittest
import sys
import os
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests(verbosity=2):
    """运行所有测试"""
    print("=" * 70)
    print("  蚁群算法测试套件")
    print("  Ant Colony Optimization Test Suite")
    print("=" * 70)
    print()
    
    # 发现并加载所有测试
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # 统计测试数量
    test_count = suite.countTestCases()
    print(f"发现 {test_count} 个测试用例")
    print("-" * 70)
    print()
    
    # 运行测试
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    elapsed_time = time.time() - start_time
    
    # 打印总结
    print()
    print("=" * 70)
    print("  测试总结")
    print("=" * 70)
    print(f"  运行测试: {result.testsRun}")
    print(f"  成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败: {len(result.failures)}")
    print(f"  错误: {len(result.errors)}")
    print(f"  跳过: {len(result.skipped)}")
    print(f"  耗时: {elapsed_time:.3f} 秒")
    print("=" * 70)
    
    # 返回是否全部通过
    return len(result.failures) == 0 and len(result.errors) == 0


def run_specific_test(test_name):
    """运行特定测试模块"""
    print(f"运行测试模块: {test_name}")
    print("-" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{test_name}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 运行特定测试
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # 运行所有测试
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
