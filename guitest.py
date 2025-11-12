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
        match_attribs_list = ['Date','Time','Opponent']
        roles_list = ['Not Coming','Entrance','Crowd','Player Tunnel','Role 4','Role 5','Role 6','Role 7']
        n_match_attribs = len(match_attribs_list)
        n_roles = len(roles_list)
        n_matches = 8

        radiobutton_matrix = []
        matchinfo_matrix = []

        for i in range(n_matches):
            radiobutton_row = []
            matchinfo_row = []

            for j in range(n_match_attribs):
                matchinfo_row.append(QLabel(str(i) + ' ' + str(j)))
                
            matchinfo_matrix.append(matchinfo_row)

            for j in range(n_roles):
                radiobutton = QRadioButton(str(i) + ' ' + str(j))
                radiobutton_row.append(radiobutton)

            radiobutton_matrix.append(radiobutton_row)

        
        radiobuttongroup_list = []

        for i in range(n_matches):
            radiobutton_group = QButtonGroup(widget)
            for j in range(n_roles):
                radiobutton_group.addButton(radiobutton_matrix[i][j],j)
            radiobuttongroup_list.append(radiobutton_group)

        # Rendering
        for (j, match_attrib) in enumerate(match_attribs_list):
            grid_layout.addWidget(QLabel(match_attrib),0,j)
        for (j, role) in enumerate(roles_list):
            grid_layout.addWidget(QLabel(role),0,j+n_match_attribs)
        for i in range(n_matches):
            for j in range(3):
                grid_layout.addWidget(matchinfo_matrix[i][j],i+1,j)
            for j in range(n_roles):
                grid_layout.addWidget(radiobutton_matrix[i][j],i+1,j+n_match_attribs)

        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)
        v_layout.addWidget(QPushButton('Submit'))

        
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()