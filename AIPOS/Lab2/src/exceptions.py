class AdministratorNotAllowedException(Exception):
    def __init__(self, employee_id: int):
        super().__init__(f"you cannot handle employee with id {employee_id}")


class DatabaseException(Exception):
    pass


class EmployeeNotFoundException(DatabaseException):
    def __init__(self, employee_id: int):
        super().__init__(f"Employee with id = {employee_id} not found")


class PositionNotFoundException(DatabaseException):
    def __init__(self, employee_id: int):
        super().__init__(f"Position with id = {employee_id} not found")
