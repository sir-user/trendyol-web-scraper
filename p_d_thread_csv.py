import threading
import os
from threader import *
from time import time, sleep
from console_writer import console_writer


def thread_product_details(txt, waiting=None, limit=None, csv_name="example"):
    """A function which is faster by using threading, has same purpose with product_details function.

    This function must be use alone to store data in a csv file.

    Do not include it in any algorithm.

    Function runs 8 product_details by threading. This process takes a time related to your internet speed. But threading makes it 8 time faster by process these at the almost same time.
    So this func should not include it in any algoritm.

    :param txt: product txt file name, do not include '.txt'
    :param waiting: waiting time for between threading groups to not hurt the cpu
    :param limit:   limit of processing data from txt
    :param csv_name:    will be csv name for your data
    """
    lw = trendyolscraper.TScraper()

    project_directory = os.path.dirname(__file__)      # The project directory from 'example' file

    with open(f"{project_directory}/data/{txt}.txt", "r") as file:
        lines = file.readlines()

        start = time()
        df = pd.DataFrame(csv_format(lw.find_product_details(lines[0][:-1])))
        df.to_csv(f'{csv_name}.csv', index=False)
        if waiting:
            sleeping = waiting
            if sleeping > 8:
                sleeping = 12
        else:
            sleeping = time() - start + 2

        counter = 0
        full = len(lines) - 1

        for line in lines[1:]:
            threading.Thread(target=threader, args=(line[:-1],)).start()     # Not taking \n's as inputs with [:-1]
            console_writer(int((counter/full)*100))
            counter += 1
            if counter % 8 == 0:
                sleep(sleeping)
            if limit:
                if counter == limit:
                    break
            else:
                pass

        file.close()


def view_csv(csv_name="example"):
    df = pd.read_csv(f'{csv_name}.csv')
    print(df.head().to_markdown())
