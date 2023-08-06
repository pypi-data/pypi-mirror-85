from os import listdir,path
from mrcfile import mmap as mrcfile_mmap        #it is not in the setup.py because it is already installed by cryolo
import numpy as np
from cryoloBM import MySketch
from cryolo import imagereader

def get_all_loaded_filesnames(root):
    """
    get the list of the loaded file
    :param root: QtG.QTreeWidget obj
    :return: list of filenames
    """
    child_count = root.childCount()
    filenames = []
    for i in range(child_count):
        item = root.child(i)
        filename = path.splitext(item.text(0))[0]
        filenames.append(filename)
    return filenames

def resize_box(rect, new_size):
    """
    resize a 'matplotlib.patches.Rectangle' obj
    :param rect: a 'matplotlib.patches.Rectangle' obj
    :param new_size: new width and height
    :return: None
    """
    if isinstance(rect,MySketch.MyCircle) and rect.get_radius() != new_size:
        rect.set_radius = new_size
    elif isinstance(rect,MySketch.MyRectangle) and (rect.get_width() != new_size or rect.get_height() != new_size):
        height_diff = new_size - rect.get_height()
        width_diff = new_size - rect.get_width()
        newy = rect.get_y() - height_diff / 2
        newx = rect.get_x() - width_diff / 2
        rect.set_height(new_size)
        rect.set_width(new_size)
        rect.set_xy((newx, newy))


def get_only_files(dir_path,wildcard,is_list_tomo):
    """
    generate list of files in 'dir_path' path
    :param dir_path: path to the folder
    :param wildcard: using wildcard
    :param is_list_tomo: True if folder of 3D tomo
    :return: list of valid files in 'dir_path'
    """
    onlyfiles = [
        f
        for f in sorted(listdir(dir_path))
        if path.isfile(path.join(dir_path, f))
    ]

    if wildcard:
        import fnmatch
        onlyfiles = [
            f
            for f in sorted(listdir(dir_path))
            if fnmatch.fnmatch(f, wildcard)
        ]

    if is_list_tomo is False:
        onlyfiles = [
            i
            for i in onlyfiles
            if not i.startswith(".")
               and i.endswith((".jpg", ".jpeg", ".png", ".mrc", ".mrcs", ".tif", ".tiff", ".rec"))]
    else:
        onlyfiles_all = [i for i in onlyfiles if not i.startswith(".") and i.endswith((".mrc", ".mrcs",".rec"))]
        onlyfiles.clear()
        for f in onlyfiles_all:
            with mrcfile_mmap(path.join(dir_path, f), permissive=True, mode="r") as mrc:
                if len(mrc.data.shape) == 3:
                    onlyfiles.append(f)
                mrc.close()

    return onlyfiles


def filter_tuple_is_equal(a,b):
    return a[0]==b[0] and a[1]==b[1] and a[2] == b[2]


def is_helicon_with_particle_coords(path_f):
    with open(path_f) as f:
        first_line = f.readline()
        f.close()
    return "#micrograph" in first_line


def is_eman1_helicion(path_f):
    try:
        box_lines = np.atleast_2d(np.genfromtxt(path_f))
        if len(box_lines) < 2:
            return False
        return (
                len(box_lines[0]) == 5
                and box_lines[0][4] == -1
                and box_lines[1][4] == -2
        )
    except ValueError:
        return False


def getEquidistantRectangles(x_start, y_start, x_end, y_end, width, parts, edgecolor,is_circle = False, is_3d_tomo =False):
    points = zip(
        np.linspace(x_start, x_end, parts + 1, endpoint=False),
        np.linspace(y_start, y_end, parts + 1, endpoint=False),
    )
    new_rectangles = []

    for point in points:
        sketch = MySketch.MySketch(
            is_circle = is_circle,
            xy=(point[0], point[1]),
            width=width,
            height=width,
            is_3d_tomo=is_3d_tomo,
            confidence= 1,
            linewidth=1,
            edgecolor=edgecolor,
            facecolor="none",
        )
        new_rectangles.append(sketch)
    return new_rectangles


def get_file_type(file_path):
    im_type = None
    if file_path.endswith(("jpg", "jpeg", "png")):
        im_type = 0
    if file_path.endswith(("tif", "tiff")):
        im_type = 1
    if file_path.endswith(("mrc", "mrcs","rec")):
        im_type = 2
    return im_type


def read_image(file_path, use_mmap=False):
    im_type = get_file_type(file_path)

    img = imagereader.image_read(file_path, use_mmap=use_mmap)
    img = normalize_and_flip(img, im_type)
    return img

def normalize_and_flip(img, file_type):
    if file_type == 0:
        # JPG
        img = np.flip(img, 0)
    if file_type == 1 or file_type == 2:
        # tif /mrc
        if not np.issubdtype(img.dtype, np.float32):
            img = img.astype(np.float32)
        if len(img.shape) == 3:
            img = np.flip(img, 1)
        else:
            img = np.flip(img, 0)
        mean = np.mean(img)
        sd = np.std(img)
        img = (img - mean) / sd
        img[img > 3] = 3
        img[img < -3] = -3
    return img


def get_number_visible_boxes( rectangles):
    i = 0
    for box in rectangles:
        if box.is_figure_set():
            i = i + 1
    return i

def get_corresponding_box(x, y, rectangles, current_conf_thresh, box_size, get_low=False):
    a = np.array([x, y])

    for box in rectangles:
        b = np.array(box.get_xy())
        dist = np.linalg.norm(a - b)
        if get_low:
            if dist < box_size / 2 and box.get_confidence() < current_conf_thresh:
                return box
        else:
            if dist < box_size / 2 and box.get_confidence() > current_conf_thresh:
                return box
    return None

def check_if_should_be_visible( box, current_conf_thresh, upper_size_thresh, lower_size_thresh):
    return box.get_confidence() > current_conf_thresh and upper_size_thresh >= box.get_est_size() >= lower_size_thresh


def convert(boxes_in_dict, use_circle):
    """
    Convert a list of boxes
    :param boxes_in_dict: list of MySketch obj
    :param use_circle: True if the MySketch objs should be convert to rect
    :return False if there is nothing to convert
    """
    for b in boxes_in_dict:
        try:
            """
            due the high number of possible combination (folder case, pick with rect-convert-load,
            load pick convert, etc.) a set of 'if-elif' should be implement to avoid to try to convert a
            circle in a circle or a rect in a rect.
            e.g.: pick with rect ,convert to circle and load data from file ( if at least one loaded value is
                    in the same image with a picked one wehave this situation).
            For this reason we use a 'not beautiful to look at but effective' try-except solution
            """
            if use_circle:
                b.convert(width=b.get_width())
            else:
                b.convert(radius=b.get_radius())
        except AttributeError:
            return False
    return True


def resize(boxes_in_dict, new_size):
    """
    Convert a list of boxes
    :param boxes_in_dict: list of MySketch obj
    :param new_size: the new size (radius if circle, height and width otherwise)
    :return False if there is nothing to convert
    """
    for b in boxes_in_dict:
        b.resize(new_size)


def create_deep_copy_box_dict(d,is_tomo_folder = False):
    """
    Since we cannot deepcopy 'self.box_dictionary' we have to duplicate it
    :param d: the self.box_dictionary
    :param is_tomo_folder: True if it is a folder of tomos
    :return the copy of the dict
    """

    if is_tomo_folder:
        out = {k: dict() for k in d.keys()}
        for k,d_in in d.items():
            for k2 in d[k].keys():
                out[k].update({k2:list()})
            for k_in,v_in in  d_in.items():
                try:
                    for b in v_in:
                        out[k][k_in].append(MySketch.MySketch(is_circle=True, xy=b.get_xy(), radius=b.get_radius(),
                                                        is_3d_tomo=b.get_is_3d_tomo(), est_size=b.get_est_size(),
                                                        confidence=b.get_confidence(),
                                                              only_3D_visualization=b.only_3D_visualization,
                                                        edgecolor=b.getSketch().get_edgecolor(),
                                                        linewidth=1, facecolor="None"))
                except AttributeError:
                    for b in v_in:
                        out[k][k_in].append(MySketch.MySketch(is_circle=False, xy=b.get_xy(), width=b.get_width(),
                                                        height=b.get_height(), is_3d_tomo=b.get_is_3d_tomo(),
                                                        angle=b.get_angle(), est_size=b.get_est_size(),
                                                        confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                        edgecolor=b.getSketch().get_edgecolor(),
                                                        linewidth=1, facecolor="None"))
    else:
        out ={k:list() for k in d.keys()}
        for k,v in d.items():
            try:
                for b in v:
                    out[k].append(MySketch.MySketch(is_circle=True,  xy=b.get_xy(), radius=b.get_radius(),
                                                    is_3d_tomo=b.get_is_3d_tomo(), est_size=b.get_est_size(),
                                                    confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                    edgecolor=b.getSketch().get_edgecolor(),
                                                    linewidth=1, facecolor="None"))
            except AttributeError:
                for b in v:
                    out[k].append(MySketch.MySketch(is_circle=False,  xy=b.get_xy(), width=b.get_width(),
                                                    height=b.get_height(), is_3d_tomo=b.get_is_3d_tomo(),
                                                    angle=b.get_angle(), est_size=b.get_est_size(),
                                                    confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                    edgecolor=b.getSketch().get_edgecolor(),
                                                    linewidth=1, facecolor="None"))

    return out



def create_restore_box_dict(d,is_tomo_folder = False):
    """
    Since we cannot deepcopy 'self.box_dictionary' we have to duplicate it
    :param d: the self.box_dictionary
    :param is_tomo_folder: True if it is a folder of tomos
    :return the copy of the dict
    """

    if is_tomo_folder:
        out = {k: dict() for k in d.keys()}
        for k,d_in in d.items():
            for k2 in d[k].keys():
                out[k].update({k2:list()})
            for k_in,v_in in  d_in.items():
                try:
                    for b in v_in:
                        if b.only_3D_visualization is False:
                            out[k][k_in].append(MySketch.MySketch(is_circle=True, xy=b.get_xy(), radius=b.get_radius(),
                                                        is_3d_tomo=b.get_is_3d_tomo(), est_size=b.get_est_size(),
                                                        confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                        edgecolor=b.getSketch().get_edgecolor(),
                                                        linewidth=1, facecolor="None"))
                except AttributeError:
                    for b in v_in:
                        if b.only_3D_visualization is False:
                            out[k][k_in].append(MySketch.MySketch(is_circle=False, xy=b.get_xy(), width=b.get_width(),
                                                        height=b.get_height(), is_3d_tomo=b.get_is_3d_tomo(),
                                                        angle=b.get_angle(), est_size=b.get_est_size(),
                                                        confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                        edgecolor=b.getSketch().get_edgecolor(),
                                                        linewidth=1, facecolor="None"))
    else:
        out ={k:list() for k in d.keys()}
        for k,v in d.items():
            try:
                for b in v:
                    if b.only_3D_visualization is False:
                        out[k].append(MySketch.MySketch(is_circle=True,  xy=b.get_xy(), radius=b.get_radius(),
                                                    is_3d_tomo=b.get_is_3d_tomo(), est_size=b.get_est_size(),
                                                    confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                    edgecolor=b.getSketch().get_edgecolor(),
                                                    linewidth=1, facecolor="None"))
            except AttributeError:
                for b in v:
                    if b.only_3D_visualization is False:
                        out[k].append(MySketch.MySketch(is_circle=False,  xy=b.get_xy(), width=b.get_width(),
                                                    height=b.get_height(), is_3d_tomo=b.get_is_3d_tomo(),
                                                    angle=b.get_angle(), est_size=b.get_est_size(),
                                                    confidence=b.get_confidence(),only_3D_visualization=b.only_3D_visualization,
                                                    edgecolor=b.getSketch().get_edgecolor(),
                                                    linewidth=1, facecolor="None"))

    return out



def is_cbox_untraced(b):
    """
    :param b: loaded box of a cbox file
    return False True if the file is cobx_untraced
    """
    return int(b.depth) == 1