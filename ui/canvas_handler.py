import tkinter as tk
from PIL import Image, ImageTk

class ImageCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, highlightthickness=0, bg="gray")

        self.image_path = None
        self.original_image = None # lưu ảnh gốc
        self.display_image = None # lưu ảnh hiển thị trên canvas
        self.image_id = None # id của ảnh trên canvas

    def load_image(self, path):
        self.image_path = path
        self.original_image = Image.open(path) # mở ảnh bằng thư viện Pillow

        self.render()

    def render(self):
        if self.original_image is None:
            return
        
        # chuyển đổi ảnh để Tkinter có thể hiển thị
        self.display_image = ImageTk.PhotoImage(self.original_image)

        # nếu đã có ảnh trên canvas rồi thì xóa đi
        if self.image_id:
            self.delete(self.image_id)

        # vẽ ảnh mới lên canvas, đặt ở góc trên bên trái
        self.image_id = self.create_image(0, 0, anchor="nw", image=self.display_image)

        # cập nhật vùng cuộn của canvas theo kích thước ảnh
        self.config(scrollregion=self.bbox("all"))
