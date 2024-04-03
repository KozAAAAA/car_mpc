import pygame
import numpy as np


class CarVis:
    BACKGROUND_COLOR = (255, 255, 255)
    CAR_COLOR = (255, 0, 0)
    CAR_SIZE = (50, 20)

    def __init__(self, setpoint, t_step, window_size):
        self._setpoint = setpoint
        self._t_step = t_step
        self._win = pygame.display.set_mode(window_size)
        self._car = pygame.Surface(CarVis.CAR_SIZE, pygame.SRCALPHA)
        pygame.init()

    def __del__(self):
        pygame.quit()

    def make_step(self, x0):
        x_pos, y_pos, theta, delta = x0
        pygame.time.delay(self._t_step)
        self._win.fill(CarVis.BACKGROUND_COLOR)
        self._car.fill(CarVis.CAR_COLOR)
         
        theta_deg = np.rad2deg(theta)
        car, rect = self._rotate(self._car, theta_deg, (x_pos, y_pos), pygame.Vector2(CarVis.CAR_SIZE[0]/2, 0))
        # car = self.car
        self._win.blit(car, rect)
        pygame.display.update()

    def _rotate(self, surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        return rotated_image, rect


def main():
    x_pos = 0
    y_pos = 0
    theta = 12
    delta = 12

    car = CarVis(0, 1, (1000, 1000))
    for i in range(10000):
        # x_pos += 1
        theta += 0.01
        car.make_step([x_pos, y_pos, theta, delta])


if __name__ == "__main__":
    main()
