# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.image as mpimg
from PyQt4 import QtGui
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class ImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.initUI()

    # Initialize the UI
    def initUI(self):
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
            self._plt.plot(xs + [xs[0]], ys + [ys[0]], 'o-', color='red')

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
        if n == 4:
            return

        # Else a verification must be done
        if not self._lieIntoTriangle(x, y):
            self._points.append((x, y))

        # Reorder points to have consistant rectangle when drawing
        self._reorderPoints()

    # Remove an existing point
    def _removePoint(self, x, y):
        self._points = list(filter(lambda v: v != (x,y), self._points))

    # Check if the last points lie into the triangle formed by other ones
    def _lieIntoTriangle(self, x, y):
        # Shortcut to access points
        x1, y1 = self._points[0]
        x2, y2 = self._points[1]
        x3, y3 = self._points[2]

        # Compute barycentric alpha
        alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) /\
                ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))

        # If alpha smaller than 0 then outside the triangle
        if alpha <= 0:
            return False

        # Compute barycentric beta
        beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) /\
               ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))

        # If beta smaller than 0 then outside the triangle
        if beta <= 0:
            return False

        # Compute barycentric gamma
        gamma = 1.0 - alpha - beta

        # If gamma smaller than 0 then outside the triangle
        if gamma <= 0:
            return False

        # Else inside the triangle
        return True

    # Reorder points to have a planar graph (meaning no line crossing)
    def _reorderPoints(self):
        p1 = self._points[0]
        others = list(filter(lambda v: v != p1, self._points))
        pass

