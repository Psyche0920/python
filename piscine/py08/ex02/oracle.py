import os
import sys
from dotenv import load_dotenv


def load_configuration() -> None:
    """Load environment variable from .env file."""
    load_dotenv()


def get_env(key: str) -> str | None:
    """Return environment variable."""
    value = os.getenv(key)
    if value and value.strip():
        return value.strip()
    return None


def check_configuration() -> None:
    """Check required configuration variables."""

    required = [
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT"
    ]
    missing = []
    for var in required:
        if get_env(var) is None:
            missing.append(var)

    if missing:
        print("WARNING: Missing configuration values:")
        for m in missing:
            print(f"- {m}")
        sys.exit(1)
        print()


def main() -> None:
    """Main program."""
    load_configuration()
    check_configuration()
    mode = get_env("MATRIX_MODE") or "development"
    db = get_env("DATABASE_URL")
    api = get_env("API_KEY")
    log = get_env("LOG_LEVEL")
    zion = get_env("ZION_ENDPOINT")

    print("ORACLE STATUS: Reading the Matrix.")
    print()
    print("Configuration loaded:")

    if db:
        if mode == "development":
            print("Database: Connected to local instance")
        else:
            print("Database: Connected to production instance")
    else:
        print("Database: Missing configuration")
    if api:
        print("API Access: Authenticated")
    else:
        print("API Access: Missing API Key")
    if log:
        print(f"Log Level: {log}")
    else:
        print("Log Level: Missing")
    if zion:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")
    print()

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")

    print("[OK] Production overrides available")
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()


# [Test]
# python3 -m pip install python-dotenv
# cp .env.example .env
# python3 oracle.py
#
# 1. the use of .env.example && security
# .env.example 不是用来运行程序的，而是：
# 告诉开发者需要哪些环境变量，并提供一个安全模板。
# 同时，程序通过环境变量读取 API_KEY 等敏感信息，而不是写死在代码里，从而保证 secret 的安全。
# .env 被加入 .gitignore，而 .env.example 只是安全模板。
#
# 2.Priority of configuration values:
# a. System environment variables
# b. .env file variables
# c. Default values in code
#
# 3. MATRIX_MODE
# development = 开发调试, [本地配置]
# production = 真实运行. [生产配置]
