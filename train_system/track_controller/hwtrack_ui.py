# train_system/track_controller/hwtrack_ui.py


import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton #QLabel
from PyQt6.QtCore import Qt 

class TrackControllerWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(TrackControllerWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hardware Track Controller UI")
        button = QPushButton("Insert Train Block #")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        self.setCentralWidget(button)

        #label = QLabel("Hardware Track Controller UI")
        #label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #self.setCentralWidget(label)

    def the_button_was_clicked(self):
        print("Clicked!")

    
app = QApplication(sys.argv)
window = TrackControllerWindow()
window.show() #IMPORTANT!!!

app.exec()


