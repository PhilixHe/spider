# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


def table_tennis_comments_parse(response):
    comments = response.xpath('//div[@id="usrRevBlk"]/ul//li')
    comment_set = []
    for comment in comments:

        name_node = comment.xpath('.//dt[@class="usrBox clearfix"]//em[@itemprop="author"]')
        critics = name_node.xpath('string(.)').get().strip()

        chart_head = comment.xpath('.//dt[@class="usrBox clearfix"]//img/@src').get()

        table_tennis_history = comment.xpath('.//dt[@class="usrBox clearfix"]/p').xpath('text()').extract()
        if len(table_tennis_history) > 2:
            table_tennis_history = table_tennis_history[1].strip()
        else:
            table_tennis_history = ''

        trs = comment.xpath('.//dd[@class="usrEvl clearfix"]//div[@class="floatR"]/table//tr')
        attribute = []
        for tr in trs:
            attribute.append(tr.xpath('string(.)').get().split())

        description = comment.xpath('.//dd[@class="usrEvl clearfix"]//div[@class="comnt"]['
                                    '@itemprop="description"]/p').xpath('string(.)').get()

        recom_hub = []
        recomhub = comment.xpath('./div[@class="recomRub"]//p')
        for recom in recomhub:
            span = recom.xpath('./span/text()').get()
            name = recom.xpath('./a/text()').get()
            url = recom.xpath('./a/@href').get()
            recom_hub.append({span: [name, url]})

        date = comment.xpath('.//dd[@class="usrEvl clearfix"]//small[@class="date"]/text()').get()

        praise = comment.xpath('./div[@class="vote"]/div/label/span/text()').get()

        cm = dict()
        cm['name'] = critics
        cm['chart_head'] = chart_head
        cm['table_tennis_history'] = table_tennis_history
        cm['attribute'] = attribute
        cm['description'] = description
        cm['recommend'] = recom_hub
        cm['date'] = date
        cm['praise'] = praise
        comment_set.append(cm)

    return comment_set