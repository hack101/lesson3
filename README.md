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

### Setting up

So naturally, our first step will be signing up for Firebase. You can do that for free [here](https://www.firebase.com/signup/), and when you are logged in you will already have a database ready for you to use, with a randomly-generated name - mine is "fiery-torch-8827.firebaseio.com", for example. We will use this when we develop our application.

Next, we will need to install Flask and other necessary dependencies. I will assume you have pip installed; if you are using a Trottier computer, pip will already be installed, but you will need to run [this shell script](https://github.com/hack101/lesson3/blob/master/setup.sh) to allow yourself to install packages. One easy way to do this is with the following command:

`curl https://raw.githubusercontent.com/hack101/lesson3/master/setup.sh | sh`

This downloads the script and runs it on your computer. You do not need to do this if you are using your own computer.

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

If you are using a Trottier computer you do not need "sudo".

### Organizing our application

Now we are all set to start developing our application. Let's begin by creating a new folder for our project, called `lesson3`, and inside of it we will add two folders: `static` and `templates`. The `static` folder will hold any assets that we want to be able to access, such as CSS and Javascript files. The other folder, `templates`, will hold our *templates*, which will specify how we want the pages on our website to look. Before, we used HTML files to represent the structure of our pages. Our templates are special types of HTML files, which can include variables which our Python application will fill in. More on this soon.

The logic behind our application will be in a file called `app.py`, which will sit inside of `lesson3`. So make an empty file called `app.py`, and now our directory structure should look like this:

![Folder structure](http://i.imgur.com/lCDA1wu.png)

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

![source](http://i.imgur.com/8YSWEDl.png)

Finally, the last piece of the file starts the application:

```python
# start the application if this is the main python module (which it is)
if __name__ == "__main__":
  app.run()
```

