api_key = {
    'darksky': '60569b87b5b2a6220c135e9b2e91646b',
    'knowledge_graph': 'AIzaSyD-zGrQKPO9MUVLP0O4iOzAdhf3QUKSEsc'
}

def checkAPIActive(key):
    if(api_key[key]=='xxyyzz'):
        print('Please get an API key for this feature from '+key)
        return False
    return True