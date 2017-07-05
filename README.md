# Flask-Access [![CircleCI](https://img.shields.io/circleci/project/github/barischj/flask-access.svg)](https://circleci.com/gh/barischj/flask-access) [![Codecov](https://img.shields.io/codecov/c/github/barischj/flask-access.svg)](https://codecov.io/gh/barischj/flask-access)

Easily protect access to Flask endpoints.

Works nicely with [Flask-Login](https://flask-login.readthedocs.io/en/latest/).

## Usage

### Protect endpoints

In this example the endpoint `"/secret-code"` requires a user to have `"admin"` rights:

``` Python
@app.route("/secret-code")
@flask_access.require("admin")
def secret_code():
    return "1234"
```

You can require any combination of rights for an endpoint, the rights can be any
type of object you like and you can use any number of positional or keyword
arguments:

``` Python
@flask_access.require("boss", 7, funny=True, hair=False)
```

### Register a user loader

When a user attempts to access a protected endpoint Flask-Access needs to load
the respective user object to check their access rights. For this reason set a
function **or** variable in `app.config[flask_access.CURRENT_USER]` that returns
the current user object. If the user has no account simply return `None`.

If you are also using Flask-Login you can simply do:

``` Python
app.config[flask_access.CURRENT_USER] = flask_login.current_user
```

### User access logic

When a user attempts to access an endpoint Flask-Access will load the user
object `u` and run `u.has_access(rights)` where `rights` are what is required
for the current endpoint.

If a user object has no `has_access` method, or if `has_access` returns anything
but `True`, then access will be denied.

So you need to implement `has_access(self, rights) -> bool` on your user class.
The `rights` that get passed in are the arguments you specified in
`@flask_access.require` for the current endpoint.

### Access denied handler

The default access denied handler calls `flask.abort(403)`

To set a custom access-denied handler:

``` Python
app.config[flask_access.ABORT_FN] = custom_abort_fn
```

### Login required

If you are using `flask_login.current_user` as your user loader then
`flask_access.require` implies `flask_login.login_required`, so no need to also
specify the latter.

Why? Well, if a user is not logged-in, `flask_login.current_user` will return a
`flask_login.AnonymousUserMixin` which does not have `has_access` implemented,
hence no access for the user.

## Example

For an example which includes a login/out system
see [example.py](example/example.py).
