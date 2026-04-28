import json
import os
from datetime import datetime
import arcade
from button import Button
from quiz import Quiz
from utils import get_formated_time

BASE_FILE = "base.json"

class StatsView(arcade.View):
    def __init__(self, quiz: Quiz, title: str) -> None:
        super().__init__()
        self.quiz = quiz
        self.title = title
        self.sprites = arcade.SpriteList()
        self._save_statistics()

        center_x = self.window.width / 2
        center_y = self.window.height / 2

        self.title_text = arcade.Text(title, center_x, center_y + 80, font_size=40, anchor_x="center")
        self.correct_text = arcade.Text(f"Верных ответов: {self.quiz.correct_answers}", center_x, center_y + 20, font_size=30, anchor_x="center")
        self.incorrect_text = arcade.Text(f"Неверных ответов: {self.quiz.incorrect_answers}", center_x, center_y - 20, font_size=30, anchor_x="center")

        formatted_time = get_formated_time(self.quiz.total_time)
        self.time_text = arcade.Text(f"Время прохождения: {formatted_time}", center_x, center_y - 60, font_size=25, anchor_x="center")
        self.restart_button = Button(340, 90, int(center_x), int(center_y - 170), "В меню")
        self.sprites.append(self.restart_button)
        self.hint_text = arcade.Text("Нажмите ESC, чтобы выйти", center_x, center_y - 260, font_size=20, anchor_x="center")

    def _save_statistics(self) -> None:
        data = {"statistics": []}
        if os.path.exists(BASE_FILE):
            with open(BASE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": self.title,
            "correct_answers": self.quiz.correct_answers,
            "incorrect_answers": self.quiz.incorrect_answers,
            "total_questions": self.quiz.correct_answers + self.quiz.incorrect_answers,
            "time_seconds": round(self.quiz.total_time, 2),
            "formatted_time": get_formated_time(self.quiz.total_time),
        }

        data["statistics"].append(record)
        with open(BASE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def on_draw(self) -> None:
        self.clear()
        self.sprites.draw()
        self.title_text.draw()
        self.correct_text.draw()
        self.incorrect_text.draw()
        self.time_text.draw()
        self.hint_text.draw()
        arcade.draw_text(self.restart_button.text, self.restart_button.center_x, self.restart_button.center_y, arcade.color.BLACK, 24, anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol: int, _: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.exit()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        from menu_view import MenuView
        if button != arcade.MOUSE_BUTTON_LEFT: return
        if self.restart_button.collides_with_point((x, y)):
            self.window.show_view(MenuView())
            self.window.player.play("click1")