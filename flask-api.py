from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import numpy as np
import os

# 初始化Flask应用
app = Flask(__name__, static_folder='./web/dist', static_url_path='')  # 明确指定静态目录

# 启用跨域支持
CORS(app)  # 启用CORS

# 加载预训练的VGG16模型，不包括最后的全连接层
base_model = VGG16(weights='imagenet', include_top=False)

# 定义新的模型，将原VGG16模型的输出直接作为新模型的输出
model = Model(inputs=base_model.input, outputs=base_model.output)

# 提取图像特征的函数
def extract_features(img_path, model):
    """从指定路径的图像中提取特征"""
    # 加载图像，调整大小为224x224，VGG16模型要求的输入大小
    img = image.load_img(img_path, target_size=(224, 224))
    
    # 将PIL图像转换为numpy数组，并添加一个维度表示批大小
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # 预处理图像
    img_array = preprocess_input(img_array)
    
    # 通过模型获取图像的特征
    features = model.predict(img_array)
    
    # 扁平化特征使其成为一维数组
    flatten_features = features.flatten()
    
    # 归一化特征向量以比较它们的相似性
    normalized_features = flatten_features / np.linalg.norm(flatten_features)
    
    return normalized_features

# 计算相似度的函数
def calculate_similarity(features1, features2):
    """计算两组特征之间的相似度"""
    similarity = np.dot(features1, features2)
    return similarity

# 定义 API 路由
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # 获取上传的图片文件
        img1 = request.files['img1']
        img2 = request.files['img2']
        
        # 保存临时文件
        img_path1 = '/tmp/' + img1.filename
        img_path2 = '/tmp/' + img2.filename
        img1.save(img_path1)
        img2.save(img_path2)
        
        # 提取图像特征
        features1 = extract_features(img_path1, model)
        features2 = extract_features(img_path2, model)
        
        # 计算相似度
        similarity = calculate_similarity(features1, features2)
        
        # 将相似度从numpy类型转换为Python原生float
        similarity = float(similarity)
        
        # 返回相似度结果
        return jsonify({"similarity": similarity})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 为静态资源提供服务
@app.route('/')
def serve_home():
    """返回index.html页面"""
    return send_from_directory(app.static_folder, 'index.html')

# 为静态资源提供访问
@app.route('/<path:filename>')
def serve_static(filename):
    """为静态文件提供访问支持"""
    return send_from_directory(app.static_folder, filename)

# 启动Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
