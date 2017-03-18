"""Tests for flask_access.py."""

import flask
from flask_access import flask_access
import mock
from nose.tools import assert_equal, assert_not_equal


class NoAccess:
    """User who has no access rights."""

    def has_access(self, _):
        return False


class AdminAccess:
    """User who has admin access rights."""

    def has_access(self, access):
        return access == "admin"


class ArgsAndKwargsAccess:
    """User whose access rights depend on given args and kwargs."""

    def has_access(self, a, b, c=False, d=False):
        return all([
            a == "Alpha",
            b == "Bravo",
            c == "Charlie",
            d == "Delta"
        ])


class TruthyAccess:
    """User whose access rights are truthy but not True."""

    def has_access(self, _):
        return "true"


class TestFlaskAccess:
    """All tests for flask_access.py."""

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

    def test_current_user_as_variable_equal(self):
        user = object()
        self.app.config[flask_access.CURRENT_USER] = user
        with self.app.app_context():
            assert_equal(user, flask_access._current_user())

    def test_current_user_as_variable_not_equal(self):
        self.app.config[flask_access.CURRENT_USER] = object()
        with self.app.app_context():
            assert_not_equal(object(), flask_access._current_user())

    def test_current_user_as_function_equal(self):
        user = object()
        user_fn = lambda: user  # flake8: disable=E731
        self.app.config[flask_access.CURRENT_USER] = user_fn
        with self.app.app_context():
            assert_equal(user_fn(), flask_access._current_user())

    def test_current_user_as_function_not_equal(self):
        self.app.config[flask_access.CURRENT_USER] = lambda: object()
        with self.app.app_context():
            assert_not_equal(object(), flask_access._current_user())

    @mock.patch.object(flask, "abort")
    def test_require_user_has_no_access(self, mock_abort):
        @flask_access.require("admin")
        def secret_code():
            return "1234"
        self.app.config[flask_access.CURRENT_USER] = NoAccess()
        with self.app.app_context():
            secret_code()
        mock_abort.assert_called_once_with(403)

    @mock.patch.object(flask, "abort")
    def test_require_admin_has_admin_access(self, mock_abort):
        @flask_access.require("admin")
        def secret_code():
            return "1234"
        self.app.config[flask_access.CURRENT_USER] = AdminAccess()
        with self.app.app_context():
            secret_code()
        mock_abort.assert_not_called()

    @mock.patch.object(flask, "abort")
    def test_require_admin_has_no_access(self, mock_abort):
        @flask_access.require("top-secret")
        def launch_code():
            return "4321"
        self.app.config[flask_access.CURRENT_USER] = AdminAccess()
        with self.app.app_context():
            launch_code()
        mock_abort.assert_called_once_with(403)

    @mock.patch.object(flask, "abort")
    def test_has_access_args_and_kwargs(self, mock_abort):
        @flask_access.require("Alpha", "Bravo", c="Charlie", d="Delta")
        def secret_code():
            return "1234"
        self.app.config[flask_access.CURRENT_USER] = ArgsAndKwargsAccess()
        with self.app.app_context():
            secret_code()
        mock_abort.assert_not_called()

    @mock.patch.object(flask, "abort")
    def test_has_access_args_and_kwargs_failure(self, mock_abort):
        @flask_access.require("Alpha", "Bravo")
        def secret_code():
            return "1234"
        self.app.config[flask_access.CURRENT_USER] = ArgsAndKwargsAccess()
        with self.app.app_context():
            secret_code()
        mock_abort.assert_called_once_with(403)

    @mock.patch.object(flask, "abort")
    def test_has_access_returns_truthy_value(self, mock_abort):
        @flask_access.require("secret-code")
        def secret_code():
            return "1234"
        self.app.config[flask_access.CURRENT_USER] = TruthyAccess()
        with self.app.app_context():
            secret_code()
        mock_abort.assert_called_once_with(403)
