# Flask-Access [![CircleCI](https://circleci.com/gh/barischrooneyj/flask-access.svg?style=svg)](https://circleci.com/gh/barischrooneyj/flask-access)

Simple protection of Flask endpoints.

Integrates well with [Flask-Login](https://flask-login.readthedocs.io/en/latest/).

## Protect endpoints

Here, the endpoint `"/secret-code"` requires a user to have `"admin"` rights:

``` Python
@app.route("/secret-code")
@flask_access.require("admin")
def secret_code():
    return "1234"
```

You could have other requirements:

``` Python
@flask_access.require("boss", 7, funny=True, bald=None)
```

## Register a user loader

Flas-Access needs to associate the current request with a user that
has permission or not. Flask-Access will look for the current user
in `app.config[flask_access.CURRENT_USER]`, here you can assign a
function that returns the current user.

``` Python
app.config[flask_access.CURRENT_USER] = my_current_user_func
```

The type of the returned user can be whatever you are using in your
application to model users already, the only condition is that the user
class implements a method `has_access`. If the user has no account return
`True` to allow access. Anything other than `True` or an instance of a
class implementing `has_access` will have access denied.

If you are also using Flask-Login you can simply apply the assignment
below :clap:

``` Python
app.config[flask_access.CURRENT_USER] = flask_login.current_user

```

## User access logic

In short, implement `has_access(self, rights) -> bool` on your user class.

When a user attempts to access an endpoint, Flask-Access will load the current
user object `user` and run `user.has_access(rights)`, the `rights` that get
passed in are the `"boss", 7, funny=True, bald=None` from above.

If a user doesn't have an `has_access` method, or the method doesn't return
`True`, then access is denied :speak_no_evil:

## Access denied handler

The default access denied handler calls `flask.abort(403)`

To set a custom access-denied handler:

``` Python
app.config[flask_access.ABORT_FN] = my_custom_abort_func
```

## Login required

If you are using `flask_login.current_user` as your user loader then
`flask_access.require` implies `flask_login.login_required`, so no need to also
specify the latter.

Why? Well, if a user is not logged-in, `flask_login.current_user` will return a
`flask_login.AnonymousUserMixin` which does not have `has_access` implemented,
hence no access for the user.

## Example

An [example](example/example.py) with a primitive login/out system.
