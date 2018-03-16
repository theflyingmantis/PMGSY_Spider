import scrapy

class GPItem(scrapy.Item):
    DistrictName = scrapy.Field()
    StateName = scrapy.Field()
    Year = scrapy.Field()
    Month = scrapy.Field()
    Nos = scrapy.Field()
    Length = scrapy.Field()
    Cost = scrapy.Field()
    Jun = scrapy.Field()
    Jul = scrapy.Field()
    Aug = scrapy.Field()
    Sep = scrapy.Field()
    Oct = scrapy.Field()
    Nov = scrapy.Field()
    Dec = scrapy.Field()
    Total = scrapy.Field()
    pass
