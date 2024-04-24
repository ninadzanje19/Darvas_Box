def scrape_3M_data():

    import datetime
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    import os
    import csv


    # Read the CSV file into a DataFrame
    df = pd.read_csv('52_Week_High.csv')

    # Specify the column name you want to extract
    column_name = ' Company Name'  

    # Extract the column values into a list
    column_values = df[column_name].tolist()

    # Remove nan values from list
    company_list = [x for x in column_values if x == x]

    # This is the path for folder where you want to save 3M data csv files
    path = r"C:\Users\Dell\Desktop\My Projects\Sem 3 Project\Datasets"

    # Initialize a web driver (make sure you have the appropriate driver installed and configured)
    driver = webdriver.Chrome()

    # Open the MoneyControl website
    driver.get("https://www.moneycontrol.com/stocks/histstock.php")


    # In this for loop, we scrape 3M data from website company-wise
    for company in company_list:
        # Find and fill in the 'Enter company' text field
        company_input = driver.find_element_by_id("mycomp")
        company_input.clear()
        company_input.send_keys(company)
        time.sleep(1)  # Wait for suggestions to appear
        company_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for the page to load
        
        # Line 46 to 54 is used to enter value in listbox since just typing the value
        # in listbox still shows suggestions in dropdown box unless you select/enter the value
        dropdown_ul = driver.find_element(By.CLASS_NAME, "sugbx")

        # Find the list items ('li') within the 'ul' element
        dropdown_options = dropdown_ul.find_elements(By.TAG_NAME, "li")

        # Check if there are dropdown options
        if dropdown_options:
            # Click on the first option (you can adjust the index to select a different option)
            dropdown_options[0].click()

        # Select the 'From' date (3 months ago from current date)
        three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)
        '''datetime.datetime(2023,9,8)#(datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%d/%m/%Y")'''
        three_months_ago_str = three_months_ago.strftime("%d/%m/%Y")
        day, month, year = three_months_ago_str.split('/')
        form = driver.find_element_by_xpath("//form[@name='frm_dly']")
        from_date_day = Select(form.find_element_by_name("frm_dy"))
        from_date_day.select_by_value(day)
        from_date_month = Select(form.find_element_by_name("frm_mth"))
        from_date_month.select_by_value(month)
        from_date_year = Select(form.find_element_by_name("frm_yr"))
        from_date_year.select_by_value(year)
        

        """
        from_date_day.send_keys(day)
        from_date_month.send_keys(month)
        from_date_year.send_keys(year)"""

        # Select the 'To' date (current date)
        current_date = datetime.datetime.now() #three_months_ago + datetime.timedelta(days=90)#time.strftime("%d/%m/%Y")
        current_date_str = current_date.strftime("%d/%m/%Y")
        day, month, year = current_date_str.split('/')
        form = driver.find_element_by_xpath("//form[@name='frm_dly']")
        to_date_day = Select(form.find_element_by_name("to_dy"))
        to_date_day.select_by_value(day)
        to_date_month = Select(form.find_element_by_name("to_mth"))
        to_date_month.select_by_value(month)
        to_date_year = Select(form.find_element_by_name("to_yr"))
        to_date_year.select_by_value(year)
        
        """
        to_date_day.send_keys(day)
        to_date_month.send_keys(month)
        to_date_year.send_keys(year)"""

        # Click the 'Go' button (It goes to relevant historical data webpage)
        form = driver.find_element_by_xpath("//form[@name='frm_dly']")
        go_button = form.find_element_by_xpath("//input[@type='image']")
        #go_button = form.find_element_by_css_selector(f"img[src='{moneycontrol.com/images/histstock/go_btn.gif}']")
        driver.execute_script("arguments[0].click();", go_button)
        #go_button.click()

        # Wait for the data to load (you may need to adjust the time depending on your internet speed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tblchart")))  # Wait for the table to load

        # Extract the data (assuming there's a table with the desired columns)
        table = driver.find_element_by_xpath("//table[@class='tblchart']")
        rows = table.find_elements_by_tag_name("tr")

        data = []

        # Get the required data from historical data table
        # If there is no historical data , go to next company table
        for row in rows[2:]:  # Skip the header row
            try:
                columns = row.find_elements_by_tag_name("td")
                cname = company
                date = columns[0].text
                close = columns[4].text
                volume = columns[5].text
            except IndexError:
                print("No data to fetch")
                continue
            data.append([company,date, close, volume])
            
        # Create new csv file for each company and store it in folder
        filename = os.path.join(path, company + ".csv")

        # Write the data to a CSV file
        with open(filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company Name","Date", "Close", "Volume"])  # Write header row
            csvwriter.writerows(data)
            #csvwriter.writerows([])
        
        driver.get("https://www.moneycontrol.com/stocks/histstock.php")    
        

    # Close the web driver
    driver.quit()