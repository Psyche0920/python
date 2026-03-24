"""
Exercise 0: Entering the Matrix
Detect Python virtual environment and display relevant information.

Strict version:
- Detect venv
- Print Python/environment info
- If no venv: print instructions to create/activate one
- Show difference between global and venv package locations
"""

import os
import site
import sys
from typing import List


def is_virtual_env() -> bool:
    """
    Determine whether the current Python interpreter is running
    inside a virtual environment.

    Detection is based on comparing:
    - sys.base_prefix (system Python)
    - sys.prefix (current environment)
    """

    return sys.prefix != sys.base_prefix


def get_venv_name() -> str:
    """
    Extract the name of the active virtual environment directory.

    Example:
        /path/to/project/ex0/matrix_env -> "matrix_env"
    """

    return os.path.basename(sys.prefix)


def get_package_paths(venv_only: bool = False) -> List[str]:
    """
    Retrieve site-packages directories for the current Python environment.

    -If venv_only is True and we are in a venv,
    keep only paths inside sys.prefix.
    -if site.gesitepackages() is unavailable, fall back to:
    * In venv: construct the typical venv site-packages path
    * outside venv: scan sys.path for directories containing 'site-packages'
    """

    paths: List[str] = []

    try:
        all_paths = site.getsitepackages()
        if venv_only and is_virtual_env():
            paths = [p for p in all_paths if p.startswith(sys.prefix)]
        else:
            paths = all_paths
    except Exception:
        if venv_only and is_virtual_env():
            py_version = (
                f"python{sys.version_info.major}."
                f"{sys.version_info.minor}"
            )
            fallback = os.path.join(
                sys.prefix, "lib", py_version, "site-packages"
            )
            paths = [fallback]
        else:
            paths = [p for p in sys.path
                     if "site-packages" in p and os.path.isdir(p)]
    return paths


def print_venv_instructions() -> None:
    """
    Print copy-paste friendly instructions for creating and activating a venv.
    """
    """
    Print instructions for creating and activating a virtual environment.
    """
    print("To enter the construct, run:")
    print("python3 -m venv matrix_env")
    print("source matrix_env/bin/activate  # On Unix/macOS")
    print("matrix_env\\Scripts\\activate   # On Windows")
    print()
    print("Then run this program again.")


def print_status_report() -> None:
    """
    Print the current Python environment status.
    Output differs inside vs outside a venv
    """

    python_version = (
        f"{sys.version_info.major}."
        f"{sys.version_info.minor}."
        f"{sys.version_info.micro}"
    )
    if not is_virtual_env():
        print()
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Python Version: {python_version}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("Gloabl package installation paths:")
        for path in get_package_paths(venv_only=False):
            print(f" {path}")
        print()
        print_venv_instructions()
        return

    print()
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Python Version: {python_version}")
    print(f"Virtual Environment: {get_venv_name()}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()
    print("Package installation path:")
    for path in get_package_paths(venv_only=True):
        print(f" {path}")


def main() -> None:
    """Program entry point. """
    try:
        print_status_report()
    except Exception as exc:
        print(f"Critical system failure: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


# 1. [sys.executable]：当前正在运行的 Python 解释器的完整路径。它是一个字符串，
# 例如 /usr/bin/python3 或 /home/user/venv/bin/python。
# 通过它可以直接确认你使用的是哪个 Python 解释器（全局的还是虚拟环境内的），这正是题目要求显示的“Current Python”信息。
# [sys.path]：是一个列表，包含了 Python 解释器搜索模块的所有路径（例如当前目录、标准库路径、site-packages 路径等）。
# 它用于确定 import 语句去哪里找模块，而不是标识解释器本身。
# 2. .venv/
# ├── bin/
# │   ├── activate              # 给 sh/bash/zsh 用的激活脚本
# │   ├── activate.csh          # 给 csh 用
# │   ├── activate.fish         # 给 fish shell 用
# │   ├── pip                   # 这个虚拟环境自己的 pip
# │   ├── pip3
# │   ├── python                # 这个虚拟环境自己的 Python 解释器
# │   ├── python3
# │   └── python3.11            # 可能链接到 python
# ├── include/
# │   └── python3.11/           # C 扩展编译时可能用到的头文件
# ├── lib/
# │   └── python3.11/
# │       └── site-packages/    # 第三方库安装位置（最重要）
# │           ├── numpy/
# │           ├── pandas/
# │           ├── matplotlib/
# │           ├── requests/
# │           ├── pip/
# │           ├── setuptools/
# │           └── ...
# ├── pyvenv.cfg                # 虚拟环境配置文件
# └── .gitignore                # 有些工具可能自动生成
# bin/ and Scripts/ same purpose:store executables for the virtual environment.
# bin/ is used on Unix-like systems, while Scripts/ is used on Windows.
# site-packages is where the installed Python libraries live.
# 3. ➜  ex0 ls -l /usr/bin/python3
# lrwxrwxrwx 1 root root 10 Aug  8  2024 /usr/bin/python3 -> python3.10
# 4.packages search sequence:
# 总结一下每个路径的作用：
# 路径	用途
# site-packages	pip 安装的第三方库
# local/dist-packages	本地系统包
# dist-packages	系统 apt 安装的 Python 库 minor-> major
