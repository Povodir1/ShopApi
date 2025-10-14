from app.database import db_session
from app.models.user import User
from app.models.item import Item
from app.models.user_tag_preference import UserTagPreference

def update_user_preference(user_id,item_id):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        item = session.query(Item).filter(Item.id == item_id).first()

        user_tags = {tag.tag_id:tag.score for tag in user.user_tag_preferences}
        item_tags = [tag.tag_id for tag in item.item_tags]

        for tag,val in user_tags.items():
            if tag in item_tags:
                updated_tag = session.query(UserTagPreference).filter(UserTagPreference.tag_id == tag).first()
                updated_tag.score +=1
            else:
                user_tags[tag] -= 1
                if user_tags[tag] == 0:
                    user_tag = session.query(UserTagPreference).filter(UserTagPreference.tag_id == tag).first()
                    session.delete(user_tag)
        new_tags = [tag for tag in item_tags if tag not in user_tags.keys()]
        for tag in new_tags:
            session.add(UserTagPreference(user_id = user_id,tag_id = tag,score = 1))

