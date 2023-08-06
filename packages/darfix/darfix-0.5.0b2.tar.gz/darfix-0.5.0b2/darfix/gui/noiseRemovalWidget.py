# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "23/09/2020"

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.StackView import StackViewMainWindow

import darfix
from darfix.core.dataset import Operation
from darfix.core.imageOperations import Method

from .operationThread import OperationThread


class _ParametersDock(qt.QDockWidget):

    def __init__(self, parent=None):
        """
        Dock widget containing the input parameters for the noise removal operations.
        """
        qt.QDockWidget.__init__(self, parent)
        widget = qt.QWidget()
        self.layout = qt.QGridLayout()

        # Background subtraction
        bsLabel = qt.QLabel("Background Substraction")
        # Font for operations titles
        font = qt.QFont()
        font.setBold(True)
        bsLabel.setFont(font)
        self.layout.addWidget(bsLabel, 0, 0, 1, 2)
        self.bsMethodsCB = qt.QComboBox(self)
        for method in Method.values():
            self.bsMethodsCB.addItem(method)
        self.bsBackgroundCB = qt.QComboBox(self)
        self.computeBS = qt.QPushButton("Compute")
        self.abortBS = qt.QPushButton("Abort")
        self.abortBS.hide()
        methodLabel = qt.QLabel("Method:")
        bgLabel = qt.QLabel("Background:")
        self.inDiskCheckbox = qt.QCheckBox("Use chunks to compute median")
        # Step widget
        self.stepWidget = qt.QWidget()
        stepLayout = qt.QHBoxLayout()
        stepLayout.addWidget(qt.QLabel("Step:"))
        self.step = qt.QLineEdit("1")
        stepLayout.setContentsMargins(0, 0, 1, 1)
        stepLayout.addWidget(self.step)
        self.stepWidget.setLayout(stepLayout)
        # Chunks widget
        self.chunksWidget = qt.QWidget()
        chunksLayout = qt.QHBoxLayout()
        chunksLabel = qt.QLabel("Chunks:")
        self.verticalChunkSize = qt.QLineEdit("100")
        self.verticalChunkSize.setValidator(qt.QIntValidator())
        self.horizontalChunkSize = qt.QLineEdit("100")
        self.horizontalChunkSize.setValidator(qt.QIntValidator())
        chunksLayout.addWidget(chunksLabel)
        chunksLayout.addWidget(self.verticalChunkSize)
        chunksLayout.addWidget(self.horizontalChunkSize)
        chunksLayout.setContentsMargins(0, 0, 1, 1)
        self.chunksWidget.setLayout(chunksLayout)

        self.inDiskWidget = qt.QWidget()
        inDiskLayout = qt.QVBoxLayout()
        inDiskLayout.addWidget(self.inDiskCheckbox, alignment=qt.Qt.AlignRight)
        inDiskLayout.addWidget(self.stepWidget)
        inDiskLayout.addWidget(self.chunksWidget)
        self.chunksWidget.hide()
        self.inDiskCheckbox.stateChanged.connect(self.toggleChunks)
        self.inDiskWidget.setLayout(inDiskLayout)

        self.layout.addWidget(methodLabel, 1, 0, 1, 0.7)
        self.layout.addWidget(bgLabel, 2, 0, 1, 0.7)
        self.layout.addWidget(self.bsMethodsCB, 1, 1, 1, 1)
        self.layout.addWidget(self.bsBackgroundCB, 2, 1, 1, 1)
        self.layout.addWidget(self.inDiskWidget, 3, 0, 1, 2)
        self.inDiskWidget.hide()
        # Hot pixel removal
        hpLabel = qt.QLabel("Hot Pixel Removal")
        hpLabel.setFont(font)
        self.layout.addWidget(hpLabel, 0, 2, 1, 2)
        ksizeLabel = qt.QLabel("Kernel size:")
        self.layout.addWidget(ksizeLabel, 1, 2, 1, 1)
        self.hpSizeCB = qt.QComboBox(self)
        self.hpSizeCB.addItem("3")
        self.hpSizeCB.addItem("5")
        self.computeHP = qt.QPushButton("Compute")
        self.abortHP = qt.QPushButton("Abort")
        self.layout.addWidget(self.hpSizeCB, 1, 3, 1, 1)
        self.layout.addWidget(self.computeHP, 3, 3, 1, 1)
        self.layout.addWidget(self.abortHP, 3, 2, 1, 1)
        self.abortHP.hide()

        widget.setLayout(self.layout)
        self.setWidget(widget)

    def toggleChunks(self, checked):
        if checked:
            self.chunksWidget.show()
            self.stepWidget.hide()
        else:
            self.chunksWidget.hide()
            self.stepWidget.show()


class NoiseRemovalDialog(qt.QDialog):
    """
    Dialog with `NoiseRemovalWidget` as main window and standard buttons.
    """

    okSignal = qt.Signal()

    def __init__(self, parent=None):
        qt.QDialog.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        types = qt.QDialogButtonBox.Ok
        _buttons = qt.QDialogButtonBox(parent=self)
        _buttons.setStandardButtons(types)
        resetB = _buttons.addButton(_buttons.Reset)
        self.mainWindow = NoiseRemovalWidget(parent=self)
        self.mainWindow.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self.mainWindow)
        self.layout().addWidget(_buttons)

        _buttons.accepted.connect(self.okSignal.emit)
        resetB.clicked.connect(self.mainWindow.resetStack)


class NoiseRemovalWidget(qt.QMainWindow):
    """
    Widget to apply noise removal from a dataset.
    For now it can apply both background subtraction and hot pixel removal.
    For background subtraction the user can choose the background to use:
    dark frames, low intensity data or all the data. From these background
    frames, an image is computed either using the mean or the median.
    """

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        self._update_dataset = None
        self.indices = None
        self.bg_indices = None
        self.bg_dataset = None
        self.setWindowFlags(qt.Qt.Widget)

        self._parametersDock = _ParametersDock()
        self._parametersDock.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._sv = StackViewMainWindow()
        self._sv.setColormap(Colormap(name=darfix.config.DEFAULT_COLORMAP_NAME,
                                      normalization=darfix.config.DEFAULT_COLORMAP_NORM))

        self._size = self._parametersDock.hpSizeCB.currentText()
        self._method = self._parametersDock.bsMethodsCB.currentText()
        self._background = self._parametersDock.bsBackgroundCB.currentText()
        self.setCentralWidget(self._sv)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._parametersDock)
        self._parametersDock.computeBS.clicked.connect(self.__computeBS)
        self._parametersDock.computeHP.clicked.connect(self.__computeHP)
        self._parametersDock.abortBS.clicked.connect(self.__abortBS)
        self._parametersDock.abortHP.clicked.connect(self.__abortHP)
        self._parametersDock.bsMethodsCB.currentTextChanged.connect(self._toggleMethod)

    def __computeBS(self):
        """
        Function that starts the thread to compute the background
        subtraction.
        """
        method = self._parametersDock.bsMethodsCB.currentText()
        background = self._parametersDock.bsBackgroundCB.currentText()
        self._thread = OperationThread(self, self._update_dataset.apply_background_subtraction)
        bg = None
        chunks = None
        step = None
        if background == "Dark data":
            bg = self.bg_dataset
        elif background == "Low intensity data":
            bg = self.bg_indices
        if self._parametersDock.inDiskWidget.isVisible():
            if self._parametersDock.inDiskCheckbox.isChecked():
                chunks = [int(self._parametersDock.verticalChunkSize.text()),
                          int(self._parametersDock.horizontalChunkSize.text())]
            else:
                step = int(self._parametersDock.step.text())
        self._thread.setArgs(bg, method, self.indices, step, chunks)
        self._thread.finished.connect(self._updateData)
        self._parametersDock.abortBS.show()
        self._thread.start()
        self._parametersDock.computeBS.setEnabled(False)
        self._parametersDock.computeHP.setEnabled(False)

    def __computeHP(self):
        """
        Function that starts the thread to compute the hot pixel
        removal.
        """
        self._size = self._parametersDock.hpSizeCB.currentText()
        self._thread = OperationThread(self, self._update_dataset.apply_hot_pixel_removal)
        self._thread.setArgs(int(self._size), self.indices)
        self._thread.finished.connect(self._updateData)
        self._parametersDock.abortHP.show()
        self._thread.start()
        self._parametersDock.computeBS.setEnabled(False)
        self._parametersDock.computeHP.setEnabled(False)

    def __abortBS(self):
        self._parametersDock.abortBS.setEnabled(False)
        self._update_dataset.stop_operation(Operation.BS)

    def __abortHP(self):
        self._parametersDock.abortHP.setEnabled(False)
        self._update_dataset.stop_operation(Operation.HP)

    def _updateData(self):
        """
        Updates the stack with the data computed in the thread
        """
        self._thread.finished.disconnect(self._updateData)
        self._parametersDock.abortBS.setEnabled(True)
        self._parametersDock.abortHP.setEnabled(True)
        self._parametersDock.abortBS.hide()
        self._parametersDock.abortHP.hide()
        self._parametersDock.computeBS.setEnabled(True)
        self._parametersDock.computeHP.setEnabled(True)
        if self._thread.data is not None:
            self._update_dataset = self._thread.data
            self.setStack(self._update_dataset)
        else:
            print("\nComputation aborted")

    def setDataset(self, dataset, indices=None, bg_indices=None, bg_dataset=None):
        """
        Dataset setter. Saves the dataset and updates the stack with the dataset
        data

        :param Dataset dataset: dataset
        """
        self.dataset = dataset
        self._update_dataset = dataset
        self.indices = indices
        self.setStack()
        self.bg_indices = bg_indices
        self.bg_dataset = bg_dataset
        if not dataset.in_memory:
            self._parametersDock.layout.addWidget(self._parametersDock.abortBS, 4, 0, 1, 1)
            self._parametersDock.layout.addWidget(self._parametersDock.computeBS, 4, 1, 1, 1)
        else:
            self._parametersDock.layout.addWidget(self._parametersDock.abortBS, 3, 0, 1, 1)
            self._parametersDock.layout.addWidget(self._parametersDock.computeBS, 3, 1, 1, 1)

        """
        Sets the available background for the user to choose.
        """
        self._parametersDock.bsBackgroundCB.clear()
        if bg_dataset is not None:
            self._parametersDock.bsBackgroundCB.addItem("Dark data")
        if bg_indices is not None:  # TODO: modify
            self._parametersDock.bsBackgroundCB.addItem("Low intensity data")
        self._parametersDock.bsBackgroundCB.addItem("Data")

        self._parametersDock.bsBackgroundCB.currentIndexChanged.connect(self.toggleInDiskWidget)

    def _toggleMethod(self, text):
        if text == Method.mean.value:
            self._parametersDock.inDiskWidget.hide()
        elif text == Method.median.value:
            self.toggleInDiskWidget(self._parametersDock.bsBackgroundCB.currentIndex())

    def toggleInDiskWidget(self, index):
        if self._parametersDock.bsMethodsCB.currentText() == Method.median.value:
            if self.bg_dataset is None:
                self._parametersDock.inDiskWidget.hide() if self.dataset.in_memory else \
                    self._parametersDock.inDiskWidget.show()
            elif not (index or self.bg_dataset.in_memory) or (index and not self.dataset.in_memory):
                self._parametersDock.inDiskWidget.show()
            else:
                self._parametersDock.inDiskWidget.hide()
        else:
            self._parametersDock.inDiskWidget.hide()

    def getDataset(self):
        return self._update_dataset, self.indices, self.bg_indices, self. bg_dataset

    def resetStack(self):
        self.setStack()

    def clearStack(self):
        self._sv.setStack(None)

    def getStack(self):
        return self._sv.getStack(False, True)[0]

    def setStack(self, dataset=None):
        """
        Sets new data to the stack.
        Mantains the current frame showed in the view.

        :param Dataset dataset: if not None, data set to the stack will be from the given dataset.
        """
        if dataset is None:
            dataset = self.dataset
        nframe = self._sv.getFrameNumber()
        self._sv.setStack(dataset.get_data(self.indices))
        self._sv.setFrameNumber(nframe)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self._parametersDock.hpSizeCB.setCurrentText(size)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method
        self._parametersDock.bsMethodsCB.setCurrentText(method)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        self._background = background
        self._parametersDock.bsBackgroundCB.setCurrentText(background)
