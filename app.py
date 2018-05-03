import os, sys, random
from flask import Flask, request
from utils import wit_response, getNewsElements,biet_announcement,wiki_search
from pymessenger import Bot

app = Flask(__name__)
#PAGE_ACCESS_TOKEN="EAABw6t3yAPsBAOMt9yCD8PurBkT2X2PhcWZAwk5cJewteVZC719Xzd3LitruFDgBJmZBijX4w4g0BOk0OkVaNzQ6gIiOYnZBrZCZB86lMRKMbflTGyY83e7SVgNltZBYoZAdtu4IV6tEUY2OeJn4eNR9vulowYPp4imZCBQuDrkSfcwZDZD"
PAGE_ACCESS_TOKEN = "EAAGZCB3HGWlUBAPcoDUtUAFPheVAbZAgSelMOXVmPkxI7npRf5pgJZCIgNPejbE2m6pK08XL0bHnG6kDno2IIMBmMgIDPmYrC59XnVCQ845DlfchjlFZBrpdUJQBB3JVqKifek1b9gS3mvzbiyoZABbthZB7DqGZAZBNAIAE5mZBdswZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
    

@app.route('/', methods=['POST'])
def webhook():
    #bot.send_raw("BIET NOTICES")

    print("RECIEVED".center(200,'-'))
    data = request.get_json()
    log(data)
    if data['object'] == 'page':
        for entry in data['entry']:
         if 'messaging' in entry:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                bot.send_action(sender_id,'mark_seen')
                if messaging_event.get('postback'):
                    title=messaging_event['postback']['title']
                    if title == 'Get Started':
                        user=bot.get_user_info(sender_id)
                        #greet=bot.greeting_text(user['first_name'])
                        bot.send_text_message(sender_id, 'Hi {} What can I help you?'.format(user['first_name']))   
                        #print("\nUSER=\n\n",greet,"\n\n")
                #us=bot.get_user_info(recipient_id)
                #print(us)
                #gs=bot.greeting_text()
                #gs=bot.add_persistent_menu()
                #gs=bot.add_getting_started(start_me)
                #print("\n\nGS = ",gs,"\n\n")
                #bot.send_list_message(sender_id,elements)
                #bot.send_action(sender_id,'typing_on')
                   
                #temp=get_user_info(recipient_id)
                #print("USER = ", recipient_id)
                #print("\tMessage_EVENT---", messaging_event,'\n\n\n')
                if messaging_event.get('message'):
                    # Extracting messaging_text message
                    if 'text' in messaging_event['message']:
                        
                        if 'is_echo' in messaging_event['message']:
                            #print("\tEXECCCCCCC\n\n")
                            break
                        messaging_text = messaging_event['message']['text']
                        
                    else:
                        messaging_text = 'no text'
                    response = None
                    
                    categories = wit_response(messaging_text)
                    print("CATEGORIES", categories)
                    if categories.get('newstype'):
                        response = getNewsElements(categories)
                        bot.send_generic_message(sender_id,response)
                        response =True
                    elif categories.get('bye'):
                        by=['Bye bye','Sayonara','Good bye! Take care','Hope I\'ll see you later']
                        response = random.choice(by) + ' :)'
                    elif categories.get('eat'):
                        response = 'I prefer to eat electricity :)'

                    elif categories.get('abuse'):
                        vulgur=['Offending me implies, insulting yourself','Are you taking about yourself, jerk?', 'Thank God! finally got new idiot to talk to','You are living proof that a human can live without a brain!','Same to you, jerk']
                        response=random.choice(vulgur)
                    elif categories.get('bietnotices'):
                        #print("ENTER BIET")
                        response = biet_announcement('notices')
                        bot.send_list_message(sender_id, response,'View News & Events','bietnews')
                        '''
                    else:
                        response = biet_announcement('news')
                        bot.send_list_message(sender_id, response,'View Notices','bietnotices')'''
                    elif categories.get('number'):
                        response = "Oh, your age is {}, I'll remember this".format(categories['number'])

                    elif categories.get('greetings'):
                        rs=['Hey there! How may I help you?', 'Hi there! What do you want to talk about?','Hi there!']
                        response = random.choice(rs)

                    elif categories.get('head'):
                        bs=['creator','boss']
                        response = 'My '+random.choice(bs)+' is Shubham Bansal'

                    elif categories.get('location'):
                        if 'wh_query' in categories:
                            if categories['location'] == 'sx':
                              sx=('I\'m only a bot, talk to human for this','Talking a computer about sex is little wierd, change the topic, please!')
                              response=random.choice(sx)
                            else:
                           #if categories['location'] == 'live'

                             response=wiki_search(categories['location'])

                        elif categories['location'] == 'biet':
                            print('BIET \n\n',type(categories['location']),'\n\n\n')
                            if categories.get('bietnotices'):
                                response = biet_announcement('notices')
                                bot.send_list_message(sender_id, response,'View News & Events','bietnews')
                            else:
                                response = biet_announcement('news')
                                bot.send_list_message(sender_id, response,'View Notices','bietnotices')
                            response = True
                    
                    if response == None:
                        response = "I have no idea what you are saying!"
                        bot.send_text_message(sender_id,response)
                    elif response != True:
                        bot.send_text_message(sender_id,response)
                    
                elif messaging_event.get('postback'):
                    
                    if 'bietnotices' in messaging_event['postback']['payload']:
                        response=biet_announcement('notices')
                        bot.send_list_message(sender_id,response,'View News & Events','bietnews')
                    elif 'bietnews' in messaging_event['postback']['payload']:
                        response = biet_announcement('news_events')
                        bot.send_list_message(sender_id, response,'View Notices', 'bietnotices')
                    #elif messaging_event['postback']['payload']=='Getting Started':
                    #print("TYPE=  ",type(elements))
                    
                    #bot.send_generic_message(sender_id,elements)
                    #bot.send_button_message(sender_id,'he there', elements)
                    #ot.send_action(sender_id,'typing_off')
                  
    return "ok", 200

def log(message):   
    print(message)
    sys.stdout.flush()
if __name__ == "__main__":
 app.run(debug = True, port=80)