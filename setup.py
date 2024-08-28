from setuptools import setup, find_packages


setup(
    name="rrd_view",
    version="1.0",
    description='Django server to view RRD charts from voltage logger',
    author='Tom Pavel',
    author_email='pavel@alum.mit.edu',
    packages=find_packages(),
    py_modules=["manage"],
    #scripts=["manage.py"],
    data_files=[
        ('rrd_view', ['init-data.json', 'test_data.json']),
    ],
    # package_data={
    #     '': ['*.html', '*.css', '*.png']
    # },
    package_data={
        '': ['*/*/*.html', 'templates/*/*.css', 'static/favicon.png']
    },
    install_requires=['django >= 4.0', 'rrdtool'],

    # This would catch .json file if they were under the pkgs
    #include_package_data=True,

    # Use this when pkgs are under a src tree:
    #package_data={"": ["src"]},
)
