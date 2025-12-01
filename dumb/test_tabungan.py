from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton, MDIconButton
from kivymd.uix.snackbar import MDSnackbar
from datetime import datetime
import locale
import os


# Set Locale IDR
try:
    locale.setlocale(locale.LC_ALL, "id_ID.utf8")
except:
    try:
        locale.setlocale(locale.LC_ALL, "id_ID")
    except:
        pass


class SavingApp(MDApp):

    goal_name = StringProperty("iPhone 15 Pro")
    target_amount = NumericProperty(15000000)
    current_amount = NumericProperty(6000000)
    target_date = StringProperty("2025-12-31")

    progress_value = NumericProperty(0.0)

    history = ListProperty([])

    quick_amounts = [10000, 25000, 50000, 100000, 250000, 500000]

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Light"

        with open("saving.kv", "r", encoding="utf-8") as kv:
            root = Builder.load_string(kv.read())

        # sample history
        self.history = [
            {"amount": 100000, "date": "28 Nov 2025"},
            {"amount": 50000, "date": "27 Nov 2025"},
            {"amount": 25000, "date": "26 Nov 2025"},
        ]

        Clock.schedule_once(self.post_build_init, 0.1)
        self.update_progress()

        return root

    # ------------------------------------------------
    # UTIL
    # ------------------------------------------------
    def notify(self, msg):
        MDSnackbar(text=msg, duration=1.2).open()

    def format_rupiah(self, number):
        try:
            return locale.currency(number, grouping=True)
        except:
            return "Rp " + f"{int(number):,}".replace(",", ".")

    @property
    def remaining_amount(self):
        return max(0, self.target_amount - self.current_amount)

    # ------------------------------------------------
    # INIT
    # ------------------------------------------------
    def post_build_init(self, *args):
        quick_box = self.root.ids.quick_btns

        for amt in self.quick_amounts:
            btn = MDButton(
                text=f"+{self.format_rupiah(amt).replace('Rp', '').strip()}",
                size_hint=(None, None),
                on_release=lambda inst, a=amt: self.handle_deposit(a),
            )
            btn.height = dp(40)
            btn.width = dp(110)
            quick_box.add_widget(btn)

        self.populate_history()

    # ------------------------------------------------
    # PROGRESS
    # ------------------------------------------------
    def update_progress(self):
        if self.target_amount <= 0:
            self.progress_value = 0
        else:
            self.progress_value = min(100, (self.current_amount / self.target_amount) * 100)

        try:
            self.root.ids.circ.value = self.progress_value
        except:
            pass

    # ------------------------------------------------
    # HISTORY
    # ------------------------------------------------
    def populate_history(self):
        history_list = self.root.ids.history_list
        history_list.clear_widgets()

        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel

        for item in self.history:
            amt = item["amount"]
            date = item["date"]

            text = (
                f"+{self.format_rupiah(amt)}"
                if amt > 0 else
                f"-{self.format_rupiah(abs(amt))}"
            )

            color = (0, 0.6, 0, 1) if amt > 0 else (1, 0.2, 0.2, 1)

            row = MDBoxLayout(
                orientation="horizontal",
                padding=(12, 8),
                spacing=8,
                size_hint_y=None,
                height=56
            )

            lbl_amt = MDLabel(
                text=text,
                font_style="Subtitle1",
                theme_text_color="Custom",
                text_color=color
            )

            lbl_date = MDLabel(
                text=date,
                font_style="Caption",
                halign="right"
            )

            row.add_widget(lbl_amt)
            row.add_widget(lbl_date)

            history_list.add_widget(row)

    # ------------------------------------------------
    # DEPOSIT
    # ------------------------------------------------
    def handle_deposit_from_input(self, *args):
        raw = self.root.ids.deposit_input.text.strip()
        if not raw:
            self.notify("Masukkan nominal dulu ya")
            return

        try:
            val = int(float(raw))
        except:
            self.notify("Nominal tidak valid")
            return

        self.root.ids.deposit_input.text = ""
        self.handle_deposit(val)

    def handle_deposit(self, amount):
        if amount <= 0:
            self.notify("Nominal harus > 0")
            return

        if self.current_amount + amount > self.target_amount:
            self.notify("Melebihi target!")
            return

        self.current_amount += amount
        self.history.insert(0, {
            "amount": amount,
            "date": datetime.now().strftime("%d %b %Y")
        })

        self.update_progress()
        self.populate_history()
        self.notify("Berhasil ditambahkan")

    # ------------------------------------------------
    # WITHDRAW
    # ------------------------------------------------
    def handle_withdraw(self):
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.textfield import MDTextField

        box = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        self.withdraw_input = MDTextField(
            hint_text="Jumlah yang ingin diambil",
            input_filter="int"
        )

        box.add_widget(self.withdraw_input)

        def ok(inst):
            try:
                val = int(self.withdraw_input.text)
            except:
                self.notify("Nominal tidak valid")
                return

            if val <= 0 or val > self.current_amount:
                self.notify("Jumlah tidak valid")
                return

            self.current_amount -= val

            self.history.insert(0, {
                "amount": -val,
                "date": datetime.now().strftime("%d %b %Y")
            })

            self.update_progress()
            self.populate_history()
            self.withdraw_dialog.dismiss()
            self.notify("Withdraw berhasil")

        self.withdraw_dialog = MDDialog(
            title="Withdraw",
            type="custom",
            content_cls=box,
            buttons=[
                MDButton(text="Batal", on_release=lambda x: self.withdraw_dialog.dismiss()),
                MDButton(text="OK", on_release=ok),
            ]
        )

        self.withdraw_dialog.open()

    # ------------------------------------------------
    # RESET
    # ------------------------------------------------
    def handle_reset(self):
        def yes(inst):
            self.current_amount = 0
            self.history = []
            self.update_progress()
            self.populate_history()
            self.reset_dialog.dismiss()
            self.notify("Reset selesai")

        self.reset_dialog = MDDialog(
            title="Reset Tabungan",
            text="Yakin reset semua progress?",
            buttons=[
                MDButton(text="Batal", on_release=lambda x: self.reset_dialog.dismiss()),
                MDButton(text="Reset", on_release=yes),
            ]
        )

        self.reset_dialog.open()

    # ------------------------------------------------
    # EDIT GOAL
    # ------------------------------------------------
    def open_edit_dialog(self):
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.textfield import MDTextField

        box = MDBoxLayout(orientation="vertical", spacing=10, padding=10)

        self.edit_name = MDTextField(text=self.goal_name, hint_text="Nama Barang")
        self.edit_target = MDTextField(text=str(self.target_amount), hint_text="Target Jumlah", input_filter="int")
        self.edit_date = MDTextField(text=self.target_date, hint_text="Tanggal (YYYY-MM-DD)")

        box.add_widget(self.edit_name)
        box.add_widget(self.edit_target)
        box.add_widget(self.edit_date)

        def save(inst):
            try:
                new_target = int(self.edit_target.text)
            except:
                self.notify("Target tidak valid")
                return

            self.goal_name = self.edit_name.text
            self.target_amount = new_target
            self.target_date = self.edit_date.text

            self.update_progress()
            self.populate_history()
            self.edit_dialog.dismiss()
            self.notify("Goal diperbarui")

        self.edit_dialog = MDDialog(
            title="Edit Target",
            type="custom",
            content_cls=box,
            buttons=[
                MDButton(text="Batal", on_release=lambda x: self.edit_dialog.dismiss()),
                MDButton(text="Simpan", on_release=save),
            ]
        )

        self.edit_dialog.open()


if __name__ == "__main__":
    SavingApp().run()
