# from scrapy.settings import default_settings as settings


# def write_file(data, filename, file_format=''):
#     path = "%s%s.%s" % (settings['STORAGE_PATH'], filename, file_format)
#     with open(path, '+wb') as f:
#         if isinstance(data, str):
#             data = bytes(data, encoding='utf-8')
#         f.write(data)