from pydantic import BaseModel, Field

class PermissionDataSchema(BaseModel):
    resource:str
    actions:list[str]


class RolePermissionSchema(BaseModel):
    role:str
    permissions: list[PermissionDataSchema]

class AddPermissionSchema(BaseModel):
    role:str
    resource:str
    action:str