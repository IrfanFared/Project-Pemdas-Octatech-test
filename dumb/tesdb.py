import sqlite3
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.uix.screenmanager import ScreenManager

# Kita simpan nama DB di variabel global agar mudah diubah
DB_NAME = "users.db"

# --- 1. SCREEN SIGN UP (Punya Logika INSERT) ---
class SignupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "signup"
        
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            adaptive_height=True,
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )

        layout.add_widget(MDLabel(text="SIGN UP", halign="center", font_style="Display", role="small", bold=True))

        # Username Input
        self.user_field = MDTextField(mode="outlined")
        self.user_field.add_widget(MDTextFieldHintText(text="Buat Username"))
        layout.add_widget(self.user_field)

        # Password Input
        self.pass_field = MDTextField(mode="outlined", password=True)
        self.pass_field.add_widget(MDTextFieldHintText(text="Buat Password"))
        layout.add_widget(self.pass_field)

        # Tombol Daftar
        btn_register = MDButton(style="filled", pos_hint={"center_x": 0.5})
        btn_register.add_widget(MDButtonText(text="Daftar Sekarang"))
        # Panggil fungsi lokal do_signup
        btn_register.bind(on_release=self.do_signup)
        layout.add_widget(btn_register)

        # Tombol Kembali
        btn_back = MDButton(style="text", pos_hint={"center_x": 0.5})
        btn_back.add_widget(MDButtonText(text="Kembali ke Login"))
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def do_signup(self, instance):
        # LOGIKA DB ADA DI SINI SEKARANG
        username = self.user_field.text
        password = self.pass_field.text

        if not username or not password:
            self.show_snackbar("Isi semua kolom!")
            return

        try:
            # Buka koneksi lokal di fungsi ini
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user_data (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            
            self.show_snackbar("Sukses! Silakan Login.")
            # Reset field
            self.user_field.text = ""
            self.pass_field.text = ""
            # Pindah screen
            self.manager.current = "login"
            
        except sqlite3.IntegrityError:
            self.show_snackbar("Username sudah ada!")

    def go_back(self, instance):
        self.manager.current = "login"

    def show_snackbar(self, text):
        snackbar = MDSnackbar(
            MDSnackbarText(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        )
        snackbar.open()


# --- 2. SCREEN LOGIN (Punya Logika SELECT) ---
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"
        
        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            adaptive_height=True,
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )

        layout.add_widget(MDLabel(text="LOGIN", halign="center", font_style="Display", role="small", bold=True))

        self.user_field = MDTextField(mode="outlined")
        self.user_field.add_widget(MDTextFieldHintText(text="Username"))
        layout.add_widget(self.user_field)

        self.pass_field = MDTextField(mode="outlined", password=True)
        self.pass_field.add_widget(MDTextFieldHintText(text="Password"))
        layout.add_widget(self.pass_field)

        btn_login = MDButton(style="filled", pos_hint={"center_x": 0.5})
        btn_login.add_widget(MDButtonText(text="Masuk"))
        # Panggil fungsi lokal do_login
        btn_login.bind(on_release=self.do_login)
        layout.add_widget(btn_login)

        btn_signup = MDButton(style="text", pos_hint={"center_x": 0.5})
        btn_signup.add_widget(MDButtonText(text="Belum punya akun? Daftar"))
        btn_signup.bind(on_release=self.go_to_signup)
        layout.add_widget(btn_signup)

        self.add_widget(layout)

    def do_login(self, instance):
        # LOGIKA DB ADA DI SINI
        username = self.user_field.text
        password = self.pass_field.text

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_data WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()

        if result:
            # Jika sukses, kita harus "melempar" data username ke HomeScreen
            # Kita akses HomeScreen lewat ScreenManager (self.manager)
            home_screen = self.manager.get_screen('home')
            
            # Kita panggil method update_ui yang ada di HomeScreen
            home_screen.update_ui(username)
            
            self.manager.current = "home"
            
            # Reset password field biar aman
            self.pass_field.text = ""
        else:
            self.show_snackbar("Gagal Login!")

    def go_to_signup(self, instance):
        self.manager.current = "signup"

    def show_snackbar(self, text):
        snackbar = MDSnackbar(
            MDSnackbarText(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        )
        snackbar.open()


# --- 3. SCREEN HOME (Menerima Data) ---
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"

        layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=dp(20),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Simpan referensi label ke self supaya bisa diubah nanti
        self.welcome_label = MDLabel(
            text="Selamat Datang!",
            halign="center",
            font_style="Headline",
            role="medium"
        )
        layout.add_widget(self.welcome_label)

        btn_logout = MDButton(style="tonal", pos_hint={"center_x": 0.5})
        btn_logout.add_widget(MDButtonText(text="Logout"))
        btn_logout.bind(on_release=self.do_logout)
        layout.add_widget(btn_logout)

        self.add_widget(layout)

    def update_ui(self, username):
        # Fungsi ini dipanggil oleh LoginScreen saat login sukses
        self.welcome_label.text = f"Halo, {username}!"

    def do_logout(self, instance):
        self.manager.current = "login"


# --- 4. MAIN APP ---
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        
        # Pastikan tabel dibuat DULUAN sebelum screen dimuat
        self.create_table()
        
        sm = ScreenManager()
        # Masukkan screen instance
        sm.add_widget(LoginScreen())
        sm.add_widget(SignupScreen())
        sm.add_widget(HomeScreen())
        
        return sm

    def create_table(self):
        # Hanya membuat tabel, tidak mengurusi insert/select
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

if __name__ == "__main__":
    MainApp().run()