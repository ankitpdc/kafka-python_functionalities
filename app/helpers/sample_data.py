from datetime import datetime

def get_student_data():
    return [[int(datetime.now().timestamp()*1000), 'Ankit', 'Dec 1, 2005', '11', 'A', ['Physics', 'Chemistry', 'Mathematics', 'Computer', 'Hindi']],
    [int(datetime.now().timestamp()*1000), 'Sonali', 'January 16, 2006', '11', 'B', ['Physics', 'Chemistry', 'Biology', 'Literature', 'Hindi']],
    [int(datetime.now().timestamp()*1000), 'Amar', 'June 1, 2005', '12', 'C', ['Accounts', 'Commerse', 'Mathematics', 'Computer', 'Hindi']],
    [int(datetime.now().timestamp()*1000), 'Harshal', 'Febuary 28, 2005', '12', 'A', ['Physics', 'Chemistry', 'Mathematics', 'Computer', 'Literature']]
    ]