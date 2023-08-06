from pandas_datareader import data as web
import datetime
import pandas as pd

start = datetime.datetime(1987,1,1)
end = datetime.date.today()

apple = web.DataReader("AAPL", "yahoo", start, end)['Close']
ibm = web.DataReader("IBM", "yahoo", start, end)['Close']
microsoft = web.DataReader("MSFT", "yahoo", start, end)['Close']
oracle = web.DataReader("ORCL", "yahoo", start, end)['Close']
data = pd.DataFrame([apple, ibm, microsoft, oracle], index=['apple', 'ibm', 'microsoft', 'oracle']).T

data.head()