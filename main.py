
import pygame
import numpy as np

from transformations import (
    translation, scaling,
    rotation_x, rotation_y, rotation_z,
    transform_points
)

from projection import (
    orthographic_projection,
    perspective_projection
)

pygame.init()

WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Transformation & Projection Simulator")

clock = pygame.time.Clock()

WHITE = (245, 247, 250)
BLACK = (25, 30, 40)
BLUE = (40, 120, 230)
RED = (230, 65, 65)
GRAY = (190, 195, 205)
GREEN = (30, 160, 100)

font = pygame.font.SysFont("Arial", 21)
small_font = pygame.font.SysFont("Arial", 16)

# 3D cube vertices
vertices = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
], dtype=float)

# Cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Transformation settings
tx, ty, tz = 0, 0, 0
rx, ry, rz = 20, 25, 0
sx, sy, sz = 1, 1, 1

projection_mode = "Perspective"


def make_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, BLUE, rect, border_radius=7)
    pygame.draw.rect(screen, BLACK, rect, 1, border_radius=7)

    label = small_font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))

    return rect


def draw_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def get_transformed_cube():
    # Composite transformation matrix
    matrix = (
        translation(tx, ty, tz)
        @ rotation_z(rz)
        @ rotation_y(ry)
        @ rotation_x(rx)
        @ scaling(sx, sy, sz)
    )

    return transform_points(vertices, matrix)


def draw_cube():
    transformed = get_transformed_cube()

    if projection_mode == "Perspective":
        projected = perspective_projection(
            transformed, WIDTH, HEIGHT
        )
    else:
        projected = orthographic_projection(
            transformed, WIDTH, HEIGHT
        )

    for start, end in edges:
        p1 = projected[start]
        p2 = projected[end]

        if p1 is not None and p2 is not None:
            pygame.draw.line(screen, BLUE, p1, p2, 4)

    for point in projected:
        if point is not None:
            pygame.draw.circle(screen, RED, point, 5)


def draw_interface():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT))

    pygame.draw.rect(screen, (225, 232, 242),
                     (0, 0, WIDTH, 55))

    draw_text("3D TRANSFORMATION & PROJECTION SIMULATOR",
              20, 15)

    # Information panel
    pygame.draw.rect(screen, (230, 235, 243),
                     (15, 80, 310, 420), border_radius=10)

    draw_text("TRANSFORMATION VALUES", 30, 95)

    values = [
        f"Translation: {tx}, {ty}, {tz}",
        f"Rotation X: {rx} degrees",
        f"Rotation Y: {ry} degrees",
        f"Rotation Z: {rz} degrees",
        f"Scaling: {sx:.2f}, {sy:.2f}, {sz:.2f}",
        f"Projection: {projection_mode}"
    ]

    for i, value in enumerate(values):
        screen.blit(
            small_font.render(value, True, BLACK),
            (30, 145 + i * 42)
        )

    # Projection buttons
    draw_text("PROJECTION MODE", 30, 525)

    ortho_button = make_button(
        "Orthographic", 30, 565, 125, 40
    )

    perspective_button = make_button(
        "Perspective", 170, 565, 125, 40
    )

    # Reset button
    reset_button = make_button(
        "RESET OBJECT", 30, 620, 265, 42
    )

    # Instructions
    draw_text("KEYBOARD CONTROLS", 680, 565)

    instructions = [
        "Arrow Keys: Rotate X / Y",
        "Q / E: Rotate Z",
        "W / S: Move Z",
        "A / D: Move X",
        "I / K: Move Y",
        "+ / -: Scale",
        "ESC: Exit"
    ]

    for i, instruction in enumerate(instructions):
        screen.blit(
            small_font.render(instruction, True, BLACK),
            (680, 600 + i * 20)
        )

    return ortho_button, perspective_button, reset_button


def reset():
    global tx, ty, tz, rx, ry, rz, sx, sy, sz

    tx, ty, tz = 0, 0, 0
    rx, ry, rz = 20, 25, 0
    sx, sy, sz = 1, 1, 1


running = True

while running:
    ortho_button, perspective_button, reset_button = draw_interface()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if ortho_button.collidepoint(event.pos):
                projection_mode = "Orthographic"

            elif perspective_button.collidepoint(event.pos):
                projection_mode = "Perspective"

            elif reset_button.collidepoint(event.pos):
                reset()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_LEFT:
                ry -= 5
            elif event.key == pygame.K_RIGHT:
                ry += 5
            elif event.key == pygame.K_UP:
                rx -= 5
            elif event.key == pygame.K_DOWN:
                rx += 5

            elif event.key == pygame.K_q:
                rz -= 5
            elif event.key == pygame.K_e:
                rz += 5

            elif event.key == pygame.K_w:
                tz += 0.2
            elif event.key == pygame.K_s:
                tz -= 0.2

            elif event.key == pygame.K_a:
                tx -= 0.2
            elif event.key == pygame.K_d:
                tx += 0.2

            elif event.key == pygame.K_i:
                ty += 0.2
            elif event.key == pygame.K_k:
                ty -= 0.2

            elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                sx *= 1.1
                sy *= 1.1
                sz *= 1.1

            elif event.key == pygame.K_MINUS:
                sx *= 0.9
                sy *= 0.9
                sz *= 0.9

    draw_cube()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
