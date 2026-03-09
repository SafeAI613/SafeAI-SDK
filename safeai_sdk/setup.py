from setuptools import setup, find_packages

setup(
    name="safeai-sdk",
    version="0.1.0",
    description="SafeAI filtering SDK",
    packages=find_packages(),
    install_requires=[
        "requests",
        "httpx"
    ],
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)


