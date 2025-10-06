import requests
from app.models.user import CurrencyType

currency_data ={}


def update_data():
    usd_data = requests.get("https://api.nbrb.by/exrates/rates/431").json()  # Usd
    rub_data = requests.get(" https://api.nbrb.by/exrates/rates/456").json()  # RUB
    currency_data['usd'] = usd_data
    currency_data['rus'] = rub_data

def convert_currency(cur_type:CurrencyType,value_usd):
    if cur_type == CurrencyType.usd:
        return value_usd
    elif cur_type == CurrencyType.byn:
        return round(value_usd*currency_data['usd']["Cur_OfficialRate"],2)
    elif cur_type == CurrencyType.rub:
        return round((value_usd*currency_data['usd']["Cur_OfficialRate"])/(currency_data['rus']["Cur_OfficialRate"]/currency_data['rus']["Cur_Scale"]),2)
    else:
        raise ValueError("Неприемлемая валюта")

