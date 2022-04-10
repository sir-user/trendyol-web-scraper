from cloudscraper import create_scraper
from bs4 import BeautifulSoup
from colorama import Fore, init
from time import localtime, strftime
import wait2load
from numpy import nan
from re import compile, search
import os


class TScraper:
    def __init__(self):
        self.url = "https://www.trendyol.com"
        self.w2l = wait2load.Wait2Load(self.url)

    @staticmethod
    def _to_html(url):
        scraper = create_scraper()
        trc = scraper.get(url).content
        return BeautifulSoup(trc, "lxml")

    def find_all_cats(self):
        """A category finder function from trendyol's website.

        This function returns a list of all categories. An element from list contains:

        [Gender, Category, Extension, Type]

        :return: list
        """
        links = []
        scraper = create_scraper()
        trc = scraper.get(self.url).content
        r = BeautifulSoup(trc, "lxml")
        x = r.find_all("li", class_="tab-link")
        for link in x:
            cat_boxes = link.find_all("div", class_="category-box")
            for cat_box in cat_boxes:
                cats = cat_box.find_all("a", href=compile("/"))
                for cat in cats[1:]:
                    links.append([link.a.text, cat_box.a.text, cat.get('href'), cat.text])
        return links

    def _find_product(self, url):
        links = []
        r = self._to_html(url)
        x = r.find_all("div", class_=compile("p-card-chldrn-cntnr"))
        for link in x:
            link = link.a.get('href')
            links.append(link)
        return links

    def find_product(self, ext, max_page=250):
        """A product writer function from trendyol's website.

        Trendyol allows us to search up to page 250. So max_page is limited by 250.

        A text document is written by the function to the data file inside the project file.
        File name writing rule is (category_extension)_date_time.txt

        :param ext: A category extension from all_cats function or any extension to fit with trendyol's website
        :param max_page: Last page to be processed
        :return: None
        """
        if max_page > 250:
            max_page = 250
        url = f"{self.url}{ext}"
        while True:
            try:
                first_page = self._find_product(url)
                if first_page:
                    break
            except Exception as err:
                print(Fore.RED + (str(err) + "\nConnection Error!\nConnecting to server"))
                init(autoreset=True)
                pass
        time_string = strftime("%m%d%Y_%H%M%S", localtime())
        project_directory = os.path.dirname(__file__)
        with open(f"{project_directory}/data{ext}_{time_string}.txt", "w+") as file:
            status = False
            for i in first_page:
                file.writelines(i + "\n")
            for page in range(2, max_page+1):
                print(page, f" / {max_page}")
                url = f"{self.url}{ext}?pi={page}"
                product_group = self._find_product(url)
                counter = 0
                while len(product_group) == 0:
                    product_group = self._find_product(url)
                    counter += 1
                    if counter > 10:
                        status = True
                        break
                for i in product_group:
                    if i in first_page:
                        print(i)
                        status = True
                        break
                    else:
                        file.writelines(i + "\n")
                if status:
                    print(Fore.YELLOW + "DONE!\nAll data is written to {}_{}.txt file.".format(ext[1:], time_string))
                    init(autoreset=True)
                    break
            file.close()

    @staticmethod
    def _find_product_name_brand(html):
        return html.find("h1", class_="pr-new-br")

    @staticmethod
    def _find_product_review(html):
        x = html.find("div", class_="pr-in-rnr")
        try:
            return int(x.find("a", class_="rvw-cnt-tx").text.split()[0])
        except AttributeError:
            return nan

    @staticmethod
    def _find_product_fav(html):
        try:
            return int(html.find("div", class_="fv-dt").text.split()[0])
        except AttributeError:
            return nan

    @staticmethod
    def _find_product_price(html):
        return float(html.find("span", class_="prc-dsc").text[:-3].replace(",", "."))

    @staticmethod
    def _product_to_cargo_days(html):
        return int(html.find("span", class_="dd-txt-vl").text.split()[0])

    @staticmethod
    def _find(source, class_name):
        """A function to find the classes what is look for

        :param source:  Source code from website
        :param class_name:  class_name for searching in source by looking class_name
        :return:    Returns the appropriate class tags for the search within a list.
        """
        soup = BeautifulSoup(source, "lxml")
        return soup.find_all("div", class_=class_name)

    def _product_after_load(self, ext):
        ttl = ["pr-mb-mn", "pr-in-rnr"]
        saf = self.w2l.page_source(ttl[0], ext)
        found = []
        for _class in ttl:
            while True:
                try:
                    found.append(self._find(saf, _class))
                    break
                except Exception as err:
                    saf = self.w2l.page_source(_class, ext)
                    print(Fore.RED + err)
                    init(autoreset=True)
        saf = BeautifulSoup(saf, "lxml")
        saf = saf.find("div", class_="container-right-content")  # This class includes all we want
        return saf, found

    @staticmethod
    def _find_product_seller(html):
        return html.find("div", class_="merchant-box-wrapper").a.text

    def _product_after_load_details(self, found):
        details = []
        if found[0]:
            details.append(found[0][0].find("div", class_="seller-container").a.text)                    # seller_name
            details.append(self.url + found[0][0].find("div", class_="seller-container").a.get('href'))  # seller_link
            details.append(float(found[0][0].find("div", class_="sl-pn").text))                          # seller_point
            if len(found[0]) > 1:
                other_seller_num = len(found[0])-1
                details.append(other_seller_num)                                                 # other_seller_num
                other_sellers = []
                for i in found[0][1:]:
                    other_sellers.append([i.find("div", class_="seller-container").a.text,
                                          float(i.find("div", class_="sl-pn").text)])            # [o_s_name, o_s_point]
                details.append(other_sellers)
            else:
                details.append(0)
                details.append(nan)
        else:
            details.append(nan)
            details.append(nan)
            details.append(nan)
            details.append(nan)
            details.append(nan)
        if found[1]:
            point = 0
            for i in (found[1][0].find("div", class_="rt-st-avg")).find_all("div", class_="star-w"):
                p = i.find("div", class_="full").get('style').split()[1][:-2]
                if p == "0p":
                    pass
                else:
                    point += int(p)

            if found[1][0].find("img"):
                details.append(1)           # image answer exist
            else:
                details.append(0)           # image answer does not exist
            details.append(point)           # product rate out of 500
        else:
            details.append(0)
            details.append(nan)

        return details

    @staticmethod
    def _find_text_between_tags(bs4_element):
        str_tag = str(bs4_element)
        return search(r'"h1">(.*?)<span>', str_tag).group(1)

    def find_product_details(self, ext):
        """A data finder for product from trenyol's website.

        The function returns a list by every process, they can be stored and turn to dataframe for some process.

        :param ext: A product extension from the 'product.txt' file by written 'find_product' function or any extension to fit with trendyol's website
        :return: [product_link, brand, name, fav, price, review, shipping_time(days), seller_name, seller_link, seller_point, num_of_other_sellers, other_seller_list[seller_name, seller_point], img_answer(0or1), product_rate(outof500)]
        """
        _product_link = f"{self.url}{ext}"
        data = [_product_link]
        ######
        counter = 0
        found = []
        while counter < 10:
            try:
                source, found = self._product_after_load(ext)
                _to_name_brand = self._find_product_name_brand(source)
                try:
                    data.append(_to_name_brand.a.text)              # brand
                except AttributeError:
                    data.append(self._find_text_between_tags(_to_name_brand))
                data.append(_to_name_brand.span.text[1:-1])         # name
                data.append(self._find_product_fav(source))         # fav
                data.append(self._find_product_price(source))       # price
                data.append(self._find_product_review(source))      # review
                try:
                    data.append(self._product_to_cargo_days(source))    # shipping time (days)
                except AttributeError:
                    data.append(nan)
                break
            except Exception as err:
                print(Fore.RED + (str(err) + "\nConnection Error!\nConnecting to server"))
                init(autoreset=True)
            counter += 1

        if counter == 10:
            return [_product_link, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]

        ######
        details = self._product_after_load_details(found)
        if len(data) == 0:
            data = [_product_link, nan, nan, nan, nan, nan, nan]
            details = [nan, nan, nan, nan, nan, nan, nan]
        data = data + details
        return data
