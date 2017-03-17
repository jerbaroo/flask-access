"""Tests for flask_acces.py."""

import flask
from flask_access import flask_access
import mock
from nose.tools import assert_equal, assert_not_equal


class TestFlaskAccess:

    def setup(self):
        self.app = flask.Flask(__name__)

    @mock.patch.object(flask, "abort")
    def test_abort_with_default_handler(self, mock_abort):
        with self.app.app_context():
            flask_access._abort()
            mock_abort.assert_called_once_with(403)

    def test_abort_with_custom_handler(self):
        custom_fn = mock.Mock()
        self.app.config[flask_access.ABORT_FN] = custom_fn
        with self.app.app_context():
            flask_access._abort()
            custom_fn.assert_called_once_with()

    def test_current_user_as_variable_success(self):
        user = object()
        self.app.config[flask_access.CURRENT_USER] = user
        with self.app.app_context():
            assert_equal(user, flask_access._current_user())

    def test_current_user_as_variable_failure(self):
        self.app.config[flask_access.CURRENT_USER] = object()
        with self.app.app_context():
            assert_not_equal(object(), flask_access._current_user())

    def test_current_user_as_function_success(self):
        user = object()
        user_fn = lambda: user  # noqa: E731
        self.app.config[flask_access.CURRENT_USER] = user_fn
        with self.app.app_context():
            assert_equal(user_fn(), flask_access._current_user())

    def test_current_user_as_function_failure(self):
        self.app.config[flask_access.CURRENT_USER] = lambda: object()
        with self.app.app_context():
            assert_not_equal(object(), flask_access._current_user())
