from src.dao.base import BaseDAO
from src.models.models import Organization, Employee, OrganizationResponsible


class OrganizationDAO(BaseDAO):
    model = Organization

class EmployeeDAO(BaseDAO):
    model = Employee

class OrganizationResponsibleDAO(BaseDAO):
    model = OrganizationResponsible