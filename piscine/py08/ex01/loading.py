"""
Exercise 01 – Loading Programs

This program demonstrates:

1. Dependency checking using importlib
2. Difference between pip and Poetry dependency setups
3. Basic data analysis using pandas and numpy
4. Visualization using matplotlib

Output:
    matrix_analysis.png
"""
import importlib
from importlib.util import find_spec
import sys
import os
from typing import List, Tuple

REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib"]
OPTIONAL_PACKAGES = ["requests"]


def is_installed(package_name: str) -> bool:
    return find_spec(package_name) is not None


def get_version(package_name: str) -> str:
    """Return the installed version of a package, or 'unknown'. """
    module = importlib.import_module(package_name)
    return getattr(module, "__version__", "unknown")


def detect_dependency_files() -> str:
    """
    Detect dependency configuration files in the project.
    """

    if os.path.exists("pyproject.toml"):
        return "Poetry configuration detected (pyproject.toml)"
    if os.path.exists("requirements.txt"):
        return "pip configuration detected (requirements.txt)"
    return "No dependency configuration file detected"


def check_dependencies() -> Tuple[bool, List[str]]:
    """
    Check required and optional dependencies.
    Check required packages and optional packages.
    """
    all_required = True
    installed_optionals: List[str] = []
    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    #  check required packages
    for pkg in REQUIRED_PACKAGES:
        if is_installed(pkg):
            version = get_version(pkg)
            print(f"[OK] {pkg} ({version}) - ready")
        else:
            print(f"[MISSING] {pkg} - required")
            all_required = False

    # check optional packages
    for pkg in OPTIONAL_PACKAGES:
        if is_installed(pkg):
            version = get_version(pkg)
            print(f"[OK] {pkg} ({version}) - optional")
            installed_optionals.append(pkg)
        else:
            print(f"[INFO] {pkg} - optional and not installed")
    return all_required, installed_optionals


# installation instructions
def print_install_help() -> None:
    """Print installation instructions. """
    print()
    print("Missing required dependencies.")
    print("Install with pip:")
    print("  pip install -r requirements.txt")

    print()
    print("Install with Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


# data analysis section
def analyze_data() -> None:
    """Generate Matrix data and create visualization. """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    print()
    print("Analyzing Matrix data...")
    data = np.array([5, 8, 3, 10, 7, 6, 9, 4, 11, 2])
    df = pd.DataFrame({"signal": data})
    print("DataFrame preview:")
    print(df)

    print(f"Processing {len(df)} data points...")
    print("Generating visualization...")

    plt.plot(df.index, df["signal"])
    plt.title("Matrix Signal")
    plt.xlabel("Index")
    plt.ylabel("Signal")
    plt.savefig("matrix_analysis.png")
    print()

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")
    plt.close()


def main() -> None:
    """Main program execution."""

    print(f"Dependency setup: {detect_dependency_files()}")
    print()
    required_ok, _ = check_dependencies()

    if not required_ok:
        print_install_help()
        sys.exit(1)

    try:
        analyze_data()
    except Exception as exc:
        print(f"\nERROR during analysis: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# [Testing]
# python3 -m venv venv1
# source venv02/bin/activate
# $> python3 loading.py
# $> pip install -r requirements.txt
# $ python3 loading.py
#
# python3 -m venv venv2
# source venv2/bin/activate
# $> python3 loading.py
# $> poetry install
# $ poetry run python loading.py
# [the difference between pip and poetry]
# pip: manage packages
# poetry: project management (including auto venv)
# 1.  sys.path 是 Python 在执行 import 时搜索模块的目录列表。
# 顺序由 Python 启动时决定，主要来源是：
# 当前脚本目录
# PYTHONPATH
# Python标准库
# site-packages
# Python会按顺序逐个目录查找模块
# 2. 启动程序
#  ↓
# 检测项目依赖文件
#  ↓
# 检查 pandas / numpy / matplotlib
#  ↓
# 如果缺失 → 提示安装
#  ↓
# 如果存在 → 生成数据
#  ↓
# 用 pandas 处理
#  ↓
# 用 matplotlib 画图
#  ↓
# 保存 matrix_analysis.png
# 3. pandas 里最常见的数据结构就是 DataFrame。
# #你可以把它理解成：表格像 Excel 表、数据库表。
#      signal
# 0    0.496714
# 1   -0.138264
# 2    0.647689
# 3    1.523030
# 4   -0.234153
# ...
# 左边是行号（index），右边是列 signal
