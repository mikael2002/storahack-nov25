import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QWidget,
    QButtonGroup,
    QLabel,
    QRadioButton,
    QPushButton,
)

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Volunteer Management System")



        widget = QWidget()

        grid_layout = QGridLayout()
        rb1 = QRadioButton()
        rb2 = QRadioButton()
        rb3 = QRadioButton()
        rb4 = QRadioButton()
        rbg1 = QButtonGroup(widget)
        rbg2 = QButtonGroup(widget)
        rbg1.addButton(rb1)
        rbg1.addButton(rb2)
        rbg2.addButton(rb3)
        rbg2.addButton(rb4)
        grid_layout.addWidget(rb1,0,0)
        grid_layout.addWidget(rb2,0,1)
        grid_layout.addWidget(rb3,1,0)
        grid_layout.addWidget(rb4,1,1)

        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)
        v_layout.addWidget(QPushButton('Submit'))

        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()