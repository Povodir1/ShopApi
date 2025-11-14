import requests
from app.models.user import CurrencyType
#from fastapi import BackgroundTasks

currency_data ={}


def update_data():
    usd_data = requests.get("https://api.nbrb.by/exrates/rates/431").json() # Usd
    rub_data = requests.get(" https://api.nbrb.by/exrates/rates/456").json()  # RUB
    currency_data[CurrencyType.USD] = 1
    currency_data[CurrencyType.BYN] = float(usd_data["Cur_OfficialRate"]/usd_data["Cur_Scale"])
    currency_data[CurrencyType.RUB] = float(currency_data[CurrencyType.BYN]/(rub_data["Cur_OfficialRate"]/rub_data["Cur_Scale"]))

def convert_currency(input_type:CurrencyType,output_type:CurrencyType,value):
    value = float(value)
    #вынести отсюда апдате и сделать его обновляемым
    if not currency_data:
        update_data()
    return  round(value*(1/currency_data[input_type])*currency_data[output_type],2)


