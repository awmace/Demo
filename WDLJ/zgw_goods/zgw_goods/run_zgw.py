import os
from scrapy import cmdline

# os.system('scrapy crawl tly')
# cmdline.execute("scrapy crawl uploadcaicbao".split())
cmdline.execute("scrapy crawl zgw -o zgw.csv".split())
# cmdline.execute("scrapy crawl caicbao".split())
