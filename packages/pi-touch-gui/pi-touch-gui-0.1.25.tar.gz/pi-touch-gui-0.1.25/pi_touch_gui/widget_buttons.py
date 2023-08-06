# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Buttons are widgets that are pressed. They typically update their function
    on release, and the contents can be as simple as a label and as complex
    as a multivalued graph.
"""
import logging
import uuid
from typing import Tuple, Optional

import pygame
from custom_inherit import doc_inherit

from pi_touch_gui._widget_bases import (IButtonWidget,
                                        IWidgetInterface)

LOG = logging.getLogger(__name__)


class Button(IButtonWidget):
    """ A simple rectangular button that calls its function on release.

    It is an empty instantiation of IButtonWidget.
    """
    # Button style
    RECTANGLE = 0
    LEFT_ROUND = 1
    RIGHT_ROUND = 2
    OBROUND = 3

    # Button behavior
    CLICK = 0
    HOLD = 1
    TOGGLE = 2

    @doc_inherit(IButtonWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size,
                 style=None,
                 behavior=None,
                 **kwargs):
        """ Initialize the Button.

        Parameters
        ----------
        style : Int
            The style in which the button is rendered (Button.RECTANGLE is the
            default, but you can also specify LEFT_ROUND, RIGHT_ROUND, or both
            with OBROUND)
        behavior : Int
            The behavior of the button (Button.CLICK is the default, activating
            on release, but you can specify HOLD which activates on press
            and stops on release, or TOGGLE which turns on and off on each
            release).
        """
        super(Button, self).__init__(position, size, **kwargs)
        self.style = Button.RECTANGLE if style is None else style
        self.behavior = Button.CLICK if behavior is None else behavior
        self.active = False

    @doc_inherit(IButtonWidget.render, style='numpy_with_merge')
    def render(self, surface):
        """ Render the button.

        Complicated by the need for one or two rounded ends.  If you play
        your parameters right, you get a circle!
        """
        color, label_color = self.state_colors(self.active)

        radius = int(self.h / 2)
        inset_x = radius if self.style & self.LEFT_ROUND else 0
        inset_w = radius if self.style & self.RIGHT_ROUND else 0
        inset_w = inset_w + inset_x
        subrect = ((self.x + inset_x, self.y),
                   (self.w - inset_w, self.h))
        pygame.draw.rect(surface, color, subrect, 0)
        if self.style & self.LEFT_ROUND:
            pygame.draw.circle(surface, color,
                               (self.x + radius, self.y + radius),
                               radius)
        if self.style & self.RIGHT_ROUND:
            pygame.draw.circle(surface, color,
                               (self.x + self.w - radius, self.y + radius),
                               radius)

        self.render_centered_text(surface, self.label, label_color, color)

        if self._focus:
            self.render_focus(surface)

    def set(self):
        print(f"### BUTTON SET")
        if self.behavior == Button.TOGGLE:
            self.active = True
            if self.function:
                return self.function(self, self.active)

    def clear(self):
        print(f"### BUTTON CLEAR")
        if self.behavior == Button.TOGGLE:
            self.active = False
            if self.function:
                return self.function(self, self.active)

    def on_press(self, touch) -> None:
        """ Hold behavior calls their function on the press event.

        Parameters
        ----------
        touch : Touch
            Touch object; generally not used for buttons
        """
        self.press()

    def press(self):
        print(f"### BUTTON PRESS")
        if self.behavior == self.HOLD:
            self.active = True
            if self.function:
                self.function(self, self.active)
        super(Button, self).press()

    def on_release(self, touch):
        return self.release()

    def release(self):
        print(f"### BUTTON RELEASE")
        if self.behavior == self.TOGGLE:
            self.active = not self.active
            print(f"### ... TOGGLE {self.label} TO {self.active}")
        else:
            self.active = False
        self._pressed = False
        if self.function:
            return self.function(self, self.active)


class ButtonGroup(IWidgetInterface):
    """ A group of ToggleButton where zero or one may be active.

    When a button is made active, all the remaining are
    forced to be inactive.

    It is possible for none of the buttons to be active, if you
    de-activate the active button.

    Starts with the first button in the list active.
    """

    @doc_inherit(IWidgetInterface.__init__, style='numpy_with_merge')
    def __init__(self, toggle_buttons, widget_id=None):
        """ Initialize the button group, and hook the button functions.

        Parameters
        ----------
        toggle_buttons : List[ToggleButton]
            An ordered list of ToggleButton objects, where the first button
            is active on startup.
        widget_id : str
            Optional ID for this group, if not given, gets a random uuid.
        """
        self.label = 'group'
        self._id = str(uuid.uuid4()) if widget_id is None else widget_id
        self._neighbors = [None, None, None, None]

        self._widgets = list()
        for idx, button in enumerate(toggle_buttons):
            if not isinstance(button, Button):
                raise ValueError(f"Item {idx} {type(button)!r} "
                                 f"is not a Button")
            if button.behavior != Button.TOGGLE:
                raise ValueError(f"Button {idx} is not a TOGGLE")

            # Insert the group control method into the button
            old_function = button.function
            button.function = self.group_function
            self._widgets.append((button, old_function))

    @property
    def neighbors(self):
        return self._neighbors

    def group_function(self, button, state):
        """ Enforce the group behavior; one button on, all others off.

        Parameters
        ----------
        button : ToggleButton
            The button that is receiving the event
        state : bool
            The state being sent to the button

        Returns
        -------
        Optional['Page']
            Returns whatever the button's function returns.  The disabled
            button results are ignored.
        """
        # If we are enabling this button, disable all other buttons
        for b, f in self._widgets:
            if b.id != button.id:
                b.active = False
                if f:
                    f(b, False)

        # Now the actual button press
        f = next(f for b, f in self._widgets if b.id == button.id)
        if f:
            return f(button, state)
        return None

    @property
    def id(self):
        return self._id

    def event(self, event, touch) -> Tuple[bool, Optional['Page']]:
        for button, _ in self._widgets:
            consumed, new_page = button.event(event, touch)
            if consumed:
                return True, new_page
        return False, None

    def can_focus(self) -> bool:
        return False

    def render(self, surface):
        for button, _ in self._widgets:
            button.render(surface)

    def render_focus(self, surface):
        pass
