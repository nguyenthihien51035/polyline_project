import cv2
import numpy as np

class PolylineExtractor:
    def __init__(self, epsilon_factor=0.001):
        # epsilon_factor: độ sai số để làm mượt đường line, 
        # càng nhỏ đường càng chi tiết (nhiều điểm), càng lớn thì càng phẳng
        self.epsilon_factor = epsilon_factor

    def extract(self, mask):
        # tìm các đường bao (contours) từ ảnh mask
        # cv2.RETR_LIST: lấy tất cả các đường
        # cv2.CHAIN_APPROX_SIMPLE: nén các điểm thẳng hàng để tiết kiệm bộ nhớ
        contours, _= cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        polylines = []
        for cnt in contours:
            # tinh do dai duong bao
            peri = cv2.arcLength(cnt, True)
            # duomg bao thanh cac doan thang
            approx = cv2.approxPolyDP(cnt, self.epsilon_factor * peri, True)
            # chuyen doi tu mang numpy sang list toa do (x, y) 
            points = []
            for point in approx:
                x, y = point[0]
                points.append((float(x), float(y)))

            # chi lay cac duong co 2 duong tro len
            if len(points) > 1:
                polylines.append(points)

        return polylines