from setuptools import setup
import cyrating

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='cyrating',
    version=cyrating.__version__,
    description="Python wrapper for https://www.cyrating.com.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Cyrating',
    author_email='tech@cyrating.com',
    packages=[
        'cyrating'
    ],
    url="",
    license="MIT",
    zip_safe=False,
    keywords='cyrating',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent'
    ],
    install_requires=open('requirements.txt').readlines(),
    test_suite='tests',
)
