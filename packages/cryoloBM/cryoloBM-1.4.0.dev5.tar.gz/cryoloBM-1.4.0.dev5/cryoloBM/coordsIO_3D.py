import numpy as np
from cryolo.utils import  BoundBox
from os import path as os_path
from csv import writer as csv_writer
from csv import QUOTE_NONE as csv_QUOTE_NONE
from cryolo import CoordsIO
def read_eman1_boxfile(path):
    """
    Read a box file in EMAN1 box format. It is the 3D version of cryolo.CoordsIO.py
    :param path: Path to box file
    :return: Dict of list  (key = slice tomo, value = list of bounding boxes)
    """
    boxreader = np.atleast_3d(np.genfromtxt(path))
    slices = np.unique(boxreader[:, 2].astype(np.int8)).tolist()
    boxes = {key: [BoundBox(x=box[0], y=box[1], w=box[3], h=box[4]) for box in boxreader if box[2] == key] for key in slices}
    return boxes

def read_star_file(path, box_width):
    """
    Read a box file from STAR file
    :param path: Path to star file
    :param box_width: size width and height box
    """
    _, skip_indices = CoordsIO.get_star_file_header(path)
    boxreader = np.atleast_2d(np.genfromtxt(path, skip_header=skip_indices))

    slices = np.unique(boxreader[:, 2].astype(np.int8)).tolist()
    boxes = {key: [BoundBox(x=box[0] - box_width / 2, y=box[1] - box_width / 2, w=box_width, h=box_width) for box in
                       boxreader if box[2] == key] for key in slices}

    return boxes

def read_cbox_boxfile(path):
    """
    Read a box file from CBOX file
    :param path: Path to star file
    """
    _, skip_indices = CoordsIO.get_star_file_header(path)
    boxreader = np.atleast_3d(np.genfromtxt(path, skip_header=skip_indices))

    slices = np.unique(boxreader[:, 2].astype(np.int8)).tolist()

    boxes = {key: [BoundBox(x=box[0], y=box[1], w=box[3], h=box[4]) for box in
                   boxreader if box[2] == key] for key in slices}
    return boxes


def write_eman1_boxfile(path, boxes, z=None):
    """
    Write the selected boxes on EMAN box file
    :param path: Path to star file
    :param boxes: list of boxes
    :param z: axis z, None if it is not a 3D tomo
    """
    append = os_path.isfile(path)
    mode = "w" if append is False else "a"
    with open(path, mode) as boxfile:
        box_writer = csv_writer(boxfile, delimiter="\t", quotechar="|", quoting=csv_QUOTE_NONE)
        for box in boxes:
            box_writer.writerow([box.x, box.y, z, box.w, box.h])


def write_star_file(path, boxes, z=None):
    """
    Write the selected boxes on STAR file. It is the 3D version of cryolo.CoordsIO.py
    :param path: Path to star file
    :param boxes: list of boxes
    :param z: axis z, None if it is not a 3D tomo
    """
    append = os_path.isfile(path)
    mode = "w" if append is False else "a"
    with open(path, mode) as boxfile:
        box_writer = csv_writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv_QUOTE_NONE
        )
        if z is None:
            print ("Error: no slice value inserted")
        else:
            if append is False:
                box_writer.writerow([])
                box_writer.writerow(["data_"])
                box_writer.writerow([])
                box_writer.writerow(["loop_"])
                box_writer.writerow(["_rlnCoordinateX #1 "])
                box_writer.writerow(["_rlnCoordinateY #2"])
                box_writer.writerow(["_rlnCoordinateZ #3"])
                box_writer.writerow(["_rlnClassNumber #4"])
                box_writer.writerow(["_rlnAnglePsi #5"])
                box_writer.writerow(["_rlnAutopickFigureOfMerit  #6"])
            for box in boxes:
                box_writer.writerow(
                    [box.x + box.w / 2, box.y + box.h / 2, z, -999, -999.00000, -999.00000]
                )


def write_cbox_file(path, boxes,z=None):
    """
    Write the selected boxes on CBOX file.
    It is the version of cryolo.CoordsIO.py but we get the box.z value as input to manage the 3d folder image case
    :param path: Path to star file
    :param boxes: list of boxes
    :param z: axis z, None if it is not a 3D tomo.
    """
    append = os_path.isfile(path)
    mode = "w" if append is False else "a"
    with open(path, mode) as boxfile:
        box_writer = csv_writer(
            boxfile, delimiter="\t", quotechar="|", quoting=csv_QUOTE_NONE
        )
        if z is None:
            print ("Error: no slice value inserted")
        else:
            if append is False:
                box_writer.writerow([])
                box_writer.writerow(["data_cryolo"])
                box_writer.writerow([])
                box_writer.writerow(["loop_"])
                box_writer.writerow(["_CoordinateX #1"])
                box_writer.writerow(["_CoordinateY #2"])
                box_writer.writerow(["_CoordinateZ #3"])
                box_writer.writerow(["_Width #4"])
                box_writer.writerow(["_Height #5"])
                box_writer.writerow(["_Depth #6"])
                box_writer.writerow(["_EstWidth #7"])
                box_writer.writerow(["_EstHeight #8"])
                box_writer.writerow(["_Confidence #9"])

            for box in boxes:
                six_row= -1
                seven_row = -1
                if "boxsize_estimated" in box.meta:
                    six_row= box.meta["boxsize_estimated"][0]
                    seven_row = box.meta["boxsize_estimated"][1]
                box_writer.writerow(
                    [box.x, box.y, z, box.w, box.h, box.depth,six_row,seven_row,box.c])
