# Hand Digit Recognition - 手势数字识别

> 一个基于 **Python、OpenCV、Mediapipe 和 PyQt5** 的实时手势数字识别应用，能够通过摄像头识别 0-5 个手指数量，并在界面中显示结果。  
> A real-time hand digit recognition application using **Python, OpenCV, Mediapipe, and PyQt5**, which can detect 0-5 fingers through a webcam and display the recognized digit.

---

##  功能 Features

- **实时手势识别**：通过摄像头识别手势 Real-time hand gesture recognition via webcam
- **数字显示**：在界面上显示当前识别数字 Show the detected digit on GUI
- **美观界面**：使用 PyQt5 创建用户友好界面 Stylish GUI built with PyQt5
-  **开始/停止按钮**：方便控制识别 Start/Stop recognition buttons

---

##  技术栈 Tech Stack

- **Python 3.x**
- **OpenCV** (`opencv-python`)
- **Mediapipe** (`mediapipe`)
- **PyQt5** (`PyQt5`)

---



## 安装 Installation

### 一条条完整命令 Complete Installation Commands

```bash
# 1. 克隆仓库
git clone https://github.com/devlogix01/hands_detection.git
cd hands_detection

# 2. 创建虚拟环境（可选，但推荐）
# Windows
python -m venv venv
# Linux / Mac
# python3 -m venv venv

# 3. 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux / Mac
# source venv/bin/activate

# 4. 升级 pip
pip install --upgrade pip

# 5. 安装依赖库
pip install opencv-python==4.8.1.78 mediapipe==0.10.13 PyQt5==5.15.9

# 6. 运行程序
python hand_digit_app.py


