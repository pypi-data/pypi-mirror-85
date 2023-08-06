from setuptools import setup

setup(
    name="safe-commit",
    author="Crawford Collins",
    description="A pre-commit hook for stopping you from committing to the main branch.",
    version="1.0.1",
    packages=["src"],
    install_requires=["gitpython"],
    entry_points={"console_scripts": ["safe-commit=src.main:main"]},
    python_requires=">=3.8",
)
