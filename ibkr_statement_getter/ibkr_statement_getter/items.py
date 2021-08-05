# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DailyPerfSummItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    table = scrapy.Field()
    asset = scrapy.Field()
    asset_class = scrapy.Field()
    init_pos = scrapy.Field()
    final_pos = scrapy.Field()
    init_px = scrapy.Field()
    final_px = scrapy.Field()
    pos_pnl = scrapy.Field()
    final_pnl = scrapy.Field()
    commissions = scrapy.Field()
    other_pnl = scrapy.Field()

class DailyMarkToMarketItem(scrapy.Item):
    date = scrapy.Field()
    table = scrapy.Field()
    ticker = scrapy.Field()
    asset_class = scrapy.Field()
    symbol = scrapy.Field()
    mtm_mtd = scrapy.Field()
    mtm_ytd = scrapy.Field()
    realized_st_mtd = scrapy.Field()
    realized_st_ytd = scrapy.Field()
    realized_lt_mtd = scrapy.Field()
    realized_lt_ytd = scrapy.Field()

class DailyTransactionItem(scrapy.Item):
    date = scrapy.Field()
    table = scrapy.Field()
    symbol = scrapy.Field()
    asset_class = scrapy.Field()
    transaction_time = scrapy.Field()
    quantity = scrapy.Field()
    trade_px = scrapy.Field()
    close_px = scrapy.Field()
    proceeds = scrapy.Field()
    comm_fee = scrapy.Field()
    basis = scrapy.Field()
    realized_pnl = scrapy.Field()
    mtm_pnl = scrapy.Field()
    code = scrapy.Field()
