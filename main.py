from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.animation import Animation
import datetime

class EdithUI(BoxLayout):
    def __init__(self, **k):
        super().__init__(orientation='vertical', padding=15, spacing=10, **k)
        h=BoxLayout(size_hint_y=0.08); h.add_widget(Label(text='STARK INDUSTRIES', font_size=10, color=(0,0.8,1,1))); h.add_widget(Label(text='EDITH MARK 5', font_size=10, color=(0,0.8,1,1))); self.add_widget(h)
        self.orb=Label(text='◉', font_size=200, color=(0,0.9,1,1), size_hint_y=0.45); self.add_widget(self.orb); Clock.schedule_interval(self.pulse, 2)
        self.status=Label(text='Hola Jefe, soy Edith', font_size=22, bold=True, color=(0.7,0.9,1,1), size_hint_y=0.08); self.add_widget(self.status)
        self.sub=Label(text='Sistemas activos - Nucleo 97%', font_size=11, color=(0,0.6,0.8,1), size_hint_y=0.05); self.add_widget(self.sub)
        ib=BoxLayout(size_hint_y=0.12); self.inp=TextInput(hint_text='Escribe tu comando...', background_color=(0.05,0.05,0.08,1), foreground_color=(0,0.9,1,1), multiline=False, padding=15); self.inp.bind(on_text_validate=lambda x: self.cmd()); ib.add_widget(self.inp); self.add_widget(ib)
        b=BoxLayout(size_hint_y=0.12, spacing=10); b.add_widget(Button(text='HABLAR', on_press=lambda x: self.cmd())); b.add_widget(Button(text='ESCUCHAR', on_press=lambda x: self.listen())); self.add_widget(b)
        try:
            from jnius import autoclass; self.tts=autoclass('android.speech.tts.TextToSpeech')(autoclass('org.kivy.android.PythonActivity').mActivity, None)
        except: self.tts=None
    def pulse(self, dt):
        a=Animation(font_size=210, duration=0.8)+Animation(font_size=200, duration=0.8); a.start(self.orb)
    def speak(self, t):
        if any(x in t.lower() for x in ['import','cat','.py']): return
        self.status.text=t
        if self.tts:
            try:
                from jnius import autoclass; self.tts.setLanguage(autoclass('java.util.Locale')("es","MX")); self.tts.setSpeechRate(0.85); self.tts.speak(t,0,None)
            except: pass
    def cmd(self):
        c=self.inp.text.lower().strip()
        if 'hora' in c: self.speak(f"Son las {datetime.datetime.now().strftime('%H:%M')} Jefe")
        elif 'hola' in c: self.speak("Hola Jefe")
        elif 'salir' in c: self.speak("Adios Jefe")
        else: self.speak("Entendido Jefe")
        self.inp.text=""
    def listen(self):
        self.status.text="Escuchando..."
        try:
            import subprocess; o=subprocess.check_output(['termux-speech-to-text'], timeout=6).decode().strip(); self.inp.text=o; self.cmd()
        except: self.status.text="Escribe Jefe"
from kivy.core.window import Window
Window.clearcolor=(0,0,0,1)
class EdithApp(App):
    def build(self): return EdithUI()
EdithApp().run()

