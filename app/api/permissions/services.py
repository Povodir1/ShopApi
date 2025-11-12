from app.models import Permission,Role,User

from app.api.permissions.schemas import PermissionDataSchema,RolePermissionSchema,AddPermissionSchema
from app.api.users.schemas import UserTokenDataSchema

from app.core.exceptions import (ObjectNotFoundError, ObjectAlreadyExistError,
                                 InvalidDataError, NoPermissionsError)
from app.core.enums import ResourceEnum, ActionEnum, RoleEnum




def db_get_all_permissions(session):
    all_roles = session.query(Role).all()
    all_role_permissions = []

    for role in all_roles:
        permissions = session.query(Permission).filter(Permission.role_id == role.id).all()

        resource_actions_map = {}
        for perm in permissions:
            resource = perm.resource
            action = perm.action

            if resource not in resource_actions_map:
                resource_actions_map[resource] = []

            if action not in resource_actions_map[resource]:
                resource_actions_map[resource].append(action)
        permission_data_list = []
        for resource, actions in resource_actions_map.items():
            permission_data_list.append(
                PermissionDataSchema(resource=resource, actions=sorted(actions))
            )
        all_role_permissions.append(
            RolePermissionSchema(
                role=role.name,
                permissions=permission_data_list
            )
        )

    return all_role_permissions


def db_add_permission(role:RoleEnum,
                      resource:ResourceEnum,
                      action:ActionEnum,
                      user:UserTokenDataSchema,
                      session):
    role_obj = session.query(Role).filter(Role.name == role.value).first()
    if user.role == role.value:
        raise NoPermissionsError("No Permissions")
    if not role_obj:
        raise ObjectNotFoundError(f"Роль '{role.name}' не найдена.")

    existing_perm = session.query(Permission).filter(
        Permission.role_id == role_obj.id,
        Permission.resource == resource.value,
        Permission.action == action.value
    ).first()

    if existing_perm:
        raise ObjectAlreadyExistError("Разрешение для данной роли, ресурса и действия уже существует.")

    new_permission = Permission(
        role_id=role_obj.id,
        resource=resource.value,
        action=action.value
    )

    session.add(new_permission)
    return AddPermissionSchema(role = role_obj.name,resource=resource.value,action= action.value)

def db_delete_permission(role:RoleEnum,
                      resource:ResourceEnum,
                      action:ActionEnum,
                      session):

    role_obj = session.query(Role).filter(Role.name == role.value).first()

    if not role_obj:
        raise ObjectNotFoundError(f"Роль '{role.name}' не найдена.")

    permission_to_delete = session.query(Permission).filter(
        Permission.role_id == role_obj.id,
        Permission.resource == resource.value,
        Permission.action == action.value
    ).first()

    if not permission_to_delete:
        raise InvalidDataError("Разрешение для данной роли, ресурса и действия не найдено.")

    session.delete(permission_to_delete)


def db_update_user_role(user_id: int, role: RoleEnum, session):
    user_to_update = session.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise ObjectNotFoundError(f"Пользователь с ID {user_id} не найден.")

    new_role_obj = session.query(Role).filter(Role.name == role.value).first()
    if not new_role_obj:
        raise  ObjectNotFoundError(f"Целевая роль '{role.value}' не найдена в базе данных.")
    user_to_update.role_id = new_role_obj.id

    return user_to_update