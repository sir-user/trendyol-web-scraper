import os
import trendyolscraper
import time

# You can review code below to see product details.
# [product_link, brand, name, fav, price, review, shipping_time(days), seller_name, seller_link, seller_point,
# num_of_other_sellers, other_seller_list[seller_name, seller_point], img_answer(0or1), product_rate(outof500)]

txt = "elbise-x-c56_04072022_184024.txt"
# To create this file, run find_product function.
# This text document is written inside the project file.
# File name writing rule is (category_extension)_date_time.txt

LW = trendyolscraper.TScraper()

project_directory = os.path.dirname(os.path.dirname(__file__))      # The project directory from 'example' file

with open(f"{project_directory}/data/{txt}", "r") as file:
    lines = file.readlines()
    for line in lines:
        start = time.time()
        print(LW.find_product_details(line[:-1]))                   # Not taking \n's as inputs with [:-1]
        print("Process time :", time.time()-start)
    file.close()
