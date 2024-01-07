import typing

from pygame import Surface
import pygame


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Dimension:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Insets:

    def __init__(self, top=0, right=0, bottom=0, left=0):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class Color:
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


COLOR_BLACK = Color(0,0,0)
COLOR_WHITE = Color(255,255,255)
COLOR_RED = Color(255,0,0)
COLOR_GREEN = Color(0,255,0)
COLOR_BLUE = Color(0,0,255)
COLOR_YELLOW = Color(255,255,0)
COLOR_MAGENTA = Color(255,0,255)
COLOR_TEAL = Color(0,255,255)


class LayoutHints:
    flex: int = 0

    def __init__(self, flex: int = 0):
        self.flex = flex


class Widget:

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 width: int = 0,
                 height: int = 0,
                 background_color: Color = None,
                 border_color: Color = None,
                 border_width: int = 0,
                 border_radius: int = 0,
                 layout_hints: LayoutHints = LayoutHints()):
        self.position = Point(x,y)
        self.size = Dimension(width, height)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.layout_hints = layout_hints

    def render(self, surface: Surface):
         # Draw border only if border_color and border_width are set
        if self.border_width > 0 and self.border_color:
            pygame.draw.rect(
                surface, 
                (self.border_color.r, self.border_color.g, self.border_color.b),
                (self.position.x, self.position.y, self.size.width, self.size.height),
                width=self.border_width, border_radius=self.border_radius
            )

        # Draw background only if background_color is set
        if self.background_color:
            inner_rect = (
                self.position.x + self.border_width, 
                self.position.y + self.border_width, 
                self.size.width - 2 * self.border_width, 
                self.size.height - 2 * self.border_width
            )
            pygame.draw.rect(
                surface, 
                (self.background_color.r, self.background_color.g, self.background_color.b),
                inner_rect, 
                border_radius=self.border_radius
            )


class Container(Widget):

    children: list[Widget] = []
    padding: Insets = Insets()

    def __init__(self,
                 children: list[Widget] = [],
                 padding: Insets = Insets(),
                 layout_hints: LayoutHints = LayoutHints()):
        super().__init__(layout_hints=layout_hints)
        self.children = children
        self.padding = padding

    def add_child(self, child: Widget):
        self.children.append(child)

    def remove_child(self, child: Widget):
        self.children = [c for c in self.children if c is not child]

    def render(self, surface: Surface):
        super().render(surface)
        self.layout_children()
        for child in self.children:
            child.render(surface)

    def layout_children(self):
        pass

    def get_usable_space(self) -> Dimension:
        usable_width = self.size.width - self.padding.left - self.padding.right
        usable_height = self.size.height - self.padding.top - self.padding.bottom
        return Dimension(usable_width, usable_height)


class Column(Container):

    def __init__(self,
                 children: list[Widget] = [],
                 padding: Insets = Insets(),
                 gap: int = 0,
                 layout_hints: LayoutHints = LayoutHints()):
        super().__init__(children=children, padding=padding, layout_hints=layout_hints)
        self.gap = gap

    def layout_children(self):
        flex_children = [c for c in self.children if c.layout_hints.flex > 0]
        fixed_children = [c for c in self.children if c.layout_hints.flex == 0]

        fixed_children_height = max(0, sum([c.size.height for c in fixed_children]) + (len(fixed_children) - 1) * self.gap)
        total_flex_space = self.get_usable_space().height - fixed_children_height - (len(flex_children) - 1) * self.gap
        total_flex_factor = sum([c.layout_hints.flex for c in flex_children])

        current_y = self.position.y + self.padding.top
        for child in self.children:
            child.size.width = self.get_usable_space().width
            if child.layout_hints.flex > 0:
                flex_factor = child.layout_hints.flex
                child.size.height = flex_factor / total_flex_factor * total_flex_space
            child.position.x = self.position.x + self.padding.left
            child.position.y = current_y
            current_y += child.size.height + self.gap


class Row(Container):

    def __init__(self,
                 children: list[Widget] = [],
                 padding: Insets = Insets(),
                 gap: int = 0,
                 layout_hints: LayoutHints = LayoutHints()):
        super().__init__(children=children, padding=padding, layout_hints=layout_hints)
        self.gap = gap

    def layout_children(self):
        flex_children = [c for c in self.children if c.layout_hints.flex > 0]
        fixed_children = [c for c in self.children if c.layout_hints.flex == 0]

        fixed_children_width = max(0, sum([c.size.width for c in fixed_children]) + (len(fixed_children) - 1) * self.gap)
        total_flex_space = self.get_usable_space().width - fixed_children_width - (len(flex_children) - 1) * self.gap
        total_flex_factor = sum([c.layout_hints.flex for c in flex_children])

        current_x = self.position.x + self.padding.left
        for child in self.children:
            child.size.height = self.get_usable_space().height
            if child.layout_hints.flex > 0:
                flex_factor = child.layout_hints.flex
                child.size.width = flex_factor / total_flex_factor * total_flex_space
            child.position.x = current_x
            child.position.y = self.position.y + self.padding.top
            current_x += child.size.width + self.gap


class Canvas:

    position: Point = Point(0,0)
    size: Dimension = Dimension(0,0)
    root_widget: Widget = None
    padding: Insets = Insets()

    def __init__(self, x, y, width, height, root_widget: Widget, padding: Insets=Insets()):
        self.position = Point(x,y)
        self.size = Dimension(width, height)
        self.root_widget = root_widget
        self.padding = padding

        self.root_widget.size = self.get_usable_space()

    def get_usable_space(self) -> Dimension:
        usable_width = self.size.width - self.padding.left - self.padding.right
        usable_height = self.size.height - self.padding.top - self.padding.bottom
        return Dimension(usable_width, usable_height)
    
    def render(self, surface: Surface):
        self.root_widget.render(surface)