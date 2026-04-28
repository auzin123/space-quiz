import os
import arcade
import config
from button import Button

class MenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.sprites = arcade.SpriteList()
        self.background_image = None
        background_path = config.DIR_IMG / "menu_background.jpg"
        if background_path.exists():
            self.background_image = arcade.load_texture(background_path)
        
        center_x = self.window.width / 2
        center_y = self.window.height / 2

        self.title_text = arcade.Text(
            "ГЛАВНОЕ МЕНЮ", center_x, center_y + 200, font_size=50, anchor_x="center", bold=True
        )

        self.start_button = Button(350, 80, int(center_x), int(center_y + 50), "Начать игру")
        self.stats_button = Button(350, 80, int(center_x), int(center_y - 50), "Статистика")
        self.exit_button = Button(350, 80, int(center_x), int(center_y - 150), "Выход")
        
        self.sprites.extend([self.start_button, self.stats_button, self.exit_button])

    def on_draw(self) -> None:
        self.clear()
        if self.background_image:
            arcade.draw_texture_rect(
                self.background_image,
                arcade.rect.XYWH(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
            )

        self.title_text.draw()
        self.sprites.draw()
        
        for button in self.sprites:
            if isinstance(button, Button):
                arcade.draw_text(
                    button.text, button.center_x, button.center_y, arcade.color.BLACK, 24, anchor_x="center", anchor_y="center"
                )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        from game_view import GameView
        from global_stats_view import GlobalStatsView

        if self.start_button.collides_with_point((x, y)):
            self.window.player.play("click1")
            self.window.show_view(GameView())
        elif self.stats_button.collides_with_point((x, y)):
            self.window.player.play("click1")
            self.window.show_view(GlobalStatsView())
        elif self.exit_button.collides_with_point((x, y)):
            self.window.player.play("click1")
            arcade.exit()

    def on_key_press(self, symbol: int, _: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.exit()