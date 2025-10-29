#!/bin/bash
# Python Logger 项目运行脚本

echo "Python Logger 项目"
echo "===================="

# 显示菜单
echo "请选择要运行的程序:"
echo "1. 运行功能演示 (logger_demo.py)"
echo "2. 运行测试 (test_logger.py)"
echo "3. 查看日志文件"
echo "4. 清理日志文件"
echo "5. 显示项目文件"
echo "6. 退出"

read -p "请输入选择 (1-6): " choice

case $choice in
    1)
        echo "运行功能演示..."
        python logger_demo.py
        ;;
    2)
        echo "运行测试程序..."
        python test_logger.py
        ;;
    3)
        echo "日志文件内容:"
        echo "==================="
        if [ -d "logs" ]; then
            for file in logs/*.log; do
                if [ -f "$file" ]; then
                    echo "--- $file ---"
                    head -5 "$file"
                    echo ""
                fi
            done
        else
            echo "没有找到logs目录，请先运行演示程序"
        fi
        ;;
    4)
        echo "清理日志文件..."
        if [ -d "logs" ]; then
            rm -rf logs/
            echo "日志文件已清理"
        else
            echo "没有找到logs目录"
        fi
        ;;
    5)
        echo "项目文件:"
        echo "========="
        ls -la *.py *.md *.txt
        ;;
    6)
        echo "退出程序"
        exit 0
        ;;
    *)
        echo "无效选择，请重新运行脚本"
        ;;
esac

echo ""
echo "按回车键继续..."
read