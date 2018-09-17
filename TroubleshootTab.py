from os import system
from platform import system as system_name
from message_handler import LoggingMessageHandler
from PyQt5.QtWidgets import (QCheckBox, QGridLayout, QGroupBox, QLabel, QMessageBox, QPlainTextEdit, QPushButton,
                             QSpinBox, QVBoxLayout, QWidget)


class Troubleshoot(QWidget):
    """ The GUI for the build page of a project. """

    # The page's label.
    label = "Troubleshooting"

    def __init__(self):
        """ Initialise the page. """

        super().__init__()

        self.project = None

        # Create the page's GUI.
        layout = QGridLayout()

        self._log_viewer = QPlainTextEdit(
            whatsThis="This displays the messages generated when loading the router.",
                readOnly=True)
        layout.addWidget(self._log_viewer, 0, 0, 4, 1)

        ping = QPushButton("ping",
                            whatsThis="Ping a Device",
                            clicked=self._ping
                            )
        layout.addWidget(ping, 4, 0)


        traceroute = QPushButton("Traceroute",
                whatsThis="Traceroute to a device.",
                clicked=self._traceroute)
        layout.addWidget(traceroute, 4, 1)

        layout.setRowStretch(4, 1)

        self.setLayout(layout)
    '''actions'''
    def _ping(self, _):
        """ Invoked when the user clicks the build button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        """ex: ping 8.8.8.8  or  ping hostname   """
        if system_name().lower() == 'windows':
            system(f'ping {arg}')
        else:
            system(f'ping {arg}')
        logger.clear()
        logger.status_message("Verifying Cisco IOS version")
        logger.status_message("Loading Configuration....")
        logger.status_message("Load Complete")

    def _traceroute(self, _):
        """ Invoked when the user clicks the build button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)

        logger.clear()
        logger.status_message("Verifying Cisco IOS version")
        logger.status_message("Loading Configuration....")
        logger.status_message("Load Complete")
