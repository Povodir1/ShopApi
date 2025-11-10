from app.models.category import Category
def serv_get_categories(session):
    categories = session.query(Category).all()

    category_dict = {cat.id: {'id': cat.id, 'name': cat.name, 'parent_id': cat.parent_id, 'children': []}
                     for cat in categories}

    root_categories = []
    for cat in categories:
        if cat.parent_id and cat.parent_id in category_dict:
            category_dict[cat.parent_id]['children'].append(category_dict[cat.id])
        else:
            root_categories.append(category_dict[cat.id])

    return root_categories