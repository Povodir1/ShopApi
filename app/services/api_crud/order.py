
from app.models import Order,BasketItem,OrderItem,User
from app.schemas.order import OrderSchema,OrderItemSchema
from app.services.emai_sender import send_email

def serv_create_order(user_id:int,session):
    #задать пустой заказ
    order = Order(user_id = user_id,price = 0)
    session.add(order)
    session.flush()

    #добавить товары в заказ
    basket_items = session.query(BasketItem).filter(BasketItem.user_id == user_id).all()

    if not basket_items:
        raise ValueError("Корзина пуста")

    res_price = 0
    for item in basket_items:
        order_item = OrderItem(item_id = item.item_id,order_id = order.id,count = item.count,
                               item_price = item.items.price)
        session.add(order_item)
        res_price += item.items.price*item.count

    #оплата заказа юзером
    user = session.query(User).filter(User.id ==user_id).first()
    if not user:
        raise ValueError("Пользователь не найден")

    if user.money < res_price:
        raise ValueError("Недостаточно средств")

    user.money -= res_price

    #убрать товары из корзины
    for item in basket_items:
        session.delete(item)


    res_item_arr = []
    order_items = session.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    for item in order_items:
        res_images = None
        if item.items.images:
            main_images = [im for im in item.items.images if im.is_main]
            res_images = main_images[0].url if main_images else None
        res_item_arr.append(OrderItemSchema(item_id = item.item_id,item_name=item.items.name,
                                            item_image=res_images,count = item.count,
                                            item_price = item.items.price))

    #отправить сообщение
    send_email(user.email,"вы сделали такой-то такой-то заказ","New Order")

    return OrderSchema(id = order.id, items = res_item_arr,price = res_price)




def serv_get_all_orders(user_id:int,session):
    orders = session.query(Order).filter(Order.user_id == user_id).all()
    orders_arr = []
    for order in orders:
        res_item_arr = []
        res_price = 0
        for item in order.order_items:

            res_images = None
            if item.items.images:
                main_images = [im for im in item.items.images if im.is_main]
                res_images = main_images[0].url if main_images else None

            res_item_arr.append(OrderItemSchema(item_id = item.item_id,item_name=item.items.name,
                                                item_image=res_images,count = item.count,
                                                item_price = item.items.price))
            res_price += item.items.price*item.count
        orders_arr.append(OrderSchema(id = order.id, items = res_item_arr,price = res_price))
    return orders_arr

