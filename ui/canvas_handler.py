import tkinter as tk
from PIL import Image, ImageTk

class ImageCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, highlightthickness=0, bg="#2b2b2b")

        self.image_path = None
        self.original_image = None # lưu ảnh gốc
        self.display_image = None # lưu ảnh hiển thị trên canvas
        self.image_id = None # id của ảnh trên canvas

        self.layers_data = {
            "raw_layer": {"data": [], "color": "red", "visible": True},
            "final_layer": {"data": [], "color": "green", "visible": True}
        }

        self.polylines = []

        # các biến để sử lý zoom và pan
        self.scale = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
    
        # gán sự kiện chuột 
        self.bind("<MouseWheel>", self.on_zoom) # cho windows
        self.bind("<Button-4>", self.on_zoom) # cho linux (cuộn lên)
        self.bind("<Button-5>", self.on_zoom) # cho linux (cuộn xuống)

        self.bind("<ButtonPress-1>", self.on_pan_start) # bắt đầu kéo
        self.bind("<B1-Motion>", self.on_pan_move) # di chuột khi đang nhấn giữ

    def load_image(self, path):
        self.image_path = path
        self.original_image = Image.open(path) # mở ảnh bằng thư viện Pillow
        self.scale = 1.0

        self.render()

        self.view_init() # khởi tạo vùng xem ban đầu

    def render(self):
        if self.original_image is None:
            return
        
        # tính kích thước mới của ảnh dựa trên tỉ lệ zoom
        width, height = self.original_image.size
        new_size = (int(width * self.scale), int(height * self.scale))

        # resize ảnh, dùng Resampling.LANCZOS để ảnh nét hơn
        resized_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_image)

        # nếu đã có ảnh trên canvas rồi thì xóa đi
        if self.image_id:
            self.delete(self.image_id)

        # vẽ ảnh mới lên canvas, đặt ở góc trên bên trái
        self.image_id = self.create_image(0, 0, anchor="nw", image=self.tk_image)

        # cập nhật vùng cuộn của canvas theo kích thước ảnh
        self.config(scrollregion=self.bbox("all"))

        # Vẽ lại tất cả các lớp đang có
        for tag, info in self.layers_data.items():
            if info["visible"]:
                self._draw_specific_layer(tag)

    def update_layer_data(self, tag, polylines, color=None):
        """Cập nhật dữ liệu cho một lớp cụ thể"""
        if tag in self.layers_data:
            self.layers_data[tag]["data"] = polylines
            if color:
                self.layers_data[tag]["color"] = color
            self._draw_specific_layer(tag)

    def _draw_specific_layer(self, tag):
        """Hàm nội bộ để vẽ một lớp dựa trên tag"""
        self.delete(tag) # Xóa nét vẽ cũ của tag này
        info = self.layers_data[tag]
        if not info["data"] or not info["visible"]:
            return

        for line in info["data"]:
            scaled_points = []
            for (x, y) in line:
                scaled_points.append(x * self.scale)
                scaled_points.append(y * self.scale)
            
            if len(scaled_points) >= 4:
                self.create_line(scaled_points, fill=info["color"], width=2, tags=tag)

    def toggle_layer_visibility(self, tag, is_visible):
        """Ẩn hoặc hiện một lớp"""
        if tag in self.layers_data:
            self.layers_data[tag]["visible"] = is_visible
            if is_visible:
                self._draw_specific_layer(tag)
            else:
                self.delete(tag)

    def view_init(self):
        """Đưa ảnh về vị trí ban đầu"""
        self.xview_moveto(0)
        self.yview_moveto(0)

    # xử lý lan
    def on_pan_start(self, event):
        self.scan_mark(event.x, event.y)

    def on_pan_move(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    # xử lý zoom
    def on_zoom(self, event):
        # xác định hướng zoom
        if event.num == 4 or event.delta > 0:
            self.scale *=1.1
        elif event.num == 5 or event.delta < 0:
            self.scale /=1.1

        # giới hạn tỉ lệ zoom
        self.scale = max(0.1, min(self.scale, 10.0))
        
        self.render()

    def raw_polylines(self, polylines, color="red", tag="polyline"):
        """vẽ các đường  polyline lên canvas dựa trên tỉ lệ scale hiện tại"""
        self.polylines = polylines
        self.delete(tag)
        if not polylines: return

        for line in polylines:
            # tinh lai toa do dua tren ti le zoom
            scaled_points = []
            for(x, y) in line:
                scaled_points.append(x * self.scale)
                scaled_points.append(y * self.scale)

            # ve duong noi cac diem
            if len(scaled_points) >= 4:
                self.create_line(scaled_points, fill=color, width=2, tags=tag)