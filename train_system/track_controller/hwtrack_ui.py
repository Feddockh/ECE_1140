# train_system/track_controller/hwtrack_ui.py


import sys
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QTableWidget, QPushButton, QVBoxLayout, QWidget, QComboBox #QLabel
from PyQt6.QtCore import Qt 

class TrackControllerWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(TrackControllerWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hardware Track Controller UI")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(15) #16 rows, 15 for tracks 1 - 15
        self.table_widget.setColumnCount(6) #6 columns

        #column headers
        self.table_widget.setHorizontalHeaderLabels([
            "Block", "Track Occupancy", "Switch State", "Speed(miles per hour)", "Authority (feet)", "Light Signal Color"
        ])

        for row in range(15):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # Block numbers 1-15
            self.table_widget.setItem(row, 1, QTableWidgetItem("Occupied" if row % 2 == 0 else "Unoccupied"))
            
            #drop down menu for switch position
            switch_combo = QComboBox() 
            switch_combo.addItems(["Block 6", "Block 11"])   
            if row % 2 == 0:
                switch_combo.setCurrentText("Switch to Block 6")
            else:
                switch_combo.setCurrentText("Block 11")
            self.table_widget.setCellWidget(row, 2, switch_combo)
            
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(60 + row * 5)))  # Speed in some units
            self.table_widget.setItem(row, 4, QTableWidgetItem("Authority " + str(row + 1)))
           
            color_item = QTableWidgetItem("Green" if row % 2 == 0 else "Red")
            if row % 2 == 0:
                color_item.setBackground(QColor("green"))
            else:
                color_item.setBackground(QColor("red"))
            self.table_widget.setItem(row, 5, color_item)
        
        #set layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)



app = QApplication(sys.argv)
window = TrackControllerWindow()
window.show() #IMPORTANT!!!
app.exec()