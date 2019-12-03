<p align="center">
  <h1 align="center">🚖Vehicle-Classify</h1>
  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/github/license/joey66666/vehicle-classify?color=blue&style=flat-square"></a>
    <img src="https://github.com/joey66666/vehicle-classify"></a>
    <a href="http://hits.dwyl.io/joey66666/vehicle-classify" alt="hit count"><img src="http://hits.dwyl.io/joey66666/vehicle-classify.svg?style=flat-square" /></a> 
  </p>
</p>

**[中文版](#chinese)**

> Vehicle brand &amp; model classification based on [RetinaNet](https://github.com/fizyr/keras-retinanet) & [Stanford Car Dataset](https://ai.stanford.edu/~jkrause/cars/car_dataset.html)

### ✔️Feature

1. Detect vehicle in the image and mark with box. (Work on 196 brands)
2. Show the brand of the vehicle with probability.
3. Time spent during the detection.

### 👋🏻How to start

> cd vehicle_UI
>
> conda install tensorflow==1.14.0 opencv numpy matplotlib keras
>
> pip install pyqt5 keras-retinanet 
>
> python vehicle_ui.py

### 📸Screenshots

<img src="pics/ui_en.png" style="zoom:50%;" />

### 📃Tips

- **It may take serval seconds to run the program related to the hardware, please wait after start.**
- Trained Models are [here](https://github.com/joey66666/vehicle-classify/releases)

### ⚙️Dependencies 

- keras-retinanet
- Pyqt5
- Opencv
- Tensorflow
- Matplotlib

----

# <span id="chinese">🚖车辆型号检测识别</span>

> 基于 [RetinaNet](https://github.com/fizyr/keras-retinanet) 和 [Stanford Car Dataset](https://ai.stanford.edu/~jkrause/cars/car_dataset.html) 的车辆型号检测识别方案

### ✔️功能

1. 检测画面中车辆并使用方框标记（可识别196种型号）
2. 给出车辆型号与可信度
3. 显示识别耗时

### 👋🏻如何启动

> cd vehicle_UI
>
> conda install tensorflow==1.14.0 opencv numpy matplotlib keras
>
> pip install pyqt5 keras-retinanet 
>
> python vehicle_ui_cn.py

### 📸截图

<img src="pics/ui_cn.png" style="zoom:50%;" />

### 📃注意

1. **根据不同硬件情况，识别可能耗费数十秒钟，请耐心等待**

2. 训练后的模型在[这里](https://github.com/joey66666/vehicle-classify/releases)

### ⚙️依赖

- keras-retinanet
- Pyqt5
- Opencv
- Tensorflow
- Matplotlib
