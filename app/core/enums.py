from enum import Enum

class LanguageList(Enum):
    ru = "ru"
    en = "en"

class CurrencyType(Enum):
    BYN = "BYN"
    USD = "USD"
    RUB = "RUB"

class RoleEnum(Enum):
    User = "User"
    Manager = "Manager"
    Admin = "Admin"

class SortType(Enum):
    by_rating = "rating_desc"
    to_increase = "price_desc"
    to_decrease = "price_asc"
    by_date = "date_desc"
    by_preference = "by_preference"

class ActionEnum(Enum):
    CREATE = "CREATE"
    READ = "READ"
    READ_ALL = "READ_ALL"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class ResourceEnum(Enum):
    ITEMS = "ITEMS"
    FAVORITE_ITEMS = "FAVORITE_ITEM"
    COMMENTS = "COMMENTS"
    ATTRIBUTE = "ATTRIBUTE"
    CATEGORY = "CATEGORY"
    ORDERS = "ORDERS"
    BASKET_ITEMS = "BASKET_ITEMS"
    USERS = "USERS"
    ROLES = "ROLES"
    PERMISSIONS = "PERMISSIONS"

class StatusList(Enum):
    pending = "pending"
    paid = "paid"
    in_process = "in_process"

class PaymentMethods(Enum):
    by_card = "by_card"
    by_cash = "by_cash"