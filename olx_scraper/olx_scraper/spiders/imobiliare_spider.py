import scrapy
from ..items import ApartamentItem


# noinspection SpellCheckingInspection
class ImobiliareSpider(scrapy.Spider):
    name = "imobiliare_spider"
    start_urls = ["https://www.imobiliare.ro/vanzare-apartamente/bucuresti?id=259446998"]

    def parse(self, response):
        # all divs on page
        divs = response.xpath("//div[@class='box-anunt']")
        for div in divs:
            # make an item
            item = ApartamentItem()

            # titlu_anunt, url_anunt, adresa, suprafata_utila, etaj, nr_total_etaje, compartimentare,
            # pret, moneda,
            titlu_anunt = div.xpath(".//h2//span/text()").get().strip()
            url_anunt = div.xpath(".//h2//a/@href").get().strip()
            adresa = div.xpath(".//div[@class='location_wp']/p/text()").get().strip()
            caracteristici = div.xpath(".//ul[@class='caracteristici']")
            if caracteristici:
                lis_text = [li.strip().lower() for li in caracteristici.xpath('.//li/span/text()').getall()]
                for li_text in lis_text:
                    if "mp" in li_text:
                        suprafata_utila = li_text.strip()
                        item['suprafata_utila'] = suprafata_utila
                    if 'etaj' in li_text:
                        x = li_text.split('/')
                        etaj = x[0].strip()
                        nr_total_etaje = x[-1].strip()
                        item['etaj'] = etaj
                        item['nr_total_etaje'] = nr_total_etaje
                    if 'semi' in li_text or 'decomandat' == li_text:
                        item['compartimentare'] = li_text

            pret = div.xpath('.//span[@class="pret-mare"]/text()').get().replace('.', '').strip()
            moneda = div.xpath('.//span[@class="tva-luna"]/text()').get().strip()

            item['titlu_anunt'] = titlu_anunt
            item['url_anunt'] = url_anunt
            item['adresa'] = adresa
            item['pret'] = pret
            item['moneda'] = moneda

            yield item

        # next
        next_link = response.xpath('//a[@class="inainte butonpaginare"]/@href').get()
        if next_link:
            yield response.follow(next_link.strip(), self.parse)
