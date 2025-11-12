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
    QPushButton,
)

shift_list_base_filename = 'shiftlist'
memberlist_filename = 'memberlist.txt'
schedule_filename = 'schedule.txt'

def getmemberlist():
    with open(memberlist_filename, mode='r') as f:
        return f.readline().split(',')

# Get the list of matches
def getmatches():
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

def batch_read():
    shift_dict = {}
    member_list = getmemberlist()
    for member_id in member_list:
        shift_list_filename = shift_list_base_filename + '-' + str(member_id) + '.txt'
        try:
            shift_dict[member_id] = read_shift_list(shift_list_filename)
        except OSError:
            initialize_shift_list(shift_list_filename)
            shift_dict[member_id] = read_shift_list(shift_list_filename)
    return shift_dict




def read_shift_list(shift_list_filename):
    with open(shift_list_filename, mode='r') as f:
        shift_list = f.readline().split(',')
        return [int(x) for x in shift_list]

def initialize_shift_list(shift_list_filename):
    with open(shift_list_filename, mode='w') as f:
        row_output = ''
        for i in range(len(getmatches())):
            row_output += '0,'
        row_output = row_output[:-1]
        f.write(row_output)

def getroleaverage(shift_matrix):
    return np.average(shift_matrix,axis=0)

def getmatchsum(shift_matrix):
    return np.sum(shift_matrix[:,1:],axis=1)

class MainWindow(QMainWindow):

    def get_vlm(self,shift_dict):

        volunteer_list_matrix = []
        for i in range(self.n_matches):
            volunteer_list_row = []
            for j in range(self.n_roles):
                volunteer_list_row.append([])
            volunteer_list_matrix.append(volunteer_list_row)
        
        for member_id in shift_dict:
            member_shift_list = shift_dict[member_id]
            for (i_match, member_role) in enumerate(member_shift_list):
                volunteer_list_matrix[i_match][member_role].append(member_id)

        return volunteer_list_matrix

    def get_shift_matrix(self,vlm):
        return np.int8(np.array([[len(cell) for cell in row] for row in vlm]))

    def show_volunteers(self,i_match,i_role):
        message = ''
        
        if i_role == 0:
            if self.vlm[i_match][i_role] == []:
                message += 'Everyone is helping '
            else:
                message += 'Not helping '
        elif self.vlm[i_match][i_role] == []:
            message += 'No one is helping '
        else:
            message += 'Helping '
        message += 'at the match on ' + self.match_matrix[i_match][0]
        message += ' at ' + self.match_matrix[i_match][1]
        message += ' against ' + self.match_matrix[i_match][2]
        if i_role != 0:
            message += ' in role ' + self.roles_list[i_role]
        if self.vlm[i_match][i_role] != []:
            message += ' are: '
            for member_id in self.vlm[i_match][i_role]:
                message += member_id + ', '
            message = message[:-2] + '.'
        else:
            message += '.'
        self.status_bar.setText(message)

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Volunteer Management System")

        widget = QWidget()

        grid_layout = QGridLayout()

        match_attribs_list = ['Date','Time','Opponent']
        self.match_matrix = getmatches()
        self.roles_list = getroles()

        self.n_match_attribs = len(match_attribs_list)
        self.n_roles = len(self.roles_list)
        self.n_matches = len(self.match_matrix)
        

        pushbutton_matrix = []
        matchinfo_matrix = []

        shift_dict = batch_read()
        self.vlm = self.get_vlm(shift_dict)
        shift_matrix = self.get_shift_matrix(self.vlm)
        role_avg = getroleaverage(shift_matrix)
        match_sum = getmatchsum(shift_matrix)
        total_avg = np.average(match_sum)

        # Add match info & labels into arrays
        for i in range(self.n_matches):
            pushbutton_row = []
            matchinfo_row = []

            for j in range(self.n_match_attribs):
                matchinfo_row.append(QLabel(self.match_matrix[i][j]))
                
            matchinfo_matrix.append(matchinfo_row)

            for j in range(self.n_roles):
                pushbutton = QPushButton(str(shift_matrix[i][j]))
                pushbutton.clicked.connect(partial(self.show_volunteers,i,j))
                pushbutton_row.append(pushbutton)

            pushbutton_matrix.append(pushbutton_row)

        pushbuttongroup_list = []
        
        # Rendering
        for (j, match_attrib) in enumerate(match_attribs_list):
            grid_layout.addWidget(QLabel(match_attrib),0,j)
        for (j, role) in enumerate(self.roles_list):
            grid_layout.addWidget(QLabel(role),0,j+self.n_match_attribs)
        grid_layout.addWidget(QLabel('TOTAL'),0,self.n_match_attribs+self.n_roles)
        for i in range(self.n_matches):
            for j in range(3):
                grid_layout.addWidget(matchinfo_matrix[i][j],i+1,j)
            for j in range(self.n_roles):
                grid_layout.addWidget(pushbutton_matrix[i][j],i+1,j+self.n_match_attribs)
            grid_layout.addWidget(QLabel(str(match_sum[i])),i+1,self.n_match_attribs+self.n_roles)

        grid_layout.addWidget(QLabel('AVERAGE'),2+self.n_matches,self.n_match_attribs-1)
        for j in range(self.n_roles):
            grid_layout.addWidget(QLabel(f'{role_avg[j]:.1f}'),2+self.n_matches,j+self.n_match_attribs)
        grid_layout.addWidget(QLabel(f'{total_avg:.1f}'),2+self.n_matches,self.n_match_attribs+self.n_roles)



        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)


        # Status bar
        self.status_bar = QLabel('Click on a button to show who\'s volunteering in a particular role in a particular match.')
        v_layout.addWidget(self.status_bar)
        
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.show()

app = QApplication(sys.argv)
w = MainWindow()
app.exec()
