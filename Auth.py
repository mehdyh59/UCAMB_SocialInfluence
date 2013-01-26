import twitter

def get_authentication(screen_name=None,param=1):
    if screen_name=="data1_surgeon" and param==1:
        con_key='95xlaFoKBsebx6dVUh9WSw'
        con_sec='ERNTKp0m1SvaXi3Y6NIF97JKIp4pn2DiTOvR3vVGR1U'
        acc_tok='897433675-1EdKl4xnaxImIG2uf95CXoH25xGfIEfO5H7GxRz4'
        acc_sec='lqXp0hPX5FkKQPych8mAbPNE1tm6Gfj2LuCdGyaViM'
    if screen_name=="data1_surgeon" and param==2:
        con_key='OSjYBYINrL35g7wA9BLTDw'
        con_sec='sOX5S1HYJ8O8Mcim7GZI2oNAgpfC1xXHhjMmizXYcw'
        acc_tok='897433675-XKPbvzCOm6ZQbR3kpq8CXYMALH6iam2NVSu4R2kL'
        acc_sec='5WbknHKq2g2I0V5YjXCY6urWYPEByihahQe7sdOzg'   
    if screen_name=="mehdy_h59" and param==1:
        con_key='49Jf6XcYS6nFfDAnD8OxA'
        con_sec='Ny7hLvcGNCfafcJykkPpFED350BQ0JjrweOJcVsJs'
        acc_tok='34409944-kRuM7yKAqsAR1x7PROK6PPH0VWdIKu3ds4cIV8Oz0'
        acc_sec='jX2ZwxgkV3pg3M8z2FAfoQ50zIgvLnrw2frLVbr9E'
    if screen_name=="CoxA59" and param==1:
        con_key='PjjHAiKPiF0RQAGDGZkXpg'
        con_sec='ekFzdJjZ6GX1jKUlPM6QcBP2ZpltdbuHHrXF0G10'
        acc_tok='866936262-LPB2wZZRkjaaGeCoTUxwpBuFWzex9iuDsUdthwm2'
        acc_sec='9rwhbLYdCOiz0BX1yX4X0XZc2B7781mUDQFd6a1LzWQ'
    if screen_name=="mana_macaron" and param==1:
        con_key='n8HFqkfo9eSHpL5hN32NZw'
        con_sec='2J6Ka4HUEZH1ao1KMtletQmmfaGQeeRroh9RSIgC0'
        acc_tok='1095166206-pPaI71WYh5SzOCVueDAXan671MAvyuhedX6sVmJ'
        acc_sec='VIYzqiL7o7EvPJUVLRha9WBwKuEsSTltC3S7cJNFPI'
    
    api=twitter.Api(consumer_key=con_key,consumer_secret=con_sec,access_token_key=acc_tok,access_token_secret=acc_sec)
    return api


    
    


