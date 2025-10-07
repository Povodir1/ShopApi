import requests
from app.models.user import CurrencyType

currency_data ={}


def update_data():
    usd_data = requests.get("https://api.nbrb.by/exrates/rates/431").json()  # Usd
    rub_data = requests.get(" https://api.nbrb.by/exrates/rates/456").json()  # RUB
    currency_data[CurrencyType.USD] = usd_data
    currency_data[CurrencyType.RUB] = rub_data

def convert_currency(cur_type:CurrencyType,value_usd):
    value_usd = float(value_usd)
    #вынести отсюда апдате и сделать его обновляемым
    if not currency_data:
        update_data()
    if cur_type == CurrencyType.USD:
        return value_usd
    elif cur_type == CurrencyType.BYN:
        return round(value_usd*currency_data[CurrencyType.USD]["Cur_OfficialRate"],2)
    elif cur_type == CurrencyType.RUB:
        return round((value_usd*currency_data[CurrencyType.USD]["Cur_OfficialRate"])/(currency_data[CurrencyType.RUB]["Cur_OfficialRate"]/currency_data[CurrencyType.RUB]["Cur_Scale"]),2)
    else:
        raise ValueError("Неприемлемая валюта")
