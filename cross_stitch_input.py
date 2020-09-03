import argparse

import cross_stitch_consts as consts


def get_input():
    parser = argparse.ArgumentParser(description="Cross Stitch Pattern Maker")
    parser.add_argument('file', help="Input file name")
    parser.add_argument('-w', '--width', help="Target width of the image in cross stitches", type=int,
                        default=consts.DEFAULT_PATTERN_WIDTH)
    parser.add_argument('-c', '--colors', help="Target number of colors in the cross stitch pattern", type=int,
                        default=consts.DEFAULT_COLORS_NUMBER)

    return parser.parse_args()
