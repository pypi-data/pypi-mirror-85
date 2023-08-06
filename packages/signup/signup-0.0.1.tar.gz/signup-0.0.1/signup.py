import setuptools

with open("signup.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signup",
    version="0.0.1",
    author="LoveNishimiyaShouko",
    author_email="LoveNishimiyaShouko@LoveNishimiyaShouko.LoveNishimiyaShouko",
    description="Auto sign up.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LoveNishimiyaShouko/signup",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="auto,sign up,auto sign up",
    project_urls={
        "Documentation": "https://github.com/LoveNishimiyaShouko/signup/tree/main/docs",
        "Source": "https://github.com/LoveNishimiyaShouko/signup/tree/main/code"
    },
    packages=setuptools.find_packages(include=['signup']),
    install_requires=["requests"],
    python_requires='>=3',
    package_data={
        'signup_log': ['signup_log.txt'],
        'signup_error': ['signup_error.txt']
    },
    entry_points={
        'console_scripts': [
            'signup=signup:main',
        ],
    },
)
