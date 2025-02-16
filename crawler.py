import requests
import json
import pandas as pd
from datetime import datetime


def get_fund_information():
    url = "https://api.fmarket.vn/res/products/filter"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "types": ["NEW_FUND", "TRADING_FUND"],
        "issuerIds": [],
        "sortOrder": "DESC",
        "sortField": "navTo12Months",
        "page": 1,
        "pageSize": 100,
        "isIpo": False,
        "fundAssetTypes": [],
        "bondRemainPeriods": [],
        "searchField": "",
        "isBuyByReward": False,
        "thirdAppIds": []
    }
      

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()['data']['rows']
        pd.DataFrame(data).to_excel('all_funds_information.xlsx',index=False)
        return response.json()['data']['rows']
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


def get_fund_history(product_id):
    url = "https://api.fmarket.vn/res/product/get-nav-history"
    headers = {
        "Content-Type": "application/json"
    }
    

    payload = {
        "isAllData": 1,
        "productId": product_id,
        "fromDate": None,
        "toDate": datetime.today().strftime('%Y%m%d') # Get today's date in the format YYYYMMDD
    }


    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        return {"error": f"Request failed with status code {response.status_code}"}


def get_all_funds_history(list_product_id:list):
    lst_all_history = []
    for product_id in list_product_id:
        data_fund_id = get_fund_history(product_id)
        lst_all_history = lst_all_history + data_fund_id
    df_all_history = pd.DataFrame(lst_all_history)
    df_all_history.to_excel('all_funds_history.xlsx',index=False)
    return df_all_history


def get_vnindex_information(authorization):
    headers = {
    "authorization": authorization,}
    response = requests.get(f'https://restv2.fireant.vn/symbols/VNINDEX/historical-quotes?startDate=2000-01-16&endDate={datetime.today().strftime('%Y-%m-%d')}&offset=0&limit=100000',headers=headers)
    pd.DataFrame(response.json()).to_excel('all_vnindex_information.xlsx',index=False)

if __name__ == "__main__":
    data_funds_information = get_fund_information()
    df_funds_information = pd.DataFrame(data_funds_information)
    id_funds = df_funds_information['id'].values.tolist()
    get_all_funds_history(id_funds)

    # get authorization from this page: https://fireant.vn/dashboard/content/symbols/VNINDEX
    get_vnindex_information("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg")





