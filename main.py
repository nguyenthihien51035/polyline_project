import customtkinter as ctk

# cấu hình giao diện (sáng/tối)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

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
    
        # phần hiển thị bên phải (canvas)
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, sticky="nswe")
        self.status_label = ctk.CTkLabel(self.canvas_frame, text="Ảnh sẽ được hiển thị ở đây")
        self.status_label.pack(expand=True)
    
    def select_image(self):
        print("Đã nhấn nút chọn ảnh") #hàm xử lý chọn ảnh

# chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()