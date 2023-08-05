from setuptools import setup

setup(
    name="uofg-timetable",
    version="0.2",
    py_modules=['extractor'],
    license="MIT",
    author="Swetank Poddar",
    author_email="hello@swetankpoddar.me",
    url="https://github.com/SwetankPoddar/UofG-Timetable-CLI/",
    download_url="https://github.com/SwetankPoddar/UofG-Timetable-CLI/archive/v0.2.tar.gz",
    keywords = ["UofG", "timetable", "University of Glasgow", "Glasgow"],
    install_requires = [
        'Click',
        'requests',
        'pytz'
    ],
    entry_points='''
        [console_scripts]
        timetable=extractor:cli
    ''',
)