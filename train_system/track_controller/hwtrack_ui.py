import sys
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QApplication, QLineEdit, QMainWindow, 
    QTableWidgetItem, QTableWidget, QPushButton, QVBoxLayout, 
    QWidget, QComboBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from hw_plc import HWPLC

class TrackControllerWindow(QMainWindow):
    
    def __init__(self, track_controller, *args, **kwargs):
        super(TrackControllerWindow, self).__init__(*args, **kwargs)

        self.track_controller = track_controller

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
        
        # Upload PLC layout
        upload_layout = QHBoxLayout()
        upload_layout.addWidget(self.upload_button)
        
        # Line selection layout (TOP of Screen)
        line_select_layout = QHBoxLayout()
        line_select_layout.addWidget(QLabel("Select Line: "))
        line_select_layout.addWidget(self.line_combo)

        # Test Bench button
        self.test_bench_button = QPushButton("Test Bench")
        self.test_bench_button.clicked.connect(self.open_test_bench)

        # Maintenance Bench button
        self.maintenance_button = QPushButton("Maintenance Bench")
        self.maintenance_button.clicked.connect(self.open_maintenance_bench)

        # Primary UI button
        self.primary_ui_button = QPushButton("Primary UI")
        self.primary_ui_button.clicked.connect(self.reset_to_primary_ui)

        # The table layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.color_bar)  # Add the color bar widget
        main_layout.addLayout(line_select_layout)
        main_layout.addWidget(self.table_widget)
        main_layout.addWidget(self.search_bar)
        main_layout.addWidget(self.search_button)
        main_layout.addWidget(self.test_bench_button)
        main_layout.addWidget(self.maintenance_button)
        main_layout.addWidget(self.primary_ui_button)
        main_layout.addLayout(upload_layout)  # Add the upload button layout to the main layout

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

        # Dummy data initialization for occupancy status
        block_occupancies = [False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True ]

        # Populate table based on selected line
        for row in range(15):
            block_number = row + 1

            # Block number
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(block_number)))  # Block numbers 1-15

            # Track occupancy
            occupancy_status = "Occupied" if block_occupancies[row] else "Unoccupied"
            self.table_widget.setItem(row, 1, QTableWidgetItem(occupancy_status))

            # Switch State
            switch_combo = QComboBox()
            if block_number == 5:
                switch_combo.addItems(["Station B", "Station C"])
                switch_combo.setCurrentText("Station C" if self.track_controller.switch_position else "Station B")
            else:
                switch_combo.setEnabled(False)  # Disable ComboBox for non-applicable blocks
            self.table_widget.setCellWidget(row, 2, switch_combo)

            # Speed (dummy data)
            speed = 60 + row * 5
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(speed)))  # Speed in some units

            # Authority
            authority = self.track_controller.authority
            self.table_widget.setItem(row, 4, QTableWidgetItem(f" {authority} feet"))

            # Light signals
            if (block_number in [2, 3, 4] and block_occupancies[1]) or \
               (block_number in [7, 8, 9, 10, 11] and any(block_occupancies[6:11])) or \
               (block_number in [12, 13, 14, 15, 16] and any(block_occupancies[11:])):
                light_color = "RED"
            else:
                light_color = "GREEN" if not block_occupancies[row] else "RED"

            color_item = QTableWidgetItem(light_color)
            color_item.setBackground(QColor("green") if light_color == "GREEN" else QColor("red"))
            self.table_widget.setItem(row, 5, color_item)

            # Crossing signal (dummy data)
            crossing_signal = "Active" if row == 2 else "Inactive"
            self.table_widget.setItem(row, 6, QTableWidgetItem(crossing_signal))

    def search_block(self):
        block_number = self.search_bar.text()
        if block_number.isdigit():
            block_number = int(block_number)
            if 1 <= block_number <= 15:
                self.table_widget.selectRow(block_number - 1)
                self.table_widget.scrollToItem(self.table_widget.item(block_number - 1, 0),
                                               QTableWidget.ScrollHint.PositionAtCenter)
            else:
                self.show_error_message(f"Block number must be between 1 and 15 for {self.line_combo.currentText()}.")
        else:
            self.show_error_message(f"Please enter a valid block number for {self.line_combo.currentText()}.")

    def open_test_bench(self):
        # Implement Test Bench functionality
        for row in range(15):
            # Track occupancy (editable)
            occupancy_item = QTableWidgetItem()
            occupancy_item.setFlags(occupancy_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(row, 1, occupancy_item)

            # Switch State (editable for specific blocks)
            switch_combo = QComboBox()
            if row == 4:  # Example: make block 5's switch state editable
                switch_combo.addItems(["Station B", "Station C"])
                switch_combo.setCurrentText("Station C" if self.track_controller.switch_position else "Station B")
                self.table_widget.setCellWidget(row, 2, switch_combo)
            else:
                switch_combo.setEnabled(False)
                self.table_widget.setCellWidget(row, 2, switch_combo)

    def open_maintenance_bench(self):
        # Implement Maintenance Bench functionality
        for row in range(15):
            # Track occupancy (not editable)
            occupancy_status = "Under Maintenance" if row == 2 else "Unoccupied"  # Example: mark block 3 under maintenance
            self.table_widget.setItem(row, 1, QTableWidgetItem(occupancy_status))

            # Switch State (editable for all)
            switch_combo = QComboBox()
            switch_combo.addItems(["Station B", "Station C"])
            switch_combo.setCurrentText("Station C" if self.track_controller.switch_position else "Station B")
            self.table_widget.setCellWidget(row, 2, switch_combo)

    def reset_to_primary_ui(self):
        # Reset table to the original state (Primary UI)
        self.update_table_for_line(self.line_combo.currentIndex())

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()
    
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
                    track_occupancies = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True ]  # Initialize with 16 elements (index 0 to 15)
                    authority = 0  # Example initial authority
                    print(f"Blue Line Example Instance 1")
                    plc_instance = HWPLC(track_occupancies, authority)
                    
                    # Simulate PLC logic
                    switch_position, crossing_signal, light_colorB, light_colorC, authority = plc_instance.plc()

                    # Update table based on PLC simulation results
                    # Example: update switch state and authority for block 5
                    block_number = 5  # Example block number
                    switch_combo = self.table_widget.cellWidget(block_number - 1, 2)
                    switch_combo.setCurrentText(f"Switch to Block {11 if switch_position else 6}")
                    
                    self.table_widget.item(block_number - 1, 4).setText(f"Authority {authority}")

                except Exception as e:
                    self.show_error_message(f"Error loading or executing PLC file: {str(e)}")

app = QApplication(sys.argv)

# Example initialization of HWTrackController
track_occupancies = [False] * 16
authority = 45
track_controller = HWPLC(track_occupancies, authority)

window = TrackControllerWindow(track_controller)

window.show()
sys.exit(app.exec())
