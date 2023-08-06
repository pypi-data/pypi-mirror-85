import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="techsig", # Replace with your own username
    version="1.0.5",
    author="Aayush Talekar Saloni Jaitly",
    author_email="aayush.talekar57@nmims.edu.in",
    description="Technical charts with signals",
    py_modules=['techsig'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
           'yfinance', 'ta', 'numpy', 'pandas', 'plotly'
      ],
    python_requires='>=3.6',
)
