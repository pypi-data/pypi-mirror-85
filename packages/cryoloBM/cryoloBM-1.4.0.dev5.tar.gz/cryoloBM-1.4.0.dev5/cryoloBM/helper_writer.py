from cryolo.utils import BoundBox
from cryolo import CoordsIO
from cryoloBM import  helper
from os import path,makedirs, remove as os_remove

try:
    import PyQt4.QtCore as QtCore
except ImportError:
    import PyQt5.QtCore as QtCore


def prepare_vars_for_writing(box_dir,file_type, is_3D_tomo):
    d = path.join(box_dir, file_type)
    makedirs(d, exist_ok=True)

    file_ext = ".box"
    write_coords_ = CoordsIO.write_eman1_boxfile if is_3D_tomo is False else  CoordsIO.write_eman_boxfile3d

    if file_type == "STAR":
        file_ext = ".star"
        write_coords_ = CoordsIO.write_star_file
    elif file_type == "CBOX":
        file_ext = ".cbox"
        write_coords_ = CoordsIO.write_cbox_file
    return file_ext, write_coords_


def write_coordinates(pd, box_dictionary, ignored_slice, empty_slice,fname, box_dir, is_3D_tomo, file_ext, is_cbox, current_conf_thresh, upper_size_thresh,lower_size_thresh,boxsize,write_coords_):
    # only in a 3D tomo image we have to delete an existing file before starting to write the new one.
    # Basically because we write in append mode on a file the selected particles slice after slice
    overwrite = True

    num_writtin_part = 0
    counter = 0
    slice_index = None
    boxes = []
    for filename, rectangles in box_dictionary.items():

        if pd.wasCanceled():
            break
        else:
            pd.show()
            val = int((counter + 1) * 100 / len(box_dictionary.items()))
            pd.setValue(val)
        QtCore.QCoreApplication.instance().processEvents()

        if is_3D_tomo is True:
            slice_index = int(filename)
            filename = fname

        box_filename = filename + file_ext
        box_file_path = path.join(box_dir, box_filename)

        if overwrite is True:
            overwrite = False
            if is_3D_tomo is True and path.isfile(box_file_path) is True:
                os_remove(box_file_path)

        if is_cbox:
            rectangles = [
                box for box in rectangles if
                helper.check_if_should_be_visible(box, current_conf_thresh, upper_size_thresh,lower_size_thresh)
            ]
            # if self.use_estimated_size_checkbox.isChecked():
        if is_3D_tomo:
            real_rects = [rect.getSketch() for rect in rectangles]
        else:
            real_rects = [rect.getSketch() for rect in rectangles]
            for rect in real_rects:
                helper.resize_box(rect, boxsize)

        num_writtin_part = num_writtin_part + len(real_rects)

        from cryolo.utils import BoundBox
        for rect_index, rect in enumerate(real_rects):
            x_lowerleft = int(rect.get_x())
            y_lowerleft = int(rect.get_y())
            boxize = int(rect.get_width())
            confidence = 1
            if rectangles[rect_index].get_confidence() is not None:
                confidence = rectangles[rect_index].get_confidence()
            box = BoundBox(x=x_lowerleft, y=y_lowerleft, w=boxize, h=boxize, z=slice_index, c=confidence, depth=1)
            boxes.append(box)

        counter = counter + 1
        if is_3D_tomo is False:
            if is_cbox:
                write_coords_(box_file_path, boxes, empty_slice, ignored_slice)
            else:
                write_coords_(box_file_path, boxes)
            boxes = []

    if is_3D_tomo is True:
        print("Write", box_file_path)
        if is_cbox:
            write_coords_(box_file_path, boxes, empty_slice, ignored_slice)
        else:
            write_coords_(box_file_path, boxes)
    print(num_writtin_part, "particles written in '" + file_ext + "' file.")


def write_coordinates_3d_folder(pd, box_dictionary, ignored_slice, empty_slice, is_folder_3D_tomo, is_cbox, current_conf_thresh, upper_size_thresh,lower_size_thresh, boxsize, write_coords_, file_ext, box_dir):
    num_writtin_part = 0

    for filename in box_dictionary.keys():
        counter = 0
        overwrite = True
        boxes = []
        for index, rectangles in box_dictionary[filename].items():

            if pd.wasCanceled():
                break
            else:
                pd.show()
                val = int((counter + 1) * 100 / len(box_dictionary[filename].items()))
                pd.setValue(val)
            QtCore.QCoreApplication.instance().processEvents()

            box_filename = filename + file_ext
            box_file_path = path.join(box_dir, box_filename)

            if overwrite is True:
                overwrite = False
                if is_folder_3D_tomo is True and path.isfile(box_file_path) is True:
                    os_remove(box_file_path)

            if is_cbox:
                rectangles = [
                    box for box in rectangles if
                    helper.check_if_should_be_visible(box, current_conf_thresh, upper_size_thresh,lower_size_thresh)
                ]
                # if self.use_estimated_size_checkbox.isChecked():
            real_rects = [rect.getSketch() for rect in rectangles]
            for rect in real_rects:
                helper.resize_box(rect, boxsize)
            num_writtin_part = num_writtin_part + len(real_rects)


            for rect_index, rect in enumerate(real_rects):
                confidence = 1
                if rectangles[rect_index].get_confidence() is not None:
                    confidence = rectangles[rect_index].get_confidence()
                x_lowerleft = int(rect.get_x())
                y_lowerleft = int(rect.get_y())
                boxize = int(rect.get_width())
                box = BoundBox(x=x_lowerleft, y=y_lowerleft, w=boxize, h=boxize, c=confidence)
                box.z = index
                boxes.append(box)

            if is_cbox:
                write_coords_(box_file_path, boxes)     #todo how
            else:
                write_coords_(box_file_path, boxes)

            counter = counter + 1
    print(num_writtin_part, "particles written in '" + file_ext + "' file.")

