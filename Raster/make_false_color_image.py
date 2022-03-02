import stretch_histogram
import numpy as np

def make_false_color_image(raster):

    nir = raster.read(4)
    red = raster.read(3)
    green = raster.read(2)

    nirs = stretch_histogram.stretch(nir)
    reds = stretch_histogram.stretch(red)
    greens = stretch_histogram.stretch(green)

    # Create RGB false color composite stack
    rgb = np.dstack((nirs, reds, greens))

    return rgb