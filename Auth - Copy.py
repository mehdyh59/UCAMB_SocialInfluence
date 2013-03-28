import twitter

def get_authentication(screen_name=None,param=1):
    if screen_name=="X" and param==1:
        con_key='X'
        con_sec='X'
        acc_tok='X'
        acc_sec='X'
    
    api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
    return api


    
    


