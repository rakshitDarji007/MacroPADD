import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.extensions.encoder import Encoder
from kmk.extensions.display import Display, DisplayType, DisplayFrame
import adafruit_ssd1306
import busio

keyboard = KMKKeyboard()

switch_pins = (board.D7, board.D8, board.D10, board.D9, board.A0, board.A1)
keyboard.pins = switch_pins

encoder_ext = Encoder()
keyboard.extensions.append(encoder_ext)
encoder_ext.pins = ((board.A3, board.D6, None),)
encoder_ext.map = [((KC.VOLD, KC.VOLU, KC.NO),)]

try:
    i2c = busio.I2C(scl=board.D5, sda=board.D4)
    display_ext = Display(
        display_type=DisplayType.CUSTOM,
        driver=adafruit_ssd1306.SSD1306_I2C(128, 32, i2c),
        width=128, height=32,
        flip_x=False, flip_y=False,
    )
    keyboard.extensions.append(display_ext)
    loading_frame = DisplayFrame(key=None, lines=["MacroPad ON"])
    layer_frame = DisplayFrame(key="layer", lines=["Layer: {layer}"])
    display_ext.frames = [loading_frame, layer_frame]
    display_ext.enable()
except Exception as e:
    print(f"OLED Error: {e}")


SPOTIFY_MACRO = [KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(300),
                 KC.S, KC.P, KC.O, KC.T, KC.I, KC.F, KC.Y,
                 KC.MACRO_SLEEP_MS(100), KC.ENTER]
ZOOM_MACRO = [KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(300),
              KC.Z, KC.O, KC.O, KC.M,
              KC.MACRO_SLEEP_MS(100), KC.ENTER]
GOOGLE_MACRO = [KC.LGUI(KC.R), KC.MACRO_SLEEP_MS(300),
                KC.H, KC.T, KC.T, KC.P, KC.S, KC.COLN, KC.SLASH, KC.SLASH,
                KC.W, KC.W, KC.W, KC.DOT, KC.G, KC.O, KC.O, KC.G, KC.L, KC.E,
                KC.DOT, KC.C, KC.O, KC.M,
                KC.MACRO_SLEEP_MS(100), KC.ENTER]

keyboard.keymap = [
    [
        KC.MEDIA_NEXT_TRACK,
        KC.MEDIA_PREV_TRACK,
        KC.MEDIA_PLAY_PAUSE,
        KC.MACRO(*SPOTIFY_MACRO),
        KC.MACRO(*ZOOM_MACRO),
        KC.MACRO(*GOOGLE_MACRO),
    ]
]

if __name__ == '__main__':
    keyboard.go()
