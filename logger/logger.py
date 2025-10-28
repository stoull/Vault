import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import sys


class SimpleLogger:
    """简单的Python日志记录器类"""

    def __init__(self,
                 name="SimpleLogger",
                 log_file="app.log",
                 console_output=True,
                 file_output=True,
                 log_level="INFO",
                 log_format=None):
        """
        初始化日志记录器

        Args:
            name: logger名称
            log_file: 日志文件路径
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_format: 自定义日志格式
        """
        self.name = name
        self.log_file = log_file
        self.console_output = console_output
        self.file_output = file_output
        self.log_level = log_level.upper()

        # 默认日志格式
        self.log_format = log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # 创建logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, self.log_level))

        # 清除现有处理器
        self.logger.handlers.clear()

        # 添加处理器
        self._add_handlers()

    def _add_handlers(self):
        """添加日志处理器"""
        # 创建格式化器
        formatter = logging.Formatter(self.log_format)

        # 控制台处理器
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.log_level))
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # 文件处理器
        if self.file_output:
            # 确保日志目录存在
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 滚动文件处理器（10MB一个文件，保留5个备份）
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, self.log_level))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        """记录调试信息"""
        self.logger.debug(message)

    def info(self, message):
        """记录一般信息"""
        self.logger.info(message)

    def warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)

    def warn(self, message):
        """记录警告信息（warning的别名）"""
        self.logger.warning(message)

    def error(self, message):
        """记录错误信息"""
        self.logger.error(message)

    def critical(self, message):
        """记录严重错误信息"""
        self.logger.critical(message)

    def log_exception(self, message):
        """记录异常信息（包含堆栈跟踪）"""
        self.logger.exception(message)

    def set_level(self, level):
        """动态设置日志级别"""
        self.log_level = level.upper()
        self.logger.setLevel(getattr(logging, self.log_level))

        # 更新所有处理器的级别
        for handler in self.logger.handlers:
            handler.setLevel(getattr(logging, self.log_level))

    def close(self):
        """关闭logger"""
        for handler in self.logger.handlers:
            handler.close()


class ColorFormatter(logging.Formatter):
    """带颜色的日志格式化器"""

    # 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',  # 青色
        'INFO': '\033[32m',  # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',  # 红色
        'CRITICAL': '\033[35m',  # 紫色
        'RESET': '\033[0m'  # 重置
    }

    def format(self, record):
        # 添加颜色到级别名称
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"

        return super().format(record)


class ColoredLogger(SimpleLogger):
    """带颜色的日志记录器"""

    def _add_handlers(self):
        """添加带颜色的日志处理器"""
        # 创建带颜色的格式化器
        colored_formatter = ColorFormatter(self.log_format)
        default_formatter = logging.Formatter(self.log_format)

        # 控制台处理器（带颜色）
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.log_level))
            console_handler.setFormatter(colored_formatter)
            self.logger.addHandler(console_handler)

        # 文件处理器（不带颜色）
        if self.file_output:
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, self.log_level))
            file_handler.setFormatter(default_formatter)
            self.logger.addHandler(file_handler)


class PerformanceLogger:
    """性能监控日志记录器"""

    def __init__(self, name="PerformanceLogger", log_file="performance.log"):
        self.name = name
        self.log_file = log_file
        self.logger = SimpleLogger(
            name=name,
            log_file=log_file,
            console_output=False,
            file_output=True,
            log_level="INFO",
            log_format="%(asctime)s - %(message)s"
        )

    def log_function_call(self, func_name, execution_time, args=None, kwargs=None):
        """记录函数调用"""
        message = f"FUNCTION_CALL: {func_name} | EXEC_TIME: {execution_time:.4f}s"
        if args:
            message += f" | ARGS: {args}"
        if kwargs:
            message += f" | KWARGS: {kwargs}"

        self.logger.info(message)

    def log_memory_usage(self, memory_usage_mb):
        """记录内存使用"""
        self.logger.info(f"MEMORY_USAGE: {memory_usage_mb:.2f}MB")

    def log_performance_summary(self, summary):
        """记录性能摘要"""
        self.logger.info(f"PERFORMANCE_SUMMARY: {summary}")


# 便捷函数
def get_logger(name="SimpleLogger", **kwargs):
    """获取logger实例的便捷函数"""
    return SimpleLogger(name=name, **kwargs)


def get_colored_logger(name="ColoredLogger", **kwargs):
    """获取带颜色logger实例的便捷函数"""
    return ColoredLogger(name=name, **kwargs)


# 全局logger实例
_app_logger = None


def get_app_logger():
    """获取全局应用logger"""
    global _app_logger
    if _app_logger is None:
        _app_logger = SimpleLogger(
            name="App",
            log_file="logs/app.log",
            console_output=True,
            file_output=True,
            log_level="INFO"
        )
    return _app_logger


# 示例使用
if __name__ == "__main__":
    # 基本使用示例
    logger = get_logger(
        name="MyApp",
        log_file="logs/myapp.log",
        console_output=True,
        file_output=True,
        log_level="DEBUG"
    )

    logger.debug("这是调试信息")
    logger.info("应用启动")
    logger.warning("这是一条警告")
    logger.error("发生了错误")
    logger.critical("严重错误")

    try:
        # 故意引发异常
        result = 1 / 0
    except Exception as e:
        logger.log_exception("捕获到异常")

    logger.close()

    # 带颜色的logger示例
    colored_logger = get_colored_logger(
        name="ColoredApp",
        log_file="logs/colored.log"
    )

    colored_logger.debug("调试信息（带颜色）")
    colored_logger.info("信息（带颜色）")
    colored_logger.warning("警告（带颜色）")
    colored_logger.error("错误（带颜色）")

    # 性能logger示例
    perf_logger = PerformanceLogger()
    perf_logger.log_function_call("test_function", 0.1234)
    perf_logger.log_memory_usage(45.67)

    print("日志记录器示例运行完成！")