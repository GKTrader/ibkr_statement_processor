import scrapy
from ibkr_statement_getter.ibkr_statement_getter.items import DailyMarkToMarketItem, \
    DailyPerfSummItem, DailyTransactionItem

class IbkrSpider(scrapy.Spider):
    name = "ibkr_statement"

    # The way to do this is by defining custom_settings as a class attribute under the specific spider were
    # are writing the item exporter for. Spider settings override project settings.
    custom_settings = {
        'FEED_URI': 'ibkr_dict_lines.json',
        'FEED_FORMAT': 'jsonlines',
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'Q1.log',
        'FEEDS': {
            'ibkr_dict_lines.json': {
                'format': 'jsonlines',
                'overwrite': True
            }

        }
    }

    def __init__(self, statement_dates=['20210730']):
        self.statement_dates = statement_dates

    def start_requests(self):
        urls = []
        for date in self.statement_dates:
            urls.append('file:///C:/Users/geoff/Downloads/ActivityStatement.{}.html'.format(date))
        for iteration, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(date=self.statement_dates[iteration]))

    def parse(self, response, date):
        # tblMtmPerfSumByUnderlying_U379391Body
        # div with id, tbl with class
        asset_class = None
        div_ids = ['tblMtmPerfSumByUnderlying_U379391Body', 'tblMTDYTDPerfSum_U379391Body',
                   'tblTransactions_U379391Body']
        # need to somehow iterate over all three tables
        # Top Day Summary
        for div_id in div_ids:
            if div_id == 'tblMtmPerfSumByUnderlying_U379391Body':
                rows = response.css('div#{} table.table-bordered tr'.format(div_id))
                table = div_id
                for row in rows:
                    if row.css('td.header-asset'):  # Asset class data that needs to be set until next header
                        asset_class = row.css('.header-asset::text').extract()[0]
                    elif row.css('td.indent'):
                        print('Skipping total row for {}'.format(row.css('.indent::text').extract()[0]))
                        pass
                    elif asset_class == None:
                        pass
                    else:
                        perf_sum = DailyPerfSummItem()
                        perf_sum['asset'] = row.css('td:nth-child(1)::text').extract_first()
                        perf_sum['asset_class'] = asset_class
                        perf_sum['init_pos'] = row.css('td:nth-child(2)::text').extract_first()
                        perf_sum['final_pos'] = row.css('td:nth-child(3)::text').extract_first()
                        perf_sum['init_px'] = row.css('td:nth-child(4)::text').extract_first()
                        perf_sum['final_px'] = row.css('td:nth-child(5)::text').extract_first()
                        perf_sum['pos_pnl'] = row.css('td:nth-child(6)::text').extract_first()
                        perf_sum['final_pnl'] = row.css('td:nth-child(7)::text').extract_first()
                        perf_sum['commissions'] = row.css('td:nth-child(8)::text').extract_first()
                        perf_sum['other_pnl'] = row.css('td:nth-child(9)::text').extract_first()
                        perf_sum['table'] = table
                        perf_sum['date'] = date
                        yield perf_sum
            elif div_id == 'tblMTDYTDPerfSum_U379391Body':
                rows = response.css('div#{} table.table-bordered tr'.format(div_id))
                table = div_id
                asset_class = None
                for row in rows:
                    if row.css('td.header-asset'):  # No asset data, but asset class data that needs to be set until next header
                        asset_class = row.css('.header-asset::text').extract()[0]
                    elif row.css('td.indent'):
                        print('Skipping total row for {}'.format(row.css('.indent::text').extract()[0]))
                        pass
                    elif asset_class is None:
                        pass
                    else:
                        mark_to_mark_sum = DailyMarkToMarketItem()
                        mark_to_mark_sum['ticker'] = row.css('td:nth-child(1)::text').extract_first()
                        mark_to_mark_sum['asset_class'] = asset_class
                        mark_to_mark_sum['symbol'] = row.css('td:nth-child(2)::text').extract_first()
                        mark_to_mark_sum['mtm_mtd'] = row.css('td:nth-child(3)::text').extract_first()
                        mark_to_mark_sum['mtm_ytd'] = row.css('td:nth-child(4)::text').extract_first()
                        mark_to_mark_sum['realized_st_mtd'] = row.css('td:nth-child(5)::text').extract_first()
                        mark_to_mark_sum['realized_st_ytd'] = row.css('td:nth-child(6)::text').extract_first()
                        mark_to_mark_sum['realized_lt_mtd'] = row.css('td:nth-child(7)::text').extract_first()
                        mark_to_mark_sum['realized_lt_ytd'] = row.css('td:nth-child(8)::text').extract_first()
                        mark_to_mark_sum['table'] = table
                        mark_to_mark_sum['date'] = date
                        yield mark_to_mark_sum
            elif div_id == 'tblTransactions_U379391Body':
                rows = response.css('div#{} table.table-bordered tr'.format(div_id))
                table = div_id
                asset_class = None
                for row in rows:
                    if row.css('td.header-asset'):  # No asset data, but asset class data that needs to be set until next header
                        asset_class = row.css('.header-asset::text').extract()[0]
                    elif row.css('td.indent'):
                        print('Skipping total row for {}'.format(row.css('.indent::text').extract()[0]))
                        pass
                    elif asset_class is None:
                        pass
                    else:
                        trans_summ = DailyTransactionItem()
                        trans_summ['symbol'] = row.css('td:nth-child(1)::text').extract_first()
                        trans_summ['asset_class'] = asset_class
                        trans_summ['transaction_time'] = row.css('td:nth-child(2)::text').extract_first()
                        trans_summ['quantity'] = row.css('td:nth-child(3)::text').extract_first()
                        trans_summ['trade_px'] = row.css('td:nth-child(4)::text').extract_first()
                        trans_summ['close_px'] = row.css('td:nth-child(5)::text').extract_first()
                        trans_summ['proceeds'] = row.css('td:nth-child(6)::text').extract_first()
                        trans_summ['comm_fee'] = row.css('td:nth-child(7)::text').extract_first()
                        trans_summ['basis'] = row.css('td:nth-child(8)::text').extract_first()
                        trans_summ['realized_pnl'] = row.css('td:nth-child(9)::text').extract_first()
                        trans_summ['mtm_pnl'] = row.css('td:nth-child(10)::text').extract_first()
                        trans_summ['code'] = row.css('td:nth-child(11)::text').extract_first()
                        trans_summ['table'] = table
                        trans_summ['date'] = date
                        yield trans_summ
