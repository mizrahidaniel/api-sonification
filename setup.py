from setuptools import setup, find_packages

setup(
    name="apisonify",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "api-sonify=apisonify.cli:main",
        ],
    },
    author="Pixel",
    description="Transform API logs into generative music",
    python_requires=">=3.9",
)
