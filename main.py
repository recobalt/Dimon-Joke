import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import threading
import ctypes
import os
import sys
from playsound import playsound

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# === универсальная функция для ресурсов внутри exe ===
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# файлы ресурсов
MUSIC_FILE = resource_path("dimon.mp3")
WALLPAPER_FILE = resource_path("wallpaper.bmp")
GOOGLE_PNG = resource_path("google.png")
VK_PNG = resource_path("vk.png")
STEPIC_LOGO = resource_path("stepik.png")

def play_music():
    if os.path.exists(MUSIC_FILE):
        threading.Thread(target=lambda: playsound(MUSIC_FILE), daemon=False).start()

def set_wallpaper():
    image_path = WALLPAPER_FILE
    if os.path.exists(image_path):
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 1
        SPIF_SENDCHANGE = 2
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )

def load_icon_or_fallback(path, size=(24,24), fallback_color="#999999"):
    try:
        if os.path.exists(path):
            img = Image.open(path).convert("RGBA").resize(size)
            return ctk.CTkImage(img, size=size)
    except Exception:
        pass
    img = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0,0,size[0],size[1]), fill=fallback_color)
    return ctk.CTkImage(img, size=size)

class StepikLoginSocial(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("950x600")
        self.resizable(False, False)
        self.overrideredirect(True)

        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        self.bg_frame = ctk.CTkFrame(self, fg_color="#343541")
        self.bg_frame.pack(fill="both", expand=True)

        self.inner_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.inner_frame.place(relx=0.5, rely=0.55, anchor="center")

        # === логотип Stepik ===
        if os.path.exists(STEPIC_LOGO):
            logo_img = Image.open(STEPIC_LOGO).convert("RGBA").resize((100, 100))
            logo = ctk.CTkImage(logo_img, size=(100, 100))
            self.logo_label = ctk.CTkLabel(self.bg_frame, image=logo, text="")
            self.logo_label.place(relx=0.5, rely=0.15, anchor="center")

        # === тексты ===
        self.label_title = ctk.CTkLabel(
            self.inner_frame, text="Добро пожаловать в Stepik",
            font=("Helvetica", 28, "bold"), text_color="white"
        )
        self.label_title.pack(pady=(0,10))

        self.label_motivation = ctk.CTkLabel(
            self.inner_frame,
            text="Авторизуйтесь, чтобы учиться и развиваться",
            font=("Helvetica", 18, "bold"),
            text_color="#d1d5db"
        )
        self.label_motivation.pack(pady=(0,15))

        self.label_subtitle = ctk.CTkLabel(
            self.inner_frame,
            text="Выберите способ входа",
            font=("Helvetica", 17),
            text_color="#c1c5ca"
        )
        self.label_subtitle.pack(pady=(0,20))

        self.line = ctk.CTkFrame(self.inner_frame, fg_color="#56575c", height=2, width=300)
        self.line.pack(pady=(0,20))

        # кнопка входа через браузер
        self.btn_browser = ctk.CTkButton(
            self.inner_frame,
            text="Вход через браузер",
            font=("Helvetica", 16, "bold"),
            fg_color="#4b5563",
            hover_color="#6b7280",
            text_color="white",
            corner_radius=25,
            width=230,
            height=50,
            command=self.on_click
        )
        self.btn_browser.pack(pady=5)

        # кнопки соцсетей
        self.create_social_buttons()

        # политика
        self.privacy_label = ctk.CTkLabel(
            self.bg_frame,
            text="Политика конфиденциальности",
            font=("Helvetica", 14, "underline"),
            text_color="white",
            cursor="hand2"
        )
        self.privacy_label.place(relx=0.5, rely=0.95, anchor="center")

        # крестик
        self.close_button = ctk.CTkButton(
            self.bg_frame,
            text="✕",
            font=("Helvetica", 13, "bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            corner_radius=18,
            width=35,
            height=35,
            command=self.destroy
        )
        self.close_button.place(relx=0.97, rely=0.04, anchor="center")

    def create_social_buttons(self):
        frame = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        frame.pack(pady=(10,0))

        google_icon = load_icon_or_fallback(GOOGLE_PNG, size=(24,24), fallback_color="#db4437")
        vk_icon     = load_icon_or_fallback(VK_PNG, size=(24,24), fallback_color="#4a76a8")

        # Google
        btn_google = ctk.CTkButton(
            frame,
            text="Google",
            image=google_icon,
            compound="left",
            font=("Helvetica", 15, "bold"),
            fg_color="white",
            hover_color="#e5e7eb",
            text_color="black",
            width=200,
            height=45,
            corner_radius=20,
            command=self.on_click
        )
        btn_google.pack(pady=5)

        # VK
        btn_vk = ctk.CTkButton(
            frame,
            text="VK",
            image=vk_icon,
            compound="left",
            font=("Helvetica", 15, "bold"),
            fg_color="#4a76a8",
            hover_color="#3b5a82",
            width=200,
            height=45,
            corner_radius=20,
            command=self.on_click
        )
        btn_vk.pack(pady=5)

    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_move(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.geometry(f"+{x}+{y}")

    def on_click(self):
        play_music()
        set_wallpaper()

if __name__ == "__main__":
    app = StepikLoginSocial()
    app.mainloop()
