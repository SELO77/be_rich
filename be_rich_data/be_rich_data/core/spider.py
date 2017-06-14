import scrapy


class BeRichSpider(scrapy.Spider):

    def write_file_to_storage(self, data, filename, file_format=''):
        path = "%s%s.%s" % (self.settings.attributes['STORAGE_PATH'].value, filename, file_format)
        with open(path, '+wb') as f:
            if isinstance(data, str):
                data = bytes(data, encoding='utf-8')
            f.write(data)
