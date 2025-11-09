import sys
import cv2
import mediapipe as mp
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QFont

class HandDigitApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("手势数字识别")
        self.resize(900, 700)
        self.setStyleSheet("background-color: #f0f2f5;")

        # --------- UI 组件 ---------
        self.videoLabel = QLabel()
        self.videoLabel.setFixedSize(800, 500)
        self.videoLabel.setStyleSheet("border: 2px solid #ccc; background-color: #000;")

        self.digitLabel = QLabel("当前识别数字：0")
        self.digitLabel.setAlignment(Qt.AlignCenter)
        self.digitLabel.setFont(QFont("Arial", 20))
        self.digitLabel.setStyleSheet("color: #2c3e50; margin-top: 10px;")

        self.startBtn = QPushButton("▶ 开始识别")
        self.stopBtn = QPushButton("■ 停止识别")


        btnStyle = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """
        self.startBtn.setStyleSheet(btnStyle)
        self.stopBtn.setStyleSheet(btnStyle)


        buttonLayout = QHBoxLayout()
        buttonLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        buttonLayout.addWidget(self.startBtn)
        buttonLayout.addWidget(self.stopBtn)
        buttonLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout = QVBoxLayout()
        layout.addWidget(self.videoLabel, alignment=Qt.AlignCenter)
        layout.addWidget(self.digitLabel)
        layout.addLayout(buttonLayout)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def start(self):
        self.cap = cv2.VideoCapture(0,cv2.CAP_MSMF)
        self.timer.start(30)

    def stop(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.videoLabel.clear()
        self.digitLabel.setText("当前识别数字：0")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(imgRGB)
        totalFingers = 0

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((id, cx, cy))

                fingers = []
                # 拇指
                if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # 其他四指
                for i in range(1, 5):
                    if lmList[self.tipIds[i]][2] < lmList[self.tipIds[i] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers = sum(fingers)
                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        self.digitLabel.setText(f"当前识别数字：{totalFingers}")

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytesPerLine = ch * w
        qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.videoLabel.setPixmap(QPixmap.fromImage(qImg))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HandDigitApp()
    win.show()
    sys.exit(app.exec_())
