import requests
import json
import pandas as pd
import re
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ScrawlData:
    def __init__(self, url_json, verbose = True,
                 save_path = "C:/Users/User/Desktop/fetching_data/Taipower_data/energy_generation/",
                 column_name=["機組名稱", "裝置容量", "淨發電量", "備註"]):
        
        self.url = url_json
        self.verbose = verbose
        self.save_path = save_path
        self.column_name = column_name
        
        self.initial()
        
    def trans_data(self,):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = json.loads(response.text)
                print("Succesfully!")
                return data
            else:
                print(f"Status Code：{response.status_code}")
        except Exception as e:
            print(f"ERROR：{e}")

            
    # 查看所有能源種類
    def find_energy(self, text):
        match = re.search(r"<A NAME='([^']+)'></A><b>([^<]+)</b>", text)
        if match:
            return match.group(2)
        else:
            pass


    def ten_minute_data(self, data):
        df=pd.DataFrame()
        for dt in data["aaData"]:
            val = dt[2:6]
            new_row = dict(zip(self.column_name, val))
            new_row = pd.Series(new_row)
            new_row.name = pd.to_datetime(data[""])
            df = pd.concat([df, new_row], ignore_index=False)

        return df


    def save_file(self,):
        tmp_path = self.save_path + "generation_%s.csv"%datetime.now().strftime("%Y-%m-%d")
        df = pd.concat(self.df_list, keys=pd.to_datetime(self.idx_list))
        df.to_csv(tmp_path)
        print("saved at %s."%tmp_path)
        return tmp_path
        
        
    def initial(self,):
        self.nextday = 0
        self.count_m = 0
        self.df_list = []
        self.idx_list = []
        self.df = pd.DataFrame()
        
        # 一日/個月等於幾個 10 分鐘
        self.three_month = 6*24*30*3
        self.one_day = 6*24
        
    def Scrawing(self,):

        while True:

            # 若經過一天，我們匯入前一天資料繼續進行合併
            if self.nextday:
                self.df_list.append(pd.read_csv(tmp_path))
                self.nextday=0
            else:
                pass
            

            # 每十分鐘我們存下資料及指標
            data = self.trans_data()
            df_ten = self.ten_minute_data(data)
            self.df_list.append(df_ten)
            tmp_time = datetime.now()
            self.idx_list.append(tmp_time)
            if self.verbose:
                print(self.df_list)
                print(self.idx_list)

            if self.count_m < self.three_month:

                # 每日先存一次，為了保險起見
                if len(self.df_list) == self.one_day:
                    tmp_path = self.save_file()
                    self.nextday = 1
                    self.df_list = []

                self.count_m+=1

            # 滿三個月存成一筆，全部回到初始狀態
            else:
                self.save_file()
                self.initial()

            time.sleep(60*10)
            print("Wait ten minutes...")