# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from skimage.transform import warp, ProjectiveTransform


class HomographyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(HomographyWidget, self).__init__(parent)
        self._initUI()

    # Initialize the UI
    def _initUI(self):
        # Widget parameters
        self.setMinimumWidth(300)

        # Create the figure
        self._fig = Figure()

        # Canvas configuration
        self._canvas = FigureCanvas(self._fig)
        self._canvas.setParent(self)
        self._canvas.mpl_connect('button_press_event', self._onPick)

        # Plot configuration
        self._plt = self._fig.add_subplot(111)
        self._plt.xaxis.set_visible(False)
        self._plt.yaxis.set_visible(False)

        # Finalize figure
        self._fig.subplots_adjust(wspace=0, hspace=0)

        # Reset the variables
        self.reset()

        # Create the layout
        vbox = QtGui.QVBoxLayout()

        # Add Canvas to the layout
        vbox.addWidget(self._canvas)

        # Set the layout
        self.setLayout(vbox)

    # Reset the variables to original state
    def reset(self):
        self._image = None
        self._render = None
        self._points = []
        self._lastPoints = []
        self._canvas.hide()

    # Set an image to the widget
    def setImage(self, image):
        self._image = image
        self._render = image
        self._canvas.show()
        self._redraw()

    # Get the image of the widget
    def getImage(self):
        pass

    def setHomography(self, points):
        # Save points
        self._lastPoints = points

        # Redraw canvas
        self._redraw()

    # Redraw the image and points
    def _redraw(self):
        # Clear the canvas
        self._plt.clear()

        if len(self._points) == 2 and len(self._lastPoints) == 4:
            # Get points
            src = self._pointsToVector(self._lastPoints)
            dest = self._pointsToVector(self._rectangle())

            # Compute Transformation
            self._projective = ProjectiveTransform()
            self._projective.estimate(src, dest)

            # Prepare output image
            self._render = warp(self._image, self._projective.inverse)

        # Plot the image
        if self._render is not None:
            self._plt.autoscale(True)
            self._plt.imshow(self._render)
            self._plt.autoscale(False)

        # Plot the points
        if len(self._points) > 0:
            xs = [x for (x, _) in self._rectangle()]
            ys = [y for (_, y) in self._rectangle()]
            self._plt.plot(xs + [xs[0]], ys + [ys[0]], '-', color='green')

            xs = [x for (x, _) in self._points]
            ys = [y for (_, y) in self._points]
            self._plt.plot(xs + [xs[0]], ys + [ys[0]], 'o', color='blue')

        # Draw the canvas
        self._canvas.draw()

    # Handle click events
    def _onPick(self, event):
        # Get point position
        x = event.xdata
        y = event.ydata

        if x is None or y is None:
            return

        # For each existing points
        for px, py in self._points:

            # Compute distance to current point
            dst = np.sqrt((px - x) ** 2 + (py - y) ** 2)

            # If the distance is small remove it
            if dst < 10:
                self._removePoint(px, py)
                self._redraw()
                return

        # Delegate to add the point
        self._addPoint(x, y)

        # Redraw the image
        self._redraw()

    # Add a new point
    def _addPoint(self, x, y):
        # Count points
        n = len(self._points)

        # If less than 3 points just add it
        if n < 2:
            self._points.append((x, y))
            return

    # Remove an existing point
    def _removePoint(self, x, y):
        # Remove the point
        self._points = list(filter(lambda v: v != (x, y), self._points))

    def _rectangle(self):
        # Get xs and ys
        xs = [x for (x, _) in self._points]
        ys = [y for (_, y) in self._points]

        # Compute ranges
        xmax = max(xs)
        xmin = min(xs)
        ymax = max(ys)
        ymin = min(ys)

        # Return rectangle
        return [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]

    def _pointsToVector(self, points):
        # Get points values
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
        x4, y4 = points[3]

        # Return the vector
        return np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
