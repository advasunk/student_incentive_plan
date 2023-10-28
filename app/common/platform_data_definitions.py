from enum import Enum

USER_ROLE_LIST = {
    "All": "All",
    "Student": "Student",
    "Teacher": "Teacher",
    "Parent": "Parent",
    "Admin": "Admin",
    "Friend": "Friend",
    "Other": "Other"
}


class UserRole(Enum):
    STUDENT = USER_ROLE_LIST['Student']
    TEACHER = USER_ROLE_LIST['Teacher']
    PARENT = USER_ROLE_LIST['Parent']
    ADMIN = USER_ROLE_LIST['Admin']
    FRIEND = USER_ROLE_LIST['Friend']
    OTHER = USER_ROLE_LIST['Other']


USER_RELN_LIST = ['Parent', 'Teacher', 'Friend', 'Other']

academic_year_list = [
    {
        "academic_year": "2023-24",
        "academic_year_name": "2023-24"
    },
    {
        "academic_year": "2024-25",
        "academic_year_name": "2024-25"
    }
]


# define enums
class TaskStatus(Enum):
    ACTIVE = 'A'
    INACTIVE = 'I'
    DELETED = 'X'


course_subject_list = [
    {
        "subject": "History",
        "desc": "History"
    },
    {
        "subject": "Math",
        "desc": "Math"
    },
    {
        "subject": "Science",
        "desc": "Science"
    },
    {
        "subject": "English",
        "desc": "English"
    }, {
        "subject": "Religion",
        "desc": "Religion"
    },
    {
        "subject": "Social Studies",
        "desc": "Social Studies"
    },
    {
        "subject": "Computer Science",
        "desc": "Computer Science"
    },
    {
        "subject": "Other",
        "desc": "Other"
    }
]
