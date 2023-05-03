import requests as r

'''
Basic Request Module with Flask
----------------------------------
'''
class RequestProcess:
    '''
    Request Process
    ---------------
    
    This class helps HTTP response on the flask process
    
    Examples:
        RequestProcess('test_username','test@mail.com','test_password')
    '''
    def __init__(self, username:str, email:str, password:str):
        self.username = username
        self.email = email
        self.password = password
        self.local_url = "http://localhost:5000/"
        self.session = r.session()
        self.result_status_code = None

    def login_request(self):
        url = self.local_url+"login/request"
        data = {"username": self.username, "password": self.password}
        result = self.session.post(url, data=data)
        self.result_status_code = result.status_code
        print(result.json())

    def register_request(self):
        url = self.local_url+"register/request"
        data = {"username": self.username,"email":self.email,"password": self.password}
        result = self.session.post(url, data=data)
        self.result_status_code = result.status_code
        print(result.json())

    def dashboard_request(self):
        url = self.local_url+"dashboard/request"
        result = self.session.get(url)
        self.result_status_code = result.status_code
        print(result.json())

    def article_detail_request(self, article_id:int):
        url = self.local_url+"article-detail/request/%s" % (str(article_id))
        result = self.session.get(url)
        self.result_status_code = result.status_code
        print(result.json())

    def add_article_request(self, title:str, content:str):
        url = self.local_url+"add-article/request"
        article_params_data = {"title": title, "content": content}
        result = self.session.post(url, data=article_params_data)
        self.result_status_code = result.status_code
        print(result.json())

    def delete_article_request(self, article_id:int):
        url = self.local_url+"delete-article/request/%s" % (str(article_id))
        result = self.session.delete(url)
        self.result_status_code = result.status_code
        print(result.json())

    def update_article_request(self, article_id:id, title:str, content:str):
        url = self.local_url+"update-article/request/%s" % (str(article_id))
        result = self.session.put(url, data={"title": title, "content": content})
        self.result_status_code = result.status_code
        print(result.json())

    def logout_request(self):
        url = self.local_url+"logout/request"
        result = self.session.get(url)
        print(result.json())
