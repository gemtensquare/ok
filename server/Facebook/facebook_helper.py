import requests, random
from Helper import constants
from News.models import News, Template

class Facebook:
    def __init__(self, user_access_token=None, page_id=None, page_access_token=None):
        self.page_id = page_id
        self.page_access_token = page_access_token
        self.user_access_token = user_access_token
        self.url = f"https://graph.facebook.com/v19.0/{page_id}/photos"

        if not page_id:
            raise Exception("Please provide a valid page ID!")
        # if not user_access_token:
        #     raise Exception("Please provide a valid user access token!")
        if not page_access_token:
            raise Exception("Please provide a valid page access token!")

    def print_all_account(self):
        url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={self.user_access_token}"
        res = requests.get(url)
        accounts = res.json()['data']
        

        for account in accounts:
            print("^_^_"*35)
            print("Page Name: ", account['name'], "Page ID: ", account['id'])
            print("Page Token: ", account['access_token'])

        print("^_^_"*35)

    def print_response(self, response, type="Text"):
        if response.status_code == 200:
            print(f"✅ {type} posted successfully!")
            # print("📌 Post ID:", response.json().get('post_id'))
            if type == "Comment":
                return 
            print("📌 PostUrl:", "https://www.facebook.com/" + response.json().get('post_id', '') or response.json().get('comment_id', ''))
        else:
            print(f"❌ Failed to post {type}.")
            print("📄 Status Code:", response.status_code)
            print("📄 Response:", response.text)

    def post_text_to_page(self, message="Post from Python"):
        url = f'https://graph.facebook.com/v19.0/{self.page_id}/feed'
        payload = {
            'message': message,
            'access_token': self.page_access_token
        }
        response = requests.post(url, data=payload)
        self.print_response(response)

    def post_online_image_to_page(self, image_url=None, caption="Post from Python"):
        if not image_url: 
            return "Please provide an image url from online!"
        payload = {
            'url': image_url,
            'caption': caption,
            'access_token': self.page_access_token
        }
        response = requests.post(self.url, data=payload)
        self.print_response(response, type="Online Image")

    def post_local_image_to_page_working(self, image_path=None, caption="Post from Python Local Image"):
        if not image_path: 
            return "Please provide an image url from local!"
        files = {
            'source': open(image_path, 'rb')
        }
        payload = {
            'caption': caption,
            'access_token': self.page_access_token
        }
        response = requests.post(self.url, files=files, data=payload)
        self.print_response(response, type="Local Image")

    def comment_on_post(self, post_id=None, comment="Comment from Python"):
        if not post_id: 
            return "Please provide a post id!"
        url = f'https://graph.facebook.com/v19.0/{post_id}/comments'
        payload = {
            'message': comment,
            'access_token': self.page_access_token
        }
        response = requests.post(url, data=payload)
        self.print_response(response, type="Comment")
        return response

    def post_local_image_to_page(self, image_path=None, caption="Post from Python Local Image"):
        if not image_path: 
            return "Please provide an image url from local!"
        files = {
            'source': open(image_path, 'rb')
        }
        payload = {
            'caption': caption,
            'access_token': self.page_access_token,
            'published': True,
        }
        response = requests.post(self.url, files=files, data=payload)
        self.print_response(response, type="Local Image")
        return response
    
    def request_to_post_gemten(data):
        url = 'http://127.0.0.1:8000/api/post/to/facebook/'
        res = requests.post(url, json=data)

        response = res.json()
        return response
   
    

# https://developers.facebook.com/tools/explorer/?method=GET&path=me%2Faccounts%3Faccess_token%3DLONG_LIVED_USER_TOKEN&version=v22.0

