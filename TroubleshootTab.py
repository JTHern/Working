import settings
from os import system
from platform import system as system_name
from message_handler import LoggingMessageHandler
from PyQt5.QtWidgets import (QCheckBox, QGridLayout, QGroupBox, QLabel, QMessageBox, QPlainTextEdit, QPushButton,
                             QSpinBox, QVBoxLayout, QWidget)
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


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
        layout.addWidget(self._log_viewer, 0, 0, 3, 5)

        ping = QPushButton("ping",
                            whatsThis="Ping a Device",
                            clicked=self._ping
                            )
        layout.addWidget(ping, 4, 0)
        
        traceroute = QPushButton("Traceroute",
                whatsThis="Traceroute to a device.",
                clicked=self._traceroute)
        layout.addWidget(traceroute, 4, 1)
        
        self.ip = QLineEdit()
        layout.addWidget(self.ip, 4, 2)
        
        routes = QPushButton("Routes",
                whatsThis="show ip route",
                clicked=self._routes)
        layout.addWidget(routes, 5, 0)
        
        interfaces = QPushButton("Interfaces",
                whatsThis="show ip interface brief",
                clicked=self._interfaces)
        layout.addWidget(interfaces, 5, 1)
        
        dmvpn = QPushButton("DMVPN",
                whatsThis="show crypto ikev2 sa",
                clicked=self._dmvpn)
        layout.addWidget(dmvpn, 5, 3)
        
        ospf = QPushButton("OSPF",
                whatsThis="show ip ospf neigh",
                clicked=self._ospf)
        layout.addWidget(ospf, 5, 4)
        
        eigrp = QPushButton("EIGRP",
                whatsThis="show ip eigrp neigh",
                clicked=self._eigrp)
        layout.addWidget(eigrp, 5, 5)
        
        self.setLayout(layout)
        
    '''actions'''
    
    def _ping(self, _):
        """ Invoked when the user clicks the ping button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        """ex: ping 8.8.8.8  or  ping hostname   """
        if system_name().lower() == 'windows':
            output = system(f'ping {self.ip}')
        else:
            output = system(f'ping {self.ip}')
        logger.clear()
        logger.status_message(f"{output}")


    def _traceroute(self, _):
        """ Invoked when the user clicks the traceroute button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
                
        if system_name().lower() == 'windows':
            output = system(f'traceroute {self.ip}')
        else:
            output = system(f'tracert {self.ip}')
        
        logger.clear()
        logger.status_message(f"{output}")

    
    def _routes(self, _):
        """ Invoked when the user clicks the routes button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            device = settings.device[0]
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                logger.status_message("Connecting....")
                output = router.send_command('show ip route')
                router.disconnect()
                logger.status_message(f'{output}')
                
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
            
    def _interfaces(self, _):
        """ Invoked when the user clicks the interfaces button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            device = settings.device[0]
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                logger.status_message("Connecting....")
                output = router.send_command('show ip interface brief')
                router.disconnect()
                logger.status_message(f'{output}')
                
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
    def _dmvpn(self, _):
        """ Invoked when the user clicks the dmvpn button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            device = settings.device[0]
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                logger.status_message("Connecting....")
                output = router.send_command('show crypto ikev2 sa')
                router.disconnect()
                logger.status_message(f'{output}')
                
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
        
    def _ospf(self, _):
        """ Invoked when the user clicks the ospf button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            device = settings.device[0]
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                logger.status_message("Connecting....")
                output = router.send_command('show ip ospf neigh')
                router.disconnect()
                logger.status_message(f'{output}')
                
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
        
    def _eigrp(self, _):
        """ Invoked when the user clicks the eigrp button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            device = settings.device[0]
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                logger.status_message("Connecting....")
                output = router.send_command('show ip eigrp neigh')
                router.disconnect()
                logger.status_message(f'{output}')
                
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
    
    def _vlans(self, _):
        """ Invoked when the user clicks the eigrp button. """

        logger = LoggingMessageHandler(bool(self._verbose_button.checkState()),
                self._log_viewer)
        if settings.device == []:
            logger.clear()
            logger.status_message("Enter Credentials on Router Info tab.")
            logger.status_message("Once entered click Verify.")
        else:
            logger.clear()
            device = settings.device[0]
            try:
                router = ConnectHandler(**device)  # Connect to the Device
                logger.status_message("Connecting....")
                output = router.send_command('show vlan status')
                router.disconnect()
                logger.status_message(f'{output}')
                
            except ValueError:
                logger.status_message("Console is not working. Make sure you have connectivity.")
            except TimeoutError:
                logger.status_message("Telnet Error: Make sure the IP address is correct.")
            except NetMikoTimeoutException:
                logger.status_message("SSH Error: Make sure the IP address is correct.")
            except NetMikoAuthenticationException:
                logger.status_message("Check your username/password. Make sure you have an account on this device.")
            pass
      
