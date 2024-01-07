import pygame
import sys

from gui import COLOR_BLUE, COLOR_RED, COLOR_WHITE, Canvas, Column, Insets, LayoutHints, Row, Widget

def main():

    pygame.init()

    screen_width = 2256
    screen_height = 1504
    background_color = (0,0,0)

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, vsync=1)
    screen_info = pygame.display.Info()
    w, h = screen_info.current_w, screen_info.current_h

    canvas = Canvas(0, 0, w, h,
                        root_widget=Column(children=[
                            Widget(height=64, border_color=COLOR_WHITE, border_width=2, border_radius=4),
                            Row(gap=8, layout_hints=LayoutHints(flex=1), children=[
                                Widget(layout_hints=LayoutHints(flex=2), border_color=COLOR_WHITE, border_width=2, border_radius=4),
                                Widget(layout_hints=LayoutHints(flex=3), border_color=COLOR_WHITE, border_width=2, border_radius=4)
                            ]),
                            Widget(height=64, border_color=COLOR_WHITE, border_width=2, border_radius=4)
                        ],
                        padding=Insets(16, 16, 16, 16),
                        gap=8))

    def draw_scene():
        screen.fill(background_color)
        canvas.render(screen)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        draw_scene()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

main()