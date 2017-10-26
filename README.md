# Flask-Access [![CircleCI](https://img.shields.io/circleci/project/github/barischj/flask-access.svg)](https://circleci.com/gh/barischj/flask-access) [![Codecov](https://img.shields.io/codecov/c/github/barischj/flask-access.svg)](https://codecov.io/gh/barischj/flask-access)

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

We need to associate requests with users that have permissions (or not). So
please set a function *or* variable in
`app.config[flask_access.CURRENT_USER]` that returns
the current user. If the user has no account simply return `None`.

If you are also using Flask-Login you can simply :clap:

``` Python
app.config[flask_access.CURRENT_USER] = flask_login.current_user
```

## User access logic

In short, implement `has_access(self, rights) -> bool` on your user class.

When a user attempts to access an endpoint, Flask-Access will load the current
user object `u` and run `u.has_access(rights)`, the `rights` that get passed in
are the `"boss", 7, funny=True, bald=None` from above.

If a user has no `has_access` method, or it doesn't return`True`, then access
is denied :speak_no_evil:

## Access denied handler

The default access denied handler calls `flask.abort(403)`

To set a custom access-denied handler:

``` Python
app.config[flask_access.ABORT_FN] = custom_abort_fn
```

## Login required

If you are using `flask_login.current_user` as your user loader then
`flask_access.require` implies `flask_login.login_required`, so no need to also
specify the latter.

![](https://raw.githubusercontent.com/skullface/custom-chat-emoji/master/emoji/meme__roll-safe.png)

Why? Well, if a user is not logged-in, `flask_login.current_user` will return a
`flask_login.AnonymousUserMixin` which does not have `has_access` implemented,
hence no access for the user.

## Example

An [example](example/example.py) with a primitive login/out system.
