import sys
import datetime
import json
import inspect
import traceback
import types

import scrapy

from ..utils.parsing import (
    extract_text_and_get_list,
    strip_crlf
)


class NaverStockSpider(scrapy.Spider):
    name = 'naver_stock'

    codes = [
        # '005930', # 한토신
        '010060', # OCI
        # '034830',
        # '093370',
        # '000660'
    ]
    url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={code}'
    # 주요재무정보
    # http: // companyinfo.stock.naver.com / v1 / company / ajax / cF1001.aspx?cmp_cd = 005
    # 930 & fin_typ = 0 & freq_typ = A
    url_A = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={code}&fin_typ=0&freq_typ=A'

    def start_requests(self):
        # urls = [
        #         'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=034830'
        #         ]
        # e_type, e_value, tb = sys.exc_info()
        # print(traceback.format_tb(tb))
        for code in self.codes:
            url = self.url.format(code=code)
            url_A = self.url_A.format(code=code)
            # yield scrapy.Request(url=url, callback=self.parse, flags=[code, ])
            yield scrapy.Request(url=url_A, callback=self.parse, flags=[code, '_A'])

    def _write_origin_text(self, response):
        try:
            filename = ''.join(response.request.flags) + '.html'
            # filename = '{0}_A.html'.format(str(response.request.flags[0]))
            message = response.body
        except (TypeError, ValueError) as e:
            filename = "error_%s" % datetime.datetime.utcnow()
            message = e.message

        with open(filename, 'wb') as f:
            f.write(message)
        self.log('Saved file %s' % filename)

    def _write_result_in_json(self, r):
        # TODO : write json
        j = json.dumps(r)
        with open('./data/', 'rb') as f:
            f.write(j)

    def parse(self, response):
        stock_code = response.request.flags[0]
        self._write_origin_text(response)

        # thead = response.css('thead')
        # r = self._parse_thead(thead)

        finance_period_partition = response.css('thead tr')
        top_title_tr = finance_period_partition[:1]
        period_partition_tr = finance_period_partition[1:]

        top_titles = top_title_tr.css('th')

        num_yearly_colums = None
        num_quarterly_column = None

        for i, title in enumerate(top_titles):
            # skip it. 주요재무정보
            if i == 0:
                continue

            # extract how many number of columns related yearly information
            elif i == 1:
                num_yearly_colums = int(title.css('::attr(colspan)').extract_first())  # 4

            # extract how many number of columns related quarterly information
            elif i == 2:
                num_quarterly_column = int(title.css('::attr(colspan)').extract_first())  # 4

        period_partitions = period_partition_tr.css('th')
        yearly_partition = period_partitions[:num_yearly_colums]
        quarterly_partition = period_partitions[num_quarterly_column:]

        # yearly_partition_text_list = [strip_crlf(extract_text_and_get_list(yearly_partition))]
        yearly_partition_text_list = [strip_crlf(_) for _ in extract_text_and_get_list(yearly_partition)]
        quarterly_partition_text_list = [strip_crlf(_) for _ in extract_text_and_get_list(quarterly_partition)]

        # for tr in finance_period_partition:
        #     th_list = tr.css('th')
        #     for th in th_list:
        #         text = th.css('::text').extract_first()

        finance_info_tr_list = response.css('tbody tr')

        fields = []
        values = []
        for tr in finance_info_tr_list:
            title = tr.css('th::text').extract_first()
            if title is None:
                continue

            data_rows = tr.css('td')
            yearly_rows = data_rows[:num_yearly_colums]
            quarterly_rows = data_rows[num_yearly_colums:]

            yearly_data = self._parse_tr(yearly_rows)
            quarterly_data = self._parse_tr(quarterly_rows)

            fields.append(title)
            values.append({
                'title': title,
                'yearly': yearly_data,
                'quarterly': quarterly_data

            })

        r = {
            'code': stock_code,
            'name': '!',
        }

        for i, year in enumerate(yearly_partition_text_list):
            d = {}
            for f in values:
                d[f['title']] = f['yearly'][i]
            r['Y'+year] = d

        for i, quarter in enumerate(quarterly_partition_text_list):
            d = {}
            for f in values:
                d[f['title']] = f['quarterly'][i]
            r['Q'+quarter] = d

    def _parse_tr(self, tr):
        if not hasattr(tr, "__iter__"):
            return
        values = []
        for row in tr:
            value = row.css('::text').extract_first()
            values.append(value)
        return values
