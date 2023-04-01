import requests

def get_data(url):
    
    # query the URL with a get request 
    response = requests.get(url)

    #r return the CONTENT of the response. Without the content function the response code is returned. 
    return response.content

