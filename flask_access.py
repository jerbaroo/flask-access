import flask
import inspect

ABORT_FN = "flask_access_abort_fn"
CURRENT_USER = "flask_access_current_user"


def _abort():
    """Calls a custom abort function if defined, else flask's 403."""
    flask.current_app.config.get(ABORT_FN, lambda: flask.abort(403))()


def _current_user():
    """Returns the current user from the app config."""
    user = flask.current_app.config[CURRENT_USER]
    if inspect.isfunction(user):
        user = user()
    return user


def require(access):
    def decorator(original_fn):
        def new_fn(*args, **kwargs):
            user = _current_user()
            if hasattr(user, "has_access") and user.has_access(access):
                return original_fn(*args, **kwargs)
            _abort()
        return new_fn
    return decorator
