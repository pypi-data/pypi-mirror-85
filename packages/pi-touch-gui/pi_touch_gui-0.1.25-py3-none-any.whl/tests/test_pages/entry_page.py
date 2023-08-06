# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Test - An entry page with pulsing lights
"""

# ---- Pulsing light test function (light)

from colors import RED
from gui import Page
from tests._utilities import pulsing_light_func
from widget_buttons import Button
from widget_displays import Light, Label


def entry_page():
    _entry_label = Label((0, 0), (800, 50), label="ENTER"),

    _pulse1_light = Light((0, 0), (50, 50), function=pulsing_light_func)
    _pulse1_light.rate = 400

    _pulse2_light = Light((750, 0), (50, 50), function=pulsing_light_func)
    _pulse2_light.rate = 300

    _pulse3_light = Light((0, 430), (50, 50), function=pulsing_light_func)
    _pulse3_light.rate = 200

    _pulse4_light = Light((750, 430), (50, 50), pulsing_light_func)
    _pulse4_light.rate = 100

    _touch_me_button = Button((200, 150), (400, 100), font_size=100,
                              label_color1=RED, label="Touch Me")

    def _configure_page(go_to_page):
        """ Custom configuration on the entry page - sets the page and
        button functions.

        Parameters
        ----------
        go_to_page : Callable[[IWidget, bool], Optional['Page']]
        """
        _entry_page.function = go_to_page
        _touch_me_button.function = go_to_page

    _entry_page = Page(
        # Tests dynamic Light functions, Label, and default Page function
        [
            _pulse1_light,
            _pulse2_light,
            _pulse3_light,
            _pulse4_light,
            _touch_me_button
        ]
    )
    # Add a custom attribute, which is monkey-patching at its worst
    _entry_page.config = _configure_page

    return _entry_page
