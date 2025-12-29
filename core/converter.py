import cv2
import numpy as np

class BaseConverter:
    def predict(self, image):
        raise NotImplementedError("Các lớp con phải định nghĩa phương thức predict này")
    
class SimpleThresholdConverter(BaseConverter):
    def predict(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # thuật toán Otus để tự động tìm ngưỡng cắt đen trắng
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        return mask
    
class AIModelConverter(BaseConverter):
    """sau này có thể tích hợp mô hình AI ở đây"""
    def predict(self, image):
        print("Chức năng chưa được triển khai")
        return None
