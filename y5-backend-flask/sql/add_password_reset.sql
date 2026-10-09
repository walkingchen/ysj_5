-- Apply before deploying the password-reset application code.
ALTER TABLE tb_user
    ADD COLUMN session_version INT NOT NULL DEFAULT 0;

CREATE TABLE tb_password_reset_token (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    email_hash CHAR(64) NOT NULL,
    token_hash CHAR(64) NOT NULL,
    created_at DATETIME NOT NULL,
    expires_at DATETIME NOT NULL,
    used_at DATETIME NULL,
    UNIQUE KEY uq_password_reset_token_hash (token_hash),
    KEY ix_password_reset_email_created (email_hash, created_at),
    KEY ix_password_reset_expires (expires_at),
    KEY ix_password_reset_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
