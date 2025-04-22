"""
安全相关：密码哈希、Token 生成
"""

import hashlib
import secrets


def hash_password(password: str) -> str:
    """SHA-256 哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """验证密码是否匹配"""
    return hash_password(plain) == hashed


def generate_token() -> str:
    """生成安全随机 Token"""
    return secrets.token_urlsafe(32)
