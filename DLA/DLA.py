#!/usr/bin/env -S uv run --script
#
import argparse
import random
import sys
from pathlib import Path

from image import Image, rgba


class DLA:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.sim_data = Image(self.width, self.height, (255, 255, 255, 255))
        self.output_image = Image(self.width, self.height, (128, 128, 128, 255))

    def save_image(self, fname: str) -> None:
        self.output_image.save(fname)

    def random_seed(self) -> None:
        """
        place a random seed inside the boundary with a=0
        """
        x = random.randint(1, self.width - 1)
        y = random.randint(1, self.height - 1)
        self.sim_data.set_pixel(x, y, (255, 255, 255, 0))
        self.output_image.set_pixel(x, y, (0, 255, 0, 255))  # seeds are now green

    def set_seed(self, x: int, y: int) -> None:
        self.sim_data.set_pixel(x, y, (255, 255, 255, 0))
        self.output_image.set_pixel(x, y, (0, 255, 0, 255))  # seeds are now green

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
                        pixel_colour = self.sim_data.get_pixel(x + x_offset, y + y_offset)
                        if pixel_colour[3] == 0:
                            print("Found Seed")
                            self.sim_data.set_pixel(x, y, (255, 0, 0, 0))
                            self.output_image.set_pixel(x, y, (0, 0, 255, 255))
                            found = True
                            walking = False
                            break

        # 2 to move we just got -1 0 1
        # 3 get pixel at x,y does it have alpha 0 if so place and return else continue
        return found


def main(output_dir: str, file_name: str, width: int, height: int):
    sim = DLA(args.width, args.height)
    # for _ in range(20):
    #     sim.random_seed()
    for x in range(width):
        sim.set_seed(x, height // 2)
    frame_number = 0
    found_count = 0
    for _ in range(10000):
        if sim.walk():
            print("Found a seed")
            found_count += 1
            if found_count % 10 == 0:
                file = Path(output_dir) / f"{file_name}.{frame_number:04}.png"
                sim.save_image(file)
                frame_number += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple DLA Simulation")
    parser.add_argument("-o", "--output", type=str, default="./", help="output dir defaults to current")
    parser.add_argument("-n", "--name", type=str, default="Sim", help="output name for file")
    parser.add_argument("-ht", "--height", type=int, default=400, help="height of sim")
    parser.add_argument("-w", "--width", type=int, default=400, help="height of sim")

    args = parser.parse_args()
    Path(args.output).mkdir(parents=True, exist_ok=True)
    main(args.output, args.name, args.width, args.height)
