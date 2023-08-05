import setuptools


setuptools.setup(
    name="xlog",
    version="0.0.3",
    description="Xbiome pipeline log frame",
    long_description_content_type="text/markdown",
    author="xbiome-it",
    author_email="wangxi@xbiome.com",
    url="https://github.com/xbiome-it/xlog",
    packages=setuptools.find_packages(),
    keywords=["logger", "logging", "logger", "log","Xbiome"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "loguru>=0.5.3"
    ],
    python_requires=">=3.5",
)