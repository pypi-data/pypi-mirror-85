from setuptools import setup, find_packages

setup(
    name='iTesting',
    version='0.5',
    description='This is a demo framework',
    author='kevin.cai',
    author_email='testertalk@outlook.com',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'pytest',
        'pyyaml'
    ],
    packages=find_packages(),
    license='MIT',
    url='https://www.helloqa.com',
    entry_points={
        'console_scripts': [
            'iTesting = iTesting.main:main'
        ]
    }
)
