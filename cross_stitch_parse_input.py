import os.path
import sys


def parse(file_name, width, colors):
    input_params = dict()

    if not os.path.isfile(file_name):
        print("File does not exist: {}".format(file_name), file=sys.stderr)
        sys.exit()

    input_params["file"] = file_name

    input_params["file_name"], input_params["file_ext"] = os.path.splitext(file_name)

    input_params["width"] = width
    input_params["colors"] = colors

    return input_params
