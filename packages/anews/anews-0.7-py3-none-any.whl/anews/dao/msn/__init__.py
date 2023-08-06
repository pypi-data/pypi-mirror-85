import requests,json
from lxml import html

def crawl_rss():
    print("crawl rss")
def crawl_data(url):
    print("crawl data")
    try:
        page = requests.get(url, headers={"user-agent": "Googlebot-News/1.0"})
        tree = html.fromstring(page.content)
        arr_text_obj = tree.xpath('//div[@id="maincontent"]//p[not (descendant::img or descendant::a)]')
        arr_text= []
        for text in arr_text_obj:
            if text is not None and text.text is not None:
                #print(text.text)
                arr_text.append(text.text.strip())
        arr_img_obj = tree.xpath('//div[@id="maincontent"]//span/img/@data-src')
        arr_img=[]
        if arr_img_obj is not None:
            for img in arr_img_obj:
                data_src = json.loads(img)
                try:
                    src=data_src['default']['src']
                except:
                    src=data_src['default']
                arr_img.append("http:"+src.split("?")[0])
        #print(html.tostring(tree))
        arr_img_obj = tree.xpath('//ul[contains(@class,"slideshow")]/li//img/@data-src')
        if arr_img_obj is not None:
            for img in arr_img_obj:
                data_src = json.loads(img)
                try:
                    src = data_src['default']['src']
                except:
                    src = data_src['default']
                arr_img.append("http:" + src.split("?")[0])
    except:
        pass
    return arr_text, arr_img

