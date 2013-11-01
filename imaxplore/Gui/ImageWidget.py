# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.image as mpimg
from functools import cmp_to_key
from PyQt4 import QtGui
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class ImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Create the figure
        self.fig = Figure()

        # Canvas configuration
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.mpl_connect('button_press_event', self.onPick)

        # Figure configuration
        self.plt = self.fig.add_subplot(111)
        self.plt.xaxis.set_visible(False)
        self.plt.yaxis.set_visible(False)

        # Finalize figure
        self.fig.subplots_adjust(wspace=0, hspace=0)

        # Initialize variables
        self.image = None
        self.points = []

        # Create the layout
        vbox = QtGui.QVBoxLayout()

        # Add it to the layout
        vbox.addWidget(self.canvas)

        # Set layout
        self.setLayout(vbox)

    def openImage(self):
        fName = QtGui.QFileDialog.getOpenFileName(self, 'Select image', '')

        if fName is not '':
            self.image = mpimg.imread(fName)
            self.points = []
            self.redraw()

    def saveImage(self):
        pass

    def redraw(self):
        # Clear the canvas
        self.plt.clear()

        # Plot the image
        if self.image is not None:
            self.plt.autoscale(True)
            self.plt.imshow(self.image)
            self.plt.autoscale(False)

        # Plot the points
        if len(self.points) > 0:
            xs = [x for (x,_) in self.points]
            ys = [y for (_,y) in self.points]
            self.plt.plot(xs + [xs[0]], ys + [ys[0]], 'o-', color='red')

        # Draw the canvas
        self.canvas.draw()

    def onPick(self, event):
        # Get point position
        x = event.xdata
        y = event.ydata

        # For each existing points
        for pt in self.points:
            # Get point position
            px, py = pt

            # Compute distance to current point
            dst = np.sqrt((px - x) ** 2 + (py -y) ** 2)

            # If the distance is small remove it
            if dst < 10:
                self.points = list(filter(lambda v: v != pt, self.points))
                self.redraw()
                return

        if len(self.points) < 4:
            self.points.append((x,y))

        self.redraw()