import cv2
import numpy as np
from core.converter import SimpleThresholdConverter
from core.extractor import PolylineExtractor

class ProcessingPipeline:
    def __init__(self):
        # muốn dùng model nào thì khởi tạo ở đây
        self.converter = SimpleThresholdConverter()
        self.extractor = PolylineExtractor()

    def run(self, image_path):
        # đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # tiền xử lý preprocess
        processed_img = cv2.GaussianBlur(image, (3, 3), 0)

        # chuyển đổi
        mask = self.converter.predict(processed_img)

        # trich xuat extract
        raw_polylines = self.extractor.extract(mask)

        final_polylines = raw_polylines

        return {
            "preprocess": processed_img,
            "mask": mask,
            "raw_polylines": raw_polylines,
            "final_polylines": final_polylines
        }