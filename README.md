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

<p>You can start web service with <code> python service.py </code> then see  <code> localhost:5000 </code> address.</p>
<p>You can perform operations such as logging in and registering both via the web interface and through requests.</p>

<br>
<br>

## Start
<hr>

##### Web Type: 
<img width="688" alt="image1" src="https://user-images.githubusercontent.com/24435617/236053990-09db25ec-3495-4349-a6b4-7783cb9f7dc2.png">

##### Request Type:
<pre>
username = "test_username"
email = "test_email@test.com"
password = *****
user = RequestProcess(username, email, password)
</pre>

<br>
<br>
<br>

## Register
<hr>

##### Web Type
<img width="688" alt="image4" src="https://user-images.githubusercontent.com/24435617/236055236-cbacc94e-9a42-4ebd-a80f-6930425c15dd.png">

##### Request Type:
<pre>user.register_request()</pre>

<br>
<br>
<br>


## Login
<hr>

##### Web Type
<img width="688" alt="image5" src="https://user-images.githubusercontent.com/24435617/236055880-9a4b9da7-8041-4c92-becc-839576cfc042.png">

##### Request Type:
<pre>user.login_request()</pre>

<br>
<br>
<br>

## Add Article
<hr>

##### Web Type
<img width="688" alt="image7" src="https://user-images.githubusercontent.com/24435617/236056566-ca7ed43e-4a15-4f28-9371-676ce498e99f.png">

##### Request Type:

<br>
<br>
<br>

## Dashboard
<hr>

##### Web Type
<img width="688" alt="image" src="https://user-images.githubusercontent.com/24435617/236056755-8b30b07e-9e5d-4934-bd29-f109b72f9b1e.png">

##### Request Type:

<br>
<br>
<br>

## Article Detail
<hr>

##### Web Type
<img width="691" alt="resim9" src="https://user-images.githubusercontent.com/24435617/236057553-b9c516d4-0faa-42bd-a45b-185d3287a855.png">

##### Request Type:
