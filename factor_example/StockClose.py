from datetime import datetime, timedelta
from typing import List, Tuple
import pandas as pd

import rqdatac as rq

from factorbase.factor import Factor, SecurityType, Frequency


class StockClose(Factor):
    def __init__(self):
        rq.init()
    
    def factor_name(self) -> str:
        return "StockClose"
    
    def author(self) -> str:
        return "xitong"

    @Factor.checker
    def frequency(self) -> Frequency:
        return Frequency.DAILY

    @Factor.checker
    def security_type(self) -> SecurityType:
        return SecurityType.STOCK

    @Factor.checker
    def trigger_time(self) -> str:
        return "0 1 15 * * * *"

    @Factor.checker
    def run(self, start_time: datetime, end_time: datetime) -> Tuple[pd.DataFrame, Exception]:
        codes = set()
        dt = start_time
        while dt <= end_time:
            codes |= set(rq.all_instruments(type="Stock", date=dt)['order_book_id'].to_list())
            dt += timedelta(days=1)
        codes = sorted(list(codes))
        
        df_px = rq.get_price(codes,
                          start_date=start_time.strftime('%Y-%m-%d'),
                          end_date=end_time.strftime('%Y-%m-%d'),
                          frequency='1d')
               
        df = pd.DataFrame(index=df_px.index.levels[1].rename('datetime'), columns=['gen_time'] + codes)
        for idx in df_px.index:
            sym, day = idx
            close_px = df_px.loc[idx, 'close']
            
            df.loc[day, sym] = close_px
            df.loc[day, 'gen_time'] = day + timedelta(hours=15)
            
        return df, None



if __name__ == '__main__':
    now = datetime.now()
    close = StockClose()
    try:
        df, err = close.run(now - timedelta(days=10), now)
    except Exception as e:
        print("error: ", e)
        exit(-1)
    
    print(df, err)
    df.to_pickle("StockClose.pkl")
    