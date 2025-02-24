FROM tensorflow/tensorflow:2.12.0

# 设置工作目录为 /app
WORKDIR /app

# 安装必要的 Python 包
RUN pip install --no-cache-dir flask pillow

# 创建 ~/.keras 目录及其子目录
RUN mkdir -p /root/.keras/models

# 将本地的文件拷贝到容器中指定目录
# 假设 vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5 和 keras.json 在同一目录下
COPY vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5 /root/.keras/models
COPY keras.json /root/.keras

# 将 Flask API 的 Python 文件（flash-api.py）拷贝到容器中
COPY flash-api.py /app/

# 暴露 Flask 默认端口
EXPOSE 5000

# 设置启动命令
CMD ["python", "flash-api.py"]

