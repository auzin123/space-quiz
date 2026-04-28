import arcade
import config
from button import Button
from quiz import Quiz
from utils import get_formated_time


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.quiz = Quiz()
        self.max_time = 3600
        self.sprites = arcade.SpriteList()
        self.buttons: list[Button] = []
        self.question_image = None
        self.background = None

        self._load_background()

        self.question_number = arcade.Text(self._get_question_progress_text(), 50, self.window.height - 80, font_size=40)
        self.question_text = arcade.Text(
            self.quiz.text or "", self.window.width * 0.75, self.window.height * 0.6, font_size=30,
            anchor_x="center", anchor_y="center", multiline=True, width=self.window.width * 0.4
        )

        self.time_text = arcade.Text(get_formated_time(self.max_time), self.window.width - 100, self.window.height - 80, font_size=30, anchor_x="center")

        self.load_question_image()
        self.make_buttons()

    def _load_background(self) -> None:
        bg_path = config.DIR_IMG / "background_questions.png"
        if not bg_path.exists():
            return
        try:
            texture = arcade.load_texture(bg_path)
            win_w, win_h = self.window.width, self.window.height
            scale = max(win_w / texture.width, win_h / texture.height)
            self.background = {
                "texture": texture,
                "rect": arcade.rect.XYWH(win_w / 2, win_h / 2, texture.width * scale, texture.height * scale),
            }
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")

    def _get_question_progress_text(self) -> str:
        return f"{self.quiz.question_idx + 1}/{len(self.quiz.questions)}"

    def load_question_image(self) -> None:
        self.question_image = None
        image_name = self.quiz.questions[self.quiz.question_idx].get("image")

        if image_name:
            image_path = config.DIR_IMG / image_name
            if image_path.exists():
                try:
                    texture = arcade.load_texture(image_path)
                    scale = min((self.window.width * 0.45) / texture.width, (self.window.height * 0.5) / texture.height)

                    self.question_image = {
                        "texture": texture, "width": texture.width * scale, "height": texture.height * scale,
                        "x": self.window.width * 0.3, "y": self.window.height * 0.6
                    }

                    self.question_text.x = self.window.width * 0.72
                    self.question_text.y = self.window.height * 0.6
                    self.question_text.width = self.window.width * 0.4
                    self.question_text.multiline = True
                    return
                except Exception as e:
                    print(f"Ошибка загрузки: {e}")

        self.question_text.x = self.window.width / 2
        self.question_text.y = self.window.height * 0.65
        self.question_text.width = self.window.width * 0.8
        self.question_text.multiline = False

    def make_buttons(self) -> None:
        self.buttons.clear()
        self.sprites = arcade.SpriteList()

        if not self.quiz.options:
            return

        spacing = self.window.width * 0.05
        button_width = (self.window.width - spacing * (len(self.quiz.options) + 1)) / len(self.quiz.options)
        center_x = spacing + button_width / 2

        for option in self.quiz.options:
            button = Button(int(button_width), 80, int(center_x), 100, option)
            self.sprites.append(button)
            self.buttons.append(button)
            center_x += button_width + spacing

    def on_draw(self) -> None:
        self.clear()

        if self.background:
            arcade.draw_texture_rect(self.background["texture"], self.background["rect"])
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height),
                (0, 0, 0, 150)
            )

        if self.question_image:
            arcade.draw_texture_rect(
                self.question_image["texture"],
                arcade.rect.XYWH(self.question_image["x"], self.question_image["y"], self.question_image["width"], self.question_image["height"])
            )

        self.sprites.draw()
        self.question_number.draw()
        self.question_text.draw()
        self.time_text.draw()

        for button in self.buttons:
            arcade.draw_text(button.text, button.center_x, button.center_y, arcade.color.BLACK, 24, anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol: int, _: int) -> None:
        from menu_view import MenuView
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(MenuView())

    def on_update(self, delta_time: float) -> None:
        from stats_view import StatsView
        if self.quiz.total_time >= self.max_time:
            return

        self.quiz.total_time += delta_time
        remaining = max(0.0, self.max_time - self.quiz.total_time)
        self.time_text.text = get_formated_time(remaining)

        if remaining <= 0:
            self.window.show_view(StatsView(self.quiz, "Время закончилось"))

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        from stats_view import StatsView
        if self.quiz.total_time >= self.max_time or button != arcade.MOUSE_BUTTON_LEFT:
            return

        for btn in self.buttons:
            if btn.collides_with_point((x, y)):
                self.window.player.play("click1")
                if btn.text == self.quiz.answer:
                    self.quiz.correct_answers += 1
                else:
                    self.quiz.incorrect_answers += 1

                if self.quiz.next_question():
                    self.question_number.text = self._get_question_progress_text()
                    self.question_text.text = self.quiz.text or ""
                    self.load_question_image()
                    self.make_buttons()
                else:
                    self.window.show_view(StatsView(self.quiz, "Викторина завершена"))
                break