import setuptools


with open("README.md", 'r') as readme_file:
    long_desc = readme_file.read()


setuptools.setup(
    name="basic-web-scraper",
    version="0.13.7",
    author="aziznal",
    author_email="aziznal.dev@gmail.com",
    url="https://github.com/aziznal/basic-web-scraper",
    description="Basic Web Scraper made with selenium and bs4",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["selenium", "bs4", "lxml"],
    python_requires=">=3.7",
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',

        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Scientific/Engineering :: Information Analysis',


    ],
    keywords="webscraper scraper spider"
)