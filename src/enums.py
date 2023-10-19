from enum import Enum


class Permission(str, Enum):
    USER_CREATE = "USER_CREATE"
    USER_READ = "USER_READ"
    USER_UPDATE = "USER_UPDATE"
    USER_DELETE = "USER_DELETE"
