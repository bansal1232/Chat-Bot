from wit import Wit
from gnewsclient import gnewsclient

token = "3VYOQNSYLCBTFXHJG6UIKDJE7BFIHCOT"

client = Wit(access_token = token)

def wit_response(message_text):
	resp = client.message(message_text)
	category = {'newstype': None, 'location':None,'noun':None}

	entities = list(resp['entities'])
	for entity in entities:
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
	cnt=0
	for item in news_items:
		cnt =cnt +1
		element = {
								'type': 'web_url',
								'title': item['title'],
								'url': item['link']
					}
				
							
		
		elements.append(element)
		if cnt == 3:
			break
	return elements

#print(getNewsElements(wit_response("show me entertainment news of india")))