# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia.items import NewHouseItem, ESFHouseItem


class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province = province_text
            if province == '其它':
                continue

            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                url_module = city_url.split("//")
                scheme = url_module[0]
                domain = url_module[1]
                if 'bj.' in domain:
                    newhouse_url = ' http://newhouse.fang.com/house/s/'
                else:
                    newhouse_url = scheme + "//" + "newhouse." + domain + "house/s/"
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse,
                                     meta={"info": (province, city)})

    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            item_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get() or ''
            yield scrapy.Request(url=response.urljoin(item_url),
                                 callback=self.parse_new_house_step1,
                                 meta={"info": (province, city)})

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),
                                 callback=self.parse_newhouse,
                                 meta={"info": (province, city)})

    def parse_new_house_step1(self, response):
        province, city = response.meta.get('info')
        url = response.xpath('//a[contains(text(), "楼盘详情")]/@href').get()
        yield scrapy.Request(url=response.urljoin(url),
                             callback=self.parse_new_house_step2,
                             meta={"info": (province, city)})

    def parse_str(self, _str):
        if not _str:
            return ''
        _str = _str.replace('\n', '').replace('\t', '')
        return _str

    def parse_new_house_step2(self, response):
        province, city = response.meta.get('info')
        basic_div = response.xpath("//h3[contains(text(),'基本信息')]/parent::div")[0]
        sale_div = response.xpath("//h3[contains(text(),'销售信息')]/parent::div")[0]

        price = basic_div.xpath('.//div[@class="main-info-price"]/em/text()').get() or ''
        name = response.xpath('//h1/a[@class="ts_linear"]/text()').get() or ''
        wuyeleibie = basic_div.xpath('./ul/li[1]/div[2]/text()').get() or ''
        xiangmutese = basic_div.xpath('./ul/li[2]/div[2]/span/text()').get() or ''
        jianzhuleibie = basic_div.xpath('.//span[@class="bulid-type"]/text()').get() or ''
        zhuangxiuzhuangkuang = basic_div.xpath('./ul/li/div/li[2]/div[2]/text()').get() or ''
        chanquannianxian = basic_div.xpath('./ul/li/div/li[3]/div[2]/div/p/text()').get() or ''
        huanxianweizhi = basic_div.xpath('./ul/li/div/li[4]/div[2]/text()').get() or ''
        kaifashang = basic_div.xpath('./ul/li/div/li[5]/div[2]/a/text()').get() or ''
        loupandizhi = basic_div.xpath('./ul/li/div/li[6]/div[2]/text()').get() or ''

        xiaoshouzhuangtai = sale_div.xpath('.//ul/li[1]/div[2]/text()').get() or ''
        loupanyouhui = sale_div.xpath('.//ul/li[2]/div[2]/text()').get() or ''
        kaipanshijian = sale_div.xpath('.//ul/li[3]/div[2]/text()').get() or ''
        jiaofangshijian = sale_div.xpath('.//ul/li[4]/div[2]/text()').get() or ''
        shouloudizhi = sale_div.xpath('.//ul/li[5]/div[2]/text()').get() or ''
        zixundianhua = sale_div.xpath('.//ul/li[6]/div[2]/text()').get() or ''
        zhulihuxing = sale_div.xpath('.//ul/li[7]/div[2]/a/text()').get() or ''
        yushouxuke = sale_div.xpath('.//ul/li[8]/div[2]/text()').get() or ''

        item = NewHouseItem(province=province, city=city)
        item['price'] = self.parse_str(price)
        item['name'] = self.parse_str(name)
        item['wuyeleibie'] = self.parse_str(wuyeleibie)
        item['xiangmutese'] = self.parse_str(xiangmutese)
        item['jianzhuleibie'] = self.parse_str(jianzhuleibie)
        item['zhuangxiuzhuangkuang'] = self.parse_str(zhuangxiuzhuangkuang)
        item['chanquannianxian'] = self.parse_str(chanquannianxian)
        item['huanxianweizhi'] = self.parse_str(huanxianweizhi)
        item['kaifashang'] = self.parse_str(kaifashang)
        item['loupandizhi'] = self.parse_str(loupandizhi)
        item['xiaoshouzhuangtai'] = self.parse_str(xiaoshouzhuangtai)
        item['loupanyouhui'] = self.parse_str(loupanyouhui)
        item['kaipanshijian'] = self.parse_str(kaipanshijian)
        item['jiaofangshijian'] = self.parse_str(jiaofangshijian)
        item['shouloudizhi'] = self.parse_str(shouloudizhi)
        item['ziundianhua'] = self.parse_str(zixundianhua)
        item['zhulihuxing'] = self.parse_str(zhulihuxing)
        item['yushouxuke'] = self.parse_str(yushouxuke)
        item['url'] = self.parse_str(response.url)
        yield item

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        dls = response.xpath("//div[@class='houseList']/dl")

        for dl in dls:
            item = ESFHouseItem(province=province, city=city)
            item['name'] = dl.xpath(".//p[@class='mt10']/a/span/text()").get()
            infos = dl.xpath(".//p[@class='mt12']/text()").getall()
            infos = list(map(lambda x: re.sub(r"\s", "", x), infos))
            for info in infos:
                if "厅" in info:
                    item["rooms"] = info
                elif '层' in info:
                    item["floor"] = info
                elif '向' in info:
                    item['toward'] = info
                else:
                    item['year'] = info.replace("建筑年代：", "")
                item['address'] = dl.xpath(".//p[@class='mt10']/span/@title").get()
                item['area'] = dl.xpath(".//div[contains(@class,'area')]/p/text()").get()
                item['price'] = "".join(dl.xpath(".//div[@class='moreInfo']/p[1]//text()").getall())
                item['unit'] = "".join(dl.xpath(".//div[@class='moreInfo']/p[2]//text()").getall())
                detail_url = dl.xpath(".//p[@class='title']/a/@href").get()
                item['origin_url'] = response.urljoin(detail_url)
                yield item

        next_url = response.xpath("//a[@id='PageControll_hlk_next']/@href").get()
        yield scrapy.Request(url=response.urljoin(next_url),
                         callback=self.parse_esf,
                         meta={"info": (province, city)}
                         )
