import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Practical 5G Throughput simulation tool')

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create labels for input fields
        bw_label = QLabel('5G Carrier Bandwidth (MHz)', central_widget)
        ss_label = QLabel('Subcarrier Spacing (kHz)', central_widget)
        nl_label = QLabel('Number of MIMO Layers', central_widget)
        idx_label = QLabel('CQI/MCS Index', central_widget)
        val_label = QLabel('Index Value', central_widget)
        ber_label = QLabel('Block Error Rate Percentage', central_widget)

        # Set the position and size of the labels
        bw_label.setGeometry(20, 30, 200, 20)
        ss_label.setGeometry(20, 70, 200, 20)
        nl_label.setGeometry(20, 110, 200, 20)
        idx_label.setGeometry(20, 150, 200, 20)
        val_label.setGeometry(20, 205, 200, 20)
        ber_label.setGeometry(20, 230, 200, 20)

        # Create line edits for input fields
        self.bw_edit = QLineEdit(central_widget)
        self.ss_edit = QLineEdit(central_widget)
        self.nl_edit = QLineEdit(central_widget)
        self.idx_edit = QLineEdit(central_widget)
        self.val_edit = QLineEdit(central_widget)
        self.ber_edit = QLineEdit(central_widget)

        # Set the position and size of the line edits
        self.bw_edit.setGeometry(230, 30, 200, 20)
        self.ss_edit.setGeometry(230, 70, 200, 20)
        self.nl_edit.setGeometry(230, 105, 200, 20)
        self.idx_edit.setGeometry(230, 140, 200, 20)
        self.val_edit.setGeometry(230, 205, 200, 20)
        self.ber_edit.setGeometry(230, 230, 200, 20)

        # Create buttons for CQI and MCS index selection
        self.cqi_button = QPushButton('CQI Index', central_widget)
        self.mcs_button = QPushButton('MCS Index', central_widget)

        # Set the position and size of the buttons
        self.cqi_button.setGeometry(230, 165, 100, 30)
        self.mcs_button.setGeometry(330, 165, 100, 30)

        # Connect the buttons to their respective functions
        self.cqi_button.clicked.connect(self.select_cqi)
        self.mcs_button.clicked.connect(self.select_mcs)

        # Create a button for submitting the input values
        self.submit_button = QPushButton('Submit', central_widget)

        # Set the position and size of the submit button
        self.submit_button.setGeometry(20, 330, 100, 30)

        # Connect the submit button to the function that calculates the results
        self.submit_button.clicked.connect(self.calculate_results)

        # Create a plot widget for the waves
        self.plot_widget = QLabel(central_widget)
        # Set the position and size of the plot widget
        self.plot_widget.setGeometry(450, 100, 800, 400)
        self.plot_widget.setAlignment(Qt.AlignCenter)

    def select_cqi(self):
        self.idx_edit.setText('')
        self.idx_edit.setPlaceholderText('CQI Index Value')

    def select_mcs(self):
        self.idx_edit.setText('')
        self.idx_edit.setPlaceholderText('MCS Index Value')

    def calculate_results(self):
        # Get the input values from the line edits
        bw = int(self.bw_edit.text())
        ss = int(self.ss_edit.text())
        nl = int(self.nl_edit.text())
        idx = self.idx_edit.placeholderText()
        val = int(self.val_edit.text())
        ber = float(self.ber_edit.text())

        speceffmcs=[0.2344, 0.3770, 0.6016, 0.8770, 1.1758, 1.4766, 1.6953, 1.9141, 2.1602, 2.4063, 2.5703, 2.7305, 3.0293, 3.3223, 3.6094, 3.9023, 4.2129, 4.5234, 4.8164, 5.1152, 5.3320, 5.5547, 5.8906, 6.2266, 6.5703, 6.9141, 7.1602, 7.4063]
        speceffcqi=[0.1523, 0.1523, 0.3770, 0.8770, 1.4766, 1.9141, 2.4063, 2.7305, 3.3223, 3.9023, 4.5234, 5.1152, 5.5547, 6.2266, 6.9141, 7.4063]

        # Calculate the number of PRBs
        x = int(bw) * 1000 / int(ss) /12
        n_prb = x - 4
        n_prb=math.floor(n_prb)

        Dlslots = 1600

        # Calculate the maximum throughput achieved
        if idx == 'CQI Index Value':
            # Calculate the effective throughput using the CQI index value
            i=speceffcqi[int(val)]
        elif idx == 'MCS Index Value':
            # Calculate the effective throughput using the MCS index value
            i=speceffmcs[int(val)]

        TbSize = 132 * i
        TbSize = math.floor(TbSize)

        Throughput = int(TbSize) * int(n_prb) * int(Dlslots) * int(nl) * ((100 - int(ber))/100) / 1000 / 1000

        # Display the number of PRBs and maximum throughput achieved
        result_text = f'Number of PRBs: {n_prb}\nMaximum Throughput: {Throughput:.2f} Mbps'
        QMessageBox.information(self, 'Results', result_text)

        # Generate the waveform visualization
        t = np.linspace(0, 3, 100) # no of points generated from strating point 0 - 1 ending point (200)
        x = np.sin(2 * np.pi * bw * 10**6 * t)
        y = np.sin(2 * np.pi * ss * 10**3 * t)
        plt.plot(t, x, label='5G Carrier Bandwidth')
        plt.plot(t, y, label='Subcarrier Spacing')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.savefig('waves.png')

        # Display the waveform visualization in the plot widget
        pixmap = QPixmap('waves.png')
        self.plot_widget.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())