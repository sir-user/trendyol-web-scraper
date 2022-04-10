import trendyolscraper
import pandas as pd


def csv_format(p_details):
    data = {
        "Product Link": [p_details[0]],
        "Brand": [p_details[1]],
        "Name": [p_details[2]],
        "Fav": [p_details[3]],
        "Price": [p_details[4]],
        "Review": [p_details[5]],
        "Shipping Time (Days)": [p_details[6]],
        "Seller Name": [p_details[7]],
        "Seller Link": [p_details[8]],
        "Seller Point": [p_details[9]],
        "Num of Other Sellers": [p_details[10]],
        "Other Seller List": [p_details[11]],
        "Image Answer (0 or 1)": [p_details[12]],
        "Product Rate": [p_details[13]]
    }
    return data


def threader(ext):
    lw = trendyolscraper.TScraper()
    df = pd.DataFrame(csv_format(lw.find_product_details(ext)))
    df.to_csv('example.csv', mode='a', index=False, header=False)
