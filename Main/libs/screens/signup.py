import os

# Nama file database, pastikan sesuai dengan file yang digunakan aplikasi Anda
DB_NAME = "user_data.db"

# Inisialisasi database: buat tabel jika belum ada
def init_db():
    import sqlite3
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        conn.commit()
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
import sqlite3
from kivy.metrics import dp 
# Import Widget KivyMD 2.0.0
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldTrailingIcon,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kivy.uix.floatlayout import FloatLayout



# --- CLASS HALAMAN (MDScreen) ---
class SignupPage(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Di dalam Screen, kita gunakan __init__, bukan build.

        # 1. Background Image
        # Saya pakai try-except agar kalau gambar tidak ada, app tidak crash (tetap jalan dengan background warna)
        
        bg_image = FitImage(
                # Gunakan r"..." (raw string) untuk path Windows agar backslash aman
            source=r"D:\Project Pemdas Octatech test\Main\Assets\Images\latar_belakang_signup.jpg",
            radius=[0, 0, 0, 0]
            )
        self.add_widget(bg_image) # Gunakan self, bukan screen
        
            # Fallback warna jika gambar gagal load
        self.md_bg_color = (0.1, 0.1, 0.1, 1)

        layout_utama = FloatLayout()

        # 2. Membuat Card
        card = MDCard(
            style="elevated",
            size_hint=(None, None),
            size=("300dp", "550dp"), # Tinggi sedikit ditambah agar muat
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            theme_bg_color="Custom",
            md_bg_color="#106EBE",
            padding="20dp",
            radius=[30],
        )

        # 3. Konten dalam Card
        card_content = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            adaptive_height=True
        )

        # --- WIDGETS ---

        # Judul
        label_title = MDLabel(
            text="Sign Up",
            halign="center",
            font_style="Headline",
            role="medium",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
            adaptive_height=True
        )

        label_subtitle = MDLabel(
            text="Buat akunmu untuk mulai menjelajahi\nOctaTech",
            halign="center",
            font_style="Body",
            role="small",
            theme_text_color="Custom",
            text_color=(0.8, 0.8, 0.8, 1),
            adaptive_height=True
        )

        # Input Nama
        self.input_nama = MDTextField(
            MDTextFieldHintText(text="Nama"),
            MDTextFieldTrailingIcon(icon="account"),
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10]
        )

        # Input Username
        self.input_username = MDTextField(
            MDTextFieldHintText(text="Username"),
            MDTextFieldTrailingIcon(icon="at"),
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10]
            
        )

        # Input Password
        self.input_password = MDTextField(
            MDTextFieldHintText(text="Password"),
            MDTextFieldTrailingIcon(icon="key"),
            mode="filled",
            theme_bg_color="Custom",
            fill_color_normal=(1, 1, 1, 1),
            fill_color_focus=(1, 1, 1, 1),
            radius=[10, 10, 10, 10],
            password=True
            
        )    

        # Tombol Buat Akun
        btn_signup = MDButton(
            MDButtonText(
                text="Buat Akun",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            ),
            style="filled",
            pos_hint={"center_x": 0.5},
            height="40dp",
            size_hint_x=1,
        )

        # --- MENYUSUN LAYOUT ---
        card_content.add_widget(label_title)
        card_content.add_widget(label_subtitle)
        card_content.add_widget(MDLabel(text="", size_hint_y=None, height="10dp")) # Spacer
        
        card_content.add_widget(self.input_nama)
        card_content.add_widget(self.input_username)
        card_content.add_widget(self.input_password)
        
        card_content.add_widget(MDLabel(text="", size_hint_y=None, height="20dp")) # Spacer
        card_content.add_widget(btn_signup)
        btn_signup.bind(on_release=self.do_signup)



        # Tombol Kembali
        btn_back = MDButton(style="text", pos_hint={"center_x": .5})
        btn_back.add_widget(MDButtonText(text="Kembali ke Login", theme_text_color="Custom", text_color=(1,1,1,0.7)))
        btn_back.bind(on_release=self.back_to_login)
        card_content.add_widget(btn_back)

        card.add_widget(card_content)
        layout_utama.add_widget(card)
        
        # Masukkan layout utama ke dalam screen (self)
        self.add_widget(layout_utama)
    

    def do_signup(self, instance):
        # LOGIKA DB ADA DI SINI SEKARANG
        nama = self.input_nama.text
        username = self.input_username.text
        password = self.input_password.text

        if not username or not password:
            self.show_snackbar("Isi semua kolom!")
            return

        try:
            # Buka koneksi lokal di fungsi ini
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user_data (nama,username, password) VALUES (?,?,?)", (nama,username, password))
                conn.commit()
            
            self.show_snackbar("Sukses! Silakan Login.")
            # Reset field
            self.input_username.text = ""
            self.input_password.text = ""
            # Pindah screen
            self.manager.current = "login_screen"
            
        except sqlite3.IntegrityError:
            self.show_snackbar("Username sudah ada!")

    def go_back(self, instance):
        self.manager.current = "login_screen"

    def back_to_login(self, instance):
        # Cek apakah ScreenManager ada sebelum mengaksesnya
        if self.manager:
            self.manager.current = "login_screen"
            self.manager.transition.direction = "right"
        else:
            print("Screen Manager belum dipasang, tombol diklik.")
    def show_snackbar(self, text):
        snackbar = MDSnackbar(
            MDSnackbarText(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        )
        snackbar.open()
    