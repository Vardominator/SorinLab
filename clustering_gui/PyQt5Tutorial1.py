#!/usr/bin/python3


# Simple example
# Author: Varderes Barsegyan


""" 
NOTES:

QtCore: core non GUI functionality

    time, files, directories, data types, streams, urls, threads, processes


QtGui:

    windowing system integration, event handling, 2D graphics, basic imaging


QtWidgets: set of UI elements to create classic desktop-style interfaces



"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    # every PyQt5 application must create an application object
    # sys.argv is a list of arguments from a command line
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())