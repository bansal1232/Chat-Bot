from wit import Wit
from gnewsclient import gnewsclient
import requests,re,wikipedia#,sys
from bs4 import BeautifulSoup
#sys.stdin=open('in.txt','r')
token = "3VYOQNSYLCBTFXHJG6UIKDJE7BFIHCOT"

client = Wit(access_token = token)
def wiki_search(message):
	try:
		resp=wikipedia.summary(message, sentences=2)
	except:
		resp="Please ask with correct phrases"
	return resp

def biet_announcement(message):
	URL = "http://bietjhs.ac.in/"
	r = requests.get(URL)
	soup = BeautifulSoup(r.content, 'lxml')
	if message =='notices':
		table = soup.find('div',attrs = {'id':'p7VSCb_2'}).findAll('a',limit=4)
	else:
		table = soup.find('div',attrs = {'id':'p7VSCb_1'}).findAll('a',limit=4)
	#table=soup.find('div', attrs={'class':'more-news'}).findAll('a')
	elements=[]
	for item in table:
		if re.search(URL,item['href'],re.I) ==None:
			item['href'] = URL + item['href']
		element = {
					'title': item.text,
					'buttons': [{
								'type': 'web_url',
								"webview_height_ratio": "compact",
								'title': "Read more",
								'url': item['href']
					}]		
		}
		elements.append(element)
	return elements

def wit_response(message_text):
	#print("SEE this---",message_text,'\n\n\n')
	resp = client.message(message_text)
	category = {'newstype': None, 'location':None,'noun':None}

	entities = list(resp['entities'])
	for entity in entities:
		if resp['entities'][entity][0]['confidence'] >= 0.7:
			category[entity] = resp['entities'][entity][0]['value']

	return (category)

def getNewsElements(categories):
	news_client=gnewsclient()
	news_client.query='';
	if categories['newstype'] != None:
		news_client.query += categories['newstype'] + ' '
	if categories['location'] !=None:
		news_client.query += categories['location'] 
	news_items = news_client.get_news()
	elements = []

	for item in news_items:
		element = {
					'title': item['title'],
					'buttons': [{
								'type': 'web_url',
								'title': "Read more",
								'url': item['link']
					}],
					'image_url': item['img']		
		}
		elements.append(element)

	return elements
#print(wiki_search('aligarh'))
#=print(wiki_search("mallika sherawat"))
#print(wit_response("show me sports news of usa"))
#print(getNewsElements(wit_response("show me news of USA")))