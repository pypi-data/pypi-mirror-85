stockmarkettools is a one stop shop for all your stock market needs. It can give past data of stock, make graphs comparing two stocks, give information of a company including description, logo, assests, etc.


# Documentation

Replace `infosys` or `wipro` with the stock names where ever applicable.


`get_stock_all` is the main python class which users will be accessing.

### Makes graph of the performance of the company
```
get_stock_all('infosys',time='1y',sure='True').make_graph()

```

### Returns dictionary with the information of the company.
```
micr=get_stock_all('infosys',time='1d').info
print(micr)
```

### Returns the stocks it found for the input in differnt stock exchanges along with their yahoo codes
```
micr=get_stock_all('infosys',time='1d',sure='True').stocklist
print(micr)
```


### Returns the previous prices of the stock
```
micr=get_stock_all('infosys',time='1d',sure='True').history
print(micr)
```



### Makes Graph comparing two stocks
```
get_stock_all.make_graph_two('infosys','wipro','1y')
```


### Returns the infomation of the company in the form of a pandas Dataframe
```
micr=get_stock_all('infosys',time='1d',sure='True').table
print(micr)
```






Adding `sure='True'` will bypass confirming if stock exchange and stock is right or not.
By default the code will provide you a table and confirm if desired stock actually matches.

Add `time='time_period_you_want'` as an argument in the code to retrieve information for the provided time period.
