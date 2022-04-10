import trendyolscraper

# The find_product function writes the extensions of the products in the current category.
# Trendyol doesn't allow to exceed 250. page. So, max_page should be under 250 or equal.

LW = trendyolscraper.TScraper()

cat = "/elbise-x-c56"               # A random category was taken as 'cat' from the return of the all_cats function.

LW.find_product(cat)
