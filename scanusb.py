import os
import math
import psutil
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea

def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy -= p_x * math.log(p_x, 2)
    return entropy

def scan_directory(directory):
    suspicious_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                    entropy = calculate_entropy(data)
                    if entropy > 7.5:  # Threshold for high entropy
                        suspicious_files.append((file_path, entropy))
            except (PermissionError, FileNotFoundError):
                continue  # Skip inaccessible files
    return suspicious_files

def get_usb_drives():
    usb_drives = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            usb_drives.append(partition.mountpoint)
    return usb_drives

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Drive Scanner")
        self.setGeometry(200, 200, 1300, 700)
        self.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; padding: 10px; font-size: 16px; color: #ffffff; text-align: left;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()  # Vertical layout
        
        # Create a QScrollArea
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.result_label = QLabel("Scan results will appear here.", self.scroll_content)
        self.result_label.setStyleSheet("color: red;")
        self.scroll_layout.addWidget(self.result_label) 
        self.scroll_area.setWidget(self.scroll_content)
        self.legend = QLabel("<h2 style='color: green;'>SAFE<br></h2><h2 style='color: yellow;'>UNSAFE<br></h2><h2 style='color: red;'>SUSPICIOUS</h2>",self)
        self.legend.setGeometry(1050,0,250,200)
        self.legend.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; padding: 10px; border: 4px solid orange")
        # Add the scroll area to the main layout
        layout.addWidget(self.scroll_area)
        self.setLayout(layout) 
        self.start_scan()
    def start_scan(self):
        self.result_label.setText("<h2 style='color: orange; margin: 10;'>SCANNING...</h2>")  # Update label
        scan_thread = threading.Thread(target=self.scan_usb_drives)
        scan_thread.start()  # Start the scan in a new thread

    def scan_usb_drives(self):
        usb_drives = get_usb_drives()
        
        if not usb_drives:
            self.result_label.setText("No USB drives found.")
            return
        
        self.results = []
        for drive in usb_drives:
            self.results.append(f"Scanning USB drive: {drive}")
            suspicious_files = scan_directory(drive)
            #
            if suspicious_files:
                for file_path, entropy in suspicious_files:
                    if entropy > 7.90:
                        self.results.append(f"<span style='color: green; font-size: 15px;'>{file_path} - Entropy: {entropy:.2f}</span>")
                    elif entropy<7.90 and entropy>7.70:
                        self.results.append(f"<span style='color: yellow; font-size: 15px;'>{file_path} - Entropy: {entropy:.2f}</span>")
                    else:
                        self.results.append(f"<span style='color: red; font-size: 15px;'>{file_path} - Entropy: {entropy:.2f}</span>")
            else:
                self.results.append("No suspicious files found.")
        
        # Update the label with the self.results
        self.legend.deleteLater()
        self.result_label.setText("<br>".join(self.results))  # Use <br> for line breaks in HTML

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Show the window
    sys.exit(app.exec_())  # Start the event loop