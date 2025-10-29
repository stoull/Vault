"""
logger.py 使用示例
展示如何使用SimpleLogger类的各种功能
"""

from logger import SimpleLogger, ColoredLogger, PerformanceLogger, get_logger, get_colored_logger
import time
import random


def demo_basic_logger():
    """演示基本日志功能"""
    print("=== 基本日志功能演示 ===")

    # 创建logger实例
    logger = SimpleLogger(
        name="DemoApp",
        log_file="logs/demo.log",
        console_output=True,
        file_output=True,
        log_level="DEBUG"
    )

    # 记录不同级别的日志
    logger.debug("这是调试信息 - 用于开发和调试")
    logger.info("应用启动成功")
    logger.warning("检测到系统资源使用率较高")
    logger.error("数据库连接失败")
    logger.critical("系统即将崩溃！")

    logger.close()


def demo_colored_logger():
    """演示带颜色的日志功能"""
    print("\n=== 带颜色日志功能演示 ===")

    # 创建带颜色的logger
    colored_logger = ColoredLogger(
        name="ColorApp",
        log_file="logs/colored.log",
        console_output=True,
        file_output=True
    )

    colored_logger.debug("调试信息 - 蓝色")
    colored_logger.info("一般信息 - 绿色")
    colored_logger.warning("警告信息 - 黄色")
    colored_logger.error("错误信息 - 红色")
    colored_logger.critical("严重错误 - 紫色")

    colored_logger.close()


def demo_performance_logger():
    """演示性能监控日志"""
    print("\n=== 性能监控日志演示 ===")

    perf_logger = PerformanceLogger()

    # 模拟一些函数调用
    functions = ["用户登录", "数据查询", "文件上传", "图像处理"]

    for func in functions:
        # 模拟随机执行时间
        execution_time = random.uniform(0.1, 2.0)
        time.sleep(execution_time)  # 模拟处理时间

        perf_logger.log_function_call(func, execution_time)

    # 记录内存使用
    perf_logger.log_memory_usage(128.5)
    perf_logger.log_memory_usage(256.8)

    # 记录性能摘要
    perf_logger.log_performance_summary("平均响应时间: 0.8s, 峰值内存: 256MB")


def demo_exception_logging():
    """演示异常日志记录"""
    print("\n=== 异常日志记录演示 ===")

    logger = SimpleLogger(
        name="ExceptionDemo",
        log_file="logs/exceptions.log",
        log_level="DEBUG"
    )

    try:
        # 模拟一些操作
        numbers = [1, 2, 3, 4, 5]
        logger.info("开始处理数字列表")

        # 故意引发异常
        result = 10 / 0
        logger.info(f"计算结果: {result}")

    except ZeroDivisionError as e:
        logger.log_exception("发生除零异常")

    except Exception as e:
        logger.log_exception("发生未知异常")

    logger.close()


def demo_dynamic_logging():
    """演示动态日志级别设置"""
    print("\n=== 动态日志级别设置演示 ===")

    logger = SimpleLogger(
        name="DynamicApp",
        log_file="logs/dynamic.log",
        log_level="INFO"  # 初始级别为INFO
    )

    logger.debug("这条调试信息不会显示")
    logger.info("这条信息会显示")

    # 动态调整日志级别为DEBUG
    logger.set_level("DEBUG")
    logger.info("调整为DEBUG级别后：")
    logger.debug("现在这条调试信息也会显示")

    logger.close()


def demo_web_application_logging():
    """演示Web应用日志记录"""
    print("\n=== Web应用日志记录演示 ===")

    # 创建Web应用的logger
    web_logger = SimpleLogger(
        name="WebApp",
        log_file="logs/webapp.log",
        console_output=True,
        log_format="%(asctime)s [%(levelname)s] %(message)s"
    )

    # 模拟Web应用日志
    requests = [
        ("GET", "/api/users", "200 OK", "用户查询"),
        ("POST", "/api/login", "401 Unauthorized", "登录失败"),
        ("GET", "/api/products", "200 OK", "商品列表"),
        ("DELETE", "/api/user/123", "404 Not Found", "删除不存在的用户"),
        ("POST", "/api/upload", "200 OK", "文件上传成功")
    ]

    for method, path, status, message in requests:
        log_message = f"{method} {path} - {status} - {message}"

        if "200" in status:
            web_logger.info(log_message)
        elif "401" in status or "404" in status:
            web_logger.warning(log_message)
        else:
            web_logger.error(log_message)

    web_logger.close()


def demo_data_processing_logging():
    """演示数据处理日志记录"""
    print("\n=== 数据处理日志记录演示 ===")

    data_logger = SimpleLogger(
        name="DataProcessor",
        log_file="logs/data_processing.log",
        log_level="INFO"
    )

    # 模拟数据处理步骤
    processing_steps = [
        "启动数据处理任务",
        "读取CSV文件: sales_data.csv (10000 rows)",
        "数据清洗: 移除空值和重复项",
        "数据验证: 验证价格和日期格式",
        "数据转换: 计算销售额和利润",
        "保存处理结果: processed_data.csv",
        "任务完成: 处理了9876条有效记录"
    ]

    for step in processing_steps:
        data_logger.info(step)

    # 记录处理统计
    data_logger.info("处理统计: 总记录数=10000, 有效记录=9876, 错误记录=124")

    data_logger.close()


def main():
    """主函数：运行所有演示"""
    print("开始运行logger.py演示程序...\n")

    # 确保logs目录存在
    import os
    os.makedirs("logs", exist_ok=True)

    # 运行各种演示
    demo_basic_logger()
    demo_colored_logger()
    demo_performance_logger()
    demo_exception_logging()
    demo_dynamic_logging()
    demo_web_application_logging()
    demo_data_processing_logging()

    print("\n所有演示程序运行完成！")
    print("请查看 logs/ 目录下的日志文件")


if __name__ == "__main__":
    main()