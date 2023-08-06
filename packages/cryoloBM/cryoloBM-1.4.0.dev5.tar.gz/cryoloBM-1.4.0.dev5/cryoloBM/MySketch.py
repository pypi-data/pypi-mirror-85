from matplotlib.patches import  Rectangle,Circle

class MySketch:
    def __init__(self, is_circle,  xy=None, radius=None, width=None, height=None, is_3d_tomo=False, angle=0.0, est_size=None, confidence=None, only_3D_visualization= False, **kwargs):
        """
        Since in 'helper.check_if_should_be_visible' the sketches are shown in base of their 'box.est_size' value,
        we set (in the smaller sketches created on demand for the 3d visualization) these values to the 'est_size'
        of the original one (i.e.: the loaded value or picked from GUI value).
        For now the 'only_3D_visualization' instance is used for debug purpose
        """
        self.is_circle = is_circle
        self.only_3D_visualization=only_3D_visualization
        if is_circle:
            self.sketch = MyCircle( xy=xy, radius=radius, is_3d_tomo = is_3d_tomo, est_size=est_size, confidence = confidence, **kwargs)
        else:
            self.sketch = MyRectangle( xy=xy, width=width, height=height, is_3d_tomo = is_3d_tomo , angle=angle, est_size=est_size, confidence = confidence,  **kwargs)

    def convert(self, radius = None, width = None, angle =0.0):
        xy = self.get_xy()
        confidence = self.get_confidence()
        is_3d_tomo =self.get_is_3d_tomo()
        color = self.getSketch().get_edgecolor()
        est_size=self.get_est_size()
        self.remove_instance()

        if self.is_circle:
            x = xy[0] - radius
            y = xy[1] - radius
            size = radius*2
            self.sketch = MyRectangle( xy=(x,y), width=size, height=size, is_3d_tomo = is_3d_tomo , angle=angle, est_size=est_size, confidence = confidence,
                                       linewidth = 1, edgecolor = color, facecolor = "none")
        else:
            x = xy[0] + width/2
            y = xy[1] + width/2
            radius = width /2
            self.sketch = MyCircle(xy=(x,y), radius=radius, is_3d_tomo=is_3d_tomo, est_size=est_size, confidence=confidence,
                                   linewidth = 1, edgecolor = color, facecolor = "none")

        self.is_circle = not self.is_circle
        self.getSketch()    # create a new instance

    def resize(self, new_size):
        xy = self.get_xy()
        confidence = self.get_confidence()
        is_3d_tomo =self.get_is_3d_tomo()
        color = self.getSketch().get_edgecolor()

        """est_size contained the estimated size of cryolo, when loaded from '.cbox' and should be never changed"""
        est_size = self.get_est_size()

        self.remove_instance()

        if self.is_circle:
            self.sketch = MyCircle(xy=xy, radius=new_size/2, is_3d_tomo=is_3d_tomo, est_size=est_size,
                                   confidence=confidence, linewidth=1, edgecolor=color, facecolor="none")
        else:
            x = xy[0] + (self.get_width()-new_size)/2
            y = xy[1] + (self.get_width()-new_size)/2
            self.sketch = MyRectangle(xy=(x,y), width=new_size, height=new_size, is_3d_tomo=is_3d_tomo,
                                      angle=self.get_angle(),est_size=est_size, confidence=confidence,
                                      linewidth=1, edgecolor=color, facecolor="none")
        self.getSketch()  # create a new instance

    def remove_instance(self):
        self.sketch.remove_istance()

    def getSketch(self):
        return self.sketch.getSketch()

    def set_xy(self, xy):
        self.sketch.xy = xy

    def set_radius(self, radius):
        self.sketch.radius = radius

    def set_width(self, width):
        self.sketch.width = width

    def set_height(self, height):
        self.sketch.height = height

    def set_is_3d_tomo(self, is_3d_tomo):
        self.sketch.is_3d_tomo = is_3d_tomo

    def set_angle(self, angle):
        self.sketch.angle = angle

    def set_est_size(self, est_size):
        self.sketch.est_size = est_size

    def set_confidence(self, confidence):
        self.sketch.confidence = confidence

    def get_xy(self):
        return self.sketch.xy

    def get_radius(self):
        return self.sketch.radius

    def get_width(self):
        return self.sketch.width

    def get_height(self):
        return self.sketch.height

    def get_is_3d_tomo(self):
        return self.sketch.is_3d_tomo

    def get_angle(self):
        return self.sketch.angle

    def get_est_size(self):
        return self.sketch.est_size

    def get_confidence(self):
        return self.sketch.confidence



class MyCircle:
    def __init__(self, xy, radius, is_3d_tomo = False, est_size=None, confidence = None, **kwargs):
        self.confidence = confidence
        self.est_size = est_size
        self.is_3d_tomo = is_3d_tomo
        self.xy = xy
        self.radius = radius
        self.circleInstance = None
        self.kwargs = kwargs

    def getSketch(self):
        if self.circleInstance is None:
            self.circleInstance = Circle(xy=self.xy, radius=self.radius, **self.kwargs)
        return self.circleInstance

    def remove_istance(self):
        self.circleInstance = None


class MyRectangle:
    def __init__(self, xy, width, height, is_3d_tomo = False,  angle=0.0, est_size=None, confidence = None,  **kwargs):
        self.confidence = confidence
        self.est_size = est_size
        self.is_3d_tomo = is_3d_tomo
        self.xy = xy
        self.width = width
        self.height = height
        self.angle = angle
        self.rectInstance = None
        self.kwargs = kwargs

    def getSketch(self):
        if self.rectInstance is None:
            self.rectInstance = Rectangle(self.xy, self.width, self.height, self.angle, **self.kwargs)
        return self.rectInstance

    def remove_istance(self):
        self.rectInstance = None