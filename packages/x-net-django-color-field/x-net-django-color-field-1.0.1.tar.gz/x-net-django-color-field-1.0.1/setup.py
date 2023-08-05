from setuptools import (
    find_packages,
    setup,
)

import x_net_django_color_field

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version=x_net_django_color_field.__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x-net-services/x-net-django-color-field",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "Django>=2.2.17",
    ],
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
