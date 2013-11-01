# -*- coding: utf-8 -*-

from imaxplore.Util.Geometry import lieIntoTriangle, allSameSide

from PyQt4 import QtGui

import numpy as np
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class ImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self._initUI()

    # Initialize the UI
    def _initUI(self):
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
        self._points = []
        self._canvas.hide()

    # Set an image to the widget
    def setImage(self, fName):
        if fName is not '':
            self._image = mpimg.imread(fName)
            self._points = []
            self._redraw()
            self._canvas.show()

    # Get the image of the widget
    def getImage(self):
        pass

    # Redraw the image and points
    def _redraw(self):
        # Clear the canvas
        self._plt.clear()

        # Plot the image
        if self._image is not None:
            self._plt.autoscale(True)
            self._plt.imshow(self._image)
            self._plt.autoscale(False)

        # Plot the points
        if len(self._points) > 0:
            xs = [x for (x, _) in self._points]
            ys = [y for (_, y) in self._points]
            self._plt.plot(xs + [xs[0]], ys + [ys[0]], '-', color='red')
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

        # Add the points
        self._addPoint(x, y)

        # Redraw the image
        self._redraw()

    # Add a new points
    def _addPoint(self, x, y):
        # Count points
        n = len(self._points)

        # If less than 3 points just add it
        if n < 3:
            self._points.append((x, y))
            return

        # If already 4 points, ignore it
        if n >= 4:
            return

        # Else a verification must be done
        if self._validPoint(x, y):
            self._points.append((x, y))

            # Reorder points to have consistant rectangle when drawing
            self._reorderPoints()

    # Remove an existing point
    def _removePoint(self, x, y):
        self._points = list(filter(lambda v: v != (x, y), self._points))

    # Reorder points to have a planar graph (meaning no line crossing)
    def _reorderPoints(self):
        # List of reordoned points
        ordPoints = [self._points[0]]

        # List of selectionnable points
        others = self._points[1:]

        # Fill reordoned points
        while len(ordPoints) < 4:
            # Previous point
            p = ordPoints[-1]

            # Test other points
            for pn in others:
                # Points to verify side
                verify = list(filter(lambda v: v != pn and v != p,
                                     self._points))

                # Verify side
                if allSameSide(p, pn, verify):
                    ordPoints.append(pn)
                    others = list(filter(lambda v: v != pn, others))
                    break

        # Set the reordoned points
        self._points = ordPoints

    def _validPoint(self, x, y):
        a = [p for p in self._points] + [(x, y)]
        triangles = [[a[0], a[1], a[2]], [a[0], a[1], a[3]],
                     [a[0], a[2], a[3]], [a[1], a[2], a[3]]]
        points = [a[3], a[2], a[1], a[0]]

        for triangle, point in zip(triangles, points):
            px, py = point
            if lieIntoTriangle(triangle, px, py):
                return False

        return True
