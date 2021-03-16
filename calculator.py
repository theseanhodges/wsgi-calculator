"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

host = ""

def add(*args):
  """ Returns a STRING with the sum of the arguments """

  try:
    result = int(args[0]) + int(args[1])
  except ValueError:
    raise NameError

  return str(result)

def subtract(*args):
  """ Returns a STRING with the result of subtracting arg[1] from arg[0] """

  try:
    result = int(args[0]) - int(args[1])
  except ValueError:
    raise NameError

  return str(result)

def multiply(*args):
  """ Returns a STRING with the product of the arguments """

  try:
    result = int(args[0]) * int(args[1])
  except ValueError:
    raise NameError

  return str(result)

def divide(*args):
  """ Returns a STRING with the result of dividing arg[1] from arg[0] """

  try:
    result = int(args[0]) / int(args[1])
  except ValueError:
    raise NameError

  return str(result)

def help():
  """ Returns a guide to using the calculator """

  return """<h1>WSGI Calculator</h1>
This calculator performs the requested result on the arguments in the path:<br />
<br />
{}/<b>operation</b>/<b>number1</b>/<b>number2</b><br />
<br />
<b>operation</b> can be any of the following.  Click the operation for an example.
<ul>
<li /><a href="/add/23/42">add</a>
<li /><a href="/subtract/23/42">subtract</a>
<li /><a href="/multiply/3/5">multiply</a>
<li /><a href="/divide/22/11">divide</a>
</ul>
""".format(host)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    handlers = {
        '': help,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')
    try:
        return handlers[path[0]], path[1:]
    except KeyError:
        raise NameError
    raise NotImplementedError

def application(environ, start_response):
    status = "200 OK"
    headers = [('Content-type', 'text/html')]

    global host
    host = "{}://{}".format(
      environ.get('wsgi.url_scheme'),
      environ.get('HTTP_HOST')
    )

    try:
      path, args = resolve_path(environ.get('PATH_INFO'))
      status = "200 OK"
      body = path(*args)
    except NameError:
      status = "404 Not Found"
      body = "<h1>404 Not Found</h1>"
    except Exception:
      status = "500 Internal Server Error"
      body = "<h1>500 Internal Server Error</h1>"
    start_response(status, headers)

    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
