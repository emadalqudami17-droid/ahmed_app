# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock

# مسار الخط العربي
FONT_ARABIC = 'ArabicFont.ttf'

# Kivy 2.3.1+ يدعم RTL أصلياً
def ar(text):
    return text

# مدة صوت التشجيع
CHEER_DURATION = 2.0


# ---------------- الشاشة الرئيسية ----------------
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        title = Label(
            text=ar("تطبيق أحمد"),
            font_size='34sp',
            bold=True,
            font_name=FONT_ARABIC,
            halign='center',
            size_hint=(1, 0.2)
        )
        layout.add_widget(title)

        btn_routine = Button(
            text=ar("روتين الحمام"),
            font_size='24sp', bold=True,
            font_name=FONT_ARABIC,
            background_color=(0.2, 0.7, 0.9, 1),
            size_hint=(1, 0.25)
        )
        btn_routine.bind(on_press=lambda x: setattr(self.manager, 'current', 'toilet_routine'))
        layout.add_widget(btn_routine)

        btn_aac = Button(
            text=ar("أنا أريد"),
            font_size='24sp', bold=True,
            font_name=FONT_ARABIC,
            background_color=(0.3, 0.8, 0.4, 1),
            size_hint=(1, 0.25)
        )
        btn_aac.bind(on_press=lambda x: setattr(self.manager, 'current', 'aac_board'))
        layout.add_widget(btn_aac)

        btn_game = Button(
            text=ar("لعبة الأسئلة"),
            font_size='24sp', bold=True,
            font_name=FONT_ARABIC,
            background_color=(0.9, 0.6, 0.2, 1),
            size_hint=(1, 0.25)
        )
        btn_game.bind(on_press=lambda x: setattr(self.manager, 'current', 'quiz_game'))
        layout.add_widget(btn_game)

        self.add_widget(layout)


# ---------------- شاشة روتين الحمام ----------------
class ToiletRoutineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps = [
            {"text": "1. أشعر برغبة", "image": "images/step1_feel.png", "audio": "audio/audio1.wav"},
            {"text": "2. أمشي إلى الحمام", "image": "images/step2_walk.png", "audio": "audio/audio2.wav"},
            {"text": "3. أنزل البنطال", "image": "images/step3_pants_down.png", "audio": "audio/audio3.wav"},
            {"text": "4. أجلس وأنتظر", "image": "images/step4_sit.png", "audio": "audio/audio4.wav"},
            {"text": "5. أنظف نفسي", "image": "images/step5_clean.png", "audio": "audio/audio5.wav"},
            {"text": "6. أرفع ملابسي", "image": "images/step6_pants_up.png", "audio": "audio/audio6.wav"},
            {"text": "7. أغسل يدي", "image": "images/step7_wash_hands.png", "audio": "audio/audio7.wav"}
        ]
        self.current_step = 0
        self.current_sound = None
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text=ar("القائمة"),
            font_size='18sp', font_name=FONT_ARABIC,
            size_hint=(1, 0.1),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=ar(self.steps[0]["text"]),
            font_size='28sp', bold=True,
            font_name=FONT_ARABIC,
            size_hint=(1, 0.12),
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.layout.add_widget(self.label)

        self.img = Image(
            source=self.steps[0]["image"],
            size_hint=(1, 0.58),
            allow_stretch=True,
            keep_ratio=True,
            nocache=True
        )
        self.layout.add_widget(self.img)

        self.btn_next = Button(
            text=ar("تم!"),
            font_size='26sp',
            font_name=FONT_ARABIC,
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.2)
        )
        self.btn_next.bind(on_press=self.next_step)
        self.layout.add_widget(self.btn_next)

        self.add_widget(self.layout)

    def on_enter(self):
        if self.current_step == -1:
            self.current_step = 0
            self.label.text = ar(self.steps[0]["text"])
            self.img.source = self.steps[0]["image"]
            self.btn_next.text = ar("تم!")
        Clock.schedule_once(lambda dt: self.play_step_audio(), 0.3)

    def play_step_audio(self):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        if 0 <= self.current_step < len(self.steps):
            sound = SoundLoader.load(self.steps[self.current_step]["audio"])
            if sound:
                self.current_sound = sound
                sound.play()

    def next_step(self, instance):
        if self.current_step == -1:
            self.current_step = 0
            self.label.text = ar(self.steps[0]["text"])
            self.img.source = self.steps[0]["image"]
            self.btn_next.text = ar("تم!")
            self.play_step_audio()
            return

        cheer = SoundLoader.load('audio/cheer.wav')
        if cheer:
            cheer.play()

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.label.text = ar(self.steps[self.current_step]["text"])
            self.img.source = self.steps[self.current_step]["image"]
            Clock.schedule_once(lambda dt: self.play_step_audio(), CHEER_DURATION)
        else:
            Clock.schedule_once(lambda dt: self.show_final_message(), CHEER_DURATION)

    def show_final_message(self):
        self.label.text = ar("رائع جداً! أنت بطل!")
        self.btn_next.text = ar("إعادة")
        self.current_step = -1

    def go_home(self, instance):
        self.current_step = 0
        self.label.text = ar(self.steps[0]["text"])
        self.img.source = self.steps[0]["image"]
        self.btn_next.text = ar("تم!")
        self.manager.current = 'main_menu'


# ---------------- شاشة لوحة التواصل AAC ----------------
class AACBoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text=ar("القائمة"),
            font_size='18sp', font_name=FONT_ARABIC,
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        main_layout.add_widget(btn_back)

        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.92))

        self.cards = [
            {"title": "أنا أحمد", "audio": "audio/say_ahmed.wav", "color": (0.2, 0.7, 0.9, 1)},
            {"title": "بابا عماد", "audio": "audio/say_dad.wav", "color": (0.3, 0.8, 0.4, 1)},
            {"title": "أخي محمد", "audio": "audio/say_mohamed.wav", "color": (0.2, 0.8, 0.7, 1)},
            {"title": "أخي ميلاد", "audio": "audio/say_milad.wav", "color": (0.9, 0.5, 0.7, 1)},
            {"title": "ماء", "audio": "audio/say_water.wav", "color": (0.2, 0.6, 0.9, 1)},
            {"title": "طعام", "audio": "audio/say_food.wav", "color": (1, 0.6, 0.2, 1)},
            {"title": "حمام", "audio": "audio/say_toilet.wav", "color": (0.4, 0.6, 0.8, 1)},
            {"title": "نوم", "audio": "audio/say_sleep.wav", "color": (0.6, 0.4, 0.8, 1)},
            {"title": "مساعدة", "audio": "audio/say_help.wav", "color": (0.9, 0.3, 0.3, 1)},
            {"title": "لعب", "audio": "audio/say_play.wav", "color": (0.3, 0.8, 0.3, 1)},
            {"title": "توقف", "audio": "audio/say_stop.wav", "color": (0.8, 0.2, 0.2, 1)},
            {"title": "سعيد", "audio": "audio/say_happy.wav", "color": (1, 0.4, 0.6, 1)}
        ]

        for card in self.cards:
            btn = Button(
                text=ar(card["title"]),
                font_size='22sp', bold=True,
                font_name=FONT_ARABIC,
                background_color=card["color"],
                size_hint=(1, 1)
            )
            btn.bind(on_press=lambda instance, a=card["audio"]: self.play_phrase(a))
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def play_phrase(self, audio_file):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        sound = SoundLoader.load(audio_file)
        if sound:
            self.current_sound = sound
            sound.play()


# ---------------- قسم لعبة الأسئلة ----------------
class QuizGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None
        self.questions = [
            {
                "question": "أين أحمد؟",
                "audio": "audio/q_ahmed.wav",
                "correct": "images/aac_ahmed.png",
                "options": ["images/aac_water.png", "images/aac_ahmed.png", "images/aac_food.png"]
            },
            {
                "question": "أين بابا عماد؟",
                "audio": "audio/q_dad.wav",
                "correct": "images/aac_dad.png",
                "options": ["images/aac_dad.png", "images/aac_play.png", "images/aac_toilet.png"]
            },
            {
                "question": "أين محمد؟",
                "audio": "audio/q_mohamed.wav",
                "correct": "images/aac_mohamed.png",
                "options": ["images/aac_milad.png", "images/aac_mohamed.png", "images/aac_ahmed.png"]
            },
            {
                "question": "أين ميلاد؟",
                "audio": "audio/q_milad.wav",
                "correct": "images/aac_milad.png",
                "options": ["images/aac_mohamed.png", "images/aac_food.png", "images/aac_milad.png"]
            }
        ]
        self.current_q = 0

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        btn_back = Button(
            text=ar("القائمة"),
            font_size='18sp', font_name=FONT_ARABIC,
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=ar(self.questions[0]["question"]),
            font_size='28sp', bold=True,
            font_name=FONT_ARABIC,
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.layout.add_widget(self.label)

        self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.77))
        self.update_options()
        self.layout.add_widget(self.grid)

        self.add_widget(self.layout)

    def on_enter(self):
        self.current_q = 0
        self.label.text = ar(self.questions[0]["question"])
        self.update_options()
        Clock.schedule_once(lambda dt: self.play_q_audio(), 0.3)

    def play_q_audio(self):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        sound = SoundLoader.load(self.questions[self.current_q]["audio"])
        if sound:
            self.current_sound = sound
            sound.play()

    def update_options(self):
        self.grid.clear_widgets()
        q_data = self.questions[self.current_q]
        for opt in q_data["options"]:
            btn = Button(
                background_normal='',
                background_color=(0.95, 0.95, 0.95, 1),
                size_hint=(1, 1)
            )
            img = Image(
                source=opt,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            btn.add_widget(img)
            btn.bind(on_press=lambda instance, i=opt: self.check_answer(i))
            self.grid.add_widget(btn)

    def check_answer(self, selected_img):
        correct_img = self.questions[self.current_q]["correct"]
        if selected_img == correct_img:
            cheer = SoundLoader.load('audio/cheer.wav')
            if cheer:
                cheer.play()
            if self.current_q < len(self.questions) - 1:
                self.current_q += 1
                self.label.text = ar(self.questions[self.current_q]["question"])
                self.update_options()
                Clock.schedule_once(lambda dt: self.play_q_audio(), CHEER_DURATION)
            else:
                self.label.text = ar("ممتاز! أنهيت الأسئلة")
                self.grid.clear_widgets()
        else:
            self.play_q_audio()


# ---------------- التطبيق ----------------
class AhmedApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(ToiletRoutineScreen(name='toilet_routine'))
        sm.add_widget(AACBoardScreen(name='aac_board'))
        sm.add_widget(QuizGameScreen(name='quiz_game'))
        return sm

    def on_start(self):
        Window.clearcolor = (1, 1, 1, 1)


if __name__ == '__main__':
    AhmedApp().run()
