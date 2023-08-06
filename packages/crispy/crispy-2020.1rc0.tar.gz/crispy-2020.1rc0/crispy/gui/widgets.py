# coding: utf-8
###################################################################
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility #
#                                                                 #
# Author: Marius Retegan                                          #
#                                                                 #
# This work is licensed under the terms of the MIT license.       #
# For further information, see https://github.com/mretegan/crispy #
###################################################################
"""Custom widgets."""

import logging

from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit
from PyQt5.QtGui import (
    QDoubleValidator,
    QIntValidator,
    QRegExpValidator,
    QPalette,
    QColor,
)
from PyQt5.QtCore import QRegExp, Qt, QEvent

logger = logging.getLogger(__name__)


class ComboBox(QComboBox):
    def setItems(self, items, currentItem):
        self.blockSignals(True)
        self.clear()
        self.addItems(items)
        self.setCurrentText(currentItem)
        self.blockSignals(False)

    def setModelData(self, model, index):
        value = self.currentText()
        if value == model.data(index, role=Qt.EditRole):
            return
        model.setData(index, value, Qt.EditRole)

    def setEditorData(self, index):
        item = index.internalPointer()
        self.setItems(item.items, item.currentItem)


# Initially the line edits were implemented to return the types specified in
# their names, i.e. the IntLineEdit would return an int, etc. In the end I found it
# better to delegate the conversion to the items in the model. The validators take care
# of having the proper format.


class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator = None
        self.currentText = None
        self.textEdited.connect(self.updateBackgroundColor)
        self.installEventFilter(self)

    def focusInEvent(self, event):
        self.currentText = self.text()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setBackgroundColor("#FFFFFF")
        if not self.text():
            self.setText(self.currentText)
        super().focusOutEvent(event)

    def setTextColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(color))
        self.setPalette(palette)

    def setBackgroundColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(color))
        self.setPalette(palette)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.setBackgroundColor("#FFFFFF")
        return super().eventFilter(source, event)

    def updateBackgroundColor(self):
        self.setBackgroundColor("#FFFF8D")

    def setModelData(self, model, index):
        value = self.text()
        # Don't update the model's data if it did not change.
        if value == model.data(index, role=Qt.EditRole):
            return
        model.setData(index, value, Qt.EditRole)
        self.currentText = value

    def setEditorData(self, index):
        value = index.data()
        self.setText(value)


class IntLineEdit(LineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator = QIntValidator()
        self.setValidator(self.validator)


class DoubleLineEdit(LineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator = QDoubleValidator()
        self.setValidator(self.validator)


class Vector3DLineEdit(LineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regex = QRegExp()
        # Regex that matches the vectors input format, e.g. (1, 0, 1), (-1,0,1)
        # + and - are allowed and any number of spaces after comma. The regex has
        # groups that can be captured.
        # pylint: disable=anomalous-backslash-in-string
        self.regex.setPattern("\\(([+-]?\d?),\s*([+-]?\d?),\s*([+-]?\d?)\\)")
        self.validator = QRegExpValidator(self.regex, self)
        self.setValidator(self.validator)


class CheckBox(QCheckBox):
    def setModelData(self, model, index):
        value = self.isChecked()
        if value == model.data(index, role=Qt.UserRole):
            return
        model.setData(index, value, Qt.EditRole)

    def setEditorData(self, index):
        value = index.data(Qt.UserRole)
        self.setChecked(value)
