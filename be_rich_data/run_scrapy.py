import sys

from scrapy import cmdline


def get_spider_name(count=0):
    if count == 0:
        try:
            return sys.argv[1]
        except:
            print("Something is wrong!!")
            get_spider_name(count=(count+1))
    elif 4 > count > 0:
        spider_name = input('Input spider name that you wanna run.')
        try:
            return str(spider_name)
        except:
            print("Given wrong input %s" % spider_name)
            get_spider_name(count=(count+1))
    else:
        exit()


if __name__ == '__main__':
    spider_name = get_spider_name()
    command = "scrapy crawl %s" % spider_name
    cmdline.execute(command.split())