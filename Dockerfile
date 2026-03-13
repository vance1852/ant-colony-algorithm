# 蚁群算法 Dockerfile
# 支持 ARM 和 X86 架构

FROM python:3.11-slim

WORKDIR /app

# 复制源代码
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 默认运行主程序
CMD ["python", "main.py"]
