import trendyolscraper

# find_all_cats returns lists of [Gender, Category, Extension, Type]

LW = trendyolscraper.TScraper()

cats = LW.find_all_cats()

for cat in cats:
    print(cat)
