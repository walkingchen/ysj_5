"""Migrate legacy plaintext passwords without exposing them in output.

Run from y5-backend-flask with its virtualenv Python. Defaults to a read-only
count; pass --apply only after all app workers have the compatible login code.
The migration is resumable and uses conditional updates to avoid overwriting
a password changed by a concurrent login or registration.
"""

import argparse
import os

from sqlalchemy import create_engine, text

from passwords import hash_password, is_password_hash


def migrate(engine, apply=False, batch_size=100):
    last_id = 0
    pending = 0
    migrated = 0
    skipped = 0
    while True:
        with engine.connect() as connection:
            rows = connection.execute(
                text('SELECT id, password FROM tb_user WHERE id > :last_id '
                     'ORDER BY id LIMIT :batch_size'),
                {'last_id': last_id, 'batch_size': batch_size},
            ).fetchall()
        if not rows:
            break
        last_id = rows[-1][0]
        legacy = [(user_id, password) for user_id, password in rows
                  if password is not None and not is_password_hash(password)]
        pending += len(legacy)
        if apply:
            for user_id, password in legacy:
                new_hash = hash_password(password)
                with engine.begin() as connection:
                    result = connection.execute(
                        text('UPDATE tb_user SET password = :new_password '
                             'WHERE id = :user_id AND password = :old_password'),
                        {'new_password': new_hash, 'user_id': user_id,
                         'old_password': password},
                    )
                if result.rowcount == 1:
                    migrated += 1
                else:
                    skipped += 1
    return pending, migrated, skipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='write password hashes')
    parser.add_argument('--batch-size', type=int, default=100)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error('--batch-size must be positive')

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        from config import SQLALCHEMY_DATABASE_URI
        database_url = SQLALCHEMY_DATABASE_URI
    engine = create_engine(database_url)
    try:
        pending, migrated, skipped = migrate(engine, args.apply, args.batch_size)
    finally:
        engine.dispose()
    if args.apply:
        print('Legacy passwords found: {}; migrated: {}; changed concurrently: {}'.format(
            pending, migrated, skipped))
    else:
        print('Dry run: {} legacy passwords need migration'.format(pending))


if __name__ == '__main__':
    main()
