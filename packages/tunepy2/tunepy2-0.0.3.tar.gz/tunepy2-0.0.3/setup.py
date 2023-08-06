import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="tunepy2",
    version="0.0.3",
    author="Ethan Fortner",
    author_email='ethan.fortner@icloud.com',
    description="A package containing a set of bitstring optimizers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/efortner/tunepy",
    packages=setuptools.find_packages(exclude='test'),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'scikit-learn>=0.23.2',
        'numpy>=1.19.2',
    ]
)
