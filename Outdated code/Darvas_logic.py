import pandas as pd
import numpy as np

UPPER_BOX_LIMIT = 10
LOWER_BOX_LIMIT = -10

week_high_52 = pd.read_csv("52_Week_High.csv")
# number of companies currently is 15
breakout_stocks_list = []
#stocks broken out of box that are to be brought
box_check = False

def darvas_logic():
    for i in range(0, len(week_high_52[" Company Name"])):
        stock_name = week_high_52[" Company Name"][i]
        stock_price = week_high_52.iloc[i]
        # stock_price[0] = stock name
        print(stock_name)
        for value in range(1, len(stock_price) - 1):
            stock_price[value] = float(stock_price[value])
            stock_price[value + 1] = float(stock_price[value + 1])
            print(str(stock_price[value]) + "-" + str(stock_price[value + 1]) + " = " + str(stock_price[value] - stock_price[value + 1]))
            if stock_price[value] - stock_price[value + 1] > UPPER_BOX_LIMIT:
                print("Breakout of box, buy it!!!")
                breakout_stocks_list.append(stock_name)
                break
            elif stock_price[value] - stock_price[value + 1] < LOWER_BOX_LIMIT:
                print("Stop loss omitted, sell it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                break
            elif stock_price[value] - stock_price[value + 1] > -10 and stock_price[value] - stock_price[value + 1] < 10:
                print("Stagnating in the box")

darvas_logic()
#Cycle 1 check from moneycontrol if there are any stocks that are breaking out of the box
#Cycle 2 check
# from the list of stocks that have previously broken out and wether they have broken any stoploss or not