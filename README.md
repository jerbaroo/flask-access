# Flask-Access [![CircleCI](https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser.svg)](https://circleci.com/gh/barischj/flask-access)

Easily control access to Flask endpoints.

Works well with [Flask-Login](https://flask-login.readthedocs.io/en/latest/).

## Usage

### Protect endpoints

To require access rights (e.g. `"admin"`) for an endpoint:

``` Python
@app.route("/secret-code")
@flask_access.require("admin")
def secret_code():
    return "Secret code: 1234"
```

The access rights required for an endpoint can be anything you like, not just a
string. You can pass in as many positional or keyword arguments as you like.

### Register a user loader

Set a function **or** variable in `app.config[flask_access.CURRENT_USER]` which
returns the current user. When a client attempts to access a protected endpoint
we use this to load the user whose access rights we check.

If you are using Flask-Login you can just do:

``` Python
app.config[flask_access.CURRENT_USER] = flask_login.current_user
```

### User access logic

Implement `has_access(self, *args, **kwargs) -> bool` on your user class.

Implement any kind of access logic you like. The arguments this function
receives are whatever you set in `@flask_access.require`, for the endpoint
currently being checked.

If a user does not have `has_access` implemented, or the function returns
anything but `True`, then access will be denied.

### Access denied handler

The default access denied handler calls `flask.abort(403)`

To set a custom access-denied handler:

``` Python
app.config[flask_access.ABORT_FN] = custom_abort_fn
```

### Login required

If you are using `flask_login.current_user` as your user loader then
`flask_access.require` implies `flask_login.login_required`. Why? If a user is
not logged-in, `flask_login.current_user` will return a
`flask_login.AnonymousUserMixin` which does not have `has_access` implemented.

## Example

For an example which includes a login/out system
see [example.py](example/example.py).
