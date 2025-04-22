import socket
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor

class VPNClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_ip = self.get_local_ip()  # Get the local IP
        self.exit_node_ip = "Not Connected"  # Placeholder for exit node IP
        self.timer_value = 300  # 5 minutes countdown (in seconds)
        self.vpn_running = False
        self.timer = QTimer(self)

        self.initUI()

    def initUI(self):
        # Set dark grey background color
        self.setStyleSheet("background-color: #2e2e2e;")
        
        # Main layout for the window
        layout = QVBoxLayout()

        # Round VPN button in the center
        self.vpn_button = QPushButton(self)
        self.vpn_button.setFixedSize(150, 150)  # Round button with equal width and height
        self.vpn_button.setStyleSheet(""" 
            QPushButton {
                background-color: #d3d3d3;  /* Light grey */
                border-radius: 75px;  /* Round button */
                font-size: 18px;
                color: black;
            }
        """)
        self.vpn_button.clicked.connect(self.toggle_vpn)
        self.update_vpn_button_shadow()

        # Square box for current IP and timer
        ip_timer_box = QWidget(self)
        ip_timer_box.setStyleSheet("background-color: #2e2e2e; border: none;")  # Match background
        ip_timer_layout = QVBoxLayout(ip_timer_box)

        self.ip_label = QLabel(f'Current IP: {self.current_ip}', self)
        self.ip_label.setAlignment(Qt.AlignCenter)
        self.ip_label.setStyleSheet("font-size: 16px; color: #ffffff;")  # White text

        self.timer_label = QLabel(f'Time until next node switch: {self.timer_value} seconds', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 16px; color: #00ff00;")  # Green text

        ip_timer_layout.addWidget(self.ip_label)
        ip_timer_layout.addWidget(self.timer_label)

        # Set up the window layout
        layout.addStretch()
        layout.addWidget(self.vpn_button, 0, Qt.AlignCenter)
        layout.addSpacing(20)  # Space between buttons and IP/timer area
        layout.addWidget(ip_timer_box, 0, Qt.AlignCenter)

        # Set up the main container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set window properties
        self.setWindowTitle('VPN Client')
        self.setFixedSize(400, 300)  # Fixed size for the window
        self.show()

        # Timer connection
        self.timer.timeout.connect(self.update_timer)

    def get_local_ip(self):
        # Get the local IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Connect to a public DNS
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = "Unable to get IP"
        finally:
            s.close()
        return local_ip

    def update_timer(self):
        # Decrease the timer value every second
        if self.timer_value > 0:
            self.timer_value -= 1
            self.timer_label.setText(f'Time until next node switch: {self.timer_value} seconds')
        else:
            self.switch_exit_node()

    def switch_exit_node(self):
        # Change to a new exit node IP
        self.exit_node_ip = "123.45.67.89"  # Example new IP after node switch
        self.ip_label.setText(f'Current IP: {self.exit_node_ip}')
        self.timer_value = 300  # Reset to 5 minutes
        self.timer_label.setText(f'Time until next node switch: {self.timer_value} seconds')

    def toggle_vpn(self):
        if not self.vpn_running:
            self.vpn_running = True
            self.vpn_button.setText('Stop VPN')
            self.exit_node_ip = "Connecting..."
            self.ip_label.setText(f'Current IP: {self.exit_node_ip}')
            self.start_timer()
        else:
            self.vpn_running = False
            self.ip_label.setText(f'Current IP: {self.get_local_ip()}')  # Show local IP when VPN is stopped
            self.vpn_button.setText('Start VPN')
            self.stop_timer()

        self.update_vpn_button_shadow()

    def start_timer(self):
        if not self.timer.isActive():  # Start timer only if it's not already running
            self.timer_value = 300  # Reset to 5 minutes when starting
            self.timer.start(1000)  # Start timer to call update_timer every second
            self.timer_label.setText(f'Time until next node switch: {self.timer_value} seconds')

    def stop_timer(self):
        self.timer.stop()
        self.timer_value = 300  # Reset the timer value when stopping
        self.timer_label.setText(f'Time until next node switch: {self.timer_value} seconds')

    def update_vpn_button_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        if self.vpn_running:
            shadow.setColor(QColor(0, 255, 0))  # Green shadow for VPN on
        else:
            shadow.setColor(QColor(255, 0, 0))  # Red shadow for VPN off
        shadow.setBlurRadius(50)
        self.vpn_button.setGraphicsEffect(shadow)

if __name__ == '__main__':
    app = QApplication([])
    ex = VPNClientGUI()
    app.exec_()
