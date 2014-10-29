##III. HTTP, and Backend programming

When we introduced the idea of a server and a client, we gave a simplified version. We said that a client asks a server for a file and a server gives it back to the client. What we didn't explain was exactly how does a client ask a server something? And what kind of things can a client ask? What does a request look like? We will answer all these questions today.

### HTTP ###

HTTP stands for HyperText Transfer Protocol. HyperText is the text that makes up the internet (you will recall that HTML stands for HyperText Markup Language). HTTP is a protocol for sending HyperText over the internet. But how is it sent? It is send in the form of requests and response.

When a client "asks" for a file, the client is making a request. This request is send as an HTTP packet over the internet to the server. The server then processes the request and sends a response (`index.html` for example). Along with this response, the server send and HTTP response status. Come common status codes which you may have encountered are 

* 200: "OK" - This status means that everything went well.
* 403: "FORBIDDEN" - This status means that you (read: your IP) were not authorized to access the content
* 404: "NOT FOUND" - This means that what you asked for was not found
* 500: "INTERNAL SERVER ERROR" - This status means that there was an error on the server side (could be a bug in the website)

There are of course many more statuses. 

So what type of requests are there? 

* **GET** 
* **POST**
* PUT
* DELETE
* PATCH
* HEAD
* TRACE
* OPTIONS
* CONNECT

We're only going to worry about **GET** and **POST**, as those are the ones you will use most frequently.

#### GET ####

A GET request is the most basic request. A GET request is sent when a client wants information from the server, and nothing more - the client doesn't want to modify any of the server's data, only to read it. When you type a URL into your browser, your browser sends a GET request to the server at that URL, and the response is the HTML which makes up the page that you see after entering that URL.

We can send some additional data along with the request as well. We do this with URL parameters: these show up at the end of the URL, starting with a ?. Each parameter is set with "param=value", and we separate these assignments with &. So the URL "www.website.com/page?key=val&foo=bar" corresponds to a GET request sent to "www.website.com/page" with the parameter "key" set to "value" and the parameter "foo" set to "bar".

When you search on a search engine, you are actually just sending a GET request! I'm going to navigate to Bing and instead of using the search bar, I'm going to type in *URL parameters* that define my get request. (Google used to work by GET requests as well, but now does something a little different. It's OK though, I'm sure the traffic from this tutorial will make the people at bing pretty excited so we might as well do something nice)

![Bing](http://s28.postimg.org/kfqey59hp/Screen_Shot_2014_10_25_at_11_06_58_PM.png)

![Type in a GET request](http://s13.postimg.org/p3cq9xcuf/Screen_Shot_2014_10_25_at_11_07_21_PM.png)

What I've done here is sent a GET request to the `/search/` route at Bing with the parameter `q` having the value `google`. You can think of this as calling a function `search` and passing it a `q` (presumably standing for "query") parameter with the value `google`. 

![We searched for Google](http://s13.postimg.org/rpxanzadj/Screen_Shot_2014_10_25_at_11_13_14_PM.png)

And there we go. We made a GET request to Bing's servers asking for the search results for the query "Google" and it displayed them to us!

A GET request is called a safe method, as it's not supposed to alter the data on the server in any significant way, just to retrieve information.


#### POST ####

POST is used to send user data to the server. For example, when you log into a website, your username and password are probably being sent by POST, or if you post to a message board, the message content may be being posted as well. 

POST requests don't have to navigate you away from a page, a user can send information to a server without going to a whole new page (in a chatroom for example, each message is POSTed but the user always stays on the same page). Whenever you, as a web developer want to get some information from a user, you will likely set them up to make a POST request.

Unlike in a GET request, where the parameters are visible in the URL, if we want to see the data that a POST request carries we need to inspect the request object itself. We can see these by using the Chrome developer tools, for example.

## Building a simple backend with Flask

When we began developing our webpage over the course of the past two lessons, we noted that we were making a *static website*. Our webpages always showed the same information, and unless we manually modified our HTML or CSS, they never changed. Static websites are fine for what we've been doing so far, but what if we want our webpages to have dynamic functionality? What if we want other people to be able to leave comments, or interact with our website in a lasting way?

Today we will take the first steps towards building a dynamic web application. Starting with our existing webpage, we will add a comment box, and also create a new page which lists the comments people have left in the past. To do this, we will use a *web application framework*, in this case the framework Flask, which helps us write a web application in Python.

Hopefully you've started to get the impression that the fundamental functionality that makes the internet work the way it does is in the form of requests. By sending and recieving requests appropriately, both clients and servers are able to carry out the tasks that make them useful. It follows that our application will need to handle requests. A framework like Flask helps us do this. Flask will make handling and sending requests much simpler than if we were to work with these requests on our own.

Broadly, Flask will make it easy to do two things: handle requests users make for different parts of our website, and render a webpage based on data we store in a database. For a database, we will use Firebase, which provides an easy way to store and access data. Other popular databases include various SQL implementations, and so-called "no-SQL" databases, which are often based on simple key-value storage.

### Starter package

To make things easier, I've created a sort of "starter package" which has the files and folders you will need, missing the essential things we will cover. You can download it by running

`git clone -b starter https://github.com/hack101/lesson3.git`

This will create a `lesson3` folder in whatever directory you run this command. Inside this folder will be two folders, an empty `app.py` file, a shell script `setup.sh` which is explained in the next section, and a list of packages you will need for this lesson. The folder `static` includes Foundation, which we introduced before, and in `templates` there are 3 files which we will use. The file `index.html` is based on Amiel's webpage which he created in the last lesson.

You can start from scratch if you'd like to as well - this lesson will cover everything you need to do to start from scratch.

### Setting up

So naturally, our first step will be signing up for Firebase. You can do that for free [here](https://www.firebase.com/signup/), and when you are logged in you will already have a database ready for you to use, with a randomly-generated name - mine is like "fiery-torch-12341234.firebaseio.com", for example. We will use this when we develop our application.

Next, we will need to install Flask and other necessary dependencies. I will assume you have pip installed; if you are using a Trottier computer, pip will already be installed, but you will need to run [this shell script](https://github.com/hack101/lesson3/blob/master/setup.sh) to allow yourself to install packages. One easy way to do this is with the following command:

`curl https://raw.githubusercontent.com/hack101/lesson3/master/setup.sh | sh`

This downloads the script and runs it on your computer. You do not need to do this if you are using your own computer. If you downloaded the starter packages, `setup.sh` is already there, and you can simply type `sh setup.sh` to run it.

As for the packages, we will be using these packages:

```
Flask
requests
python-firebase
```

You can install each one by typing `pip install Flask`, `pip install requests`, and `pip install python-firebase`, or by downloading [this file](https://raw.githubusercontent.com/hack101/lesson3/master/packages.txt) and running `pip install -r FILENAME` where `FILENAME` is what you called the downloaded file. Or, you can type in the following two lines:

```
curl https://raw.githubusercontent.com/hack101/lesson3/master/packages.txt > packages.txt
sudo pip install -r packages.txt
```

If you are using a Trottier computer you do not need "sudo". The starter package also includes this packages file, so if you downloaded that you only need to run `sudo pip install -r packages.txt`.

### Organizing our application

Now we are all set to start developing our application. Let's begin by creating a new folder for our project, called `lesson3`, and inside of it we will add two folders: `static` and `templates`. The `static` folder will hold any assets that we want to be able to access, such as CSS and Javascript files. The other folder, `templates`, will hold our *templates*, which will specify how we want the pages on our website to look. Before, we used HTML files to represent the structure of our pages. Our templates are special types of HTML files, which can include variables which our Python application will fill in. More on this soon.

The logic behind our application will be in a file called `app.py`, which will sit inside of `lesson3`. So make an empty file called `app.py`, and now our directory structure should look like this:

![Folder structure](http://i.imgur.com/sKmzkPA.png)

Let's get a sort of "hello world" going with Flask. Inside `app.py`, we will add the following code:

```python
from flask import Flask

# config
# server will reload on source changes, and provide a debugger for errors
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__) # consume the configuration above

# decorator which tells flask what url triggers this fn
@app.route('/')
def index():
  return 'Hello world'

# start the application if this is the main python module (which it is)
if __name__ == "__main__":
  app.run()
```

If we save this file, and in another terminal window type `python app.py`, we should get the following output:
```
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

If we open a browser and go to http://127.0.0.1:5000/, we should see "Hello world". Yay! Let's look at what we've done, piece by piece. The first part of the file is

```python
from flask import Flask
```

This imports the flask module with the name `Flask`, allowing us to use it. We can do this because we installed Flask with pip earlier.

```python
# config
# server will reload on source changes, and provide a debugger for errors
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__) # consume the configuration above
```

This part of the file does two things: first, we set a configuration open, `DEBUG`, to be true. This will make it easier to develop our app, because if we are running `app.py`, we can make changes to the file and the running version will update itself without needing a manual restart. Then, we make a new app, called `app`, and tell it to read the configuration in `__name__`, which is just this file itself. If we put our configuration in another file, we would tell Flask to look in that file instead.

```python
# decorator which tells flask what url triggers this fn
@app.route('/')
def index():
  return 'Hello world'
```

This is the interesting part. `def` is how you declare a function in Python. So we create a function called `index()` which just returns 'Hello world'. What is above the function? The line `@app.route('/')` means that when a request for "/" is made (remember, "/" is the highest-level part of our website - when you go to "google.com/" you are requesting "/" from google.com), Flask will run the function `index()`. This is how we handle requests with Flask - for each request we want to handle, we create a function like `index()` and above it we use a [decorator](http://thecodeship.com/patterns/guide-to-python-function-decorators/) to tell Flask to run this function for a certain request. The function will return the HTML for the page we want to show for that request. In this case, we are only returning 'Hello world', which we can see if we look at the source for the page at http://127.0.0.1:5000/.

![source](http://i.imgur.com/16oSW1h.png)

Finally, the last piece of the file starts the application:

```python
# start the application if this is the main python module (which it is)
if __name__ == "__main__":
  app.run()
```

### Templates

Let's make our main page just as nice as it was in the last lesson. We saw that the return value of a function given for a particular request is the HTML we want to render for that request. Usually HTML files get pretty big, and we definitely don't want to have to include big strings of HTML in our Python source code. This is where templates come in. We can write external files with the HTML we want, and then in our `app.py` code we can return these files. Flask provides a function called `render_template` which lets us do this.

First let's make our templates. We are going to make two templates. One will be a sort of "general" template. We will be making two pages today: one is our main page, and one will be a list of comments people leave on our website. We want the style of these two pages to be consistent, and we will want to use the frontend framework Foundation again, on each page. To make sure we don't need to repeat ourselves, and include the same CSS file manually on each page, we will use the general template to do this stuff, and then make new templates - one for the main page, and one for the list - which will use the general template as a base.

So inside our `templates` folder, let's make a new file called "layout.html". Inside this file, we will write the following:

```html
<!doctype html>
<html>
<head>
  {% block head %}{% endblock %}
  <link rel=stylesheet type=text/css href="{{ url_for('static', filename='foundation.css') }}">

</head>
<body>
  <div class="row">
    <div class="large-12 columns">
      {% block body %}{% endblock %}
    </div>
  </div>
</body>
</html>
```

We also need to place the `foundation.css` file from last time into the folder `static`. You can download it [here](http://foundation.zurb.com/develop/download.html) if you don't have the file from last time. If you downloaded the starter folder in the beginning, it should be inside the `static` folder already.

The template looks like normal HTML, except for the stuff inside the curly braces `{{ }}` and `{% %}`. First, we have two lines which say `{% block NAME %}{% endblock %}`, where NAME is either "head" or "body". These lines define "blocks", which we can fill in with other templates that will extend this main, general layout template.

Meanwhile, the stuff inside the `{{ }}` is Python code. When the template is "rendered", this code is executed. In this case, it will create a URL for the Foundation CSS file in our `static` folder.

Now let's make the template for our main page. Create another file in `templates`, called "index.html". In here, we can pretty much copy over our HTML from the previous lesson. For example, continuing with Amiel's page, my "index.html" looks like this:

```html
{% extends "layout.html" %}

{% block head %}
<title>Amiel's Bio</title>
{% endblock %}

{% block body %}
<h2> Amiel Kollek's Webpage </h2>

<div class='panel'>
  <p>
    Hello, my name is Amiel. I study math and physics at McGill university and I am going to make my own website!
  </p>
</div>

<h4> My Interests </h4>

<p> Here are a few things I like: </p>

<div class="large-3 columns">
  <h5> Computers </h5>
  <p>
    I like programming!
  </p>
</div>

<div class="large-3 columns">
  <h5> Math </h5>
  <p>
    Math is fun!
  </p>
</div>

<div class="large-3 columns">
  <h5> Hiking </h5>
  <p>
    I like the outdoors
  </p>
</div>

<div class="large-3 columns">
  <h5> Physics </h5>
  <p>
    <em>E=mc<sup>2</sup></em>
  </p>
</div>
{% endblock %}
```

This file does differ from the HTML from before though. Notice, first, that at the top of the file we have

```html
{% extends "layout.html" %}
```

This means that this template will use the structure we laid out in "layout.html". This line is what lets us write the next part in the template file:

```html
{% block head %}
<title>Amiel's Bio</title>
{% endblock %}
```

Remember the `{% block head %}{% endblock %}` in "layout.html"? This part of "index.html" is where we define the HTML that will fill in the block called "head" in "layout.html". So we are saying "replace the line `{% block head %}{% endblock %}` in "layout.html" with the line `<title>Amiel's Bio</title>`". Since the "head" block in "layout.html" is inside of a `<head>` tag, we can use the `<title>` tag.

The next part of the "index.html" template is all inside a big `{% block body %}{% endblock %}` piece. Basically, we took everything inside of the `<body>` tag from our page last time, and put it inside `{% block body %}{% endblock %}` here. Since the template "layout.html" places the "body" block inside of "<body>" tags, we don't need the actual `<body>` tags from last time, just what was inside them.

Now that we have these two templates, we can modify `app.py` a little bit so they get used. First, modify the import line in `app.py` to add new packages to import:

```python
from flask import Flask, redirect, request, url_for, render_template
```

and inside the function `index()` we will change the return value, so that the function now looks like this:

```python
@app.route('/')
def index():
  return render_template('index.html')
```

Now when we go to http://127.0.0.1:5000/ we should see our webpage, like before.

### Adding a comment box

Okay, now we've recreated what we had before - big deal, right? Why are we using Flask in the first place?

Let's do something we couldn't do before. We are going to add a comment box to the page. To do this, we need to add it to the template. In "index.html", add the following HTML at the end of the file, but before the closing `{% endblock %}`:

```html
<h4>Leave me a message</h4>

<p>
  You can leave me a message below, or see messages people have left me <a href="{{ url_for('messages') }}">here</a>
</p>

<div class="large-8 columns">
<form action="/submit_message" method="post">
  <input type="text" placeholder="Name" name="who">
  <textarea placeholder="Enter your message here" name="message" cols="50" rows="4"></textarea>
  <input type="submit" value="Submit">
</form>
</div>
```

If you downloaded the starter package, you still need to add this to the "index.html`" file.

Note that this includes `url_for('messages')`, so let's add a function to show the messages page too: in `app.py`, add the following stuff after the end of the `index()` function:

```python
@app.route('/messages')
def messages():
  return 'Messages'
```

so now we have routes for two pages:

```python
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/messages')
def messages():
  return 'Messages'
```

Now we can go to http://127.0.0.1:5000/messages and get a page. We also added a form to the bottom of the page:

![form](http://i.imgur.com/pvAKzzF.png)

Looking at the HTML for the form, we have this: `<form action="/submit_message" method="post">`. This specifies what to do with the stuff in our form when the user clicks the submit button. It says when submit is clicked, the page will make a POST request to the URL "/submit_message". The content of the post request will be the data the user typed into the form.

Right now, if the user pressed submit, what happens? Well, we never defined a "/submit_message" URL, so clicking "submit" takes the user to a "404 not found" page.

Let's add a route for "/submit_message". After the end of the `messages()` function definition, add the following:

```python
@app.route('/submit_message', methods=['POST'])
def submit_message():
  print request.form
  return redirect(url_for('messages'))
```

This says that when a POST request (and only a POST request) is made to the URL "/submit_message", we will print the contents of the form to the Python console, and then redirect to our messages page. After saving `app.py` with these new lines, we can click the submit button, and we will be redirected to the messages page. Try filling out the form and submitting it, and look at the terminal window you're running the app in. You should see it print out what you typed in the form!

![Terminal output](http://i.imgur.com/kN3z0uK.png)

### Hooking up our database

Okay so we're in the home stretch. We have a way to submit comments, but we aren't doing anything with them yet. 

We want to store the comments people leave, so we can make a list of them and show them in the "messages" page. We will store these in Firebase. First, we need to import the Firebase module, which will make it easy to work with our database in Python. After the import line for Flask, add this line:

```python
from firebase import firebase
```

and after the line where we tell Flask to use the config we provides, add this:

```python
firebase = \
    firebase.FirebaseApplication(URL, None)
```

where URL is the URL of your Firebase database. It will look something like 'https://fiery-torch-12341234.firebaseio.com'. You can see it when you go to https://www.firebase.com/account/#/, under "My First App".

Finally, let's modify the `submit_message()` function so it looks like this:

```python
def submit_message():
  message = {
    'body': request.form['message'],
    'who': request.form['who']
  }
  firebase.post('/messages', message)
  return redirect(url_for('messages'))
```

Now, when a message is submitted, we will take the contents of the form, and post them to our Firebase database. The whole `app.py` should look like:

```python
from flask import Flask, redirect, request, url_for, render_template
from firebase import firebase

# config
# server will reload on source changes, and provide a debugger for errors
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__) # consume the configuration above

firebase = \
    firebase.FirebaseApplication(URL, None)

# decorator which tells flask what url triggers this fn
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/messages')
def messages():
  return 'Messages'

@app.route('/submit_message', methods=['POST'])
def submit_message():
  message = {
    'body': request.form['message'],
    'who': request.form['who']
  }
  firebase.post('/messages', message)
  return redirect(url_for('messages'))

# start the application if this is the main python module (which it is)
if __name__ == "__main__":
  app.run()
```

Ok here is the cool part. If you go to your Firebase URL in your browser, you should see a little message that says "This location is empty!". That's because we haven't added any data yet. But now we have our app set up to add data the Firebase when the comment form is submitted, right? So go to your main page, type in a comment, and submit it. Firebase should automatically update, showing the data you submitted!

Now that we have the data stored, all we need to do is list it on the messages page! First, let's make a template for the list page. Inside the `templates` folder, add a file "list.html" with the following contents:

```html
{% extends "layout.html" %}

{% block head %}
  <title>Messages</title>
{% endblock %}

{% block body %}
  <h2>Messages</h2>
  {% if messages %}
    <ul>
      {% for message in messages %}
        <li>
          <h5>{{ messages[message].who }}</h5> 
          <p>{{ messages[message].body }}</p>
        </li>
      {% endfor %}
    </ul>
  {% else %}
    No messages!
  {% endif %}
  <a href="{{ url_for('index') }}">Go back to the main page</a>
{% endblock %}
```

Once again, we extend our "layout.html" template, and then provide stuff to fill in the "head" and "body" blocks. We make pretty heavy use of `{% %}` in this one, so let's break it down. When we render this template, we are going to provide a "messages" object which will hold all the message data. So first, we check that the messages object is not empty with:

```html
{% if messages %}
  ...etc
{% else %}
  No messages!
{% endif %}
```

If it is empty, then we go into the `else` branch, and instead of doing what we'd do if we had messages, we just print "No messages". 

If there *are* messages, we make a list for them with the `<ul></ul>` tags, and inside of these tags we use a `for` loop to create a `<li></li>` for each message:

```html
<ul>
  {% for message in messages %}
    <li>
      <h5>{{ messages[message].who }}</h5> 
      <p>{{ messages[message].body }}</p>
    </li>
  {% endfor %}
</ul>
```

At the end, we use `<a href="{{ url_for('index') }}">Go back to the main page</a>` to make a link back to our main page.

Now, we need to tell the app to use this template, so let's modify the `messages()` function so it looks like this:

```python
def messages():
  result = firebase.get('/messages', None)
  return render_template('list.html', messages=result)
```

First, we get the list of messages from Firebase. Then, we return the rendered template, and we pass the results to the template in a variable called "messages".

That's it! Now when we go to http://127.0.0.1:5000/messages, we can see the list of messages from Firebase, and when we use the form on our main page, it will add to this list. So we have a working comment box that anyone can use.

### Conclusion

Unfortunately, we cannot publish this application to Github pages like before :(. Github pages lets us publish static sites, but this time our website is not static. In the next lesson, we will cover how to publish a dynamic web application like this.
