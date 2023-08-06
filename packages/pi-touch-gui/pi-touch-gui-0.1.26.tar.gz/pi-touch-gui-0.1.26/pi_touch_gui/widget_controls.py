# Copyright (c) 2020 Edwin Wise
# MIT License
# See LICENSE for details
"""
    Controls are widgets that are manipulated and return a value. They may
    update their function on move and release.
"""
import logging
import math

import pygame
from custom_inherit import doc_inherit

from pi_touch_gui._widget_bases import IControlWidget

LOG = logging.getLogger(__name__)


class Dial(IControlWidget):
    """ Circular input control dial.
    """

    @doc_inherit(IControlWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size, **kwargs):
        """ Initialize the dial.
        """
        # Dials don't use label, so block it
        if kwargs.get('label') is not None:
            raise ValueError("Dials don't use their value as the label.")

        diameter = min(size[0], size[1])
        radius = diameter >> 1
        kw_font_size = kwargs.pop('font_size', None)
        font_size = (radius >> 1) if kw_font_size is None else kw_font_size

        # The parent init sets convenience properties like self.x, etc
        super(Dial, self).__init__(position, (diameter, diameter),
                                   font_size=font_size,
                                   **kwargs)
        self.radius = radius
        self.cx, self.cy = (self.x + self.w // 2), (self.y + self.h // 2)

    def touch_inside(self, touch):
        """ The interior of the dial is determined by a circle.
        """
        x, y = touch.position
        distance = math.hypot(x - self.cx, y - self.cy)
        if distance <= self.radius:
            return True

        return False

    def on_move(self, touch):
        # If too many touches, we bail
        if len(self.touches) > 1:
            return

        dx = touch.x - self.cx
        dy = touch.y - self.cy

        # Value is from 0.0 to 1.0 (percent of range)
        self.value = (math.atan2(dy, dx) % math.tau) / math.tau
        self.adjusted_value = self.map_value_to_adjusted_value(self.value)

        super(Dial, self).on_move(touch)

    def render(self, surface):
        wedge_rect = (self.x, self.y, self.w, self.h)
        handle_pos = (
            int(self.cx + (self.radius * math.cos(self.value * math.tau))),
            int(self.cy + (self.radius * math.sin(self.value * math.tau))))

        center = (self.cx, self.cy)
        # Draw the filled overall dial
        pygame.draw.circle(surface, self.color1, center, self.radius, 0)
        # Draw the active pie-wedge
        pygame.draw.arc(surface, self.color2, wedge_rect,
                        -self.value * math.tau, 0.0,
                        int(self.radius * 0.5))
        # Draw the handle line
        pygame.draw.line(surface, self.label_color1, center, handle_pos,
                         3)
        # Draw the handle circle
        pygame.draw.circle(surface, self.label_color1, handle_pos,
                           int(self.radius * 0.1), 0)

        self.render_centered_text(surface, self.value_str(),
                                  self.label_color1, self.color1)

        if self._focus:
            self.render_focus(surface)


class Slider(IControlWidget):
    """ Variable value input linear slider
    """

    @doc_inherit(IControlWidget.__init__, style='numpy_with_merge')
    def __init__(self, position, size, **kwargs):
        """ Initialize the slider.

        color1 is the slider background fill
        color2 is the slider outline and active value fill
        label_color1 is the slider line (and label)
        """
        # Sliders don't use label, so block it
        if kwargs.get('label') is not None:
            raise ValueError("Dials don't use their value as the label.")

        super(Slider, self).__init__(position, size, **kwargs)

    def on_move(self, touch):
        # If too many touches, bail
        if len(self.touches) > 1:
            return

        x, y = touch.position

        # Compute X/Y relative to the slider
        x -= self.x
        y -= self.y

        # Check our ratios...
        if self.w > self.h:
            # Horizontal Slider
            if 0 <= x <= self.w:
                self.value = float(x) / float(self.w)

        elif self.h > self.w:
            # Vertical Slider
            if 0 <= y <= self.h:
                self.value = (self.h - float(y)) / float(self.h)

        self.adjusted_value = self.map_value_to_adjusted_value(self.value)

        super(Slider, self).on_move(touch)

    def render(self, surface):
        pygame.draw.rect(surface, self.color1, (self.position, self.size), 0)

        if self.w > self.h:
            # Horizontal slider
            value_w = int(self.w * self.value)
            value_x = self.x + value_w
            pygame.draw.rect(surface, self.color2,
                             ((self.x, self.y), (value_w, self.h)))
            pygame.draw.line(surface, self.label_color1,
                             (value_x, self.y), (value_x, self.y + self.h),
                             3)

        elif self.h > self.w:
            # Vertical slider
            value_h = int(self.h * self.value)
            value_y = self.y + (self.h - value_h)
            pygame.draw.rect(surface, self.color2,
                             ((self.x, value_y), (self.w, value_h)))
            pygame.draw.line(surface, self.label_color1,
                             (self.x, value_y), (self.x + self.w, value_y),
                             3)

        pygame.draw.rect(surface, self.color2, (self.position, self.size),
                         3)

        self.render_centered_text(surface, self.value_str(), self.label_color1)

        if self._focus:
            self.render_focus(surface)
