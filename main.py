import os
import threading
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
import yt_dlp

# KV Design for a modern Bootstrap-like look
KV = '''
MDScreen:
    md_bg_color: 0.95, 0.95, 0.95, 1

    MDBoxLayout:
        orientation: 'vertical'
        spacing: "10dp"
        padding: "20dp"

        MDLabel:
            text: "ULTIMATE MEDIA DOWNLOADER"
            halign: "center"
            font_style: "H5"
            bold: True
            size_hint_y: None
            height: self.texture_size[1]
            theme_text_color: "Primary"

        MDLabel:
            text: "Download videos and music from anywhere"
            halign: "center"
            font_style: "Subtitle2"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]

        Widget:
            size_hint_y: None
            height: "20dp"

        MDTextField:
            id: url_input
            hint_text: "Paste your link here"
            mode: "rectangle"
            helper_text: "YouTube, Facebook, etc."
            helper_text_mode: "on_focus"
            icon_left: "link"

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "56dp"
            spacing: "10dp"

            MDTextField:
                id: mode_selector
                hint_text: "Select Download Mode"
                mode: "rectangle"
                readonly: True
                on_focus: if self.focus: app.menu.open()

        MDRaisedButton:
            text: "DOWNLOAD NOW"
            pos_hint: {"center_x": .5}
            size_hint_x: 1
            height: "56dp"
            md_bg_color: app.theme_cls.primary_color
            on_release: app.start_download()

        MDCard:
            orientation: "vertical"
            padding: "10dp"
            size_hint: 1, None
            height: "120dp"
            elevation: 1
            radius: [10, 10, 10, 10]
            md_bg_color: 1, 1, 1, 1

            MDLabel:
                text: "Status Log"
                bold: True
                font_style: "Caption"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: "20dp"

            ScrollView:
                MDLabel:
                    id: status_label
                    text: "Ready to download..."
                    font_style: "Caption"
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: "left"
'''

class MediaDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Define paths based on platform
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            self.paths = {
                'muzika': '/sdcard/muzika',
                'dramas': '/sdcard/dramas',
                'web': '/sdcard/web'
            }
        else:
            # For testing on desktop
            base_path = os.path.join(os.path.expanduser("~"), "Downloads", "MediaDownloader")
            self.paths = {
                'muzika': os.path.join(base_path, 'muzika'),
                'dramas': os.path.join(base_path, 'dramas'),
                'web': os.path.join(base_path, 'web')
            }

        for p in self.paths.values():
            if not os.path.exists(p):
                os.makedirs(p, exist_ok=True)

        self.screen = Builder.load_string(KV)
        
        # Setup Dropdown Menu
        menu_items = [
            {"text": "Music (MP3) -> /muzika", "viewclass": "OneLineListItem", "on_release": lambda x="1": self.set_item(x)},
            {"text": "Drama (MP4) -> /dramas", "viewclass": "OneLineListItem", "on_release": lambda x="2": self.set_item(x)},
            {"text": "Web Video (MP4) -> /web", "viewclass": "OneLineListItem", "on_release": lambda x="3": self.set_item(x)},
            {"text": "YouTube Playlist (MP3)", "viewclass": "OneLineListItem", "on_release": lambda x="4": self.set_item(x)},
            {"text": "YouTube Playlist (MP4)", "viewclass": "OneLineListItem", "on_release": lambda x="5": self.set_item(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.mode_selector,
            items=menu_items,
            width_mult=4,
        )
        self.selected_choice = "1"
        self.screen.ids.mode_selector.text = "Music (MP3) -> /muzika"
        
        return self.screen

    def set_item(self, choice):
        self.selected_choice = choice
        modes = {
            "1": "Music (MP3) -> /muzika",
            "2": "Drama (MP4) -> /dramas",
            "3": "Web Video (MP4) -> /web",
            "4": "YouTube Playlist (MP3)",
            "5": "YouTube Playlist (MP4)"
        }
        self.screen.ids.mode_selector.text = modes[choice]
        self.menu.dismiss()

    def update_status(self, text):
        self.screen.ids.status_label.text = text

    def start_download(self):
        url = self.screen.ids.url_input.text.strip()
        if not url:
            self.update_status("❌ Error: No link provided!")
            return
        
        self.update_status("⏳ Starting download...")
        threading.Thread(target=self.run_downloader_logic, args=(url,)).start()

    def run_downloader_logic(self, url):
        choice = self.selected_choice
        ydl_opts = {
            'logger': MyLogger(self),
            'progress_hooks': [self.progress_hook],
        }

        if choice == '1':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'outtmpl': f"{self.paths['muzika']}/%(title)s.%(ext)s",
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}],
                'noplaylist': True,
            })
        elif choice == '2':
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f"{self.paths['dramas']}/%(title)s.%(ext)s",
                'noplaylist': True,
            })
        elif choice == '3':
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f"{self.paths['web']}/%(title)s.%(ext)s",
                'noplaylist': True,
            })
        elif choice == '4':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'outtmpl': f"{self.paths['muzika']}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}],
            })
        elif choice == '5':
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f"{self.paths['dramas']}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: self.update_status("✅ DOWNLOAD COMPLETE!"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f"❌ ERROR: {str(e)}"))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            Clock.schedule_once(lambda dt: self.update_status(f"Downloading: {p} | Speed: {speed} | ETA: {eta}"))
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_status("✅ Download finished, processing..."))

class MyLogger:
    def __init__(self, app):
        self.app = app
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        Clock.schedule_once(lambda dt: self.app.update_status(f"Error: {msg}"))

if __name__ == "__main__":
    MediaDownloaderApp().run()
