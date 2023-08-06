import setuptools

setuptools.setup(
    name="eilib",
    version="0.0.1",
    author="Yury Kotov",
    author_email="koteyur@gmail.com",
    description="Library to work with Evil Islands binary formats",
    url="https://github.com/koteyur/eilib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
