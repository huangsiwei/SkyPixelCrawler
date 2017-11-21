import scrapy
from scrapy.http import Request
import json
from SkyPixelCrawler.items import MediaResourceItem


class SkyPixelCreations(scrapy.Spider):
    name = 'SkyPixelCreations'
    allowed_domains = ['skypixel.com', 'djivideos.com']
    start_urls = ['https://www.skypixel.com/api/website/resources/works/?']
    url_template = "https://www.skypixel.com/api/website/resources/works/?page={}&page_size=26&resourceType=&type=latest"

    def start_requests(self):
        for i in range(0, 10):
            current_url = self.url_template.format(i)
            request = Request(current_url)
            yield request

    def parse(self, response):
        unicode_body = response.body_as_unicode()  # 返回的html unicode编码
        result = json.loads(unicode_body)
        photos = result["photos"]
        videos = result["videos"]
        # item_list = []
        for photo in photos:
            resource_item = MediaResourceItem()
            resource_item["resource_id"] = photo["id"]
            account = photo["account"]
            resource_item["account_id"] = account["id"]
            resource_item["account_name"] = account["name"]
            resource_item["resource_time"] = "0"
            if photo["type"] == "photo":
                resource_item["resource_type"] = 1
            if photo["is_360"] is True:
                resource_item["resource_type"] = 2
            resource_item["resource_url"] = photo["image"]
            resource_item["resource_title"] = photo["title"]
            yield resource_item
        for video in videos:
            resource_item = MediaResourceItem()
            resource_item["resource_id"] = video["id"]
            account = video["account"]
            resource_item["account_id"] = account["id"]
            resource_item["account_name"] = account["name"]
            resource_item["resource_time"] = "0"
            resource_item["resource_type"] = 0
            resource_item["resource_url"] = ""
            resource_item["resource_title"] = video["title"]
            yield Request(video["embed_url"], callback=self.parse_video_url, meta={"resource_item": resource_item})
            yield resource_item

    def parse_video_url(self, response):
        print("====")
        print(response.meta['resource_item'])
