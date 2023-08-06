# coding: utf-8
###################################################################
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility #
#                                                                 #
# Author: Marius Retegan                                          #
#                                                                 #
# This work is licensed under the terms of the MIT license.       #
# For further information, see https://github.com/mretegan/crispy #
###################################################################
"""A dialog showing the progress of the calculation."""

import logging
import os
from itertools import cycle

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

from crispy import resourceAbsolutePath

logger = logging.getLogger(__name__)


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        uiPath = os.path.join("gui", "uis", "quanty", "progress.ui")
        loadUi(resourceAbsolutePath(uiPath), baseinstance=self, package="crispy.gui")

        self.message = "The calculation is running. Please wait"
        self.dots = cycle([".", "..", "..."])
        self.currentMessage = self.message + next(self.dots)

        self.label.setText(self.currentMessage)
        self.cancelButton.clicked.connect(self.reject)

        timer = QTimer(self, interval=750, timeout=self.changeMessage)
        timer.start()

    def changeMessage(self):
        self.currentMessage = self.message + next(self.dots)
        self.label.setText(self.currentMessage)

    def closeEvent(self, event):
        self.reject()
        super().closeEvent(event)


def main():
    app = QApplication([])

    dialog = ProgressDialog()
    dialog.show()

    app.exec_()


if __name__ == "__main__":
    main()
