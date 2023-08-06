from setuptools import setup, find_packages

setup(
    name='dnevnik-mos-ru',
    version="0.0.4 Alpha",
    url='https://github.com/IvanProgramming/dnevnik_mos_ru',
    author='Ivan Vlasov',
    py_modules=find_packages(),
    install_requires=[
        'requests',
    ]
)
