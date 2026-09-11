# -*- coding: utf-8 -*-
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock

# محاولة استخدام ميزة الاهتزاز إذا كانت مدعومة على الهاتف
try:
    from plyer import vibrator
    def trigger_vibration():
        try:
            vibrator.vibrate(0.05)
        except Exception:
            pass
except ImportError:
    def trigger_vibration():
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    path1 = os.path.join(BASE_DIR, filename)
    if os.path.exists(path1):
        return path1
    base_name = os.path.basename(filename)
    path2 = os.path.join(BASE_DIR, base_name)
    if os.path.exists(path2):
        return path2
    return path1

CHEER_DURATION = 2.0

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.size_hint = (1, 1)

    def on_press(self):
        trigger_vibration()
        return super().on_press()


# ---------------- Main Menu Screen ----------------
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)

        title = Label(
            text="Ahmed's App",
            font_size='32sp',
            bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, 0.15)
        )
        layout.add_widget(title)

        btn_routine = Button(
            text="Toilet Routine",
            font_size='22sp', bold=True,
            background_color=(0.2, 0.7, 0.9, 1),
            size_hint=(1, 0.18)
        )
        btn_routine.bind(on_press=self.open_routine)
        layout.add_widget(btn_routine)

        btn_aac = Button(
            text="I Want (AAC)",
            font_size='22sp', bold=True,
            background_color=(0.3, 0.8, 0.4, 1),
            size_hint=(1, 0.18)
        )
        btn_aac.bind(on_press=self.open_aac)
        layout.add_widget(btn_aac)

        btn_game = Button(
            text="Quiz Game",
            font_size='22sp', bold=True,
            background_color=(0.9, 0.6, 0.2, 1),
            size_hint=(1, 0.18)
        )
        btn_game.bind(on_press=self.open_quiz)
        layout.add_widget(btn_game)

        btn_stats = Button(
            text="Parent Dashboard",
            font_size='20sp', bold=True,
            background_color=(0.6, 0.4, 0.8, 1),
            size_hint=(1, 0.15)
        )
        btn_stats.bind(on_press=self.open_stats)
        layout.add_widget(btn_stats)

        btn_exit = Button(
            text="Exit App",
            font_size='18sp', bold=True,
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(1, 0.13)
        )
        btn_exit.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(btn_exit)

        self.add_widget(layout)

    def open_routine(self, instance):
        trigger_vibration()
        self.manager.current = 'toilet_routine'

    def open_aac(self, instance):
        trigger_vibration()
        self.manager.current = 'aac_board'

    def open_quiz(self, instance):
        trigger_vibration()
        self.manager.current = 'quiz_game'

    def open_stats(self, instance):
        trigger_vibration()
        self.manager.current = 'parent_dashboard'


# ---------------- Toilet Routine Screen ----------------
class ToiletRoutineScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.steps = [
            {"text": "1. I need to go", "image": "step1_feel.png", "audio": "audio1.wav"},
            {"text": "2. Walk to bathroom", "image": "step2_walk.png", "audio": "audio2.wav"},
            {"text": "3. Pants down", "image": "step3_pants_down.png", "audio": "audio3.wav"},
            {"text": "4. Sit and wait", "image": "step4_sit.png", "audio": "audio4.wav"},
            {"text": "5. Clean up", "image": "step5_clean.png", "audio": "audio5.wav"},
            {"text": "6. Pants up", "image": "step6_pants_up.png", "audio": "audio6.wav"},
            {"text": "7. Wash hands", "image": "step7_wash_hands.png", "audio": "audio7.wav"}
        ]
        self.current_step = 0
        self.current_sound = None
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        # Progress Bar for Visual Feedback
        self.progress = ProgressBar(max=len(self.steps), value=1, size_hint=(1, 0.05))
        self.layout.add_widget(self.progress)

        self.label = Label(
            text=self.steps[0]["text"],
            font_size='26sp', bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, 0.12),
            halign='center'
        )
        self.layout.add_widget(self.label)

        self.reward_label = Label(
            text="",
            font_size='30sp',
            color=(1, 0.8, 0, 1),
            size_hint=(1, 0.08),
            halign='center'
        )
        self.layout.add_widget(self.reward_label)

        self.img = Image(
            source=get_path(self.steps[0]["image"]),
            size_hint=(1, 0.47),
            allow_stretch=True,
            keep_ratio=True,
            nocache=True
        )
        self.layout.add_widget(self.img)

        self.btn_next = Button(
            text="Done!",
            font_size='24sp', bold=True,
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.18)
        )
        self.btn_next.bind(on_press=self.next_step)
        self.layout.add_widget(self.btn_next)

        self.add_widget(self.layout)

    def stop_audio(self):
        if self.current_sound:
            try:
                self.current_sound.stop()
                self.current_sound.unload()
            except Exception:
                pass
            self.current_sound = None

    def play_audio(self, audio_path):
        self.stop_audio()
        full_path = get_path(audio_path)
        if os.path.exists(full_path):
            sound = SoundLoader.load(full_path)
            if sound:
                self.current_sound = sound
                sound.play()

    def on_enter(self):
        if self.current_step == -1:
            self.current_step = 0
            self.label.text = self.steps[0]["text"]
            self.img.source = get_path(self.steps[0]["image"])
            self.btn_next.text = "Done!"
            self.progress.value = 1
            self.reward_label.text = ""
        Clock.schedule_once(lambda dt: self.play_audio(self.steps[self.current_step]["audio"]), 0.3)

    def next_step(self, instance):
        trigger_vibration()
        if self.current_step == -1:
            self.current_step = 0
            self.label.text = self.steps[0]["text"]
            self.img.source = get_path(self.steps[0]["image"])
            self.btn_next.text = "Done!"
            self.progress.value = 1
            self.reward_label.text = ""
            self.play_audio(self.steps[0]["audio"])
            return

        self.play_audio('cheer.wav')
        self.reward_label.text = "⭐ Excellent Job! ⭐"

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.progress.value = self.current_step + 1
            self.label.text = self.steps[self.current_step]["text"]
            self.img.source = get_path(self.steps[self.current_step]["image"])
            Clock.schedule_once(lambda dt: self.play_audio(self.steps[self.current_step]["audio"]), CHEER_DURATION)
            Clock.schedule_once(lambda dt: setattr(self.reward_label, 'text', ''), CHEER_DURATION)
        else:
            App.get_running_app().routine_completed += 1
            Clock.schedule_once(lambda dt: self.show_final_message(), CHEER_DURATION)

    def show_final_message(self):
        self.label.text = "Great job! You are a superstar!"
        self.reward_label.text = "🌟 STAR REWARD UNLOCKED! 🌟"
        self.btn_next.text = "Restart"
        self.progress.value = len(self.steps)
        self.current_step = -1

    def go_home(self, instance):
        trigger_vibration()
        self.stop_audio()
        self.current_step = 0
        self.label.text = self.steps[0]["text"]
        self.img.source = get_path(self.steps[0]["image"])
        self.btn_next.text = "Done!"
        self.progress.value = 1
        self.reward_label.text = ""
        self.manager.current = 'main_menu'


# ---------------- AAC Communication Board ----------------
class AACBoardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=self.go_home)
        main_layout.add_widget(btn_back)

        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.92))

        self.cards = [
            {"title": "Ahmed", "audio": "say_ahmed.wav", "image": "aac_ahmed.png", "color": (0.2, 0.7, 0.9, 1)},
            {"title": "Dad", "audio": "say_dad.wav", "image": "aac_dad.png", "color": (0.3, 0.8, 0.4, 1)},
            {"title": "Mohamed", "audio": "say_mohamed.wav", "image": "aac_mohamed.png", "color": (0.2, 0.8, 0.7, 1)},
            {"title": "Milad", "audio": "say_milad.wav", "image": "aac_milad.png", "color": (0.9, 0.5, 0.7, 1)},
            {"title": "Water", "audio": "say_water.wav", "image": "aac_water.png", "color": (0.2, 0.6, 0.9, 1)},
            {"title": "Food", "audio": "say_food.wav", "image": "aac_food.png", "color": (1, 0.6, 0.2, 1)},
            {"title": "Bathroom", "audio": "say_toilet.wav", "image": "aac_toilet.png", "color": (0.4, 0.6, 0.8, 1)},
            {"title": "Play", "audio": "say_play.wav", "image": "aac_play.png", "color": (0.3, 0.8, 0.3, 1)},
        ]

        for card in self.cards:
            box = BoxLayout(orientation='vertical', padding=5)
            img_btn = ImageButton(source=get_path(card["image"]))
            img_btn.bind(on_press=lambda instance, c=card: self.play_card(c))
            
            lbl = Button(
                text=card["title"],
                font_size='18sp', bold=True,
                background_color=card["color"],
                size_hint=(1, 0.3)
            )
            lbl.bind(on_press=lambda instance, c=card: self.play_card(c))

            box.add_widget(img_btn)
            box.add_widget(lbl)
            grid.add_widget(box)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

    def play_card(self, card):
        trigger_vibration()
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
        full_path = get_path(card["audio"])
        if os.path.exists(full_path):
            sound = SoundLoader.load(full_path)
            if sound:
                self.current_sound = sound
                sound.play()

    def go_home(self, instance):
        trigger_vibration()
        if self.current_sound:
            self.current_sound.stop()
        self.manager.current = 'main_menu'


# ---------------- Quiz Game Screen ----------------
class QuizGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_sound = None
        self.questions = [
            {
                "question": "Where is Ahmed?",
                "audio": "q_ahmed.wav",
                "correct": "aac_ahmed.png",
                "options": ["aac_water.png", "aac_ahmed.png", "aac_food.png"]
            },
            {
                "question": "Where is Dad?",
                "audio": "q_dad.wav",
                "correct": "aac_dad.png",
                "options": ["aac_dad.png", "aac_play.png", "aac_toilet.png"]
            },
            {
                "question": "Where is Mohamed?",
                "audio": "q_mohamed.wav",
                "correct": "aac_mohamed.png",
                "options": ["aac_milad.png", "aac_mohamed.png", "aac_ahmed.png"]
            },
            {
                "question": "Where is Milad?",
                "audio": "q_milad.wav",
                "correct": "aac_milad.png",
                "options": ["aac_mohamed.png", "aac_food.png", "aac_milad.png"]
            }
        ]
        self.current_q = 0

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp',
            size_hint=(1, 0.08),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        self.label = Label(
            text=self.questions[0]["question"],
            font_size='26sp', bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, 0.12),
            halign='center'
        )
        self.layout.add_widget(self.label)

        self.reward_label = Label(
            text="",
            font_size='28sp',
            color=(1, 0.8, 0, 1),
            size_hint=(1, 0.08),
            halign='center'
        )
        self.layout.add_widget(self.reward_label)

        self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.72))
        self.update_options()
        self.layout.add_widget(self.grid)

        self.add_widget(self.layout)

    def stop_audio(self):
        if self.current_sound:
            try:
                self.current_sound.stop()
            except Exception:
                pass
            self.current_sound = None

    def play_q_audio(self):
        self.stop_audio()
        path = get_path(self.questions[self.current_q]["audio"])
        if os.path.exists(path):
            sound = SoundLoader.load(path)
            if sound:
                self.current_sound = sound
                sound.play()

    def on_enter(self):
        self.current_q = 0
        self.label.text = self.questions[0]["question"]
        self.reward_label.text = ""
        self.update_options()
        Clock.schedule_once(lambda dt: self.play_q_audio(), 0.3)

    def update_options(self):
        self.grid.clear_widgets()
        q_data = self.questions[self.current_q]
        for opt in q_data["options"]:
            img_btn = ImageButton(
                source=get_path(opt),
                size_hint=(1, 1)
            )
            img_btn.bind(on_press=lambda instance, i=opt: self.check_answer(i))
            self.grid.add_widget(img_btn)

    def check_answer(self, selected_img):
        trigger_vibration()
        correct_img = self.questions[self.current_q]["correct"]
        if selected_img == correct_img:
            App.get_running_app().quiz_correct_answers += 1
            self.stop_audio()
            self.reward_label.text = "✨ Correct! Super! ✨"
            
            cheer_path = get_path('cheer.wav')
            if os.path.exists(cheer_path):
                cheer = SoundLoader.load(cheer_path)
                if cheer:
                    cheer.play()

            if self.current_q < len(self.questions) - 1:
                self.current_q += 1
                self.label.text = self.questions[self.current_q]["question"]
                self.update_options()
                Clock.schedule_once(lambda dt: self.play_q_audio(), CHEER_DURATION)
                Clock.schedule_once(lambda dt: setattr(self.reward_label, 'text', ''), CHEER_DURATION)
            else:
                self.label.text = "Awesome! You finished the quiz!"
                self.reward_label.text = "🏆 ALL ANSWERS CORRECT! 🏆"
                self.grid.clear_widgets()
        else:
            self.reward_label.text = "Try again!"
            self.play_q_audio()

    def go_home(self, instance):
        trigger_vibration()
        self.stop_audio()
        self.manager.current = 'main_menu'


# ---------------- Parent Dashboard Screen ----------------
class ParentDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        btn_back = Button(
            text="Back to Menu",
            font_size='18sp',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        btn_back.bind(on_press=self.go_home)
        self.layout.add_widget(btn_back)

        title = Label(
            text="Parent Dashboard",
            font_size='28sp', bold=True,
            color=(0, 0, 0, 1),
            size_hint=(1, 0.15)
        )
        self.layout.add_widget(title)

        self.stats_label = Label(
            text="Routine Completions: 0\nQuiz Correct Answers: 0",
            font_size='22sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint=(1, 0.75),
            halign='center'
        )
        self.layout.add_widget(self.stats_label)

        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.stats_label.text = (
            f"Routine Completions: {app.routine_completed}\n\n"
            f"Quiz Correct Answers: {app.quiz_correct_answers}"
        )

    def go_home(self, instance):
        trigger_vibration()
        self.manager.current = 'main_menu'


# ---------------- App Definition ----------------
class AhmedApp(App):
    routine_completed = 0
    quiz_correct_answers = 0

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(ToiletRoutineScreen(name='toilet_routine'))
        sm.add_widget(AACBoardScreen(name='aac_board'))
        sm.add_widget(QuizGameScreen(name='quiz_game'))
        sm.add_widget(ParentDashboardScreen(name='parent_dashboard'))
        return sm

    def on_start(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.canvas.ask_update()


if __name__ == '__main__':
    AhmedApp().run()
