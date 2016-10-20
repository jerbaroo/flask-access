import flask
import flask_access
import mock
import unittest


class _AbortTest(unittest.TestCase):

    @mock.patch.object(flask, "abort")
    def testDefault(self, mock_abort):
        app = flask.Flask(__name__)
        with app.app_context():
            flask_access._abort()
            mock_abort.assert_called_once_with(403)

    def testCustom(self):
        app = flask.Flask(__name__)
        custom_fn = mock.Mock()
        app.config[flask_access.ABORT_FN] = custom_fn
        with app.app_context():
            flask_access._abort()
            custom_fn.assert_called_once_with()


class _CurrentUserTest(unittest.TestCase):

    def testAttribute(self):
        app = flask.Flask(__name__)
        user = object()
        app.config[flask_access.CURRENT_USER] = user
        with app.app_context():
            self.assertEqual(user, flask_access._current_user())

    def testFunction(self):
        app = flask.Flask(__name__)
        user = object()
        user_fn = lambda: user
        app.config[flask_access.CURRENT_USER] = user_fn
        with app.app_context():
            self.assertEqual(user, flask_access._current_user())


if __name__ == "__main__":
    unittest.main()
