import os
from builtins import range
import tempfile
import math

from PIL import Image, ImageDraw, ImageFont
from skimage import io
from sklearn.cluster import KMeans

import cross_stitch_input as csi
import cross_stitch_parse_input as cspi
import cross_stitch_consts as consts


colors_to_chars = dict()
# TODO: Move chars somewhere else and expand it
chars = ['A', '<', '$', '*', '@', 'B', 'E', 'T', 'U', 'Z', '-', '4', '%', 'C', 'D', 'S', 'V', '+', 'M', 'i']


def reduce_size(in_file, width, out_file):
    image = Image.open(in_file)
    pixel_size = image.size[0] // int(width)
    pattern_width = image.size[0] // pixel_size
    pattern_height = image.size[1] // pixel_size
    print("Pattern width:", pattern_width, ", pattern height:", pattern_height)
    image = image.resize((pattern_width, pattern_height), Image.NEAREST)
    image.save(out_file)


def reduce_colors(in_file, colors, out_file):
    print("Processing", in_file + "...")
    file_handle = io.imread(in_file)
    arr = file_handle.reshape((-1, 3))
    kmeans = KMeans(n_clusters=colors, random_state=42).fit(arr)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # Create a mapping between colors and characters that will
    # be printed into pixels.
    i = 0
    for r, g, b in centers:
        r = int(math.floor(r))
        g = int(math.floor(g))
        b = int(math.floor(b))
        centers[i][0] = r
        centers[i][1] = g
        centers[i][2] = b
        rgb = (r, g, b)
        colors_to_chars[rgb] = chars[i]
        i = i + 1

    reduced_colors = centers[labels].reshape(file_handle.shape).astype('uint8')
    io.imsave(out_file, reduced_colors)


def pixelate(in_file, out_file):
    image = Image.open(in_file)
    pixel_size = 50
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
    pixel = image.load()

    d = ImageDraw.Draw(image)
    fnt = ImageFont.truetype('FreeMono.ttf', 30)

    for i in range(0, image.size[0], pixel_size):
        for j in range(0, image.size[1], pixel_size):
            for r in range(pixel_size):
                # For each 'pixel' draw a character that will make stitching easier.
                d.text((i + 10, j + 10), colors_to_chars[pixel[i + r, j]], font=fnt, fill=(0, 0, 0))
                pixel[i + r, j] = consts.SECONDARY_GRID_COLOR
                pixel[i, j + r] = consts.SECONDARY_GRID_COLOR

    for i in range(0, image.size[0], pixel_size * consts.PRIMARY_GRID_SIZE):
        for j in range(0, image.size[1], pixel_size * consts.PRIMARY_GRID_SIZE):
            for r in range(pixel_size * consts.PRIMARY_GRID_SIZE):
                if (i + r) < image.size[0]:
                    pixel[i + r, j] = consts.PRIMARY_GRID_COLOR
                if (j + r) < image.size[1]:
                    pixel[i, j + r] = consts.PRIMARY_GRID_COLOR

    image.save(out_file)


def main():
    app_args = csi.get_input()
    params = cspi.parse(app_args.file, app_args.width, app_args.colors)
    input_file = params["file"]
    width = params["width"]
    colors = params["colors"]

    # Use PNG for a lossless data compression.
    # out_filename_w260_c6.png
    output_file = "out_" + params["file_name"] + "_w" + str(width) + "_c" + str(colors) + ".png"

    tmp_file = tempfile.NamedTemporaryFile(mode='w+b', suffix=".png")
    tmp_file_name = tmp_file.name
    tmp_file.seek(0)

    reduce_size(input_file, width, tmp_file_name)
    tmp_file.seek(0)

    reduce_colors(tmp_file_name, colors, tmp_file_name)
    tmp_file.seek(0)

    pixelate(tmp_file_name, output_file)

    tmp_file.close()

    print("Cross stitch pattern saved to", output_file)


if __name__ == "__main__":
    main()
