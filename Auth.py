import twitter

def get_authentication(screen_name=None,param=1):
   
    
    api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
    return api


    
    


