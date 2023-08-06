import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gnuplot_manager", # Replace with your own username
    version="0.1.1",
    author="Pietro Mandracci",
    author_email="pietro.mandracci.software@gmail.com",
    description="A manager to symplify the use of gnuplot inside python",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/pietromandracci/gnuplot_manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3',
)
