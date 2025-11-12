import sys
import numpy as np
from functools import partial
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

shift_list_base_filename = 'shiftlist'

# Get the list of matches
def getmatches():
    schedule_filename = 'schedule.txt'
    match_info_list = []

    with open(schedule_filename, mode='r') as f:

        # When the line is '', the loop ends.
        line = f.readline()

        while line != '':
            # Line: '09-21,17:30,AIK'
            # Split: ['09-21','17:30','AIK']
            match_info_row = line.split(',')
            # Remove the ending \n
            if match_info_row[2][-1] == '\n':
                match_info_row[2] = match_info_row[2][:-1]
            match_info_list.append(match_info_row)

            # Read another line
            line = f.readline()

    return match_info_list

# Get the list of roles
def getroles():
    roles_filename = 'roles.txt'

    with open(roles_filename, mode='r') as f:
        roles_list = f.readline().split(',')

    return roles_list

def read_shift_list(shift_list_filename):
    with open(shift_list_filename, mode='r') as f:
        shift_list = f.readline().split(',')
        return [int(x) for x in shift_list]

def write_shift_list(shift_list_filename,shift_list):
    with open(shift_list_filename, mode='w') as f:
        row_output = ''
        for match_role in shift_list:
            row_output += (str(match_role) + ',')
        row_output = row_output[:-1]
        f.write(row_output)

class MainWindow(QMainWindow):

    def update_shift_list(self,radiobuttongroup_list):
    
        n_matches = len(radiobuttongroup_list)
        self.shift_list = [radiobuttongroup.checkedId() for radiobuttongroup in radiobuttongroup_list]
        if -1 not in self.shift_list:
            write_shift_list(shift_list_filename,self.shift_list)
            self.status_bar.setText('Update successful!')
        else:
            self.status_bar.setText('Update unsuccessful! Please choose a role for every match.')

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Volunteer Management System")

        try:
            self.shift_list = read_shift_list(shift_list_filename)
        except OSError:
            n_matches = len(getmatches())
            self.shift_list = [0 for x in range(n_matches)]

        widget = QWidget()

        grid_layout = QGridLayout()

        match_attribs_list = ['Date','Time','Opponent']
        match_matrix = getmatches()
        roles_list = getroles()
        n_match_attribs = len(match_attribs_list)
        n_roles = len(roles_list)
        n_matches = len(match_matrix)

        radiobutton_matrix = []
        matchinfo_matrix = []

        # Add match info & radio buttons into arrays
        for i in range(n_matches):
            radiobutton_row = []
            matchinfo_row = []

            for j in range(n_match_attribs):
                matchinfo_row.append(QLabel(match_matrix[i][j]))
                
            matchinfo_matrix.append(matchinfo_row)

            for j in range(n_roles):
                radiobutton = QRadioButton()
                radiobutton_row.append(radiobutton)

            radiobutton_matrix.append(radiobutton_row)

        radiobuttongroup_list = []

        # Add Radio Buttons into Groups
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
                if j == self.shift_list[i]:
                    radiobutton_matrix[i][j].setChecked(True)
                grid_layout.addWidget(radiobutton_matrix[i][j],i+1,j+n_match_attribs)

        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)

        # Submit Button
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(partial(self.update_shift_list,radiobuttongroup_list))
        v_layout.addWidget(submit_button)


        # Status bar
        self.status_bar = QLabel('')
        v_layout.addWidget(self.status_bar)
        
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.show()

if len(sys.argv) < 2:
    member_id = input('Enter Volunteer ID: ')
else:
    member_id = sys.argv[1]

shift_list_filename = shift_list_base_filename + '-' + member_id + '.txt'


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
