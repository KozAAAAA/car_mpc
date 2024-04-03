import pygame
import numpy as np


class CarVis:
    BACKGROUND_COLOR = (255, 255, 255)
    CAR_COLOR = (255, 0, 0)
    WHEEL_COLOR = (0, 0, 0)
    SETPOINT_COLOR = (0, 0, 255)

    CAR_SIZE = (50, 30)
    SETPOINT_SIZE = (50, 10)
    WHEEL_SIZE = (CAR_SIZE[0] // 4, CAR_SIZE[1] // 4)
    WHEEL_OFFSET = WHEEL_SIZE[0] * 1

    L = CAR_SIZE[0] - WHEEL_OFFSET * 2

    def __init__(self, setpoint, t_step, window_size):
        self._setpoint_pos = setpoint
        self._t_step = t_step
        self._win = pygame.display.set_mode(window_size)
        self._car = pygame.Surface(CarVis.CAR_SIZE, pygame.SRCALPHA)
        self._wheel = pygame.Surface(CarVis.WHEEL_SIZE, pygame.SRCALPHA)
        self._setpoint = pygame.Surface(CarVis.SETPOINT_SIZE, pygame.SRCALPHA)

        pygame.init()

    def __del__(self):
        pygame.quit()

    def make_step(self, x0):
        x, y, theta, delta = x0
        theta_deg = np.rad2deg(theta)
        delta_deg = np.rad2deg(delta)

        pygame.time.delay(self._t_step)

        self._win.fill(CarVis.BACKGROUND_COLOR)

        car, car_rect = self._draw_car(x, y, theta_deg, delta_deg)
        setpoint, setpoint_rect = self._draw_setpoint(*self._setpoint_pos)

        self._win.blit(car, car_rect)
        self._win.blit(setpoint, setpoint_rect)
        pygame.display.update()

    def _draw_car(self, x, y, theta_deg, delta_deg):
        self._car.fill(CarVis.CAR_COLOR)
        self._wheel.fill(CarVis.WHEEL_COLOR)
        self._car.blit(
            self._wheel,
            self._wheel.get_rect(center=(CarVis.WHEEL_OFFSET, CarVis.CAR_SIZE[1] // 2)),
        )
        rotated_wheel = pygame.transform.rotate(self._wheel, -delta_deg)
        self._car.blit(
            rotated_wheel,
            rotated_wheel.get_rect(
                center=(
                    CarVis.CAR_SIZE[0] - CarVis.WHEEL_OFFSET,
                    CarVis.CAR_SIZE[1] // 2,
                )
            ),
        )
        car, rect = self._rotate(
            self._car,
            theta_deg,
            (x, y),
            pygame.Vector2(CarVis.CAR_SIZE[0] / 2, 0),
        )
        return car, rect

    def _draw_setpoint(self, x, y, theta_deg):
        self._setpoint.fill(CarVis.SETPOINT_COLOR)
        setpoint = pygame.transform.rotate(self._setpoint, -theta_deg)
        return setpoint, setpoint.get_rect(center=(x, y))

    def _rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        return rotated_image, rect