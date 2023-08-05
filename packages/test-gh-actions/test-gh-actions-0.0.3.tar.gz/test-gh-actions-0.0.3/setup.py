from setuptools import setup

setup(
    name='test-gh-actions',
    packages=['test-gh-actions'],
    version=open('VERSION', 'r').read(),
    description='test-gh-actions',
    license='WTFPL',
    python_requires='>=3.5',
    install_requires=[],
    data_files=[('', ['VERSION'])],
    scripts=[],
)
