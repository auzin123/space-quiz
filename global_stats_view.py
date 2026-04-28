import json
import os
import arcade
from button import Button
from utils import get_formated_time

BASE_FILE = "base.json"

def get_global_stats():
    if not os.path.exists(BASE_FILE):
        return None
    
    with open(BASE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        stats = data.get("statistics", [])
    
    if not stats:
        return None

    users_count = len(stats)
    correct_total = sum(s["correct_answers"] for s in stats)
    incorrect_total = sum(s["incorrect_answers"] for s in stats)
    time_total = sum(s["time_seconds"] for s in stats)

    return {
        "users_count": users_count,
        "correct_avg": round(correct_total / users_count, 2),
        "incorrect_avg": round(incorrect_total / users_count, 2),
        "time_avg": get_formated_time(time_total / users_count),
        "stats": stats
    }


class GlobalStatsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.sprites = arcade.SpriteList()
        stats = get_global_stats()
        center_x = self.window.width // 2
        
        if stats:
            self.stats_lines = [
                f"{idx}. Верных: {stat['correct_answers']}, Ошибок: {stat['incorrect_answers']}, Время: {stat['formatted_time']}"
                for idx, stat in enumerate(stats['stats'][-12:], 1)
            ]
            summary = f"Всего: {stats['users_count']} | Ср. балл: {stats['correct_avg']} | Ср. время: {stats['time_avg']}"
            self.summary_text = arcade.Text(summary, center_x, 150, font_size=18, anchor_x="center", color=arcade.color.WHITE)
        else:
            self.stats_lines = []
            self.summary_text = arcade.Text("Статистика пока пуста", center_x, self.window.height // 2, font_size=30, anchor_x="center", color=arcade.color.WHITE)
        
        self.back_button = Button(300, 80, center_x, 60, "Назад")
        self.sprites.append(self.back_button)

    def on_draw(self):
        self.clear()
        start_y = self.window.height - 100
        for idx, line in enumerate(self.stats_lines):
            arcade.draw_text(line, self.window.width // 2, start_y - idx * 35, arcade.color.WHITE, 16, anchor_x="center")
        
        self.summary_text.draw()
        self.sprites.draw()
        arcade.draw_text(self.back_button.text, self.back_button.center_x, self.back_button.center_y, arcade.color.BLACK, 24, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        from menu_view import MenuView
        if self.back_button.collides_with_point((x, y)):
            self.window.player.play("click1")
            self.window.show_view(MenuView())

    def on_key_press(self, symbol: int, _: int) -> None:
        from menu_view import MenuView
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(MenuView())