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

So naturally, our first step will be signing up for Firebase. You can do that for free [here](https://www.firebase.com/signup/), and when you are logged in you will already have a database ready for you to use, with a randomly-generated name - mine is "fiery-torch-8827.firebaseio.com", for example. We will use this when we develop our application.

Next, we will need to install Flask and other necessary dependencies. I will assume you have pip installed; if you are using a Trottier computer, pip will already be installed, but you will need to run [this shell script](https://github.com/hack101/lesson3/blob/master/setup.sh) to allow yourself to install packages. One easy way to do this is with the following command:

`curl https://raw.githubusercontent.com/hack101/lesson3/master/setup.sh | sh`

This downloads the script and runs it on your computer. You do not need to do this if you are using your own computer.

As for the packages, we will be using these packages:

````
Flask
requests
python-firebase
````

You can install each one by typing `pip install Flask`, `pip install requests`, and `pip install python-firebase`, or by downloading [this file](https://raw.githubusercontent.com/hack101/lesson3/master/packages.txt) and running `pip install -r FILENAME` where `FILENAME` is what you called the downloaded file. Or, you can type in the following two lines:

````
curl https://raw.githubusercontent.com/hack101/lesson3/master/packages.txt > packages.txt
sudo pip install -r packages.txt
````

If you are using a Trottier computer you do not need "sudo".

Now we are all set to start developing our application.
