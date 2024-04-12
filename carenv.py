"""Module for visualizing the car and the setpoint."""

import os

import pygame
import numpy as np
from PIL import Image
from IPython.display import display


class Car(pygame.sprite.Sprite):
    """Sprite for the car object."""

    WIDTH_MULTIPLIER = 1.2
    WHEEL_OFFSET_MULTIPLIER = 0.6

    WHEEL_WIDTH_MULTIPLIER = 0.3
    WHEEL_HEIGHT_MULTIPLIER = 0.6

    DOT_MULTIPLIER = 0.25

    CAR_COLOR = (255, 0, 0)
    WHEEL_COLOR = (0, 0, 0)
    DOT_COLOR = (255, 255, 255)

    def __init__(self, L: int):
        """Initialize the car sprite."""
        super().__init__()

        self.L = L

        self.offset = pygame.Vector2((self.L // 2, 0))
        self.pos = pygame.Vector2((0, 0))
        self.theta = 0
        self.delta = 0

        self.wheel_offset = int(Car.WHEEL_OFFSET_MULTIPLIER * self.L)
        self.width = int(Car.WIDTH_MULTIPLIER * self.L)
        self.height = int(self.wheel_offset * 2 + self.L)
        self.wheel_width = int(Car.WHEEL_WIDTH_MULTIPLIER * self.L)
        self.wheel_height = int(Car.WHEEL_HEIGHT_MULTIPLIER * self.L)
        self.dot_size = int(Car.DOT_MULTIPLIER * self.wheel_width)

        self.base_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.wheel = pygame.Surface(
            (self.wheel_width, self.wheel_height), pygame.SRCALPHA
        )

        self.base_image.fill(Car.CAR_COLOR)
        self.wheel.fill(Car.WHEEL_COLOR)

        pygame.draw.circle(
            self.wheel,
            Car.DOT_COLOR,
            (self.wheel_width // 2, self.wheel_height // 2),
            self.dot_size,
        )

        self.base_image.blit(
            self.wheel, self.wheel.get_rect(center=(self.width // 2, self.wheel_offset))
        )

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

    def update(self, x: int, y: int, theta: float, delta: float):
        """
        Update the position and orientation of the car.
        theta and delta are in degrees.
        """
        self.pos = pygame.Vector2((x, y))
        self.theta = theta
        self.delta = delta

        self.image = self.base_image.copy()

        self._rotate_front_wheel()
        self._rotate()

    def _rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        self.image = pygame.transform.rotozoom(self.image, 90 - self.theta, 1)
        offset_rotated = self.offset.rotate(self.theta)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def _rotate_front_wheel(self):
        """Rotate the front wheel of the car."""
        rotated_wheel = pygame.transform.rotate(self.wheel, -self.delta)
        self.image.blit(
            rotated_wheel,
            rotated_wheel.get_rect(
                center=(self.width // 2, self.wheel_offset + self.L)
            ),
        )


class Setpoint(pygame.sprite.Sprite):
    """Sprite for the setpoint object."""

    BACKGROUND_COLOR = (0, 255, 0, 80)
    DOT_AND_LINE_COLOR = (0, 150, 0)

    def __init__(
        self,
        car_width: int,
        car_wheel_offset: int,
        car_dot_size: int,
        x: int,
        y: int,
        theta: float,
    ):
        """Initialize the setpoint sprite."""
        super().__init__()

        self.width = car_width
        self.height = car_wheel_offset * 2
        self.dot_size = car_dot_size
        self.pos = pygame.Vector2((x, y))
        self.theta = theta

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(Setpoint.BACKGROUND_COLOR)
        pygame.draw.circle(
            self.image,
            Setpoint.DOT_AND_LINE_COLOR,
            (self.width // 2, self.height // 2),
            self.dot_size,
        )
        pygame.draw.line(
            self.image, Setpoint.DOT_AND_LINE_COLOR, (0, 0), (self.width, 0), 5
        )

        self.image = pygame.transform.rotate(self.image, 90 - self.theta)
        self.rect = self.image.get_rect(center=self.pos)


class CarEnv:
    """Environment for visualizing the car and the setpoint."""

    ENVIROMENT_COLOR = (245, 245, 245)

    def __init__(
        self,
        L: int,
        setpoint: np.ndarray,
        env_size: tuple,
        t_step: float,
        notebook: bool = False,
    ):
        """Initialize the environment."""
        self.t_step = t_step
        self.notebook = notebook
        x, y, theta, _ = setpoint
        self.car = Car(L=L)
        self.setpoint = Setpoint(
            car_width=self.car.width,
            car_wheel_offset=self.car.wheel_offset,
            car_dot_size=self.car.dot_size,
            x=x,
            y=y,
            theta=np.rad2deg(theta),
        )
        if self.notebook:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        else:
            os.environ["SDL_VIDEODRIVER"] = "x11"

        pygame.init()
        self.screen = pygame.display.set_mode(env_size)
        self.clock = pygame.time.Clock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def make_step(self, x0: np.ndarray):
        """Perform a single step of visualization."""
        try:
            x, y, theta, delta = x0
            self.screen.fill(CarEnv.ENVIROMENT_COLOR)
            self.car.update(x, y, np.rad2deg(theta), np.rad2deg(delta))
            self.screen.blit(self.car.image, self.car.rect)
            self.screen.blit(self.setpoint.image, self.setpoint.rect)
            pygame.display.update()
            self.clock.tick(1 / self.t_step)

            if self.notebook:
                view = pygame.surfarray.array3d(self.screen).transpose(1, 0, 2)
                display(Image.fromarray(view), clear=True)


        except KeyboardInterrupt:
            self.close()

    def close(self):
        """Close the visualization window."""
        pygame.quit()