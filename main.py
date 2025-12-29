import customtkinter as ctk
from tkinter import filedialog  # Thư viện để mở hộp thoại chọn file
from ui.canvas_handler import ImageCanvas 
from core.pipeline import ProcessingPipeline

# cấu hình giao diện (sáng/tối)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.pipeline = ProcessingPipeline()

        # cấu hình cửa sổ chính
        self.title("Ứng dụng image to popyline")
        self.geometry("1000x600")
    
        # tạo bố cục các thành phần giao diện
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
        # thanh bên trái
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
    
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Dự án polyline", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,10))

        # nút chọn ảnh
        self.btn_select_image = ctk.CTkButton(self.sidebar, text="Chọn ảnh bản vẽ", command=self.select_image)
        self.btn_select_image.grid(row=1, column=0, padx=20, pady=10)

        # điều khiển layer
        self.layer_label = ctk.CTkLabel(self.sidebar, text="Các lớp hiển thị", 
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.layer_label.grid(row=2, column=0, padx=20, pady=(20,10))

        self.sw_original = ctk.CTkSwitch(self.sidebar, text="Ảnh gốc")
        self.sw_original.select() # mặc định bật
        self.sw_original.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.sw_processed = ctk.CTkSwitch(self.sidebar, text="Ảnh đã xử lý")
        self.sw_processed.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.sw_raw = ctk.CTkSwitch(self.sidebar, text="Dữ liệu thô", 
                                    command=lambda: self.toggle_layer("raw_layer", self.sw_raw))
        self.sw_raw.select()
        self.sw_raw.grid(row=5, column=0, padx=20, pady=10, sticky="w")

        self.sw_final = ctk.CTkSwitch(self.sidebar, text="Dữ liệu cuối cùng", 
                                      command=lambda: self.toggle_layer("final_layer", self.sw_final))
        self.sw_final.select()
        self.sw_final.grid(row=6, column=0, padx=20, pady=10, sticky="w")


        # phần hiển thị bên phải (canvas)
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, sticky="nswe")
        
        # khởi tạo Canvas từ file canvas_handler.py
        self.image_canvas = ImageCanvas(self.canvas_frame)
        self.image_canvas.pack(fill="both", expand=True)

    def toggle_layer(self, tag, switch_widget):
        is_visible = switch_widget.get() == 1
        self.image_canvas.toggle_layer_visibility(tag, is_visible)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )

        if file_path:
            print(f"Đã chọn ảnh: {file_path}")
            self.image_canvas.load_image(file_path)
        
            results = self.pipeline.run(file_path)
            if results:
                self.image_canvas.update_layer_data("raw_layer", results["raw_polylines"], "red")

                self.image_canvas.update_layer_data("final_layer", results["final_polylines"], "green")
# chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()