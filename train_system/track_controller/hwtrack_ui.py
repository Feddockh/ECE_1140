# train_system/track_controller/hwtrack_ui.py


import sys
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QApplication,QLineEdit, QMainWindow,QTableWidgetItem,QTableWidget, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox #QLabel
from PyQt6.QtCore import Qt 

class TrackControllerWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(TrackControllerWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hardware Track Controller UI")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(15) #16 rows, 15 for tracks 1 - 15
        self.table_widget.setColumnCount(7) #6 columns

        #column headers
        self.table_widget.setHorizontalHeaderLabels([
            "Block", "Track Occupancy", "Switch State", "Speed(miles per hour)", "Authority (feet)", "Light Signal Color", "Crossing Signal"
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
        
        #Search block layout
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_block)

        #search layout 
        
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Block: "))
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        
        #set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_widget)
        main_layout.addLayout(search_layout)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def search_block(self):
        block_number = self.search_bar.text()
        if block_number.isdigit():
            block_number = int(block_number)
            if 1<= block_number <= 15:
                self.table_widget.selectRow(block_number - 1)
                self.table_widget.scrollToItem(self.table_widget.item(block_number - 1, 0),
                                               QTableWidget.PositionAtCenter)
            else:
                self.show_error_message("Block number must be between 1 and 15 for Blue Line.")
        else:
            self.show_error_message("Please enter a valid block number for blue line.")
    
    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

app = QApplication(sys.argv)
window = TrackControllerWindow()
window.show() #IMPORTANT!!!
app.exec()