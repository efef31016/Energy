import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from pandas._libs.tslibs.timedeltas import Timedelta
import time
import warnings
warnings.filterwarnings("ignore")

class EVChargeTimeData:
    
    def __init__(self, df, st_name, ed_name, zone, power_disappear, save_path=""):
        
        '''
        parameters:
        df: DataFrame - at least including start_time, end_time, zone
        start_time_name_in_df: str - column name of recording start time points
        end_time_name_in_df: str - column name of recording end time points
        zone: str - name of park
        power_disappear: float - how many hours the power will disappear
        save_path: str - the path where you want to save the result image
        
        members:
        accu: list - EC every minute
        df: DataFrame - preprocessed data
        st_name: str - column name of recording start time points
        ed_name: str - column name of recording end time points
        time_range: pandas.core.indexes.datetimes.DatetimeIndex - continuous time in minute
        total_week: int - the number of weeks over data

        methods:
        delete_invalid_data: delete the duplicated and empty data
        which_idx: evaluate the index which time perioed cover in "accu"
        minute_EC: put the power in every minute
        minute_EC_plot: plot the EC data from "minute_EC"
        hour_load_data: transform the minute EC data into hourly load data
        hour_load_plotting: plot the load data from "hour_load_data"
        '''
        
        self.power_disappear = power_disappear
        self.st_name = st_name
        self.ed_name = ed_name
        self.zone = zone
        self.save_path = save_path
        
        # 把基本資訊印出並先算好每分鐘的用電量
        self.delete_invalid_data(df)
        self.rate_data_power_disappear()
        self.accu = self.minute_EC()
        print("after deleting")
        print(self.df.info())
        
    def delete_invalid_data(self, df):
        duplicates = df.duplicated(subset=[self.zone, self.st_name, self.ed_name])
        self.df = df[~duplicates]
        self.df.dropna(inplace=True)
    
    def rate_data_power_disappear(self,):
        
        self.df[self.st_name] = pd.to_datetime(self.df[self.st_name], format='%Y-%m-%d %H:%M:%S')
        self.df[self.ed_name] = pd.to_datetime(self.df[self.ed_name], format='%Y-%m-%d %H:%M:%S')

        num = 0
        se = self.df[self.ed_name] - self.df[self.st_name]
        for i in range(len(se)):
            if se.iloc[i] > Timedelta(hours=self.power_disappear):
                num+=1
        print("charging time over %d hour rate: "%self.power_disappear, num / len(se))
        
    
    def which_idx(self, start_time, end_time):
        hour_part = start_time.hour
        minute_part = start_time.minute
        start = datetime(start_time.year, start_time.month, start_time.day, hour_part, minute_part, 0)

        if end_time.minute==0:
            end_time += Timedelta(minutes=-1)
        hour_part = end_time.hour
        minute_part = end_time.minute
        end = datetime(end_time.year, end_time.month, end_time.day, hour_part, minute_part, 0)

        return pd.to_datetime(start), int((end - start).total_seconds() / 60)
    
    def minute_EC(self,):
        
        '''
        return: list - how strong power every minutes
        '''
        
        count_st = time.time()
        # 把秒去掉並注意最後一個時間點
        start_time = self.df[self.st_name].min()
        hour_part = start_time.hour
        minute_part = start_time.minute
        start_time = datetime(start_time.year, start_time.month, start_time.day, hour_part, minute_part, 0)
        end_time = self.df[self.ed_name].max()
        if end_time.minute!=0:
            end_time += Timedelta(minutes=1)
        self.time_range = pd.date_range(start=start_time, end=end_time, freq=f'{1}T')  # 為了取出每小時內EV最大值當作load

        # 一週的平均用
        self.total_week = (end_time-start_time).days//7
        print("total weeks: ", self.total_week)

        # 計算 EC 數量
        print("evaluating power every minute...")
        accu = np.zeros(len(self.time_range))
        for _,row in self.df.iterrows():
            target_time, idx = self.which_idx(row[self.st_name], row[self.ed_name])
            target_idx = self.time_range.get_loc(target_time)
            accu[target_idx:target_idx + min(idx, self.power_disappear*60)] += 1

        count_et = time.time()
        print("total time: ", count_et-count_st)
        return accu
    
    
    def minute_EC_plot(self,):
        
        '''
        return: dataframe - minute power weekly
        '''
        weekday = self.time_range.dayofweek + 1
        hour = self.time_range.hour
        minute = self.time_range.minute
        total = pd.Index(self.accu, dtype="int64")
        data = {"Datetime": self.time_range, "Weekday": weekday, "Hour": hour, "Minute": minute, "Total": total}
        self.df_plot = pd.DataFrame(data)
        # print(df_plot.info())
        weekly_sum = self.df_plot.groupby(["Weekday", "Hour", "Minute"])["Total"].sum().reset_index()
        plt.bar(range(len(weekly_sum)), weekly_sum["Total"])
        plt.title("weekly EC(min)")
        plt.xlabel("min")
        plt.ylabel("EC")
        label = [60*24*i for i in range(7)]
        plt.xticks(label, labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        plt.savefig(self.save_path + "weekly_EV_min.png")
        plt.show()
        
        
    def hour_load_data(self,):
        
        '''
        抓取負載資料
        return: dictionary - hourly power every week
        '''
        
        h=int()
        new_accu = self.accu
        self.hour_load = dict(zip([i for i in range(1,8)],[[0 for i in range(24)] for i in range(7)]))
        tmp = 0
        not_full_day=0
        print("初始化負載字典: ", self.hour_load)
        for i, t in enumerate(self.time_range):

            if i == 0:
                h = t.hour

            if h!=t.hour:
                h = t.hour
                self.hour_load[t.dayofweek+1][h] += max(new_accu[tmp:i-1])
                tmp = i-1
                not_full_day=0
            else:
                not_full_day+=1
                if i==len(self.time_range)-1:
                    self.hour_load[t.dayofweek+1][t.hour] += max(new_accu[-not_full_day-1:])

        # 後面未滿一小時的也要算進去
        print("=======最後%d分鐘未滿一小時======="%(-not_full_day-1))
        print("時(h)為單位的負載字典: ", self.hour_load)
    
    def hour_load_plotting(self,):
        
        self.hour_load_data()
        
        '''
        執行完hour_load_data，能依照負載資料畫出圖
        '''
        
        hour_load_plot = [value for sublist in self.hour_load.values() for value in sublist]
        self.max_value = []
        for m in self.hour_load.values():
            self.max_value.append((m.index(max(m)),int(max(m))))

        plt.figure(figsize=(8, 4))
        plt.bar(range(len(hour_load_plot)), hour_load_plot, label="load")
        label = [24*i for i in range(7)]
        vertical_label = label
        for i in range(7):
            vertical_label[i] += self.max_value[i][0]
            if i<6:
                plt.axvline(vertical_label[i], color="r", linestyle='--', linewidth=1)
                plt.text(vertical_label[i]+0.01, 2500, str(self.max_value[i][0]+1)+":00", rotation=0, fontsize=12, color='r')
            else:
                plt.axvline(vertical_label[i], color="r", linestyle='--', linewidth=1, label="max load time")
                plt.text(vertical_label[i]+0.01, 2500, str(self.max_value[i][0]+1)+":00", rotation=0, fontsize=12, color='r')
                
        plt.xticks(label, labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        plt.xlabel("min")
        plt.ylabel("load")
        plt.legend(loc="lower right")
        plt.title('weekly load(hour)')
        plt.savefig(self.save_path + "weekly_load_hour.png")
        plt.show()