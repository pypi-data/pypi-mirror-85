import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-facebook-scraper",
    version="0.2.19",
    include_package_data=True,
    author="Madhouse Inc.",
    author_email="evoex123@gmail.com",
    description="Facebook-scraper python client package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/evoup/py-facebook-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
