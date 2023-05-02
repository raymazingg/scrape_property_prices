import requests
from bs4 import BeautifulSoup
from lxml import etree as et


header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36",'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
payload = "type=SAL&subtype=ANY&sort=&sortby=&status=CUR&baseUrl=&refpage=0&perpage=15&sortcombo=updated-DES---suburb&bedroom=any&bathroom=any&garage=any&event=&auctionmin=&auctionmax=&suburb=Homebush%2C+NSW+2140&radius=10&keywords=&agent=&office=&IF=&budgetmin=&budgetmax=&budgetdisplay=&landsizemin=&landsizemax=&floorsizemin=&floorsizemax=&comtype=&_s=buy&page=2"
base_url = "https://www.raywhite.com/wp-admin/admin-ajax.php?action=dispatch&_p=rwcom/list/search/internal/true"
pages_url = []  # list to store the url of every page
listing_url = []  # list to store the url of every apartment

# begin get dom
response = requests.request("POST", base_url, headers=header, data=payload)
soup = BeautifulSoup(response.text, 'lxml')
dom = et.HTML(str(soup))
#end get dom

# import requests
#
# url = "https://www.raywhite.com/wp-admin/admin-ajax.php?action=dispatch&_p=rwcom/list/search/internal/true"
#
# payload = "type=SAL&subtype=ANY&sort=&sortby=&status=CUR&baseUrl=&refpage=0&perpage=15&sortcombo=updated-DES---suburb&bedroom=any&bathroom=any&garage=any&event=&auctionmin=&auctionmax=&suburb=Homebush%2C+NSW+2140&radius=10&keywords=&agent=&office=&IF=&budgetmin=&budgetmax=&budgetdisplay=&landsizemin=&landsizemax=&floorsizemin=&floorsizemax=&comtype=&_s=buy&page=2"
# headers = {
#     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'user-agent': 'some agent'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)
# soup = BeautifulSoup(response.text, 'lxml')
