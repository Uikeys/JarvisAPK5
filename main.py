import os
import subprocess
import threading
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

KV = """
BoxLayout:
    orientation: "vertical"
    padding: "18dp"
    spacing: "12dp"

    Label:
        text: "[b]JARVIS AI[/b]"
        markup: True
        font_size: "30sp"
        size_hint_y: None
        height: "60dp"

    Label:
        id: status
        text: "Namaste! JARVIS taiyar hai."
        font_size: "18sp"

    TextInput:
        id: command
        hint_text: "Yahan apna command likhein"
        multiline: False
        size_hint_y: None
        height: "50dp"

    Button:
        text: "COMMAND CHALAO"
        size_hint_y: None
        height: "55dp"
        on_press: app.run_command()

    Button:
        text: "BATTERY STATUS"
        size_hint_y: None
        height: "50dp"
        on_press: app.battery()

    Button:
        text: "TIME AUR DATE"
        size_hint_y: None
        height: "50dp"
        on_press: app.time_date()

    Label:
        text: "Voice, call aur WhatsApp ke liye native Android integration alag se chahiye."
        font_size: "13sp"
        size_hint_y: None
        height: "55dp"
"""

class JarvisApp(App):
    def build(self):
        self.title = "JARVIS AI"
        return Builder.load_string(KV)

    def update_status(self, message):
        self.root.ids.status.text = message

    def speak(self, message):
        if platform == "android":
            try:
                from jnius import autoclass
                PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )
                TextToSpeech = autoclass(
                    "android.speech.tts.TextToSpeech"
                )
                Locale = autoclass("java.util.Locale")

                def init_tts():
                    self.tts = TextToSpeech(
                        PythonActivity.mActivity, None
                    )
                    self.tts.setLanguage(Locale("hi", "IN"))
                    self.tts.speak(message, 0, None, "jarvis")
                Clock.schedule_once(lambda dt: init_tts(), 0)
            except Exception:
                pass

    def run_command(self):
        text = self.root.ids.command.text.strip().lower()

        if not text:
            self.update_status("Pehle command likhein.")
            return

        if "time" in text or "samay" in text:
            self.time_date()
        elif "battery" in text:
            self.battery()
        elif "whatsapp" in text:
            self.update_status(
                "WhatsApp integration abhi configure nahi hai."
            )
        elif "call" in text:
            self.update_status(
                "Call feature ke liye Android permission aur confirmation chahiye."
            )
        else:
            self.update_status(
                "Command abhi supported nahi hai: " + text
            )

    def battery(self):
        try:
            if platform == "android":
                from jnius import autoclass
                PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )
                Context = autoclass("android.content.Context")
                IntentFilter = autoclass("android.content.IntentFilter")
                BatteryManager = autoclass("android.os.BatteryManager")

                intent = PythonActivity.mActivity.registerReceiver(
                    None, IntentFilter("android.intent.action.BATTERY_CHANGED")
                )
                level = intent.getIntExtra("level", -1)
                scale = intent.getIntExtra("scale", 100)
                percent = int(level * 100 / scale) if scale > 0 else -1
                msg = f"Battery {percent}%"
            else:
                msg = "Battery status Android APK mein milega."
        except Exception:
            msg = "Battery status nahi mil saka."

        self.update_status(msg)
        self.speak(msg)

    def time_date(self):
        now = datetime.now()
        msg = now.strftime("Time %I:%M %p | Date %d-%m-%Y")
        self.update_status(msg)
        self.speak(msg)

if __name__ == "__main__":
    JarvisApp().run()
