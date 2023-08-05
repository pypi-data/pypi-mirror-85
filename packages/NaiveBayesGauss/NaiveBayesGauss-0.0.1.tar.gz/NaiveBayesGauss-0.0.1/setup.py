from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='NaiveBayesGauss',
    version='0.0.1',
    author="Ilya Novak",
    author_email="ilyanovak@gmail.com",
    description='A custom implementation of the Naive Bayes Gaussian algorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilyanovak/naive-bayes-gauss",
    py_modules=['NaiveBayes'],
    package_dir={'': '..'},
    python_requires='>=3.6',
    classifiers=[
        "Framework :: IPython",
        "Framework :: Jupyter",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization"
    ]
)
