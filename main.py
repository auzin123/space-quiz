import arcade
from sound import SoundManager
from menu_view import MenuView

BACKGROUND_COLOR = (12, 25, 40)

class App(arcade.Window):
    def __init__(self):
        super().__init__(fullscreen=True, title="Викторина про космос")
        self.player = SoundManager()
        self.player.play("background", is_loop=True, volume=0.5)
        
        view = MenuView()
        self.show_view(view)

if __name__ == "__main__":
    app = App()
    arcade.set_background_color(BACKGROUND_COLOR)
    arcade.run()