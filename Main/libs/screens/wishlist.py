import json
import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingIcon
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

# ==========================================
# WISHLIST MANAGER (LOGIC)
# ==========================================
class WishlistManager:
    def __init__(self, filename="wishlist_data.json"):
        self.filename = filename
        self.wishlist = self.load_data()

    def load_data(self):
        """Membaca data dari file JSON"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except:
            return []

    def save_data(self):
        """Menyimpan data ke file JSON"""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.wishlist, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan wishlist: {e}")

    def show_message(self, text):
        """Menampilkan pesan menggunakan MDSnackbar (Cross-platform)"""
        try:
            MDSnackbar(
                MDSnackbarText(
                    text=text,
                ),
                y="24dp",
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
            ).open()
        except Exception as e:
            print(f"Error displaying snackbar: {e}")

    def add_item(self, item_data):
        """Menambahkan item ke wishlist jika belum ada"""
        # Cek duplikasi berdasarkan Nama Laptop
        for item in self.wishlist:
            if item.get("Nama") == item_data.get("Nama") and item.get("Brand") == item_data.get("Brand"):
                self.show_message("Laptop ini sudah ada di Wishlist!")
                return
        
        self.wishlist.append(item_data)
        self.save_data()
        self.show_message("Berhasil disimpan ke Wishlist")

    def remove_item(self, index):
        """Menghapus item berdasarkan index"""
        if 0 <= index < len(self.wishlist):
            del self.wishlist[index]
            self.save_data()
            self.show_message("Item dihapus")

    def get_items(self):
        return self.wishlist

# Inisialisasi Manager (Agar bisa dipanggil dari file lain)
wishlist_manager = WishlistManager()

# ==========================================
# UI LAYOUT (KV)
# ==========================================
WISHLIST_KV = '''
<WishlistScreen>:
    name: "wishlist_screen"
    md_bg_color: app.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: 'vertical'
        
        # Header Sederhana
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "64dp"
            md_bg_color: app.theme_cls.primaryColor
            padding: [16, 0]
            spacing: "12dp"
            
            MDButton:
                # PERBAIKAN: style "icon" tidak valid di KivyMD 2.0, ganti ke "text"
                style: "text"
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}
                on_release: app.go_back_to_main()
                MDButtonIcon:
                    icon: "arrow-left"
            
            MDLabel:
                text: "Wishlist Saya"
                font_style: "Title"
                role: "large"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}

        # List Kosong atau Isi
        MDBoxLayout:
            id: content_area
            orientation: 'vertical'
            
            MDLabel:
                id: empty_label
                text: "Belum ada item di wishlist"
                halign: "center"
                pos_hint: {"center_y": .5}
                theme_text_color: "Hint"
            
            MDScrollView:
                id: scroll_view
                size_hint_y: 1
                MDList:
                    id: wishlist_list
                    spacing: "10dp"
                    padding: "10dp"
'''

# ==========================================
# SCREEN CLASS
# ==========================================
class WishlistScreen(MDScreen):
    def on_enter(self):
        """Dipanggil saat masuk ke layar ini"""
        self.refresh_list()

    def refresh_list(self):
        # Pastikan KV sudah dimuat (biasanya sudah via import di main, tapi jaga-jaga)
        try:
            Builder.load_string(WISHLIST_KV) 
        except:
            pass # Ignore if already loaded

        self.ids.wishlist_list.clear_widgets()
        items = wishlist_manager.get_items()

        if not items:
            self.ids.empty_label.opacity = 1
            self.ids.scroll_view.opacity = 0
        else:
            self.ids.empty_label.opacity = 0
            self.ids.scroll_view.opacity = 1

            for i, item in enumerate(items):
                # Tambahkan item ke list
                list_item = MDListItem(
                    MDListItemHeadlineText(text=f"{item.get('Brand', '')} {item.get('Nama', '')}"),
                    MDListItemSupportingText(text=f"Harga: {item.get('Harga', '')}"),
                    MDListItemTertiaryText(text=f"{item.get('CPU', '')}"),
                    # Icon Hapus di kanan
                    MDListItemTrailingIcon(
                        icon="trash-can-outline",
                    ),
                    pos_hint={"center_x": .5}
                )
                # Bind tombol hapus (area kanan item)
                list_item.bind(on_release=lambda x, idx=i: self.delete_item(idx))
                self.ids.wishlist_list.add_widget(list_item)

    def delete_item(self, index):
        wishlist_manager.remove_item(index)
        self.refresh_list()