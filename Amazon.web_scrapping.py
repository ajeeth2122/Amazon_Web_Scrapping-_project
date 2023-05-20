from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import html
import time
import csv
path = "C:\Program Files (x86)\chromedriver.exe" 
driver = webdriver.Chrome(path)
driver.get("https://www.amazon.in/?&ext_vrnc=hi&tag=googhydrabk1-21&ref=pd_sl_1jyasdi57f_e&adgrpid=60456322738&hvpone=&hvptwo=&hvadid=486459496700&hvpos=&hvnetw=g&hvrand=2434502659292498901&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9061895&hvtargid=kwd-295905178780&hydadcr=14451_2154369&gclid=CjwKCAiAwc-dBhA7EiwAxPRylMTkO6tqnPUDxeze_J2hVnUG9lPZlK8AKc2PLOGVUN-Gq8-WakYEDxoCGfcQAvD_BwE")
search = driver.find_element('id','twotabsearchtextbox')
time.sleep(5)
search.send_keys("Phone")
search.send_keys(Keys.RETURN)
time.sleep(5)
tree = html.fromstring(driver.page_source)
serval="Phone"
def percentage(price, old_price):
  percentage = 100 * float(price)/float(old_price)
  return str(round(percentage)) + "%"


close = driver.find_elements(By.CSS_SELECTOR, '[aria-disabled="true"]')
close = close[-1]
num=int(close.text)
print(num)
with open(serval+'.csv', 'w') as csvfile:  
    fieldnames = [ 'Title','Price',"Old price","Off" ,'Rating','Reviews']    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


for i in range(1,num+1):
	tree = html.fromstring(driver.page_source)
	for prod_tree in tree.xpath('//div[contains(@data-component-type,"s-search-result")]'):
		title = prod_tree.xpath('.//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/span/text()')
		price = prod_tree.xpath('.//span[@class="a-price-whole"]/text()')
		old_price = prod_tree.xpath('.//span[@aria-hidden="true"]/text()')
		rating = prod_tree.xpath('.//span[@class="a-icon-alt"]/text()')
		reviews=prod_tree.xpath('.//span[@class="a-size-base s-underline-text"]/text()')
		#print(rating)
		if title:
			title = title[0]
		else:
			title = 'NA'
		if price:
			price = str(price[0])
		else:
			price = 'NA'
		if rating:
			rating =rating[0][:4]
		else:
			rating = 'NA'
		if reviews:
			reviews = reviews[0]
		else:
			reviews = 'NA'
		if old_price:
			old_price = old_price[0]
			old_price = old_price[1:]
		else:
			old_price = 'NA'
		if old_price[0].isnumeric():
			old_price = old_price
		else:
			old_price = 'NA'
		if ',' in str(price):
			price = price.split(',')[0]+price.split(',')[1]
		if ',' in str(old_price):
			old_price = old_price.split(',')[0]+old_price.split(',')[1]
		if price !='NA' and old_price != 'NA':
			off=percentage(price,old_price)
		else:
			off='NA'
		print(rating,price,title)
		#print(prod_tree.xpath('.//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/span/text()'))


		with open(serval+'.csv', 'a+',encoding="utf-8") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writerow({'Title': title, 'Price': price,'Rating': rating , 'Reviews':reviews,"Old price":old_price,"Off":off})
	print('*********')
	print(i)
	time.sleep(5)
	if i+1 == num:
			print(i+1)
			break

	links = driver.find_element(By.LINK_TEXT,"Next")
	links.click()
	time.sleep(5)

