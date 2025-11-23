from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# Definisi UI dalam KV Language
KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    # Layout Utama Vertical
    MDBoxLayout:
        orientation: "vertical"
        
        # --- TOP APP BAR (MD3) ---
        MDTopAppBar:
            type: "small"

            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: app.on_menu_click()

            MDTopAppBarTitle:
                text: "Data Science Dashboard"

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "account-circle-outline"

        # --- CONTENT AREA (Scrollable) ---
        MDScrollView:
            do_scroll_x: False
            
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "24dp"
                spacing: "24dp"

                # Kartu Contoh 1: Input Data
                MDCard:
                    style: "elevated"
                    padding: "16dp"
                    size_hint_y: None
                    height: "200dp"
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "12dp"

                        MDLabel:
                            text: "Input Data Baru"
                            role: "title"
                            adaptive_height: True
                            theme_text_color: "Primary"

                        MDTextField:
                            mode: "outlined"
                            
                            MDTextFieldLeadingIcon:
                                icon: "magnify"
                                
                            MDTextFieldHintText:
                                text: "Cari Dataset..."
                                
                            MDTextFieldHelperText:
                                text: "Masukkan nama file csv"
                                mode: "persistent"

                        MDButton:
                            style: "filled"
                            pos_hint: {"right": 1}
                            on_release: app.on_process_data()
                            
                            MDButtonText:
                                text: "Proses Data"

                # Kartu Contoh 2: Statistik Dummy
                MDCard:
                    style: "outlined"
                    padding: "16dp"
                    size_hint_y: None
                    height: "150dp"
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        
                        MDLabel:
                            text: "Status Model"
                            role: "title"
                            adaptive_height: True
                        
                        MDLabel:
                            text: "Akurasi: 98.5%"
                            role: "body"
                            theme_text_color: "Secondary"
                            adaptive_height: True
                            
                        MDLabel:
                            text: "Epoch: 50/100"
                            role: "body"
                            theme_text_color: "Secondary"
                            adaptive_height: True
'''

class DataApp(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "data_app"
        self.md_bg_color = (1, 1, 1, 1)  # putih terang
    def build(self):
        # Mengatur tema ke Material Design 3
        self.theme_cls.theme_style = "Light"  # Ganti ke "Light" agar background terang
        self.theme_cls.primary_palette = "Blue"  # Warna utama aplikasi
        return Builder.load_string(KV)

    def on_menu_click(self):
        print("Menu diklik!")

    def on_process_data(self):
        print("Memproses data dummy...")

