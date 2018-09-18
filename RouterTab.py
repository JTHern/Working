import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print p

import settings
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QMessageBox,
                             QPlainTextEdit, QPushButton, QWidget)
from message_handler import LoggingMessageHandler
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


class RouterInfo(QWidget):
    label = "RouterInfo"

    def __init__(self):
        """ Initialise the page. """

        super().__init__()
        '''sets up a grid layout for the tab'''
        layout = QGridLayout()  # Page will use a grid layout.

        '''Connection method'''
        self.con_method = ''  # Once the connection method is selected it is stored in this variable.
        con_method_sel = QGroupBox("Connection method")
        con_method_sel_layout = QHBoxLayout()  # Lays out the below buttons horizontally.

        self._console_button = QCheckBox("Console",
                                         whatsThis="console",
                                         checked=False, stateChanged=self._console_button)
        con_method_sel_layout.addWidget(self._console_button)

        self._telnet_button = QCheckBox("Telnet",
                                        whatsThis="telnet",
                                        checked=False, stateChanged=self._telnet_button)
        con_method_sel_layout.addWidget(self._telnet_button)

        self._ssh_button = QCheckBox("SSH",
                                     whatsThis="ssh",
                                     checked=False, stateChanged=self._ssh_button)
        con_method_sel_layout.addWidget(self._ssh_button)

        con_method_sel.setLayout(con_method_sel_layout)
        layout.addWidget(con_method_sel, 0, 1)

        '''The username field and label'''
        label1 = QLabel('           Username')
        layout.addWidget(label1, 1, 0)
        self.username = QLineEdit()
        layout.addWidget(self.username, 1, 1)

        '''The password field and label'''
        label2 = QLabel('           Password')
        layout.addWidget(label2, 2, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)  # turn off echo mode for password
        layout.addWidget(self.password, 2, 1)

        '''The ip field and label'''
        label3 = QLabel('     COM Port or IP')
        layout.addWidget(label3, 3, 0)
        self.ip = QLineEdit()
        layout.addWidget(self.ip, 3, 1)

        '''The verify pushbutton'''
        verify = QPushButton("Verify",
                             whatsThis="Select IOS configuration to load.",
                             clicked=self.verify
                             )
        layout.addWidget(verify, 3, 2)

        label0 = QLabel('Once credentials are set click Verify.')
        layout.addWidget(label0, 4, 1)

        '''The output screen'''
        self._log_viewer = QPlainTextEdit(
            whatsThis="This displays the messages generated when loading the router.", readOnly=True)
        layout.addWidget(self._log_viewer, 5, 1, 1, 1)

        '''Displays the layout'''
        self.setLayout(layout)

    '''These fields allow for actions to take place based on the above input.'''

    def verify(self):
        """ Verifies the credentials supplied button. """
        logger = LoggingMessageHandler(bool(), self._log_viewer)
        if self.con_method == 'cisco_ios_serial':
            if 'COM' not in self.ip.text():
                logger = LoggingMessageHandler(bool(), self._log_viewer)
                logger.clear()
                logger.status_message("Com Port field requires COM1 or COM2 or COM3 etc...")
                return
            if self.ip.text() == '' or self.username.text() == '' or self.password.text() == '':
                logger = LoggingMessageHandler(bool(), self._log_viewer)
                logger.clear()
                logger.status_message("All Fields must be Completed.")
                return
            device = {
                'device_type': self.con_method,
                'username': self.username.text(),
                'password': self.password.text(),
                'serial_settings': {'port': self.ip.text()}
            }
            settings.device.append(device)
            try:
                console = ConnectHandler(**device)  # Connect to the Device to verify credentials.
                console.disconnect()
                logger.status_message('Credentials Verified on Console!')
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass

        elif self.con_method == 'cisco_ios_telnet':
            if self.ip.text() == '' or self.username.text() == '' or self.password.text() == '':
                logger = LoggingMessageHandler(bool(), self._log_viewer)
                logger.clear()
                logger.status_message("All Fields must be Completed.")
                return
            device = {
                'device_type': self.con_method,
                'ip': self.ip.text(),
                'username': self.username.text(),
                'password': self.password.text()
            }
            settings.device.append(device)
            try:
                telnet = ConnectHandler(**device)  # Connect to the Device to verify credentials.
                telnet.disconnect()
                logger.status_message('Credentials Verified on Telnet!')
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass

        elif self.con_method == 'cisco_ios':
            if self.ip.text() == '' or self.username.text() == '' or self.password.text() == '':
                logger = LoggingMessageHandler(bool(), self._log_viewer)
                logger.clear()
                logger.status_message("All Fields must be Completed.")
                return
            device = {
                'device_type': self.con_method,
                'ip': self.ip.text(),
                'username': self.username.text(),
                'password': self.password.text()
            }
            settings.device.append(device)
            try:
                ssh = ConnectHandler(**device)  # Connect to the Device to verify credentials.
                ssh.disconnect()
                logger.status_message('Credentials Verified on SSH!')
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
        else:
            logger.clear()
            logger.status_message("All Fields must be Completed.")
            return

    def _console_button(self, state):
        """ if console is checked uncheck the others """

        if state == Qt.Checked:
            self._telnet_button.setCheckState(Qt.Unchecked)
            self._ssh_button.setCheckState(Qt.Unchecked)
            self.con_method = 'cisco_ios_serial'

    def _telnet_button(self, state):
        """ if telnet is checked uncheck the others """

        if state == Qt.Checked:
            self._console_button.setCheckState(Qt.Unchecked)
            self._ssh_button.setCheckState(Qt.Unchecked)
            self.con_method = 'cisco_ios_telnet'

    def _ssh_button(self, state):
        """ if ssh is checked uncheck the others """

        if state == Qt.Checked:
            self._console_button.setCheckState(Qt.Unchecked)
            self._telnet_button.setCheckState(Qt.Unchecked)
            self.con_method = 'cisco_ios'
