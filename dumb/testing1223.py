from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

# Mengatur ukuran window agar mirip tampilan mobile/tablet (opsional)
Window.size = (1000, 700)

KV = '''
<ProfileScreen>:
    md_bg_color: [0.92, 0.94, 0.98, 1]  # Warna background biru muda lembut

    # --- Header Navigasi ---
    MDBoxLayout:
        adaptive_height: True
        pos_hint: {"top": 1}
        padding: "20dp"
        spacing: "10dp"
        
        # Tombol Kembali ke Home
        MDButton:
            style: "text"
            pos_hint: {"center_y": .5}
            theme_width: "Custom"
            width: "180dp"
            
            MDButtonIcon:
                icon: "home-outline"
                theme_icon_color: "Custom"
                icon_color: "blue"
                
            MDButtonText:
                text: "Kembali ke Home"
                theme_text_color: "Custom"
                text_color: "blue"
                font_style: "Label"
                role: "large"

        MDWidget: # Spacer agar tombol Logout terdorong ke kanan

        # Tombol Logout
        MDButton:
            style: "text"
            pos_hint: {"center_y": .5}
            
            MDButtonIcon:
                icon: "logout"
                theme_icon_color: "Custom"
                icon_color: "red"
                
            MDButtonText:
                text: "Logout"
                theme_text_color: "Custom"
                text_color: "red"
                font_style: "Label"
                role: "large"

    # --- Kartu Utama (Center Card) ---
    MDCard:
        size_hint: None, None
        size: "450dp", "600dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: "24dp"
        radius: [20, ]
        elevation: 1
        md_bg_color: "white"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: "16dp"

            # Judul
            MDLabel:
                text: "Profil Saya"
                halign: "center"
                font_style: "Headline"
                role: "medium"
                adaptive_height: True
                bold: True

            # Area Foto Profil (Circular)
            MDRelativeLayout:
                size_hint: None, None
                size: "120dp", "120dp"
                pos_hint: {"center_x": .5}

                # Lingkaran Border Foto
                MDCard:
                    size_hint: 1, 1
                    radius: [self.height / 2, ]
                    md_bg_color: [1, 1, 1, 1]
                    line_color: [0.7, 0.7, 0.9, 1] # Warna border ungu muda
                    line_width: 2
                    
                    MDLabel:
                        text: "Profile"
                        halign: "center"
                        theme_text_color: "Hint"
                        pos_hint: {"center_y": .8} # Simulasi teks di dalam lingkaran

                # Ikon Kamera (Floating Action Button style)
                MDButton:
                    style: "filled"
                    theme_width: "Custom"
                    size_hint: None, None
                    size: "36dp", "36dp"
                    radius: [18, ] # Membuat bulat sempurna
                    pos_hint: {"right": 1, "bottom": 0}
                    md_bg_color: [0.4, 0.3, 0.9, 1] # Warna ungu tua
                    
                    MDButtonIcon:
                        icon: "camera-outline"
                        theme_icon_color: "Custom"
                        icon_color: "white"
                        pos_hint: {"center_x": .5, "center_y": .5}

            # Teks Instruksi
            MDLabel:
                text: "Klik ikon kamera untuk upload foto"
                halign: "center"
                theme_text_color: "Hint"
                font_style: "Label"
                role: "medium"
                adaptive_height: True

            # Username Display
            MDBoxLayout:
                adaptive_height: True
                spacing: "8dp"
                pos_hint: {"center_x": .5}
                # Trick untuk centering boxlayout content
                padding: [self.parent.width/2 - self.width/2 - 50, 0, 0, 0] 

                MDIcon:
                    icon: "account-outline"
                    theme_text_color: "Custom"
                    text_color: "grey"
                    pos_hint: {"center_y": .5}
                
                MDLabel:
                    text: "JohnDoe"
                    font_style: "Title"
                    role: "large"
                    bold: True
                    adaptive_width: True
                    pos_hint: {"center_y": .5}

            MDWidget:
                size_hint_y: None
                height: "10dp"

            # --- Section Update Username ---
            MDCard:
                style: "filled"
                md_bg_color: [0.97, 0.97, 0.97, 1] # Abu-abu sangat muda
                radius: [8, ]
                padding: "16dp"
                adaptive_height: True
                orientation: "vertical"
                spacing: "8dp"

                MDLabel:
                    text: "Perbarui Username"
                    font_style: "Label"
                    role: "small"
                    bold: True
                    adaptive_height: True

                MDBoxLayout:
                    adaptive_height: True
                    spacing: "10dp"

                    MDTextField:
                        mode: "outlined"
                        size_hint_x: 0.7
                        
                        MDTextFieldHintText:
                            text: "Username baru"

                    MDButton:
                        style: "filled"
                        size_hint_x: 0.3
                        pos_hint: {"center_y": .5}
                        md_bg_color: [0.3, 0.2, 0.9, 1] # Ungu kebiruan
                        
                        MDButtonText:
                            text: "Update"
                            pos_hint: {"center_x": .5, "center_y": .5}

            MDWidget: # Spacer vertikal

            # --- Tombol Ganti Password ---
            MDButton:
                style: "filled"
                size_hint_x: 1
                height: "56dp"
                md_bg_color: [0.1, 0.15, 0.2, 1] # Hitam kebiruan (Dark)
                radius: [8, ]
                
                MDButtonIcon:
                    icon: "lock-outline"
                    color: "white"
                    
                MDButtonText:
                    text: "Ganti Password"
                    text_color: "white"
                    font_style: "Title"
                    role: "medium"

'''

class ProfileScreen(MDScreen):
    pass

class ProfileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo" 
        
        # 1. Muat desain KV (Blueprint)
        Builder.load_string(KV)
        
        # 2. Kembalikan INSTANCE dari ProfileScreen agar tampil di layar
        return ProfileScreen()

if __name__ == "__main__":
    ProfileApp().run()