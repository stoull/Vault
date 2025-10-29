#!/usr/bin/env python3
"""
简单的logger测试文件
用于验证logger类的各种功能
"""

import os
import tempfile
import unittest
from logger import SimpleLogger, ColoredLogger, PerformanceLogger

class TestSimpleLogger(unittest.TestCase):
    """测试SimpleLogger类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_basic_logging(self):
        """测试基本日志功能"""
        logger = SimpleLogger(
            name="TestLogger",
            log_file=self.log_file,
            console_output=False,  # 关闭控制台输出，避免干扰测试
            file_output=True,
            log_level="DEBUG"
        )
        
        # 记录各种级别的日志
        logger.debug("调试信息")
        logger.info("一般信息")
        logger.warning("警告信息")
        logger.error("错误信息")
        logger.critical("严重错误")
        
        logger.close()
        
        # 验证日志文件是否创建
        self.assertTrue(os.path.exists(self.log_file))
        
        # 验证日志内容
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("调试信息", content)
            self.assertIn("一般信息", content)
            self.assertIn("警告信息", content)
            self.assertIn("错误信息", content)
            self.assertIn("严重错误", content)
    
    def test_exception_logging(self):
        """测试异常日志记录"""
        logger = SimpleLogger(
            name="ExceptionLogger",
            log_file=self.log_file,
            console_output=False,
            file_output=True
        )
        
        try:
            result = 1 / 0
        except Exception as e:
            logger.log_exception("测试异常")
        
        logger.close()
        
        # 验证异常信息是否记录
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("测试异常", content)
            self.assertIn("ZeroDivisionError", content)
    
    def test_dynamic_level_setting(self):
        """测试动态级别设置"""
        logger = SimpleLogger(
            name="LevelLogger",
            log_file=self.log_file,
            console_output=False,
            file_output=True,
            log_level="INFO"
        )
        
        # 初始级别为INFO，DEBUG信息应该不记录
        logger.debug("这条不会显示")
        logger.info("这条会显示")
        
        # 调整到DEBUG级别
        logger.set_level("DEBUG")
        logger.debug("现在这条会显示")
        
        logger.close()
        
        # 验证日志内容
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            # 应该只有2条INFO以上的日志和1条DEBUG日志
            self.assertIn("这条会显示", content)
            self.assertIn("现在这条会显示", content)
    
    def test_custom_format(self):
        """测试自定义格式"""
        custom_format = "%(levelname)s - %(message)s - %(asctime)s"
        logger = SimpleLogger(
            name="FormatLogger",
            log_file=self.log_file,
            console_output=False,
            file_output=True,
            log_format=custom_format
        )
        
        logger.info("自定义格式测试")
        logger.close()
        
        # 验证自定义格式
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("INFO - 自定义格式测试", content)

class TestPerformanceLogger(unittest.TestCase):
    """测试PerformanceLogger类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "performance.log")
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_performance_logging(self):
        """测试性能日志记录"""
        perf_logger = PerformanceLogger(log_file=self.log_file)
        
        perf_logger.log_function_call("test_function", 0.1234)
        perf_logger.log_memory_usage(128.5)
        perf_logger.log_performance_summary("测试摘要")
        
        perf_logger.logger.close()
        
        # 验证性能日志内容
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("FUNCTION_CALL: test_function", content)
            self.assertIn("EXEC_TIME: 0.1234", content)
            self.assertIn("MEMORY_USAGE: 128.5", content)
            self.assertIn("PERFORMANCE_SUMMARY: 测试摘要", content)

def run_simple_test():
    """运行简单的功能测试"""
    print("=== 运行简单的Logger功能测试 ===")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    log_file = os.path.join(temp_dir, "simple_test.log")
    
    try:
        # 测试基本功能
        print("1. 测试基本日志功能...")
        logger = SimpleLogger(
            name="SimpleTest",
            log_file=log_file,
            console_output=True,
            file_output=True,
            log_level="DEBUG"
        )
        
        logger.debug("调试信息")
        logger.info("信息记录")
        logger.warning("警告记录")
        logger.error("错误记录")
        logger.critical("严重错误记录")
        
        # 测试异常记录
        try:
            x = 1 / 0
        except Exception:
            logger.log_exception("测试异常记录")
        
        logger.close()
        
        # 验证文件是否创建
        if os.path.exists(log_file):
            print("✅ 日志文件创建成功")
            print(f"日志文件位置: {log_file}")
            
            # 显示文件内容
            with open(log_file, 'r', encoding='utf-8') as f:
                print("日志内容:")
                print("-" * 50)
                print(f.read())
        else:
            print("❌ 日志文件创建失败")
        
        # 测试带颜色的logger
        print("\n2. 测试带颜色的Logger...")
        colored_logger = ColoredLogger(
            name="ColoredTest",
            log_file=log_file.replace(".log", "_colored.log"),
            console_output=True,
            file_output=True
        )
        
        colored_logger.info("这是一条带颜色的信息")
        colored_logger.warning("这是一条带颜色的警告")
        colored_logger.error("这是一条带颜色的错误")
        
        colored_logger.close()
        
        # 测试性能logger
        print("\n3. 测试性能Logger...")
        perf_logger = PerformanceLogger(
            log_file=log_file.replace(".log", "_performance.log")
        )
        
        perf_logger.log_function_call("test_func", 0.5678)
        perf_logger.log_memory_usage(256.7)
        
        perf_logger.logger.close()
        
        print("✅ 所有基本功能测试完成")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
    
    finally:
        # 清理临时目录
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"\n清理临时目录: {temp_dir}")

if __name__ == "__main__":
    print("Python Logger 类测试程序")
    print("=" * 50)
    
    # 运行简单测试
    run_simple_test()
    
    print("\n" + "=" * 50)
    print("运行完整单元测试...")
    
    # 运行单元测试
    unittest.main(verbosity=2)