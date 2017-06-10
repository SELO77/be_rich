import scrapy
import datetime


class NaverStockSpider(scrapy.Spider):
    name = 'naver_stock'

    codes = ['005930', '034830']
    base_url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={code}'
    # 주요재무정보
    # http: // companyinfo.stock.naver.com / v1 / company / ajax / cF1001.aspx?cmp_cd = 005
    # 930 & fin_typ = 0 & freq_typ = A
    base_url_A = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={code}&fin_typ=0&freq_typ=A'

    def start_requests(self):
        # urls = [
        #         'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=034830'
        #         ]
        for code in self.codes:
            url = self.base_url.format(code=code)
            url_A = self.base_url_A.format(code=code)
            yield scrapy.Request(url=url, callback=self.parse, flags=[code, ])
            yield scrapy.Request(url=url_A, callback=self.parse, flags=[code, '_A'])

    def parse(self, response):
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
