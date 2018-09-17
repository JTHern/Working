from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QFileDialog, QGridLayout, QGroupBox, QLabel, QMessageBox, QPlainTextEdit,
                             QPushButton, QSpinBox, QVBoxLayout, QWidget)
from message_handler import LoggingMessageHandler
import settings


class LoadPage(QWidget):
    label = "Load"

    def __init__(self):
        """ Initialise the page. """

        super().__init__()
        layout = QGridLayout()  # page will use a grid layout

        self.config = ''  # this variable overwritten after config is opened.

        '''Pulls from router tab hopefully'''
        self._log_viewer = QPlainTextEdit(
            whatsThis="This displays the messages generated when loading the router.",
                readOnly=True)
        layout.addWidget(self._log_viewer, 0, 0, 5, 1)

        openfile = QPushButton("Open",
                            whatsThis="Select IOS configuration to load.",
                            clicked=self._open
                            )
        layout.addWidget(openfile, 0, 1)

        build = QPushButton("Load",
                            whatsThis="Load an IOS configuration. ",
                            clicked=self._load
                            )
        layout.addWidget(build, 2, 1)

        optimisation = QGroupBox("Options")
        optimisation_layout = QVBoxLayout()

        self._opt1_button = QCheckBox("Verify IOS\n Version",
                whatsThis="Verify the IOS version before loading.",
                checked=True, stateChanged=self._opt1_changed)
        optimisation_layout.addWidget(self._opt1_button)
        self._opt2_button = QCheckBox("Backup Current \n Config",
                whatsThis="Backup current config before starting.",
                checked=True, stateChanged=self._opt2_changed)
        optimisation_layout.addWidget(self._opt2_button)

        optimisation.setLayout(optimisation_layout)
        layout.addWidget(optimisation, 1, 1)

        options = QGroupBox("Load Options")
        options_layout = QGridLayout()

        options_layout.addWidget(QLabel("test1"), 2, 0)
        self._resources_edit = QSpinBox(
                whatsThis="test1",
                minimum=1)
        options_layout.addWidget(self._resources_edit, 2, 1)

        options_layout.addWidget(QLabel("Timeout"), 3, 0)
        self._timeout_edit = QSpinBox(
                whatsThis="Number of milliseconds to adjust config load speed",
                minimum=1)
        self._timeout_edit.setValue(1)
        options_layout.addWidget(self._timeout_edit, 3, 1)

        options.setLayout(options_layout)
        layout.addWidget(options, 3, 1)

        zero = QPushButton("Zeroize",
                whatsThis="Zeroize the IOS configuration. ",
                clicked=self._zero)
        layout.addWidget(zero, 4, 1)

        layout.setRowStretch(4, 1)

        self.setLayout(layout)
    '''actions'''

    def _open(self, _):
        """ Invoked when the user clicks the open button. """
        fltr = "Text or Config (*.txt *.cfg)"
        obj = QFileDialog.getOpenFileName(self, 'Config to Load', '', fltr)
        if obj[0] == '':
            return
        with open(obj[0], 'r') as file:
            config = file.read()
            logger = LoggingMessageHandler(bool(), self._log_viewer)
            logger.clear()
            logger.status_message(config)
            self.config = config

    def _load(self, _):
        """ Invoked when the user clicks the load button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        if self.config == '':
            logger.clear()
            logger.status_message("No config to load.")
            return
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            logger.status_message("Verifying Cisco IOS version")
            logger.status_message("Loading Configuration....")
            logger.status_message("Load Complete")

    def _missing_prereq(self, missing):
        """ Tell the user about a missing prerequisite. """

        QMessageBox.warning(self, self.label, "The project cannot be built because the name of the {0} has "
                        "not been set.".format(missing))

    def _opt1_changed(self, state):
        """ Invoked when the user clicks on the no asserts button. """

        if state == Qt.Unchecked:
            self._opt2_button.setCheckState(Qt.Unchecked)

    def _opt2_changed(self, state):
        """ Invoked when the user clicks on the no docstrings button. """

        if state == Qt.Checked:
            self._opt1_button.setCheckState(Qt.Checked)

    def _run_qmake_changed(self, state):
        """ Invoked when the user clicks on the run qmake button. """

        if state == Qt.Unchecked:
            self._run_make_button.setCheckState(Qt.Unchecked)

    def _run_make_changed(self, state):
        """ Invoked when the user clicks on the run make button. """

        if state == Qt.Unchecked:
            self._run_application_button.setCheckState(Qt.Unchecked)
        else:
            self._run_qmake_button.setCheckState(Qt.Checked)

    def _zero(self, _):
        """ Invoked when the user clicks on the run application button. """
        logger = LoggingMessageHandler(bool(),
                                       self._log_viewer)

        logger.clear()
        logger.status_message("Zeroizing Configuration")
