import unittest

from sqlalchemy import create_engine, text

from migrate_passwords import migrate
from passwords import hash_password, is_password_hash, verify_password


class PasswordMigrationTest(unittest.TestCase):
    def test_hash_and_legacy_passwords(self):
        hashed = hash_password(' with spaces ')
        self.assertLessEqual(len(hashed), 128)
        self.assertTrue(is_password_hash(hashed))
        self.assertTrue(verify_password(hashed, ' with spaces '))
        self.assertFalse(verify_password(hashed, 'with spaces'))
        self.assertFalse(verify_password('old password', 'old password'))
        self.assertFalse(verify_password('old password', 'wrong'))
        self.assertTrue(verify_password(hash_password('旧密码'), '旧密码'))

    def test_migration_is_resumable_and_preserves_existing_hashes(self):
        engine = create_engine('sqlite:///:memory:')
        existing_hash = hash_password('already hashed')
        with engine.begin() as connection:
            connection.execute(text('CREATE TABLE tb_user (id INTEGER PRIMARY KEY, password VARCHAR(128))'))
            connection.execute(text('INSERT INTO tb_user (id, password) VALUES (1, :password)'),
                               {'password': 'legacy'})
            connection.execute(text('INSERT INTO tb_user (id, password) VALUES (2, :password)'),
                               {'password': existing_hash})
            connection.execute(text('INSERT INTO tb_user (id, password) VALUES (3, NULL)'))
        self.assertEqual(migrate(engine, batch_size=1), (1, 0, 0))
        self.assertEqual(migrate(engine, apply=True, batch_size=1), (1, 1, 0))
        self.assertEqual(migrate(engine, apply=True, batch_size=1), (0, 0, 0))
        with engine.connect() as connection:
            rows = connection.execute(text('SELECT password FROM tb_user ORDER BY id')).fetchall()
        self.assertTrue(verify_password(rows[0][0], 'legacy'))
        self.assertEqual(rows[1][0], existing_hash)
        self.assertIsNone(rows[2][0])
        engine.dispose()


if __name__ == '__main__':
    unittest.main()
