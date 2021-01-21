# -*- coding: utf-8 -*-

# Scrapy settings for zgw_goods project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

BOT_NAME = 'zgw_goods'

SPIDER_MODULES = ['zgw_goods.spiders']
NEWSPIDER_MODULE = 'zgw_goods.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'zgw_goods (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 33

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en',
#     # 'x-csrf-token': '1ymHTzYJZCRR40ZNryeTWYGW',
#     # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
#     # 'Cookie': 'homedoLogCID=1b3d31e2-0783-4887-bb20-a2151b50bb50; homedoLogTID=7ee66c37-1986-4fd0-ab2e-8948d71e4d09; homedoLogFpth=https%3A%2F%2Fb2b.homedo.com%2Fproduct%2Fsearch%3FcategoryId%3D10028; homedoLogFpthST=1611023333297; ARK_ID=JS8939d0c90ce7bcb8fd6c7e996acad37f8939; HMD_R=160973825985188122; UM_distinctid=176cbe090e4ab3-0fb0f6f2a435bf-c791039-240000-176cbe090e5d18; gr_user_id=a026e177-e9f0-41b2-ba76-4f37873b7aa2; grwng_uid=478f95b2-af76-49aa-ba80-50c6bf8a8c03; NTKF_T2D_CLIENTID=guest4B38EA92-E7EA-7836-A72C-CBE0AC385551; OriginCode=%3futm_source%3dwmt_sem_baidupc%26utm_medium%3dCPC%26utm_term%3d180524%26utm_content%3d180009516%26utm_campaign%3d18013&2021/1/18 17:42:47; Hm_lvt_d1d21a226b3b6cbb96842713353fc9f7=1609738261,1610326869,1610933466,1610962970; csrfToken=1ymHTzYJZCRR40ZNryeTWYGW; BrowseInfo=100595464; acw_tc=76b20f6316110227270182972e2bfcc9a7781766db97114ec91d5ae8970991; ARK_STARTUP=eyJTVEFSVFVQIjp0cnVlLCJTVEFSVFVQVElNRSI6IjIwMjEtMDEtMTkgMTA6MTg6NDkuNzUzIn0%3D; CNZZDATA1257983938=1843867308-1609734998-https%253A%252F%252Fwww.homedo.com%252F%7C1611019571; calendarData=19; a016ee4c2a76b6bb_gr_session_id=e4b92ae3-ac5f-40bb-a585-a5b5aab249ff; a016ee4c2a76b6bb_gr_session_id_e4b92ae3-ac5f-40bb-a585-a5b5aab249ff=true; calendarProp=true; browseNumber=%5B%7B%22aId%22%3A0%2C%22num%22%3A8%7D%5D; FZ_STROAGE.homedo.com=eyJBUktTVVBFUiI6eyJwbGF0Zm9ybV9leHRyYSI6IlBDIn0sIlNFRVNJT05JRCI6IjMxNWI2MGUzNDFkYzMyOGMiLCJTRUVTSU9OREFURSI6MTYxMTAyMzMzMjgyOCwiQU5TQVBQSUQiOiI2NmYyNzcwNGQzMTYyMjQ3IiwiQU5TJERFQlVHIjoyLCJBTlNVUExPQURVUkwiOiJodHRwczovL3Nkay5ob21lZG8uY29tIiwiRlJJU1REQVkiOiIyMDIxMDEwNCIsIkZSSVNUSU1FIjpmYWxzZSwiQVJLX0lEIjoiSlM4OTM5ZDBjOTBjZTdiY2I4ZmQ2YzdlOTk2YWNhZDM3Zjg5MzkiLCJBUktGUklTVFBST0ZJTEUiOiIyMDIxLTAxLTA0IDEzOjMxOjAwLjQwOCJ9; Hm_lpvt_d1d21a226b3b6cbb96842713353fc9f7=1611023333'
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'zgw_goods.middlewares.ZgwGoodsSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'zgw_goods.middlewares.ZgwGoodsDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zgw_goods.pipelines.ZgwGoodsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
VERSION = time.strftime('%Y%m%d', time.localtime(time.time()))
