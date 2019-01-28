from requests_html import HTMLSession

session = HTMLSession()
url = 'https://www.jianshu.com/mobile/books?category_id=284'
r = session.get(url)

# all_links = r.html.xpath('//span[@class="home-section-desc"]/text()', first=True) 
print()