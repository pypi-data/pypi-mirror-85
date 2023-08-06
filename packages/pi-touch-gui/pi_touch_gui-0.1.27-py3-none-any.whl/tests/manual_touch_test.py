# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Manual Test - set up some pages for viewing and interaction.
"""
import logging
from pathlib import Path

import pygame

from gui import GUI
from pi_touch_gui._utilities import backlog_error
from raspberrypi_ts import Touchscreen
from test_pages.entry_page import entry_page
from test_pages.poweroff_page import poweroff_page
from test_pages.sampler_page import sampler_page

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] "
           "[%(name)s.%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z"
)
LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    pygame.init()

    touchscreen = Touchscreen()
    interface = GUI(touchscreen)

    _entry_page = entry_page()
    _sampler_page = sampler_page()
    _poweroff_page = poweroff_page()


    # Page transition functions
    def go_to_page_1(button, pushed):
        return _entry_page


    def go_to_page_2(page, pushed):
        return _sampler_page


    def go_to_page_3(button, pushed):
        return _poweroff_page


    _entry_page.config(go_to_page_2)
    _background = str(Path(Path(__file__).parent, "assets/lcars_screen.png"))
    _sampler_page.config(_background, go_to_page_3, go_to_page_1)
    _poweroff_page.config(go_to_page_2)

    # Page Definitions

    try:
        # Add any hardware or other initialization here
        interface.run(_entry_page)
    except Exception as e:
        backlog_error(e, f"Unmanaged exception")
    finally:
        # Add any hardware or other teardown here
        pass
