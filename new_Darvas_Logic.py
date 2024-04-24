def new_Darvas_logic():
    import pandas as pd
    file = pd.read_csv("Datasets\ABB India.csv")
    
    upper_bound = 10
    lower_bound = -10
    
    breakout_prices = []
    lossy_prices = []
    
    closing_price_list = list(file["Close"])
    price_differences = [closing_price_list[i] - closing_price_list[i-1] for i in range(1, len(closing_price_list))]
    column_index = 0

    for diff in price_differences:
        if diff > upper_bound:
            column_index += 1
            print(f"Breakout at {diff}")
            print(column_index)
            breakout_prices.append(diff)
            #break
        elif diff < lower_bound:
            column_index += 1
            print(f"SL omitted at {diff}")
            print(column_index)
            lossy_prices.append(diff)
            #break
        else:
            column_index += 1
            print("stagnate")
            continue
        
    return breakout_prices, lossy_prices, closing_price_list

breakout_prices, lossy_prices, closing_price_list = new_Darvas_logic()