"""Модуль звука."""

import arcade
import config

class SoundManager:
    def __init__(self):
        # Загружаем звуки один раз при запуске игры
        self.sounds = {
            "click1": arcade.load_sound(config.DIR_SOUND / "click1.mp3"),
            "background": arcade.load_sound(config.DIR_SOUND / "background.mp3")
        }

    def play(self, sound_name: str, is_loop: bool = False, volume: int = 1.0) -> None:
        """Воспроизводит звук из словаря по его названию."""
        if sound_name in self.sounds:
            # В новых версиях Arcade аргумент называется 'loop'
            # Если возникнет ошибка, попробуй заменить 'loop' на 'looping'
            arcade.play_sound(self.sounds[sound_name], loop=is_loop, volume=volume)
        else:
            print(f"Ошибка: звук '{sound_name}' не найден в словаре!")