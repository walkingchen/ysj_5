"""Password hashing shared by authentication and the one-time migration."""

from hmac import compare_digest

from werkzeug.security import check_password_hash, generate_password_hash


HASH_PREFIX = 'pbkdf2:sha256:600000$'


def is_password_hash(value):
    return isinstance(value, str) and value.startswith(HASH_PREFIX)


def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256:600000', salt_length=16)


def verify_password(stored, candidate):
    if not isinstance(stored, str) or not isinstance(candidate, str):
        return False
    if is_password_hash(stored):
        return check_password_hash(stored, candidate)
    # Transitional support for passwords written before the migration.
    return compare_digest(stored.encode('utf-8'), candidate.encode('utf-8'))
