from setuptools import setup, find_packages

DESCRIPTION = '北理工校园网登录命令行工具.'
AUTHOR = 'Fang Li'
EMAIL = 'fangli-li@qq.com'
REQUIRES_PYTHON = '>=3.6.0'
URL = 'https://github.com/fangli-li/bit-srun-cli'

setup(
    name='srun-bit',
    version='0.1',
    packages=find_packages(),
    description=DESCRIPTION,
    include_package_data=True,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=REQUIRES_PYTHON,
    install_requires=[
        'Click',
        'Requests',
    ],
    entry_points='''
        [console_scripts]
        srun-bit=cli.cli:cli
    ''',
)