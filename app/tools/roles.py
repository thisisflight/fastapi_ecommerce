from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    ADMIN = "admin"
