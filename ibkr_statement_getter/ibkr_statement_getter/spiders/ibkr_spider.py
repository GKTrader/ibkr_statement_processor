import scrapy


class IbkrSpider(scrapy.Spider):
    name = "ibkr_statement"

    def start_requests(self):
        urls = ['file:///C:/Users/geoff/AppData/Local/Temp/ActivityStatement.20210716.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
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
                        print(asset_class)
                    elif row.css('td.indent'):
                        print('Skipping total row for {}'.format(row.css('.indent::text').extract()[0]))
                        pass
                    elif asset_class == None:
                        pass
                    else:
                        row_dict = {
                            'asset': row.css('td:nth-child(1)::text').extract_first(),
                            'asset_class': asset_class,
                            'init_pos': row.css('td:nth-child(2)::text').extract_first(),
                            'final_pos': row.css('td:nth-child(3)::text').extract_first(),
                            'init_px': row.css('td:nth-child(4)::text').extract_first(),
                            'final_px': row.css('td:nth-child(5)::text').extract_first(),
                            'pos_pnl': row.css('td:nth-child(6)::text').extract_first(),
                            'final_pnl': row.css('td:nth-child(7)::text').extract_first(),
                            'commissions': row.css('td:nth-child(8)::text').extract_first(),
                            'other_pnl': row.css('td:nth-child(9)::text').extract_first(),
                            'table': table
                        }
                        yield row_dict
            elif div_id == 'tblMTDYTDPerfSum_U379391Body':
                rows = response.css('div#{} table.table-bordered tr'.format(div_id))
                table = div_id
                asset_class = None
                for row in rows:
                    if row.css('td.header-asset'):  # No asset data, but asset class data that needs to be set until next header
                        asset_class = row.css('.header-asset::text').extract()[0]
                        print(asset_class)
                    elif row.css('td.indent'):
                        print('Skipping total row for {}'.format(row.css('.indent::text').extract()[0]))
                        pass
                    elif asset_class is None:
                        pass
                    else:
                        row_dict = {
                            'ticker': row.css('td:nth-child(1)::text').extract_first(),
                            'asset_class': asset_class,
                            'symbol': row.css('td:nth-child(2)::text').extract_first(),
                            'mtm_mtd': row.css('td:nth-child(3)::text').extract_first(),
                            'mtm_ytd': row.css('td:nth-child(4)::text').extract_first(),
                            'realized_st_mtd': row.css('td:nth-child(5)::text').extract_first(),
                            'realized_st_ytd': row.css('td:nth-child(6)::text').extract_first(),
                            'realized_lt_mtd': row.css('td:nth-child(7)::text').extract_first(),
                            'realized_lt_ytd': row.css('td:nth-child(8)::text').extract_first(),
                            'table': table
                        }
                        yield row_dict
            elif div_id == 'tblTransactions_U379391Body':
                rows = response.css('div#{} table.table-bordered tr'.format(div_id))
                table = div_id
                asset_class = None
                for row in rows:
                    if row.css('td.header-asset'):  # No asset data, but asset class data that needs to be set until next header
                        asset_class = row.css('.header-asset::text').extract()[0]
                        print(asset_class)
                    elif row.css('td.indent'):
                        print('Skipping total row for {}'.format(row.css('.indent::text').extract()[0]))
                        pass
                    elif asset_class is None:
                        pass
                    else:
                        row_dict = {
                            'symbol': row.css('td:nth-child(1)::text').extract_first(),
                            'asset_class': asset_class,
                            'transaction_time': row.css('td:nth-child(2)::text').extract_first(),
                            'quantity': row.css('td:nth-child(3)::text').extract_first(),
                            'trade_px': row.css('td:nth-child(4)::text').extract_first(),
                            'close_px': row.css('td:nth-child(5)::text').extract_first(),
                            'proceeds': row.css('td:nth-child(6)::text').extract_first(),
                            'comm_fee': row.css('td:nth-child(7)::text').extract_first(),
                            'basis': row.css('td:nth-child(8)::text').extract_first(),
                            'realized_pnl': row.css('td:nth-child(9)::text').extract_first(),
                            'mtm_pnl': row.css('td:nth-child(10)::text').extract_first(),
                            'code': row.css('td:nth-child(11)::text').extract_first(),
                            'table': table
                        }
                        yield row_dict
