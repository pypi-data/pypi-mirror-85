import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
class get_stock_all:
    def __init__(self,*name_company,**kwargs):
        if bool(name_company)==True:
            a=name_company
            a1=''.join(a[0])
        else:
            a=input('Enter Company name: ')
            a1=a
        if bool(kwargs)==True:
            time_for_graph=kwargs['time']
        else:
            time_for_graph=input('Enter time period for graphs for eg 5d or 7y etc: ')
          
        a1=a1.replace(" ","%20")
        tgt_website = f'https://finance.yahoo.com/lookup?s={a1}'

        df_list = pd.read_html(tgt_website)
        result_df = df_list[0]
        result_df = result_df.drop(columns=['Industry / Category','Type'])
        if 'sure' in kwargs:
          stock = yf.Ticker(result_df['Symbol'][0])
        else:
          print(result_df)
          check_stock=input('Is your stock the top one in the table? If yes then type Y; if not then type the symbol of the stocck from the above table: ')
          if check_stock=='Y' or 'y':
              stock = yf.Ticker(result_df['Symbol'][0])
          else:
              stock = yf.Ticker(check_stock)
        info=stock.info
        info_table=pd.DataFrame.from_dict(info,orient='index')
        self.stock=stock
        self.name=a1
        self.info=stock.info
        self.history=stock.history(period=time_for_graph)
        self.stocklist=result_df
        self.table=info_table
    
    def make_graph(self):
      plt.plot(self.history['Open'])
    @classmethod
    def make_graph_two(cls,name_company1,name_company2,time):
      stock1=cls(name_company1,time=time,sure='True')
      stock2=cls(name_company2,time=time,sure='True')
      # Plot everything by leveraging the very powerful matplotlib package
      plt.plot(stock1.history['Open'],label=stock1.name)
      plt.plot(stock2.history['Open'],label=stock2.name)
      plt.legend()
      plt.show()  
    
    
      
