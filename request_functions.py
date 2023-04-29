import requests as r


class RequestProcess:
    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        self.local_url = "http://localhost:5000/"
        self.session = r.session()

    def login_request(self):
        url = self.local_url+"login/request"
        data = {"username": self.username, "password": self.password}
        result = self.session.post(url, data=data)
        print(result.json(), result.status_code)

    def register_request(self):
        url = self.local_url+"register/request"
        data = {"username": self.username,"email":self.email,"password": self.password}
        result = self.session.post(url, data=data)
        print(result.json(), result.status_code)

    def dashboard_request(self):
        url = self.local_url+"dashboard/request"
        result = self.session.get(url)
        print(result.json(), result.status_code)

    def article_detail_request(self, article_id):
        url = self.local_url+"article-detail/request/%s" % (str(article_id))
        result = self.session.get(url)
        print(result.json(), result.status_code)

    def add_article_request(self, title, content):
        url = self.local_url+"add-article/request"
        article_params_data = {"title": title, "content": content}
        result = self.session.post(url, data=article_params_data)
        print(result.json(), result.status_code)

    def delete_article_request(self, article_id):
        url = self.local_url+"delete-article/request/%s" % (str(article_id))
        result = self.session.post(url)
        print(result.json(), result.status_code)

    def update_article_request(self, article_id, title, content):
        url = self.local_url+"update-article/request/%s" % (str(article_id))
        result = self.session.put(
            url, data={"title": title, "content": content})
        print(result.json(), result.status_code)

    def logout_request(self):
        url = self.local_url+"logout/request"
        result = self.session.get(url)
        print(result.json(), result.status_code)


process = RequestProcess("furkan", "testt@gmail.com","12345")
process.login_request()
process.delete_article_request(1)
#process.register_request()
#process.login_request()
#process.logout_request()
# process.login_request()
# process.dashboard_request()
# process.update_article_request(2,"Test","Testtt")
# process.delete_article_request(2)
# process.article_detail_request(1)
# process.add_article_request("Request Test","This is request test content")
