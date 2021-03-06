'''

Title: locustfile.py

Description: 
Python script that defines the behavior of the locust threads to load test Pretix by swarming it with ticket purchase requests of fictitious users.
Locust's UI is accessible at http://localhost:8089.

Notes: 
Install requirements before running this file. 
Change the values of the global variables for your own usage.
This file is also prepared to be executed inside DETI's infrastructure and from containers aimed at load testing the service from outside of your own computer.

Authors: Filipe Pires (85122) and João Alegria (85048)

'''

from locust import * #HttpLocust, TaskSet, between, task
import os
#import time
#import requests

# Change these variables if you wish to personalize the script
organizer = "ws"
event = "ws2020"
question = 1
# host = "http://localhost:7200/" # local
# token = "5iz3l7fwaw1s2mzxipbs8xdcew0bxr77uwrn7tbx5v47ac3s51fqeby34afp9u8a" # local
host = "http://10.2.0.1:7200/" # swarm
#token = "g6ohu79cix5111huvhs63ksjdvxsis6aksijlptpy3y1ffaie8re7xskkg43vkjc" # swarm
token = os.environ["TOKEN"] # test container
#nUsers = 10
nUsers=int(os.environ["USERS"])

# These variables hold the codes of the errors that occur and their frequencies
getFailures = {}
postFailures = {}

'''
r = [
    [
        host+""+organizer+"/"+event+"/",
        host+"static/CACHE/css/e69921ab2b6e.css",
        host+"media/pub/"+organizer+"/"+event+"/presale.a37ec5cea5997d87.css",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/fonts/opensans_regular_macroman/OpenSans-Regular-webfont.79515ad07889.woff",
        host+"static/fontawesome/fonts/fontawesome-webfont.af7ae505a9ee.woff2",
        host+"static/fonts/opensans_bold_macroman/OpenSans-Bold-webfont.2e90d5152ce9.woff",
        host+"static/lightbox/images/prev.84b76dee6b27.png",
        host+"static/lightbox/images/next.31f15875975a.png",
        host+"static/lightbox/images/loading.2299ad0b3f63.gif",
        host+"static/lightbox/images/close.d9d2d0b1308c.png",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png",
    ],
    [
        host+""+organizer+"/"+event+"/?require_cookie=true",
        host+"static/CACHE/css/e69921ab2b6e.css",
        host+"media/pub/"+organizer+"/"+event+"/presale.a37ec5cea5997d87.css",
        host+"static/CACHE/js/5b8f603ac609.js",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png",
        host+"static/fonts/opensans_italic_macroman/OpenSans-Italic-webfont.f42641eed834.woff"
    ],
    [
        host+""+organizer+"/"+event+"/checkout/start",
        host+""+organizer+"/"+event+"/checkout/questions/",
        host+"static/CACHE/css/e69921ab2b6e.css",
        host+"media/pub/"+organizer+"/"+event+"/presale.a37ec5cea5997d87.css",
        host+"static/CACHE/js/5b8f603ac609.js",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        #host+""+organizer+"/"+event+"/checkout/questions/", # post
        host+""+organizer+"/"+event+"/checkout/payment/",
        host+"static/CACHE/css/e69921ab2b6e.css",
        host+"media/pub/"+organizer+"/"+event+"/presale.a37ec5cea5997d87.css",
        host+"static/CACHE/js/5b8f603ac609.js",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        #host+""+organizer+"/"+event+"/checkout/payment/", # post
        host+""+organizer+"/"+event+"/checkout/confirm/",
        host+"static/CACHE/css/e69921ab2b6e.css",
        host+"media/pub/"+organizer+"/"+event+"/presale.a37ec5cea5997d87.css",
        host+"static/CACHE/js/5b8f603ac609.js",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        host+"api/v1/organizers/"+organizer+"/events/"+event+"/orders/", # post
        #host+""+organizer+"/"+event+"/order/WBWFT/14xhln2apnqkl1r7/pay/1/complete",
        #host+""+organizer+"/"+event+"/order/WBWFT/14xhln2apnqkl1r7/?thanks=yes",
        host+"static/CACHE/css/e69921ab2b6e.css",
        host+"media/pub/"+organizer+"/"+event+"/presale.a37ec5cea5997d87.css",
        host+"static/CACHE/js/5b8f603ac609.js",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ]
]
'''
r = [
    [
        host+""+organizer+"/"+event+"/",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/lightbox/images/prev.84b76dee6b27.png",
        host+"static/lightbox/images/next.31f15875975a.png",
        host+"static/lightbox/images/loading.2299ad0b3f63.gif",
        host+"static/lightbox/images/close.d9d2d0b1308c.png",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png",
    ],
    [
        host+""+organizer+"/"+event+"/?require_cookie=true",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/pretixpresale/js/ui/iframe.d76c0dc4351f.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png",
        host+"static/fonts/opensans_italic_macroman/OpenSans-Italic-webfont.f42641eed834.woff"
    ],
    [
        host+""+organizer+"/"+event+"/checkout/start",
        host+""+organizer+"/"+event+"/checkout/questions/",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        host+""+organizer+"/"+event+"/checkout/start",
        host+""+organizer+"/"+event+"/checkout/questions/",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        #host+""+organizer+"/"+event+"/checkout/questions/", # post
        host+""+organizer+"/"+event+"/checkout/payment/",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        #host+""+organizer+"/"+event+"/checkout/payment/", # post
        host+""+organizer+"/"+event+"/checkout/confirm/",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ],
    [
        host+"api/v1/organizers/"+organizer+"/events/"+event+"/orders/", # post
        #host+""+organizer+"/"+event+"/order/WBWFT/14xhln2apnqkl1r7/pay/1/complete",
        #host+""+organizer+"/"+event+"/order/WBWFT/14xhln2apnqkl1r7/?thanks=yes",
        host+"media/pub/"+organizer+"/"+event+"/presale.0334ccfc0665d0b0.css",
        host+"static/CACHE/js/output.de09cebf3454.js",
        host+"static/jsi18n/en/djangojs.366c16383242.js",
        host+"static/pretixbase/img/icons/favicon-194x194.4d77adfe376b.png",
        host+"static/pretixbase/img/icons/favicon-16x16.ce949675f6e2.png"
    ]
]


class UserBehavior(TaskSet):
    
    global nUsers
    
    totalPurchaseAttempts = 0
    maxPurchaseAttempts = nUsers
    
    #def on_start(self):
    #    pass

    #def on_stop(self):
    #    pass
    
    @task
    def get(self):
        
        if UserBehavior.totalPurchaseAttempts == UserBehavior.maxPurchaseAttempts:
            return
        
        UserBehavior.totalPurchaseAttempts+=1
        #print("Total Purchase Attempts: "+str(UserBehavior.totalPurchaseAttempts))
        
        global r
        global token
        global question
        user_email = 'user'+str(UserBehavior.totalPurchaseAttempts)+'@example.org'
        
        global getFailures
        global postFailures
               
        for i in range(0,len(r)):
            for j in range(0,len(r[i])):
                attempts = int(os.environ["ATTEMPTS"])
                
                if i==(len(r)-1) and j==0: # if POST
                    #body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","invoice_address": {"is_business": "false","company": "Sample company","name_parts": {"full_name": "John Doe"},"street": "Sesam Street 12","zipcode": "12345","city": "Sample City","state": "","internal_reference": "","vat_id": ""},"positions": [{"item": 1,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
                    body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","positions": [{"item": 2,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
                    response = self.client.post(r[len(r)-1][0], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    response_code = int(str(response).split("[")[1].split("]")[0])
                    while response_code == 409: #"201" not in str(response):
                        attempts = attempts-1
                        if attempts == 0:
                            #raise InterruptedError
                            if response_code in postFailures.keys():
                                postFailures[response_code] = postFailures[response_code] + 1
                            else:
                                postFailures[response_code] = 1
                            print(postFailures)
                            break
                        response = self.client.post(r[len(r)-1][0], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                        response_code = int(str(response).split("[")[1].split("]")[0])
                    if response_code > 299:
                        if response_code in postFailures.keys():
                            postFailures[response_code] = postFailures[response_code] + 1
                        else:
                            postFailures[response_code] = 1
                        print(postFailures)
                    continue
                
                response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                response_code = int(str(response).split("[")[1].split("]")[0])
                while response_code == 409: #"200" not in str(response):
                    attempts = attempts-1
                    if attempts == 0:
                        #raise InterruptedError
                        if response_code in getFailures.keys():
                            getFailures[response_code] = getFailures[response_code] + 1
                        else:
                            getFailures[response_code] = 1
                        print(getFailures)
                        break
                    response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                    response_code = int(str(response).split("[")[1].split("]")[0])
                if response_code > 299:
                    if response_code in getFailures.keys():
                        getFailures[response_code] = getFailures[response_code] + 1
                    else:
                        getFailures[response_code] = 1
                    print(getFailures)
                '''
                if i==0 and j==0:
                    attempts = 3
                    response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                    while "200" not in str(response):
                        #print(response)
                        attempts = attempts-1
                        if attempts == 0:
                            raise InterruptedError
                        response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                    continue
                if i==(len(r)-1) and j==0:
                    attempts = 3
                    body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","invoice_address": {"is_business": "false","company": "Sample company","name_parts": {"full_name": "John Doe"},"street": "Sesam Street 12","zipcode": "12345","city": "Sample City","state": "","internal_reference": "","vat_id": ""},"positions": [{"item": 1,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
                    response = self.client.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    #response = requests.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    while "201" not in str(response):
                        #print(response)
                        attempts = attempts-1
                        if attempts == 0:
                            raise InterruptedError
                        response = self.client.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    continue
                self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                #requests.get(r[i][j], headers={"Authorization": "Token " + token})
                '''
    
    '''
    @task
    def test(self):
        #for i in range(0,70):
        #    self.client.get("http://10.2.0.1:7200") # Pretix
            #self.client.get("http://10.2.0.1:6300") # Mattermost (Pedrosa)
            
        if UserBehavior.totalPurchaseAttempts == UserBehavior.maxPurchaseAttempts:
            return
            
        global r
        global token
        global question
        UserBehavior.totalPurchaseAttempts+=1
        user_email = 'user'+str(UserBehavior.totalPurchaseAttempts)+'@example.org'
        
        #body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","invoice_address": {"is_business": "false","company": "Sample company","name_parts": {"full_name": "John Doe"},"street": "Sesam Street 12","zipcode": "12345","city": "Sample City","state": "","internal_reference": "","vat_id": ""},"positions": [{"item": 1,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
        body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","positions": [{"item": 1,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
        self.client.post(r[len(r)-1][0], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
    '''
    
    '''
    @task
    def get(self):
        
        if UserBehavior.totalPurchaseAttempts == UserBehavior.maxPurchaseAttempts:
            return
        
        UserBehavior.totalPurchaseAttempts+=1
        #print("Total Purchase Attempts: "+str(UserBehavior.totalPurchaseAttempts))
        
        global r
        global token
        global question
        user_email = 'user'+str(UserBehavior.totalPurchaseAttempts)+'@example.org'
        
        #for i in range(0,len(r)):
        #    for j in range(0,len(r[i])):
        #        if i==(len(r)-1) and j==0:
        #            body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","invoice_address": {"is_business": "false","company": "Sample company","name_parts": {"full_name": "John Doe"},"street": "Sesam Street 12","zipcode": "12345","city": "Sample City","state": "","internal_reference": "","vat_id": ""},"positions": [{"item": 1,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
        #            response = self.client.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
        #            continue
        #        self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                
        for i in range(0,len(r)):
            for j in range(0,len(r[i])):
                if i==0 and j==0:
                    attempts = 3
                    response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                    while "200" not in str(response):
                        #print(response)
                        attempts = attempts-1
                        if attempts == 0:
                            raise InterruptedError
                        response = self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                    continue
                if i==(len(r)-1) and j==0:
                    attempts = 3
                    body = '{"detail":"", "email": "' + user_email + '","locale": "en","sales_channel": "web","invoice_address": {"is_business": "false","company": "Sample company","name_parts": {"full_name": "John Doe"},"street": "Sesam Street 12","zipcode": "12345","city": "Sample City","state": "","internal_reference": "","vat_id": ""},"positions": [{"item": 1,"attendee_name_parts": {"full_name": "Peter"},"answers": [{"question": '+str(question)+',"answer": "23","options": []}]}] }'
                    response = self.client.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    #response = requests.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    while "201" not in str(response):
                        #print(response)
                        attempts = attempts-1
                        if attempts == 0:
                            raise InterruptedError
                        response = self.client.post(r[i][j], headers={"Authorization": "Token " + token, "Content-Type": "application/json"}, data=body)
                    continue
                self.client.get(r[i][j], headers={"Authorization": "Token " + token})
                #requests.get(r[i][j], headers={"Authorization": "Token " + token})
    '''
                

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(0.1, 0.9)
    # global getFailures
    # global postFailures
    # print(getFailures)
    # print(postFailures)
