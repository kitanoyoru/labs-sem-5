class AdministratorNotAllowedException(Exception):
    def __init__(self, employee_id: int):
        super().__init__(f"you cannot handle employee with id {employee_id}")
