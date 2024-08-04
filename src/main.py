import requests
import pandas as pd
import json
import time
from datetime import datetime, timedelta


def start_fetching_sarv_data():
    url = "https://gateway.farabixo.com/api/v2/candlesticks"
    login_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjJCOTAzOURDRUFBRkE1NUQxOENCRTFDRjFBOTBDOTBDIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3MjE0NzQzOTMsImV4cCI6MTcyMTQ5NTk5MywiaXNzIjoiaHR0cHM6Ly9hY2NvdW50LmlyZmFyYWJpLmNvbSIsImF1ZCI6WyJ0c2VfYXBpIiwiYmFzZV9hcGkiLCJzdGciXSwiY2xpZW50X2lkIjoiZmFyYWJpeG8tZGVza3RvcCIsInN1YiI6IjMxZDQ2MzZlLTI5ODctNDNiNS1hN2U1LTE4NDcwOGIyMDMyZiIsImF1dGhfdGltZSI6MTcyMTQ3NDM5MSwiaWRwIjoibG9jYWwiLCJuYXRpb25hbF9jb2RlIjoiNDA0MDE3NTM1MiIsImdpdmVuX25hbWUiOiLYs9i524zYryIsIm5hbWUiOiLYs9i524zYryDYuduM2YjYttuMIiwibG9naW5fdHlwZSI6InBhc3N3b3JkIiwiaGFzX3Bhc3N3b3JkIjoidHJ1ZSIsIm1mYV9lbmFibGVkIjoiZmFsc2UiLCJwaG9uZSI6IjA5MTkwODgyODUwIiwidHJhY2tlcl9pZCI6IlNsa0E0NHcrNklpbUJURDdoaGVlKzZNQlRFK3lSckNRYWU2Umk2OGZBTG89IiwicmVnaXN0ZXJfc3RhdHVzIjoiNSIsInRzZV9ib3Vyc2Vjb2RlIjoi2LnZitmIMDQxMjUiLCJ0c2VfYm91cnNlY29kZV9pZCI6IjU2NDc4MiIsInNlY3VyaXRpZXNFeGNoYW5nZUJvdXJzZUNvZGVCaW0iOiIxODk5NDA0MDE3NTM1MiIsInNlY3VyaXRpZXNFeGNoYW5nZUJvdXJzZUNvZGVJc2luIjoiSVI5NDA0MDE3NTM1MiIsInNlY3VyaXRpZXNFeGNoYW5nZUJvdXJzZUNvZGUiOiLYudmK2YgwNDEyNSIsImltZV9ib3Vyc2Vjb2RlX2lkIjoiNTY0NzgyIiwiaW1lX2JvdXJzZWNvZGUiOiIiLCJmb3JjZV9jaGFuZ2VfcGFzcyI6IkZhbHNlIiwibGFzdF9wYXNzX2NoYW5nZSI6IjExLzE5LzIwMjIgMTg6Mjk6NTkiLCJ1c2VyX2lkIjoiMTEwODczIiwidXNlcl9uYW1lIjoic2FlZWQuZXl2YXp5IiwidXNlcl90aXRsZSI6Itiz2LnbjNivINi524zZiNi224wiLCJ1c2VyX2VuX3RpdGxlIjoiICIsInVzZXJfY29kZSI6IjEwNTc2NCIsInBlcnNvbmFnZV9pZCI6IjE3NzYxNSIsImp0aSI6IkVGMkQyM0E3Q0JFQjhGMjY0MUJDOUQ0NjJBRjg5QkUxIiwic2lkIjoiQkFDNzMxNzUwQkY3REE2RTk4NjgzMjlCMDk3RTU2QkMiLCJpYXQiOjE3MjE0NzQzOTMsInNjb3BlIjpbImltZV9hcGkiLCJwcm90b19hcGkiLCJhZ2VudF9hcGkiLCJzYWRfYXBpIiwibWFya2V0X2FwaSIsImZ1bmRfYXBpIiwidHNlX2FwaSIsImJhc2VfYXBpIiwicHJvZmlsZSIsInNydmRza19hcGkiLCJ0c2VfcHJvZmlsZSIsIm9wZW5pZCIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyJwd2QiXX0.lmMDd_MzXFXYUdkc7YI4QS7DloEGgMpgHmG-bVWbdCG_qGwW9vaBY6gxJOLdFTsESb1Y4cgD0b1T0flqGr4EWgWZz9DR2BwIJBCoPG7qL904WTWjpwOMGi_N8WnDtrMGHOoFeyGk6wJP-5BOlponoLsO9QMCt8Ydfx2fNsmS2Do1wHskby26KC4MR82AIdcs4ekhqGGBT8O7TA3rqlRESmPf9bG5tQPjbO6cVptIsWRgmPCA0PvGv_Sakkf6Jcr6l6gJdNIchontjut9Brm18dHEWlOT0GFnjyZwSm7d8A-CljW0Y2a_0VkR2bzWJTnwVsJTxHZIL6W6v200u2KMoA"
    headers = {"Host": "gateway.farabixo.com",
               "Authorization": "Bearer " + login_token}

    params = {"records": "329", "interval": "4", "isin": "IRT1SARV0001", "priceType": 2, "dateType": 7, "direction": 1}

    r = requests.get(url, headers=headers, params=params)

    df = pd.DataFrame(json.loads(r.content)['candleStickDetails'])

    base_date = round(
        datetime.strptime(str(df.head(1).get('oTime')[0]).replace('T', ' '), '%Y-%m-%d %H:%M:%S').timestamp()) * 1000
    print(df.head())
    print(base_date)
    df.to_csv('sarv.csv')
    for i in range(100):
        params = {"records": "99", "interval": "4", "isin": "IRT1SARV0001", "priceType": 2, "dateType": 7,
                  "direction": 1, "baseDate": base_date}
        r = requests.get(url, headers=headers, params=params)
        df = pd.DataFrame(json.loads(r.content)['candleStickDetails'])
        if df.head().__len__():
            base_date = round(datetime.strptime(str(df.head(1).get('oTime')[0]).replace('T', ' '),
                                                '%Y-%m-%d %H:%M:%S').timestamp()) * 1000
            print(base_date)
            df.to_csv('sarv.csv', mode='a', index=True, header=False)
        else:
            yesterday = str((datetime.fromtimestamp(base_date / 1000) + timedelta(-1)).date())
            base_date = round(
                datetime.strptime(yesterday + ' ' + '09:00:00', '%Y-%m-%d %H:%M:%S').timestamp()) * 1000


def fetch_sarv_stock_data_from_farabi():
    start_fetching_sarv_data()

    sarv_df = pd.read_csv('sarv.csv')

    sorted_sarv_csv = sarv_df

    sorted_sarv_csv = sorted_sarv_csv.reset_index(drop=True)
    del sorted_sarv_csv['Unnamed: 0']
    sorted_sarv_csv = sorted_sarv_csv.set_index('oTime')
    sorted_sarv_csv.sort_index(inplace=True)

    sorted_sarv_csv.to_csv('sorted_sarv.csv')


# fetch_sarv_stock_data_from_farabi()


############################ MOFID ###########################

to_date_timestamp = str(round(time.time()))
from_date_timestamp = str(int(time.time()) - 86400*30) #subtract 30 days from to_date_timestamp


for i in range(60):
    print(to_date_timestamp)
    print(from_date_timestamp)

    url = "https://rlcchartapi.mofidonline.com/ChartData/history?symbol=IRX6XTPI0006_1&resolution=30&from=" + from_date_timestamp + "&to=" + to_date_timestamp
    url2 = "https://rlcchartapi.mofidonline.com/ChartData/history?symbol=IRT1SARV0001_1&resolution=30&from=" + from_date_timestamp + "&to=" + to_date_timestamp

    r = requests.get(url)
    r2 = requests.get(url2)

    shakhes_kol_mofid = pd.DataFrame.from_dict(json.loads(r.content))
    shakhes_kol_mofid.to_csv('shakhes_kol_mofid.csv', mode='a', index=False, header=False)

    sarv_mofid = pd.DataFrame.from_dict(json.loads(r2.content))
    sarv_mofid.to_csv('sarv_mofid.csv', mode='a', index=False, header=False)

    to_date_timestamp = from_date_timestamp

    from_date_timestamp = str(int(to_date_timestamp) - 86400*30)


a = pd.read_csv('shakhes_kol_mofid.csv')
a.columns = ['t','o','h','l', 'c','v', 's']

a['time'] = a['t'].apply(lambda x: datetime.fromtimestamp(round(float(x))))
a = a.reset_index(drop=True)
a = a.set_index('time')
a.sort_index(inplace=True)

a.to_csv('sorted_shakhes_kol_mofid.csv')


sarv_mofid = pd.read_csv('sarv_mofid.csv')
sarv_mofid.columns = ['t','o','h','l', 'c','v', 's']

sarv_mofid['time'] = sarv_mofid['t'].apply(lambda x: datetime.fromtimestamp(round(float(x))))
sarv_mofid = sarv_mofid.reset_index(drop=True)
sarv_mofid = sarv_mofid.set_index('time')
sarv_mofid.sort_index(inplace=True)

sarv_mofid.to_csv('sorted_sarv_mofid.csv')
