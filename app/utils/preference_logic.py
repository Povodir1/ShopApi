from app.models import User,Item,UserTagPreference

from app.core.exceptions import ObjectNotFoundError



def update_user_preference(user_id: int, item_id: int, session):
    user = session.query(User).filter_by(id=user_id).first()
    item = session.query(Item).filter_by(id=item_id).first()

    if not user or not item:
        raise ObjectNotFoundError("Юзер или предмет не найден")

    # Map tag_id -> UserTagPreference object
    user_tag_objs = {utp.tag_id: utp for utp in user.user_tag_preferences}
    item_tag_ids = {it.tag_id for it in item.item_tags}

    # Tags that user already has
    for tag_id, utp in list(user_tag_objs.items()):
        if tag_id in item_tag_ids:
            utp.score += 1
            session.add(utp)
        else:
            if utp.score == 1:
                session.delete(utp)
            else:
                utp.score -= 1

    # New tags from item that user doesn't have
    new_tag_ids = item_tag_ids - set(user_tag_objs.keys())
    for tag_id in new_tag_ids:
        new_utp = UserTagPreference(user_id=user_id, tag_id=tag_id, score=1)
        session.add(new_utp)

