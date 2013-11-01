# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from imaxplore.Core.Configuration import conf
from imaxplore.Gui.ImageWidget import ImageWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(conf('app_name'))

        # Central Widget
        self.imageWidget = ImageWidget(self)
        self.setCentralWidget(self.imageWidget)

        # Open action
        openAction = QtGui.QAction(_(u'&Open'), self)
        openAction.setShortcut(_(u'Ctrl+O'))
        openAction.setStatusTip(_(u'Open an image'))
        openAction.triggered.connect(self.openImage)

        # Close action
        closeAction = QtGui.QAction(_(u'&Close'), self)
        closeAction.setShortcut(_(u'Ctrl+W'))
        closeAction.setStatusTip(_(u'Close the current image'))
        closeAction.triggered.connect(self.closeImage)

        # Save action
        saveAction = QtGui.QAction(_(u'&Save'), self)
        saveAction.setShortcut(_(u'Ctrl+S'))
        saveAction.setStatusTip(_(u'Save an image'))
        saveAction.triggered.connect(self.saveImage)

        # Exit action
        exitAction = QtGui.QAction(_(u'&Exit'), self)
        exitAction.setShortcut(_(u'Ctrl+Q'))
        exitAction.setStatusTip(_(u'Exit application'))
        exitAction.triggered.connect(QtGui.qApp.quit)

        # Status bar
        self.statusBar()

        # Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(_(u'&File'))
        fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # Show the windows
        self.show()

    def openImage(self):
        fName = QtGui.QFileDialog.getOpenFileName(self, 'Select image', '')
        self.imageWidget.setImage(fName)

    def closeImage(self):
        self.imageWidget.reset()

    def saveImage(self):
        pass