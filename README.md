# Flask-Access [![CircleCI](https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser.svg)](https://circleci.com/gh/barischj/flask-access)

Easily control access to Flask endpoints.

Works well with [Flask-Login](https://flask-login.readthedocs.io/en/latest/).

## Usage

### Register a user loader

Set a function **or** variable in `app.config[flask_access.CURRENT_USER]` which
returns the current user.

With Flask-Login simply:

`app.config[flask_access.CURRENT_USER] = flask_login.current_user`

### User access logic

Implement `has_access(self, access) -> bool` on your user class.

There are no restrictions on the kind of access logic you implement.

If a user does not have `has_access` implemented access will be denied.

### Protect a view

To require access rights e.g. `"admin"` for a view:

```
@app.route("/secret-code")
@flask_access.require("admin")
def secret_documents():
    return "Secret code: 1234"
```

### Access denied handler

The default access denied handler calls `flask.abort(403)`

To set a custom access-denied handler:

`app.config[flask_access.ABORT_FN] = custom_abort_fn`

### Login required

If you are using `flask_login.current_user` as your user loader then
`flask_access.require` implies `flask_login.login_required`. Why? If a user is
not logged-in, `flask_login.current_user` will return a
`flask_login.AnonymousUserMixin` which does not have `has_access` implemented.

## Example
For an example which includes a login/out system see [example/example.py]().
