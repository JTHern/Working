import settings
import re
from PyQt5.QtCore import (Qt, QThread, pyqtSignal)
from PyQt5.QtWidgets import (QCheckBox, QFileDialog, QGridLayout, QGroupBox, QPlainTextEdit,
                             QPushButton, QVBoxLayout, QWidget)
from message_handler import LoggingMessageHandler
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


class LoadThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    # This Class threads the connection so we don't freeze the entire program waiting on the connection to take place.

    def __init__(self):
        QThread.__init__(self)
        self.config = ''

    # run method gets called when we start() the thread
    def run(self):
        if self.config == '':
            self.signal.emit("No config to load.")
            return
        if settings.device == []:
            self.signal.emit("Enter Credentials on Router Info tab.")
            self.signal.emit("Once entered click Verify.")
            return
        if settings.device[0]['device_type'] == 'cisco_ios_serial':
            device = settings.device[0]
            try:
                self.signal.emit('Loading Configuration....')
                router = ConnectHandler(**device)  # Connect to the Device
                self.signal.emit('...connected...')
                router.enable()
                self.signal.emit('...this may take a while...')
                router.send_config_set(self.config)
                new_config = router.send_command('show run')
                self.signal.emit(new_config)
                router.disconnect()
                self.signal.emit('Load Complete')
            except ValueError:
                self.signal.emit("Console Error: Make sure you have connectivity.")
            except TimeoutError:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoTimeoutException:
                self.signal.emit("Timeout Error: Make sure you are still connected")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")
        else:
            device = settings.device[0]
            try:
                self.signal.emit('Loading Configuration....')
                router = ConnectHandler(**device)  # Connect to the Device
                self.signal.emit('...connected...')
                router.enable()
                self.signal.emit('...this may take a while...')
                router.send_config_set(self.config)
                new_config = router.send_command('show run')
                self.signal.emit(new_config)
                router.disconnect()
                self.signal.emit('Load Complete')
            except ValueError:
                self.signal.emit("User does not have permission to make these changes.")
            except TimeoutError:
                self.signal.emit("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                self.signal.emit("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                self.signal.emit("Check your username/password. Make sure you have an account on this device.")


class LoadPage(QWidget):
    label = "Load"

    def __init__(self, parent=None):
        """ Initialise the page. """

        super().__init__(parent)
        layout = QGridLayout()  # page will use a grid layout

        self.config = ''  # this variable overwritten after config is opened.
        '''Pulls from router tab hopefully'''

        self._log_viewer = QPlainTextEdit(readOnly=True)
        layout.addWidget(self._log_viewer, 0, 0, 5, 1)

        openfile = QPushButton("Open", clicked=self._open)
        openfile.setToolTip("Open a text Config.")
        layout.addWidget(openfile, 0, 1)

        load_options = QGroupBox("Load Options")
        load_layout = QVBoxLayout()

        self._backup_config = ''  # If the box below is checked, write the current config on the box to a text file.
        self._config_backup = QCheckBox("Backup Current \n Config", checked=False,
                                        stateChanged=self.config_backup)
        self._config_backup.setToolTip("Optional - backup the current config before loading the new config.")
        load_layout.addWidget(self._config_backup)

        load_options.setLayout(load_layout)
        layout.addWidget(load_options, 1, 1)

        self.load = QPushButton("Load", clicked=self._load)  # The load button which carries out the load logic.
        self.load.setToolTip("Load a new configuration.")
        layout.addWidget(self.load, 2, 1)
        self.load_thread = LoadThread()
        self.load_thread.signal.connect(self.finished)

        self.setLayout(layout)

    '''actions'''

    def _open(self, _):
        """ Invoked when the user clicks the open button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        fltr = "Text or Config (*.txt *.cfg)"
        obj = QFileDialog.getOpenFileName(self, 'Config to Load', '', fltr)
        if obj[0] == '':
            return
        with open(obj[0], 'r') as file:
            config = file.read()
            logger.clear()
            logger.status_message(config)
            logger.status_message('Remove extra lines from the text file, such as:\n '
                                  ' enable \n config t \n building \n'
                                  ' version \n etc...')
            self.load_thread.config = config

    def _load(self):
        self.load_thread.start()

    def finished(self, result):
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        logger.status_message(result)

    def config_backup(self, state):
        """ currently not operational """

        if state == Qt.Checked:
            self._backup_config = 'yes'
