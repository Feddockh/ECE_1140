import sys
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QApplication, QLineEdit, QMainWindow, 
    QTableWidgetItem, QTableWidget, QPushButton, QVBoxLayout, 
    QWidget, QComboBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from hw_plc import HWPLC  # Adjust the import path as per your directory structure

class TrackControllerWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(TrackControllerWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Hardware Track Controller UI")
        self.setGeometry(100, 100, 800, 600)

        # Line selection dropdown
        self.line_combo = QComboBox()
        self.line_combo.addItems(["Blue Line", "Green Line", "Red Line"])
        self.line_combo.currentIndexChanged.connect(self.update_table_for_line)

        # Color bar at the top
        self.color_bar = QLabel()
        self.color_bar.setFixedHeight(5)  # Set the height of the color bar
        self.update_color_bar()

        # Table widget initialization
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(15)  # 16 rows, 15 for tracks 1 - 15
        self.table_widget.setColumnCount(7)  # 7 columns

        # Column headers
        self.table_widget.setHorizontalHeaderLabels([
            "Block", "Track Occupancy", "Switch State", "Speed (miles per hour)", "Authority (feet)", "Light Signal Color", "Crossing Signal"
        ])

        # Initial table setup (default to Blue Line)
        self.update_table_for_line(0)  # Blue Line is index 0 initially

        # Search block layout
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_block)

        # Upload PLC button
        self.upload_button = QPushButton("Upload PLC")
        self.upload_button.clicked.connect(self.upload_plc_code)

        # Search box layout 
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Block: "))
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        # Upload PLC layout
        upload_layout = QHBoxLayout()
        upload_layout.addWidget(self.upload_button)

        # Line selection layout (TOP of Screen)
        line_select_layout = QHBoxLayout()
        line_select_layout.addWidget(QLabel("Select Line: "))
        line_select_layout.addWidget(self.line_combo)

        # The table layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.color_bar)  # Add the color bar widget
        main_layout.addLayout(line_select_layout)
        main_layout.addWidget(self.table_widget)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(upload_layout)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def update_color_bar(self):
        # Set color bar based on selected line
        current_index = self.line_combo.currentIndex()
        if current_index == 0:  # Blue Line
            self.color_bar.setStyleSheet("background-color: blue;")
        elif current_index == 1:  # Green Line
            self.color_bar.setStyleSheet("background-color: green;")
        elif current_index == 2:  # Red Line
            self.color_bar.setStyleSheet("background-color: red;")

    def update_table_for_line(self, index):
        # Update color bar when line selection changes
        self.update_color_bar()

        # Clear existing table contents
        self.table_widget.clearContents()

        # Re-initialize table headers
        self.table_widget.setHorizontalHeaderLabels([
            "Block", "Track Occupancy", "Switch State", "Speed (miles per hour)", "Authority (feet)", "Light Signal Color", "Crossing Signal"
        ])

        # Populate table based on selected line
        for row in range(15):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(row + 1)))  # Block numbers 1-15
            self.table_widget.setItem(row, 1, QTableWidgetItem("Occupied" if row % 2 == 0 else "Unoccupied"))
            
            # Drop down menu for switch position only at block 5 (example logic)
            if row == 4:
                switch_combo = QComboBox()
                switch_combo.addItems(["Block 6", "Block 11"])
                switch_combo.setCurrentText("Switch to Block 6")
                self.table_widget.setCellWidget(row, 2, switch_combo)
            else:
                self.table_widget.setItem(row, 2, QTableWidgetItem("N/A"))
            
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(60 + row * 5)))  # Speed in some units
            self.table_widget.setItem(row, 4, QTableWidgetItem("Authority " + str(row + 1)))
           
            color_item = QTableWidgetItem("Green" if row % 2 == 0 else "Red")
            if row % 2 == 0:
                color_item.setBackground(QColor("green"))
            else:
                color_item.setBackground(QColor("red"))
            self.table_widget.setItem(row, 5, color_item)
            
            # Crossing signal for block 3 (example logic)
            if row == 2:
                self.table_widget.setItem(row, 6, QTableWidgetItem("Crossing Active"))
            else:
                self.table_widget.setItem(row, 6, QTableWidgetItem("N/A"))

    def search_block(self):
        block_number = self.search_bar.text()
        if block_number.isdigit():
            block_number = int(block_number)
            if 1 <= block_number <= 15:
                self.table_widget.selectRow(block_number - 1)
                self.table_widget.scrollToItem(self.table_widget.item(block_number - 1, 0),
                                               QTableWidget.PositionAtCenter)
            else:
                self.show_error_message(f"Block number must be between 1 and 15 for {self.line_combo.currentText()}.")
        else:
            self.show_error_message(f"Please enter a valid block number for {self.line_combo.currentText()}.")

    def upload_plc_code(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Python Files (*.py)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            file_names = file_dialog.selectedFiles()
            # Handle the uploaded file(s) here
            for file_name in file_names:
                try:
                    # Assuming track_occupancies and authority are initialized correctly
                    track_occupancies = [False] * 16  # Initialize with 16 elements (index 0 to 15)
                    authority = 0  # Example initial authority
                    plc_instance = HWPLC(track_occupancies, authority)
                    
                    # Simulate PLC logic
                    switch_position, crossing_signal, light_StationB, light_StationC, authority = plc_instance.plc()

                    # Update table based on PLC simulation results
                    # Example: update switch state and authority for block 5
                    block_number = 5  # Example block number
                    switch_combo = self.table_widget.cellWidget(block_number - 1, 2)
                    switch_combo.setCurrentText(f"Switch to Block {11 if switch_position else 6}")
                    
                    self.table_widget.item(block_number - 1, 4).setText(f"Authority {authority}")

                except Exception as e:
                    self.show_error_message(f"Error loading or executing PLC file: {str(e)}")

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

app = QApplication(sys.argv)
window = TrackControllerWindow()
window.show()
sys.exit(app.exec())
