# Basic Flask Request
![flask](https://user-images.githubusercontent.com/24435617/236051719-a2f5066a-b49e-4167-b72b-24453295fae0.png)


It is a simple Flask project where the processing is done both in the foreground and in the background.

<br>


### Module Install ###

<pre>
pip install Flask
pip install email-validator
pip install Flask-Login
pip install Flask-SQLAlchemy
pip install WTForms
pip install requests
pip install pwinput
</pre>

<p>You can start service with <code> python service.py </code> then see  <code> localhost:5000 </code> address.</p>
<p>You can perform operations such as logging in and registering both via the web interface and through requests.</p>

<br>
<br>

## Start
<hr>
<img width="688" alt="resim1" src="https://user-images.githubusercontent.com/24435617/236053990-09db25ec-3495-4349-a6b4-7783cb9f7dc2.png">
<pre>
username = "test_username"
email = "test_email@test.com"
password = *****
user = RequestProcess(username, email, password)
</pre>
