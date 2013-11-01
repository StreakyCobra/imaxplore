# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class HomographyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(HomographyWidget, self).__init__(parent)
        self._initUI()

    # Initialize the UI
    def _initUI(self):
        # Create the figure
        self._fig = Figure()

        # Canvas configuration
        self._canvas = FigureCanvas(self._fig)
        self._canvas.setParent(self)

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
        self._canvas.hide()

    # Set an image to the widget
    def setImage(self, image):
        if fName is not '':
            self.reset()
            self._image = image
            self._canvas.show()
            self._redraw()

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

        # Draw the canvas
        self._canvas.draw()
