#!/usr/bin/env -S uv run --script
#
import random

from image import Image, rgba


class DLA:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.image = Image(self.width, self.height)
        self.image.clear((255, 255, 255, 255))

    def save_image(self, fname: str) -> None:
        self.image.save(fname)

    def random_seed(self) -> tuple[int, int]:
        """
        place a random seed inside the boundary with a=0
        """
        x = random.randint(1, self.width - 1)
        y = random.randint(1, self.height - 1)
        self.image.set_pixel(x, y, (255, 255, 255, 0))

    def _random_start(self) -> tuple[int, int]:
        x = random.randint(1, self.width - 1)
        y = random.randint(1, self.height - 1)
        return x, y

    def walk(self) -> bool:
        walking = True
        found = False
        x, y = self._random_start()
        # 1 loop until we either hit an edge or find a seed
        while walking:
            x += random.choice([-1, 0, 1])
            y += random.choice([-1, 0, 1])
            # check bounds and quit if edge is hit
            if x < 1 or x >= self.width - 1 or y < 1 or y >= self.height - 1:
                print("hit edge")
                walking = False
                found = False
                break
            else:  # check for seed
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        pixel_colour = self.image.get_pixel(x + x_offset, y + y_offset)
                        if pixel_colour[3] == 0:
                            print("Found Seed")
                            self.image.set_pixel(x, y, (255, 0, 0, 0))
                            found = True
                            walking = False
                            break

        # 2 to move we just got -1 0 1
        # 3 get pixel at x,y does it have alpha 0 if so place and return else continue
        return found


def main():
    sim = DLA(512, 512)
    for _ in range(20):
        sim.random_seed()

    for _ in range(10000):
        if sim.walk():
            print("Found a seed")
    sim.save_image("test.png")


if __name__ == "__main__":
    main()
