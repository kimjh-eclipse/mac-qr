import sys
import qrcode
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR 코드 생성기')
        self.setGeometry(100, 100, 600, 400)

        # Layout 설정
        layout = QVBoxLayout()

        # URL 입력 부분
        url_layout = QHBoxLayout()
        url_label = QLabel('URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('URL을 입력하세요')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # QR 코드 이미지 표시 부분
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_label)

        # 버튼 부분
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton('생성')
        self.save_button = QPushButton('저장')
        self.save_button.setEnabled(False)
        
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # 이벤트 연결
        self.generate_button.clicked.connect(self.generateQR)
        self.save_button.clicked.connect(self.saveQR)

    def generateQR(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, '경고', 'URL을 입력해주세요!')
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # 이미지를 QLabel에 표시
            qr_image.save('temp_qr.png')
            pixmap = QPixmap('temp_qr.png')
            self.qr_label.setPixmap(pixmap.scaled(
                400, 400,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
            
            self.save_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, '오류', f'QR 코드 생성 중 오류가 발생했습니다: {str(e)}')

    def saveQR(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'QR 코드 저장',
            '',
            'PNG 파일 (*.png);;모든 파일 (*.*)'
        )

        if file_path:
            try:
                # 이미지를 저장
                self.qr_label.pixmap().save(file_path)
                QMessageBox.information(self, '성공', 'QR 코드가 저장되었습니다!')
            except Exception as e:
                QMessageBox.critical(self, '오류', f'파일 저장 중 오류가 발생했습니다: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QRCodeGenerator()
    ex.show()
    sys.exit(app.exec_())
