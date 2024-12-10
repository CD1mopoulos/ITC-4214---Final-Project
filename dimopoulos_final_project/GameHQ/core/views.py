# Check if the user is an employee
def is_employee(user):
    return user.is_authenticated and user.is_employee