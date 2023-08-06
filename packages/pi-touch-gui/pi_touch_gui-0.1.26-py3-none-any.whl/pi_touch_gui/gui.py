# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Graphical User Interface objects

    A `Page` is a set of widgets that define the interaction and display
    surface of the GUI

    The `GUI` manages the hardware and runs the Pages
"""
import logging
import math
from typing import List, Optional, NoReturn

import pygame
from pygame.constants import *

from pi_touch_gui._utilities import backlog_error
from pi_touch_gui._widget_bases import IWidget, IWidgetInterface
from pi_touch_gui.colors import BLACK
from pi_touch_gui.multitouch.raspberrypi_ts import Touchscreen, TS_RELEASE
from widget_buttons import Button

LOG = logging.getLogger(__name__)


class Page(object):
    WALL = 'wall'
    GO_WALL = -1
    GO_UP = 0
    GO_DOWN = 1
    GO_LEFT = 2
    GO_RIGHT = 3

    GO_NEIGHBORLESS = [-1, 1, -1, 1]
    GO_NAMES = ["Up", "Down", "Left", "Right"]

    def __init__(self, widgets=None, background=None, function=None):
        """ A collection of widgets that make up an interaction page.

        Parameters
        ----------
        widgets : List[IWidget]
        background : str
            Background image resource filepath for this Page
        function : Callable[[Page], Optional[Type['Page']]]
            Function to call if none of the widgets consume
            an event.
        """
        # If no widgets added on init, they can be added with `add_widgets()`
        # later.
        self._widgets = [] if widgets is None else widgets

        if background is not None:
            self._background = pygame.image.load(background).convert()
        else:
            self._background = None
        self.function = function
        self._focus_widget = None
        if widgets is None:
            self._widgets = []
            self._prev_focus_widget = None
        else:
            self._widgets = widgets
            self._prev_focus_widget = widgets[0]

        self._last_adjustment = pygame.time.get_ticks()
        self.adjustment_rate = 100

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, filepath):
        self._background = pygame.image.load(filepath).convert()

    def add_widgets(self, widgets):
        """ Add widgets to the Page.

        Parameters
        ----------
        widgets : List[IWidget]
        """
        self._widgets += widgets
        # Set or reset the base focus widget to the top
        self._prev_focus_widget = self._widgets[0]

    def find_widget(self, widget_or_id):
        """ Given a widget ID, find that widget.

        Parameters
        ----------
        widget_or_id : Union[IWidgetInterface, String]
            If a widget is passed in, return it directly. Otherwise search
            for the id and return the widget.

        Returns
        -------
        IWidgetInterface
        """
        # Deal with the WALL case, where we _know_ there isn't a widget
        if widget_or_id == Page.WALL:
            return None
        if not isinstance(widget_or_id, str):
            return widget_or_id

        return self._scan_for_widget_by_id(self._widgets, widget_or_id)

    def _scan_for_widget_by_id(self, widgets, widget_id):
        """ Recursively scan for a widget ID, returning the widget.

        Parameters
        ----------
        widgets : List[IWidgetInterface]
            A list of widgets, some of which may container lists of widgets
        widget_id : String
            The widget ID to search for

        Returns
        -------
        IWidgetInterface
        """
        for widget in widgets:
            # See if this is a widget container...
            found_widget = None
            try:
                # Assume the widget is a widget container and assert if not
                sub_widgets = widget._widgets
                found_widget = self._scan_for_widget_by_id(sub_widgets,
                                                           widget_id)
            except AttributeError:
                if widget.id == widget_id:
                    found_widget = widget
            if found_widget is not None:
                return found_widget
        return None

    def find_next_widget(self, widget_or_id, direction):
        """ Given a widget ID, find the widget AFTER that widget.

        Parameters
        ----------
        widget_or_id : Union[IWidgetInterface, String]
        direction : Integer
            Direction of scan, sign(direction)

        Returns
        -------
        IWidgetInterface
        """
        # Deal with the WALL case, where we _know_ there isn't a widget
        if widget_or_id == Page.WALL:
            return None
        try:
            widget_or_id = widget_or_id.id
        except AttributeError:
            pass

        return self._scan_for_next_widget_by_id(self._widgets,
                                                widget_or_id,
                                                math.copysign(1, direction))

    def _scan_for_next_widget_by_id(self, widgets, widget_id, step):
        """ Recursively scan for a widget ID, returning the widget AFTER the
        widget found.

        Parameters
        ----------
        widgets : List[IWidgetInterface]
            A list of widgets, some of which may container lists of widgets
        widget_id : String
            The widget ID to search for
        step : Integer
            The step (+1, -1) we are scanning next for.

        Returns
        -------
        IWidgetInterface
        """
        step = int(step)
        for idx, widget in enumerate(widgets):
            # See if this is a widget container...
            found_widget = None
            try:
                # Assume the widget is a widget container and assert if not
                sub_widgets = widget._widgets
                found_widget = self._scan_for_widget_by_id(sub_widgets,
                                                           widget_id)
            except AttributeError:
                if widget.id == widget_id:
                    try:
                        found_widget = widgets[idx + step]
                    except Exception as e:
                        return None
            if found_widget is not None:
                return found_widget
        return None

    def touch_handler(self, event, touch) -> Optional['Page']:
        """ Update all widgets with a touch event.

            The first widget to consume the touch wins, and downstream
            widgets won't be tested.

            If no widget consumes the event, we call `function(self) -> Page`

        Parameters
        ----------
        event : int
            Event code defined for the interface; e.g. _widget_bases.py imports
            TS_PRESS, TS_RELEASE, and TS_MOVE
        touch : Touch
            The Touch object for the event.

        Returns
        -------
        Optional[Page]
            If the widget function names a new page, it is returned here
        """
        for widget in self._widgets:
            consumed, new_page = widget.event(event, touch)
            if consumed:
                return new_page

        if event == TS_RELEASE and self.function:
            return self.function(self, False)
        return None

    def render(self, surface: pygame.Surface):
        """Redraw all widgets to screen.

        Call `render()` for all widgets in the Page, once per frame.

        Parameters
        ----------
        surface : pygame.Surface
            Surface (screen) to draw to
        """
        if self.background is not None:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(BLACK)
        for widget in self._widgets:
            try:
                widget.render(surface)
            except Exception as e:
                backlog_error(e, f"Problem rendering widget {widget}")
                raise

    def focus_widget(self, enable):
        """ Wake up the focus system for gesture control.

        Will always restart on the last widget that had focus.

        Parameters
        ----------
        enable : Bool
            If True, then focus; else de-focus
        """
        if self.is_focused() == enable:
            return

        prev_widget = self._prev_focus_widget
        self._focus_widget = self._prev_focus_widget
        if enable:
            if not prev_widget.can_focus():
                # This will walk the down chain until it finds a widget
                # that can take focus.  Skips starting labels and stuff.
                self.shift_widget_focus(Page.GO_DOWN)
            else:
                prev_widget.focus(True)
        else:
            self._focus_widget = None
            prev_widget.focus(False)

    def is_focused(self):
        """ Determine if we are in widget focus mode.

        Returns
        -------
        Bool
        """
        return self._focus_widget is not None

    def shift_widget_focus(self, direction):
        """ Shift focus one way or the other, wrapping at the boundaries.

        Parameters
        ----------
        direction : int
            Direction of motion; Page.WALL (no motion),
        """
        if direction == Page.GO_WALL:
            return
        if not self.is_focused():
            return

        start_widget = test_widget = self._focus_widget
        while True:
            next_widget = test_widget.neighbors[direction]

            # We have an IWidgetInterface, ID string, or 'wall'
            if next_widget == Page.WALL:
                # Hit a wall
                return
            elif next_widget is None:
                # No neighbor specified, so use a generic direction
                next_widget = self.find_next_widget(
                    test_widget,
                    Page.GO_NEIGHBORLESS[direction])
            else:
                # Neighbor as a widget ID or index
                next_widget = self.find_widget(next_widget)

            if test_widget.label == 'group':
                pause = True

            # In case we instantiated a neighbor, store it
            test_widget.neighbors[direction] = next_widget

            if next_widget == Page.GO_WALL:
                return
            elif next_widget == start_widget:
                return
            elif next_widget is None:
                return

            # Take the tentative next widget and make it current
            test_widget = next_widget
            if test_widget.can_focus():
                break

        try:
            if self._focus_widget is not None:
                self._focus_widget.focus(False)
            next_widget.focus(True)
        except Exception:
            pause = True
        self._focus_widget = next_widget
        self._prev_focus_widget = next_widget

    def adjust_widget(self, direction):
        """ Send an up/down value adjustment to the control widget.
        """
        time = pygame.time.get_ticks()
        if time - self._last_adjustment < self.adjustment_rate:
            return

        if self._focus_widget.adjust is not None:
            self._focus_widget.adjust(direction)
            self._last_adjustment = time

    def press_widget(self):
        """ Activate the function of the widget.
        """
        if self._focus_widget.press is not None:
            self._focus_widget.press()

    def release_widget(self):
        """ Activate the function of the widget.
        """
        if self._focus_widget.release is not None:
            return self._focus_widget.release()
        return None

    def iter_widgets(self):
        """ Iterate over the widgets in the page.

        Returns
        -------
        iter(IWidget)
        """
        return iter(self._widgets)


class GUI(object):
    # Constants that define the GUI behavior
    FPS = 60
    FADE_TIME = 60
    BLACKOUT_TIME = 300
    BRIGHT_LEVEL = 128
    FADE_LEVEL = 16

    # Initialize the event timer
    last_event = pygame.time.get_ticks()

    def __init__(self, touchscreen, bright=None):
        """ A Graphical User Interface for using a touchscreen.

        Parameters
        ----------
        touchscreen : Touchscreen
            See for example the `multitouch.raspberrypi_ts.Touchscreen`
        bright : int
            Brightness level (to balance visibility and screen wear).  Defaults
            to GUI.BRIGHT_LEVEL.
        """
        self._bright_level = self.BRIGHT_LEVEL if bright is None else bright
        self._touchscreen = touchscreen
        self._current_page = None
        self._first_page = None
        self._running = False
        self._faded = False
        self._blacked = False

        with open('/sys/class/backlight/rpi_backlight/max_brightness',
                  'r') as f:
            max_str = f.readline()
        self.max_brightness = min(int(max_str), 255)
        self.set_brightness(self._bright_level)

    def reset_display(self):
        """ Enable on the backlight and bring to the default brightness.
        """
        self.last_event = pygame.time.get_ticks()

        if self._faded:
            self.set_brightness(self._bright_level)
            self.fade = False
        if self._blacked:
            self.set_light(True)
            self._blacked = False

    def set_brightness(self, level):
        """ Set the backlight to a determined brightness level.

        Parameters
        ----------
        level : int
        """
        level_str = f"{min(self.max_brightness, level)}\n"
        with open('/sys/class/backlight/rpi_backlight/brightness', 'w') as f:
            f.write(level_str)

    def set_light(self, on):
        """ Turn the backlight activateion to On or Off

        Parameters
        ----------
        on : bool
            True for On, False for Off
        """
        if on is True:
            blank_str = "0"
        else:
            blank_str = "1"
            self._current_page = self._first_page
            self._current_page.render(self._touchscreen.surface)
        with open('/sys/class/backlight/rpi_backlight/bl_power', 'w') as f:
            f.write(blank_str)

    def run(self, page) -> NoReturn:
        """ Run the GUI, staring with the initial Page.

        Does not return, but does an exit() when done. Wrapping
        code in this thread needs to embed this in a Try/Finally to do cleanup.

        Parameters
        ----------
        page : Page
        """
        self._current_page = page
        self._first_page = page
        self._running = True

        self._touchscreen.run()

        fpsClock = pygame.time.Clock()

        def handle_touches(e, t):
            """ Call the `Page.touch_handler()` to process an event. """
            if self._blacked:
                # Consume touch if we are fully blacked out
                self.reset_display()
                return
            # Reset the brightness
            self.reset_display()

            new_page = self._current_page.touch_handler(e, t)
            if new_page is not None:
                if isinstance(new_page, Page):
                    self._current_page = new_page
                else:
                    LOG.error(
                        f"Unsupported touch result {type(new_page)!r}")

        # All touch types go through the `Page.touch_handler()`
        for touch in self._touchscreen.touches:
            touch.on_press = handle_touches
            touch.on_release = handle_touches
            touch.on_move = handle_touches

        try:
            while self._running:
                # Deal with screen fade and blackout
                time = pygame.time.get_ticks()
                # deltaTime in seconds.
                deltaTime = (time - self.last_event) / 1000.0
                if deltaTime > self.BLACKOUT_TIME:
                    self.set_light(False)
                    self._blacked = True
                elif deltaTime > self.FADE_TIME:
                    self.set_brightness(self.FADE_LEVEL)
                    self._faded = True

                # Render the current page
                self._current_page.render(self._touchscreen.surface)
                pygame.display.flip()

                # Check for keyboard events, to support VNC interactions
                events = pygame.event.get()
                new_page = None
                if len(events) > 0:
                    for event in events:
                        if event.type == KEYDOWN:
                            page = self._current_page
                            if event.key in [K_SPACE, K_RETURN]:
                                if page.is_focused():
                                    page.press_widget()

                            if event.key == K_UP:
                                page.shift_widget_focus(Page.GO_UP)
                            elif event.key == K_DOWN:
                                page.shift_widget_focus(Page.GO_DOWN)
                            elif event.key == K_LEFT:
                                page.shift_widget_focus(Page.GO_LEFT)
                            elif event.key == K_RIGHT:
                                page.shift_widget_focus(Page.GO_RIGHT)
                        if event.type == KEYUP:
                            page = self._current_page
                            if event.key in [K_SPACE, K_RETURN]:
                                if page.is_focused():
                                    new_page = page.release_widget()
                                    widget = page._focus_widget
                                    if (isinstance(widget, Button)
                                            and widget.behavior != Button.HOLD):
                                        page.focus_widget(False)
                                else:
                                    page.focus_widget(True)

                            elif event.key == K_ESCAPE:
                                page.focus_widget(False)

                if pygame.key.get_pressed()[K_EQUALS]:
                    page.adjust_widget(1)
                elif pygame.key.get_pressed()[K_MINUS]:
                    page.adjust_widget(-1)

                # The keyboard interactions may have set a new page
                if new_page is not None:
                    if isinstance(new_page, Page):
                        self._current_page = new_page
                    else:
                        LOG.error(f"Unsupported page result "
                                  f"{type(new_page)!r}")

                # Lock it into the framerate
                fpsClock.tick(self.FPS)

        except Exception as e:
            backlog_error(e, f"Unmanaged exception")
        finally:
            self.reset_display()
            LOG.info("Stopping touchscreen thread...")
            self._touchscreen.stop()

            LOG.info("Exiting GUI...")
            exit()

    def stop(self):
        """ Tell the GUI to stop running.

        This method isn't really accessible, but here for completeness.
        """
        self._running = False
