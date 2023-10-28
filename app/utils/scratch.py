from enum import Enum


class UserRole(Enum):
    STUDENT = 'Student'
    TEACHER = 'Teacher'
    PARENT = 'Parent'


# iterate over enum list print all enums
for role in UserRole:
    print(role.name, '-', role.value)

