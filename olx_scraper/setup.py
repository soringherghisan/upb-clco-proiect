# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages
import pkgutil

# print(pkgutil.get_data("olx_scraper", "my_uas.txt"))

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = olx_scraper.settings']},
    # package_data = {'olx_scraper': ['my_uas.txt']},
    # include_package_data = True,
)
