import seaborn as sns
import json
import hashlib
import os

from PIL import Image, ImageChops

PALETTE_NAME_LOC = "./res/palette_names.json"
MOUTH_PATH = "./res/mouth"
EYES_PATH = "./res/eyes"
OUT_PATH = "out"
VALID_IDENTICON_SIZES = [8, 16, 32, 64, 128, 256, 512]
NUM_MOUTHS = 9
NUM_EYES = 10


class IdenticonGenerator:
    def __init__(self, name):
        hashed = hashlib.sha256(name.encode())
        self.name = name
        self.seed = int(hashed.hexdigest(), 16)
        self.palette = self.get_palette()

    def __str__(self) -> str:
        palette = [f"rgb({color[0]},{color[1]},{color[2]})" for color in self.palette]
        return f"""
name    | {self.name}
seed    | {self.seed}
palette | [{', '.join(palette)}]
"""

    def get_palette(self, n_colors=3):
        """
        Select a color palette based on a provided seed, picked from
        https://www.practicalpythonfordatascience.com/ap_seaborn_palette#all-palettes
        """
        file = open(PALETTE_NAME_LOC, 'r')
        json_string = '\n'.join(open(PALETTE_NAME_LOC, 'r').readlines())
        palette_names = json.loads(json_string)
        file.close()

        palette_name = palette_names[self.seed % len(palette_names)]
        palette = sns.color_palette(palette=palette_name, n_colors=n_colors)
        for i, (r, g, b) in enumerate(palette):
            palette[i] = (int(255 * r), int(255 * g), int(255 * b))

        return palette

    def get_mouth(self):
        mouth_path = f"{MOUTH_PATH}/{(self.seed % NUM_MOUTHS)}.bmp"
        return Image.open(mouth_path)

    def get_eyes(self):
        eyes_path = f"{EYES_PATH}/{(self.seed % NUM_EYES)}.bmp"
        return Image.open(eyes_path)

    def generate(self):
        mouth, eyes, palette = self.get_mouth(), self.get_eyes(), self.get_palette()

        face_grayscale = ImageChops.darker(mouth, eyes)
        face_rgb = Image.new("RGB", face_grayscale.size)
        face_rgb.paste(face_grayscale)

        pixels = face_rgb.load()
        for i in range(face_rgb.size[0]):
            for j in range(face_rgb.size[1]):
                if pixels[i, j] == (0, 0, 0):
                    # black pixel remapping
                    pixels[i, j] = palette[0]
                else:
                    # white pixel remapping
                    pixels[i, j] = palette[1]
                if i == 0 or j == 0 or i == face_rgb.size[0] - 1 or j == face_rgb.size[1] - 1:
                    # border pixel remapping
                    pixels[i, j] = palette[2]

        # lazily produce samples for all reasonable sizes to ./out/{name}/*.bmp
        dir_out = f"{OUT_PATH}/{self.name}"
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)
        for size in VALID_IDENTICON_SIZES:
            face_rgb.resize((size, size), resample=Image.BOX).save(f"{dir_out}/{size}x{size}.bmp")


if __name__ == '__main__':
    # example generation for "Gunnar"
    IdenticonGenerator('Gunnar').generate()

    # lazily-named generations referenced in README.md
    for i in range(16):
        IdenticonGenerator(f'{i}').generate()
