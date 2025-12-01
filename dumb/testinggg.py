from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

# Mengatur ukuran window agar mirip tampilan mobile/tablet
Window.size = (1000, 600)

# Mendefinisikan class Screen sesuai nama di file KV
class ProfileScreen(MDScreen):
    pass

class ProfileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        
        # MEMUAT FILE KV EKSTERNAL
        # Pastikan nama file sesuai dengan file yang kamu buat
        Builder.load_file("profile.kv")
        
        # Menampilkan Screen
        return ProfileScreen()

if __name__ == "__main__":
    ProfileApp().run()