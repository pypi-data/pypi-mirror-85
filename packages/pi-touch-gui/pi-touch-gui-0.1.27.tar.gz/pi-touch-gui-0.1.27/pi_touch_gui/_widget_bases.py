# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Widget Base Classes, providing the core functionality of the widgets.

    Widgets are single interactive elements attached to a Page.
"""
import math
import uuid
from abc import ABC, abstractmethod
from typing import Tuple, Union, Optional

import pygame
from custom_inherit import doc_inherit
from pygame import Color

from pi_touch_gui._utilities import snapped_value_string
from pi_touch_gui.colors import WHITE, BLACK, MEDIUM_GRAY
from pi_touch_gui.multitouch.raspberrypi_ts import (TS_PRESS, TS_RELEASE,
                                                    TS_MOVE, Touch)

# Default font name - specify one here if you want something other
# than the system default.
FONT_NAME = None


class IWidgetInterface(ABC):
    """ The bare minimum methods to implement to be a widget.
    """

    @property
    @abstractmethod
    def id(self):
        """ The Widget ID, uniquely identifies each widget.
        """

    @property
    @abstractmethod
    def neighbors(self):
        """ The Widget's Neighbors [GO_UP, GO_DOWN, GO_LEFT, GO_RIGHT], which
        may default to [None, None, None, None].
        """

    @abstractmethod
    def event(self, event, touch) -> Tuple[bool, Optional['Page']]:
        """ Handle touch events, translating them to individual `on_*` calls.

        Parameters
        ----------
        event : int
            Event code defined for the interface; e.g. _widget_bases.py imports
            TS_PRESS, TS_RELEASE, and TS_MOVE
        touch : Touch
            The Touch representing the event, where `touch.position` is the
            (x, y) coordinate of the touch.

        Returns
        -------
        Optional[Page]
            The page to transition to, or None to stay on this page
        """

    @abstractmethod
    def can_focus(self):
        """ Return True if this widget can accept focus.
        """

    @abstractmethod
    def render(self, surface):
        """ Render to the device pygame Surface.

        Parameters
        ----------
        surface : pygame.Surface
        """

    @abstractmethod
    def render_focus(self, surface):
        """ Render a default focus marker that is the extent.

        Only called if can_focus() returns True, but should be defined anyway.

        Parameters
        ----------
        surface : pygame.Surface
        """


class IWidget(IWidgetInterface):
    """ Widget base class that processes events and holds common state.

        Sub-classes can define any or all of the three event handlers:

            on_press(Touch) -> None
            on_release(Touch) -> Optional[Page]
            on_move(Touch) -> None

        where:
            `Page` : If not None, jump to that page on the next frame.
    """
    # Cache fonts, no need for each widget to have their own copy
    _font_cache = dict()

    def __init__(self, position, size,
                 widget_id=None,
                 neighbors=None,
                 font_size=None,
                 label=None,
                 color1=None,
                 color2=None,
                 label_color1=None,
                 label_color2=None):
        """ Initialize the widget.

        Most parameters can be ignored and will pick up sensible defaults.

        Parameters
        ----------
        position : Tuple[int, int]
            The (x, y) top-left corner of the widget. The screen positioning
            is accounted at (0, 0) being the far top-left, increasing down
            and to the right.
        size : Tuple[int, int]
            The (w, h) of the widget's rectangular extent.
            Note that in some widgets labels or indicators could fall outside
            of these extents, and other widgets may choose to re-define the
            extent to something less rectangular.
        widget_id : str
            Optional ID for this widget, if not given, gets a random uuid.
        neighbors : List[Union[str, IWidget]]
            The neighbors of this widget, specified by the widget itself or
            that widget's ID.  The list order is [GO_LEFT, GO_RIGHT,
            GO_UP, GO_DOWN].  If you want to stop at an edge, specify
            the neighbor as Page.WALL. These neighbor hints help with
            keyboard arrow navigation of the Page.
        font_size : int
            Height of the font in pixels.  If not specified, will be 1/2 the
            height of the widget.
        label : str
        color1 : Color
            Main color of the widget as a tuple of (r, g, b) or (r, g, b, a),
            or a pygame.Color; the unselected color or foreground color
        color2 : Color
            Secondary color of the widget; selected color or background color
        label_color1 : Union[Tuple[int, int, int], Tuple[int, int, int, int]]
            Main color of the label; unselected color
        label_color2 : Color
            Secondary color of the label; selected color
        """
        self._id = str(uuid.uuid4()) if widget_id is None else widget_id

        self.x, self.y = position
        self.w, self.h = size

        # Fill in any important values not specified
        self.label = "" if label is None else label
        self.color1 = MEDIUM_GRAY if color1 is None else color1
        self.color2 = WHITE if color2 is None else color2
        self.label_color1 = WHITE if label_color1 is None else label_color1
        self.label_color2 = BLACK if label_color2 is None else label_color2

        self.font_size = (int(min(self.w, self.h) >> 1) if font_size is None
                          else font_size)
        font_key = f"{FONT_NAME}:{self.font_size}"
        if font_key in self._font_cache:
            font = self._font_cache[font_key]
        else:
            font = pygame.font.Font(FONT_NAME, self.font_size)
            self._font_cache[font_key] = font
        self.font = font

        self._pressed = False
        self._focus = False
        self._neighbors = neighbors

        self.touches = []

        # Probe for the existence of the event handlers.
        try:
            callable(self.on_press)
        except AttributeError:
            self.on_press = None
        try:
            callable(self.on_release)
        except AttributeError:
            self.on_release = None
        try:
            callable(self.on_move)
        except AttributeError:
            self.on_move = None
        try:
            callable(self.adjust)
        except AttributeError:
            self.adjust = None

    @property
    def id(self):
        return self._id

    @property
    def position(self) -> Tuple[int, int]:
        """ The x, y top-left corner of the widget.
        """
        return self.x, self.y

    @property
    def size(self) -> Tuple[int, int]:
        """ The width, height extents of the widget.
        """
        return (self.w, self.h)

    @property
    def pressed(self) -> bool:
        """ True if the widget is currently pressed.
        """
        return len(self.touches) > 0 or self._pressed

    @property
    def neighbors(self):
        if self._neighbors is None:
            self._neighbors = [None, None, None, None]
        return self._neighbors

    @neighbors.setter
    def neighbors(self, new_neighbors):
        """ For enhanced keyboard navigation, point to the neighboring widgets.

        If neighbors are not specified, a more limited keyboard navigation is
        available based on the list order of the widgets in the Page.

        Note that you specify the neighbors as ID or IWidget objects, but on
        use the system takes the liberty of changing the representation to
        whatever it sees fit so don't be surprised if the internal values
        change.

        Parameters
        ----------
        new_neighbors : List(Union(String, IWidget))
            The list of neighbors in order Up, Down, Left, Right; where each
            entry can be an IWidget, the widget_id, or Page.WALL
        """
        if self._neighbors is None:
            self._neighbors = [None, None, None, None]

        for idx, neighbor in enumerate(new_neighbors):
            if isinstance(neighbor, IWidget):
                self._neighbors[idx] = neighbor
            elif isinstance(neighbor, str):
                self._neighbors[idx] = neighbor
            else:
                raise ValueError(f"Unsupported neighbor {idx} type "
                                 f"{type(neighbor)!r}")

    def focus(self, enabled):
        """ Set the widget's focus, for the gestural interface.

        Parameters
        ----------
        enabled : bool
            True if this Widget is receiving focus.
        """
        self._focus = enabled

    def can_focus(self) -> bool:
        return True

    def touch_inside(self, touch) -> bool:
        """ Test a touch against the generic widget rectangle.

        Parameters
        ----------
        touch : Touch
            The touch coordinates, where `touch.position` is a Tuple[int, int]
            of the (x, y) position of the touch.

        Returns
        -------
        bool
            True if the touch is inside the widget extents.
        """
        x, y = touch.position
        return (self.x <= x <= self.x + self.w and
                self.y <= y <= self.y + self.h)

    def event(self, event, touch) -> Tuple[bool, Optional['Page']]:
        # PRESS
        # A press can only be registered when it is in the widget bounds
        if self.touch_inside(touch):
            if event == TS_PRESS and touch not in self.touches:
                self.touches.append(touch)
                if self.on_press:
                    return True, self.on_press(touch)

        # RELEASE
        # A touch can be released even when its not over a widget.
        if event == TS_RELEASE and touch in self.touches:
            self.touches.remove(touch)
            if self.on_release:
                return True, self.on_release(touch)

        # MOVE
        # Touch movement is tracked even when it's not over a widget
        if event == TS_MOVE and touch in self.touches:
            if self.on_move:
                return True, self.on_move(touch)

        # "Not Me" - report not consumed
        return False, None

    def press(self):
        self._pressed = True

    def release(self):
        self._pressed = False

    def state_colors(self, active=None) -> Tuple[Color, Color]:
        """ Return the (color, label_color) appropriate to the current state.

        Parameters
        ----------
        active : bool
            Override to force the widget to render as active.

        Returns
        -------
        Tuple[Color, Color]
            Returns a tuple of (color, label_color) where the colors can
            be a pygame.Color or (r,g,b) or (r,g,b,a) tuples.
        """
        active = self.pressed or active is True
        if active:
            color = self.color2
            label_color = self.label_color2
        else:
            color = self.color1
            label_color = self.label_color1
        return color, label_color

    def focus_color(self):
        """ Return a changing color for the focus highlight
        """
        time = pygame.time.get_ticks()
        pulse = math.sin(time / 133) + 1.0  # sets to range 0..2
        return (pulse * 64 + 127,
                64 - pulse * 16,
                64 - pulse * 16)

    def render_centered_text(self, surface, text, color, bg_color=None):
        """ Render text in the center of the widget.

        Parameters
        ----------
        surface : pygame.Surface
        text : str
        color : Color
        bg_color : Color
            If you specify the background color, it can render the text a
            bit faster because it won't use alpha for a clear background.
        """
        if text is None:
            return

        text = self.font.render(text, 1, color, bg_color)
        textpos = text.get_rect()
        textpos.centerx = self.x + (self.w / 2)
        textpos.centery = self.y + (self.h / 2)
        surface.blit(text, textpos)

    def render_focus(self, surface):
        """ Render a default focus outline.

        Parameters
        ----------
        surface : pygame.Surface
        """
        fx, fy = self.x - 2, self.y - 2
        fw, fh = self.w + 4, self.h + 4
        pygame.draw.rect(surface, self.focus_color(), ((fx, fy), (fw, fh)), 4)


class IButtonWidget(IWidget):
    """ ButtonWidget base that extends IWidget for push buttons.
    """
    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size, function=None, **kwargs):
        """
        Parameters
        ----------
        function : Callable[[IWidget, bool], Optional['Page']]
            Function to call on button events, with a True/False parameter
            that is True when pressed and False when released.
            Optionally returns a new Page to change pages.
        """
        self.function = function
        super(IButtonWidget, self).__init__(position, size, **kwargs)

    def on_release(self, touch) -> Optional['Page']:
        """ Buttons always call their function on the release event.

        It has already been determined that the touch is inside the
        widget via `touch_inside()`.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for buttons

        Returns
        -------
        Page
            If specified, the new Page to go to.
        """
        return self.release()

    def release(self):
        """ Trigger the button, calling its function if specified.
        """
        super(IButtonWidget, self).release()
        if self.function:
            return self.function(self, False)

    @doc_inherit(IWidget.render, style='numpy_with_merge')
    def render(self, surface):
        """ Render the generic button as a filled rectangle with a label.
        """
        color, label_color = self.state_colors()

        pygame.draw.rect(surface, color, (self.position, self.size), 0)
        self.render_centered_text(surface, self.label, label_color, color)

        if self._focus:
            self.render_focus(surface)


class IControlWidget(IWidget):
    """ ControlWidget base that extends IWidget for input controls.
    """

    @doc_inherit(IWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 min_max,
                 start_value=None,
                 snap_value=None,
                 dynamic=None,
                 function=None,
                 **kwargs):
        """
        Parameters
        ----------
        min_max : Tuple[float, float]
            The minimum and maximum values the control might take.
        start_value : float
            The initial value the widget holds.
        snap_value : float
            A value that defines (by example) the display (snap) resolution
            of the widget's value.  E.g. 0.01, 0.1, 1.  The snap value is
            not just a display affect, but controls the resolution of the
            adjusted value of the widget itself.
        dynamic : bool
            True if the function is called each frame the control is active,
            otherwise the function is only called on release.
        function : Callable[[IWidget, float], Optional['Page']]
            Function to call on control events, with a new value for the
            control. Optionally returns a new Page to change pages on release.
        """
        self.function = function
        super(IControlWidget, self).__init__(position, size,
                                             **kwargs)

        # Constrain the snap values to usable range
        self.snap_value = 1 if snap_value is None else snap_value
        self.snap_value = 0.01 if self.snap_value < 0.01 else self.snap_value

        self.min_val, self.max_val = (min_max)
        # Value is in 0..1, where adjusted_value is in min_val..max_val
        self.range = self.max_val - self.min_val

        if start_value is not None:
            self.adjusted_value = start_value
            self.value = self.normalize_adjusted_value(start_value)
        else:
            self.adjusted_value = min_max[0]
            self.value = self.normalize_adjusted_value(min_max[0])

        self.dynamic = False if dynamic is None else dynamic

    def map_value_to_adjusted_value(self, value) -> float:
        """ Map a value in 0..1 to an interpolated value in min_val..max_val.

        Parameters
        ----------
        value : float
            Widget's internal value in 0..1

        Returns
        -------
            Widget's external value in min_val..max_val, snapped to snap_val
        """
        # map [0, 1] to [min_val, max_val] with snap
        interp_value = float(self.min_val + (self.range * value))
        return int(interp_value / self.snap_value + 0.5) * self.snap_value

    def normalize_adjusted_value(self, adjusted_value) -> float:
        """ Normalize a value in min_val..max_val to 0..1

        Parameters
        ----------
        value : float
            Widget's external value in min_val..max_val

        Returns
        -------
            Widget's internal value in 0..1
        """
        # map [min_val, max_val] to [0, 1]
        return (adjusted_value - self.min_val) / self.range

    def value_str(self) -> str:
        """ The display version of the widget's external value.

        Returns
        -------
        str
            The string version of self.adjusted_value, which is the value
            the widget represents to the outside world.
        """
        return snapped_value_string(self.adjusted_value, self.snap_value)

    def on_move(self, touch):
        """ Controls MAY call their function on the move event.

        If the widget was determined to be dynamic, the function is called
        on each move event with a value update.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for controls
        """
        if self.dynamic is True and self.function is not None:
            return self.function(self, self.adjusted_value)

    def adjust(self, direction):
        """ Adjust the control up or down based on sign(direction)
        """
        step = math.copysign(self.snap_value, direction)
        value = self.adjusted_value + step
        if value < self.min_val:
            value = self.min_val
        elif value > self.max_val:
            value = self.max_val
        self.adjusted_value = value
        self.value = self.normalize_adjusted_value(value)

        if self.function is not None:
            return self.function(self, self.adjusted_value)

    def on_release(self, touch):
        """ Controls call their function on the release event.

        It has already been determined that the touch is inside the
        widget via `touch_inside()`.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for controls
        """
        self.release()

    def release(self):
        """ Trigger the button, calling its function if specified with
        the adjusted value.
        """
        if self.function is not None:
            return self.function(self, self.adjusted_value)
