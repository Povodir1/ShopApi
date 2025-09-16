from app.database import db_session
from app.models.order import Order
from app.models.basket_item import BasketItem
from app.models.order_item import OrderItem
from app.schemas.order import OrderSchema,OrderItemSchema

def serv_create_order(user_id:int):
    with db_session() as session:
        #задать пустой заказ
        order = Order(user_id = user_id,price = 0,)
        session.add(order)
        session.commit()
        session.flush(order)

        #добавить товары в заказ
        basket_items = session.query(BasketItem).filter(BasketItem.user_id == user_id).all()
        res_price = 0
        for item in basket_items:
            order_item = OrderItem(item_id = item.item_id,order_id = order.id,count = item.count,item_price = item.items.price)
            session.add(order_item)
            res_price += item.items.price*item.count


        #обновить цену товара
        order.price = res_price
        session.commit()
        session.flush(order)

        #убрать товары из корзины
        for item in basket_items:
            session.delete(item)


        res_item_arr = []
        res_price = 0
        order_items = session.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        for item in order_items:
            res_item_arr.append(OrderItemSchema(id = item.id,item_id = item.item_id,count = item.count,item_price = item.items.price))
            res_price += item.items.price*item.count
        return OrderSchema(id = order.id, items = res_item_arr,price = res_price)



def serv_get_all_orders(user_id:int):
    with db_session() as session:
        orders = session.query(Order).filter(Order.user_id == user_id).all()
        orders_arr = []
        for order in orders:
            res_item_arr = []
            res_price = 0
            for item in order.order_items:
                res_item_arr.append(OrderItemSchema(id = item.id,item_id = item.item_id,count = item.count,item_price = item.items.price))
                res_price += item.items.price*item.count
            orders_arr.append(OrderSchema(id = order.id, items = res_item_arr,price = res_price))
        return orders_arr

