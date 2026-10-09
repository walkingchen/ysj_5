import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from flask import Flask

from blueprints.auth import bp_auth, load_user, login_manager
from extensions import db
from models import PasswordResetToken, User
from passwords import hash_password, verify_password


class PasswordResetTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY='test-secret',
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            FRONTEND_URL='https://example.test',
        )
        db.init_app(self.app)
        login_manager.init_app(self.app)
        self.app.register_blueprint(bp_auth)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        db.session.add(User(id=1, email='member@example.test', nickname='member',
                            password=hash_password('original password'), session_version=0))
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def post(self, path, payload):
        return json.loads(self.client.post(path, json=payload).data)

    @patch('blueprints.auth.send_email_async')
    def test_reset_lifecycle_and_session_invalidation(self, send_mail):
        response = self.post('/api/auth/password-reset/request', {'email': 'member@example.test'})
        self.assertEqual(response['result_code'], 2000)
        self.assertEqual(send_mail.call_count, 1)
        body = send_mail.call_args[0][2]
        url = body.split('https://example.test/#/reset-password?token=')[1].splitlines()[0]
        token = url.strip()
        self.assertNotEqual(PasswordResetToken.query.first().token_hash, token)
        self.assertIsNotNone(load_user('1'))

        response = self.post('/api/auth/password-reset/confirm',
                             {'token': token, 'password': 'new secure password'})
        self.assertEqual(response['result_code'], 2000)
        user = User.query.get(1)
        self.assertTrue(verify_password(user.password, 'new secure password'))
        self.assertFalse(verify_password(user.password, 'original password'))
        self.assertIsNone(load_user('1'))
        self.assertIsNotNone(load_user('1:1'))
        self.assertEqual(self.post('/api/auth/login',
                                   {'email': 'member@example.test', 'password': 'original password'})['result_code'], 4000)
        self.assertEqual(self.post('/api/auth/login',
                                   {'email': 'member@example.test', 'password': 'new secure password'})['result_code'], 2010)
        self.assertEqual(self.post('/api/auth/password-reset/confirm',
                                   {'token': token, 'password': 'another password'})['result_code'], 4000)

    @patch('blueprints.auth.send_email_async')
    def test_unknown_email_is_generic_and_known_email_is_rate_limited(self, send_mail):
        unknown = self.post('/api/auth/password-reset/request', {'email': 'unknown@example.test'})
        known = self.post('/api/auth/password-reset/request', {'email': 'member@example.test'})
        self.assertEqual(unknown['result_msg'], known['result_msg'])
        self.post('/api/auth/password-reset/request', {'email': 'member@example.test'})
        self.assertEqual(send_mail.call_count, 1)

    @patch('blueprints.auth.send_email_async')
    def test_expired_token_and_short_password(self, send_mail):
        self.post('/api/auth/password-reset/request', {'email': 'member@example.test'})
        token = send_mail.call_args[0][2].split('token=')[1].splitlines()[0].strip()
        self.assertEqual(self.post('/api/auth/password-reset/confirm',
                                   {'token': token, 'password': 'short'})['result_code'], 4000)
        reset_token = PasswordResetToken.query.first()
        reset_token.expires_at = datetime.utcnow() - timedelta(seconds=1)
        db.session.commit()
        self.assertEqual(self.post('/api/auth/password-reset/confirm',
                                   {'token': token, 'password': 'long enough password'})['result_code'], 4000)


if __name__ == '__main__':
    unittest.main()
