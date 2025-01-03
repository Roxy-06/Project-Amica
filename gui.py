from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSlider, QCheckBox
)
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt, QSize
import sys
import platform
import psutil
import subprocess
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRectF
import screen_brightness_control as sbc
from screen_brightness_control import get_brightness,set_brightness
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
import speedtest
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from io import BytesIO
from matplotlib.figure import Figure
import time
import socket

class Activate(QThread):
    def run(self):
        try:
            # Run main.py in a separate process
            subprocess.run(["python", "main.py"], check=True)
        except Exception as e:
            print(f"Error while running main.py: {e}")

class ScanUSB(QThread):
    def run(self):
        try:
            # Run main.py in a separate process
            subprocess.run(["python", "scanusb.py"], check=True)
        except Exception as e:
            print(f"Error while running : {e}")

class WifiSpeedWorker(QThread):
    speed_result = pyqtSignal(str)  # Signal to send results back to the main thread

    def run(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1e6  # Convert to Mbps
            upload_speed = st.upload() / 1e6  # Convert to Mbps
            ping = st.results.ping
            result = f"<h2 style='color: #ff9203; text-align: center;'>Download: {download_speed:.2f} Mbps<br>Upload: {upload_speed:.2f} Mbps<br>Ping: {ping:.2f} ms</h2>"
        except Exception as e:
            result = f"<h3 style='color: red;'>Error: {str(e)}</h3>"
        self.speed_result.emit(result)

class Health(QThread):
    def run(self):
        try:
            # Run main.py in a separate process
            subprocess.run(["python", "health.py"], check=True)
        except Exception as e:
            print(f"Error while running : {e}")

class Corecheck(QThread):
    def run(self):
        try:
            subprocess.run(["python", "cpumoniter.py"], check=True)
        except Exception as e:
            print(f"Error while running : {e}")

class URLSECURITY(QThread):
    def run(self):
        try:
            subprocess.run(["python", "cybersecurity.py"], check=True)
        except Exception as e:
            print(f"Error while running : {e}")

class ANTIVIRUS(QThread):
    def run(self):
        try:
            subprocess.run("mrt", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            pass

class amica(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Amica: To Infinity & Beyond")
        self.setGeometry(100,100,1200,700)
        self.setStyleSheet("background-color: #000000;")
        self.initUI()
        self.setWindowIcon(QIcon("amica.png"))
        self.setIconSize(QSize(100,100))
        self.graph_timer = QTimer()
        self.graph_timer.timeout.connect(self.update_graph)

        # Data for the graph
        self.cpu_usage = []
        self.memory_usage = []
        self.battery_level = []
        devices = AudioUtilities.GetSpeakers()
        self.interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

    def initUI(self):
        central=QWidget()
        self.setCentralWidget(central)
        #--------------------------------------------L1 LABEL-----------------------------------------------------------
        name=platform.system()
        l1=QLabel(f"<h2 style='color: white; margin: 10;'>DEVICE:{name}<br></h2>",self)
        l1.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        l1.setGeometry(10,10,330,680)
        l1.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; padding: 10px; font-size: 16px; color: #ffffff; text-align: left;")
        #---------------------------------------------L1 LOGO----------------------------------------------------------
        pixmap = QPixmap(r"D:\AMICA\photos\mica1.png")
        logo=QLabel(self)
        logo.setGeometry(50,90,250,250)
        logo.setScaledContents(True)
        logo.setStyleSheet("background-color: rgb(28, 29, 31);  border-radius: 125px;")
        logo.setPixmap(pixmap)
        #----------------------------------------------BUTTONS----------------------------------------------------
        self.B1 = QPushButton("STORAGE",self)
        self.B1.setGeometry(30,370,280, 50)
        self.B1.setStyleSheet(
            """
            QPushButton {
                background-color: #fa294b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a8082b;
            }
            """
        )

        self.B2 = QPushButton("ANTIVIRUS",self)
        self.B2.setGeometry(30,430,280, 50)
        self.B2.setStyleSheet(
            """
            QPushButton {
                background-color: #fa294b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a8082b;
            }
            """
        )

        self.B3 = QPushButton("CHECK URL SECURITY",self)
        self.B3.setGeometry(30,490,280, 50)
        self.B3.setStyleSheet(
            """
            QPushButton {
                background-color: #fa294b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a8082b;
            }
            """
        )

        self.B4 = QPushButton("SYSTEM CHECK",self)
        self.B4.setGeometry(30,550,280, 50)
        self.B4.setStyleSheet(
           """
            QPushButton {
                background-color: #fa294b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a8082b;
            }
            """
        )

        self.B5 = QPushButton("I-CORE ACTIVITY",self)
        self.B5.setGeometry(30,610,280, 50)
        self.B5.setStyleSheet(
            """
            QPushButton {
                background-color: #fa294b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a8082b;
            }
            """
        )
        #---------------------------------------------------------------------------------------------------------------
        
        #--------------------------------------------L3 LABEL----------------------------------------------------------
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    
        # Get the volume level
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = self.volume.GetMasterVolumeLevelScalar()  # Returns a float between 0.0 and 1.0

        # Convert to percentage
        current_volume_percentage = current_volume * 100
        cvos=current_volume_percentage
        #---------------------------------------------------------------------------------------------------------------
        l3=QLabel("<h2 style='color: white; margin: 10;'>CONTROL PANEL<br></h2> ",self)
        l3.setGeometry(890,10,300,680)
        l3.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        l3.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; padding: 10px; font-size: 16px; color: #ffffff; text-align: left;")    
        #--------------------------------------POWER BUTTON---------------------------------------------------------
        brightnlvl= sbc.get_brightness()
        self.currentb=int(brightnlvl[0])
        p_button = QLabel(self)
        p_button.setGeometry(1000,90,80,75)
        pixmap1 = QPixmap(r"D:\AMICA\photos\power2.png")
        p_button.setPixmap(pixmap1)
        p_button.setScaledContents(True)
        self.button6 = QPushButton("Activate",self)
        self.button6.setGeometry(980,170,120,40)
        self.button6.setStyleSheet(
            """
            QPushButton {
                background-color: #0dbeff;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(29, 83, 208);
            }
            """
        )
        self.button6.clicked.connect(self.act_main)
        #---------------------------------------BRIGHTNESS LEVEL---------------------------------------------------------
        temp = QLabel("<h3 style='color: #0dbeff;'>LUMINOSITY<br></h3>",self)
        temp.setGeometry(910,250,170,100)
        temp.setAlignment(Qt.AlignLeft)
        temp.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #0dbeff; border-radius: 10px; padding: 10px;color: #ffffff; text-align: left;")
        self.br_sh=QLabel(f"<h1 style='color: #0dbeff;'>{self.currentb}</h1>",self)
        self.br_sh.setGeometry(970,290,70,50)
        self.br_sh.setStyleSheet("background-color: rgb(28, 29, 31);")
        self.sld=QLabel(self)
        self.sld.setGeometry(1110,250,60,210)
        self.sld.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #0dbeff; border-radius: 10px; padding: 10px;color: #ffffff; text-align: left;")
        self.l_sld=QSlider(Qt.Vertical,self)
        self.l_sld.move(100,20)
        self.l_sld.setGeometry(1125,257,30,85)
        self.l_sld.setStyleSheet("background-color: rgb(28, 29, 31);") 
        self.l_sld.setValue(self.currentb)
        self.l_sld.valueChanged.connect(self.update_brg)
        #------------------------------------------VOLUME LEVEL-------------------------------------------------------
        self.v_sld=QSlider(Qt.Vertical,self)
        self.v_sld.move(100,20)
        self.v_sld.setGeometry(1125,367,30,85)
        self.v_sld.setStyleSheet("background-color: rgb(28, 29, 31);")
        self.v_sld.setValue(int(cvos))
        self.v_sld.setRange(0, 101)
        self.v_sld.valueChanged.connect(self.update_vol)
        vol = QLabel("<h2 style='color: #0dbeff;'>VOLUME<br></h2>",self)
        vol.setGeometry(910,360,170,100)
        vol.setAlignment(Qt.AlignLeft)
        vol.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #0dbeff; border-radius: 10px; padding-top: 10px;padding-left: 25px;color: #ffffff; text-align: left;")
        self.vo_sh=QLabel(f"<h1 style='color: #0dbeff;'>{int(cvos)}</h1>",self)
        self.vo_sh.setGeometry(965,400,70,50)
        self.vo_sh.setStyleSheet("background-color: rgb(28, 29, 31);")
        #------------------------------------------THE THERMO STAT BOX-------------------------------------------------------
        last=QLabel(self)
        last.setGeometry(910,470,260,200)
        last.setStyleSheet("background-color: rgb(28, 29, 31);border: 4px solid #0dbeff; border-radius: 10px; color:#0dbeff; font-size:20px; font-weight: bold; padding-top: 0px;")

        check = QLabel("MONITOR ACTIVITY<br><br>USB DRIVE<br><br>WIFI STATUS<br><br>AMICA  ",self)
        check.setAlignment(Qt.AlignLeft)
        check.setGeometry(920,480,240,180)
        check.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; color:#0dbeff; font-size:20px; font-weight: bold; padding-top: 5px;")
        self.scanbutton = QPushButton("SCAN",self)
        self.scanbutton.setStyleSheet(
            """
            QPushButton {
                background-color: #0dbeff;
                color: white;
                font-size: 10px;
                font-weight: bold;
                border-radius: 15px;
                padding: 7px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(29, 83, 208);
            }
            """
        )
        self.scanbutton.setGeometry(1085,530,60,30)
        self.scanbutton.clicked.connect(self.scan_usb)
        self.c1=QCheckBox(self)
        self.c1.setGeometry(1135,485,25,25)
        self.c1.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 13px;")
        self.c1.setChecked(False)
        self.wfi_s=QPushButton("CHECK",self)
        self.wfi_s.setStyleSheet(
            """
            QPushButton {
                background-color: #0dbeff;
                color: white;
                font-size: 10px;
                font-weight: bold;
                border-radius: 15px;
                padding: 7px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(29, 83, 208);
            }
            """
        )
        self.wfi_s.setGeometry(1085,578,60,30)
        self.wfi_s.clicked.connect(self.show_wifi_speed)
        self.c1.stateChanged.connect(self.checkbox)
        self.gc =QPushButton("ALL COMMANDS",self)
        self.gc.setGeometry(1020,624,125,30)
        self.gc.setStyleSheet(
            """
            QPushButton {
                background-color: #0dbeff;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border-radius: 15px;
                padding: 7px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(29, 83, 208);
            }
            """
        )
        self.gc.clicked.connect(self.commands)

 #--------------------------------------------L2 LABEL-----------------------------------------------------------
        name = platform.system()
        l2=QLabel("<h2 style='color: white; margin: 10;'>Amica: To Infinty & Beyond<br></h2>",self)
        l2.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        l2.setGeometry(350,10,530,680)
        l2.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; padding: 10px; font-size: 16px; color: #ffffff; text-align: left;")
        self.tab1= QLabel(self)
        self.tab1.setGeometry(370,90,490,250)
        self.tab1.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #ff9203; border-radius: 10px; color: #ffffff;")
        world=QPixmap(r"D:\AMICA\photos\wmap.png")
        self.tab1.setPixmap(world)
        self.tab1.setScaledContents(True)
        self.graph= QLabel(self)
        self.graph.setGeometry(370,350,490,220)
        self.graph.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #ff9203; border-radius: 10px; color: #ffffff;")
        # display_p= QLabel("YOUR PROMPT ",self)
        # display_p.setGeometry(370,580,490,100)
        # display_p.setStyleSheet("background-color: rgb(28, 29, 31); border-radius: 10px; font-size: 21px; color:#ff9203; font-weight: bold;")
        hostname = socket.gethostname()
        prompt = QLabel(self)
        prompt.setGeometry(370,580,490,100)
        prompt.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #ff9203; border-radius: 10px; color: #ff9203; font-size: 14px;")
        prompt.setText(f"<h2 style='color: orange; margin: 10;'>SYSTEM NAME : {hostname}</h2>")
        self.wfi_s.clicked.connect(self.show_wifi_speed)
        self.worker = WifiSpeedWorker()
        self.worker.speed_result.connect(self.update_wifi_speed)

        # Timer to restore default image
        self.timer = QTimer()
        self.timer.setInterval(15000)  # Restore after 5 seconds
        self.timer.timeout.connect(self.restore_image)

        # (Existing setup code remains unchanged)
        # Add graph area
        self.graph_canvas = FigureCanvas(Figure(figsize=(6, 6)))
        self.graph_layout = QVBoxLayout()
        self.graph_layout.addWidget(self.graph_canvas)
        self.graph_axes = self.graph_canvas.figure.add_subplot(111)

        # Graph area integration
        self.graph.setLayout(self.graph_layout)
        self.c1.stateChanged.connect(self.checkbox)
        self.graph_canvas.figure.set_facecolor("#1c1d1f")  # RGB(28, 29, 31) in hex
        self.graph_axes.set_facecolor("#1c1d1f")
        # Set graph title and labels
        self.graph_axes.set_title("System Resource Usage", color="white")
        self.graph_axes.set_xlabel("Time", color="white")
        self.graph_axes.set_ylabel("Percentage (%)", color="white")
        self.graph_axes.spines['top'].set_color('#1c1d1f')
        self.graph_axes.spines['bottom'].set_color('#1c1d1f')
        self.graph_axes.spines['left'].set_color('#1c1d1f')
        self.graph_axes.spines['right'].set_color('#1c1d1f')
        self.graph_axes.tick_params(axis="x", colors="white")
        self.graph_axes.tick_params(axis="y", colors="white")
        self.graph_axes.set_facecolor("#1c1d1f")
        self.graph_axes.clear()
        self.graph_canvas.draw()
        self.graph.clear()
        glitchider = QLabel(self)
        glitchider.setGeometry(820,360,30,200)
        glitchider.setStyleSheet("background-color: rgb(28, 29, 31);")
        self.fhidder= QLabel(self)
        self.fhidder.setGeometry(370,350,490,220)
        self.fhidder.setStyleSheet("background-color: rgb(28, 29, 31); border: 4px solid #ff9203; border-radius: 10px; color: #ffffff;")
        self.commandtime = QTimer()
        self.commandtime.setInterval(30000)
        self.commandtime.timeout.connect(self.restore_image)
        self.mainrunner = Activate()
        self.usbscan = ScanUSB()
        self.health = Health()
        self.B4.clicked.connect(self.sys_health)
        self.core = Corecheck()
        self.B5.clicked.connect(self.core_view)
        self.urlsec = URLSECURITY()
        self.B3.clicked.connect(self.url_check)
        self.mrt = ANTIVIRUS()
        self.B2.clicked.connect(self.antivirus)
        self.B1.clicked.connect(self.get_partition_info)

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx[FUNCTIONS]xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    def show_wifi_speed(self):
        self.tab1.setText("<h2 style='color: #ff9203; text-align: center;'>LOADING...</h2>")
        self.worker.start()

    def update_wifi_speed(self, result):
        self.tab1.setText(result)
        self.timer.start()

    def restore_image(self):
        self.timer.stop()
        self.tab1.setPixmap(QPixmap("wmap.png").scaled(self.tab1.size(), Qt.KeepAspectRatio))

    def checkbox(self, state):
        if state == 2:  # Checked
            self.fhidder.hide()
            self.graph_timer.start(1000)  # Update graph every second
        else:  # Unchecked
            self.graph_timer.stop()
            self.graph_axes.clear()
            self.graph_canvas.draw()
            self.graph.clear()
            self.fhidder.show()#ff9203; border-radius: 10px; color: #ffffff;")

    def clear_graph(self):
        self.graph_canvas.figure.clf()  # Clear the entire figure
        self.graph_canvas.draw()  # Redraw the canvas

    def update_graph(self):
        # Fetch system stats
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        battery = psutil.sensors_battery().percent if psutil.sensors_battery() else 0

        # Append to lists
        self.cpu_usage.append(cpu)
        self.memory_usage.append(memory)
        self.battery_level.append(battery)

        # Keep only the last 20 data points for visualization
        if len(self.cpu_usage) > 300:
            self.cpu_usage.pop(0)
            self.memory_usage.pop(0)
            self.battery_level.pop(0)

        # Clear and set up the graph axes
        self.graph_axes.clear()
        self.graph_canvas.figure.set_facecolor("#1c1d1f")  # Background color
        self.graph_axes.set_facecolor("#1c1d1f")
        self.graph_axes.tick_params(axis="x", colors="white")
        self.graph_axes.tick_params(axis="y", colors="white")
        self.graph_axes.text(0, 110, "CPU", color="#0dbeff", fontsize=10, ha="center", va="center")
        self.graph_axes.text(len(self.memory_usage), 110, "Memory", color="#7b19e3", fontsize=10, ha="center", va="center")
        self.graph_axes.text(len(self.memory_usage)/2, 110, "Battery", color="#fa294b", fontsize=10, ha="center", va="center")
            # Plot the data
        self.graph_axes.plot(self.cpu_usage, label="CPU Usage (%)", color="#0dbeff")
        self.graph_axes.plot(self.memory_usage, label="Memory Usage (%)", color="#7b19e3")
        self.graph_axes.plot(self.battery_level, label="Battery Level (%)", color="#fa294b")
        self.graph_axes.set_ylim(0, 100)
        self.graph_canvas.draw()

    def update_vol(self):
        try:
            new_volume = self.v_sld.value()
            self.volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
            self.vo_sh.setText(f"<h1 style='color: #0dbeff;'>{new_volume}</h1>")
        except Exception as e:
            pass

    def update_brg(self):
        newb=self.l_sld.value()
        set_brightness(newb)
        self.br_sh.setText(f"<h1 style='color: #0dbeff;'>{newb}</h1>")

    def commands(self):
        self.commandtime.start()
        self.tab1.setText("<h4 style='color: #ff9203;'>TIME NOW<br>INTRODUCE YOURSELF<br>SMALL MATHEMATICAL OPERATIONS<br>SHUTDOWN<br>OPEN YOUTUBE<br>OPEN CHATGPT<br>SYSTEM CHECK<br>CHECK SECURITY</h4>")

    def act_main(self):
        self.mainrunner.start()

    def scan_usb(self):
        self.usbscan.start()

    def sys_health(self):
        self.health.start()

    def core_view(self):
        self.core.start()

    def url_check(self):
        self.urlsec.start()

    def antivirus(self):
        self.mrt.start()

    def get_partition_info(self):
        self.commandtime.start()
        partitions = psutil.disk_partitions()
        partition_info = ""
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partition_info += (f"<h4 style='color: #ff9203;'>Partition: {partition.device}<br>"
                                f"  Total Space: {usage.total / (1024**3):.2f} GB<br>"
                                f"  Available Space: {usage.free / (1024**3):.2f} GB<br></h4>")
            except PermissionError:
                partition_info += (f"<h4 style='color: #ff9203;'>Partition: {partition.device}<br>"
                                f"  Access Denied<br></h4>")

        if self.fhidder.isHidden():
            self.tab1.setText(partition_info)
        else:
            self.fhidder.setText(partition_info)
        
#======================================================================================================================
#                                                     MAIN                                                             
#====================================================================================================================== 
app = QApplication(sys.argv)
window = amica()
window.show()
sys.exit(app.exec_())