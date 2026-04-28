import arcade


class Button(arcade.SpriteSolidColor):
    def __init__(
        self,
        width: int,
        height: int,
        center_x: int,
        center_y: int,
        text: str,
    ) -> None:
        super().__init__(width, height, arcade.color.WHITE)
        self.center_x = center_x
        self.center_y = center_y
        self.text = text

