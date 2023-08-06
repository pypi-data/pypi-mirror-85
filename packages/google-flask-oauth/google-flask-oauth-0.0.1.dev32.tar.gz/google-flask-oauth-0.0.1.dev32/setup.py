import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="google-flask-oauth",
  version="0.0.1-dev32",
  author="Michael Madison",
  author_email="cadetstar@hotmail.com",
  description="Pseudo-application for simplifying the OAuth flow with Google",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/cadetstar/google-flask-oauth",
  packages=setuptools.find_packages(),
  install_requires=[
    'Flask==1.1.2',
    'google-api-python-client==1.11.0',
    'google_auth_oauthlib==0.4.1'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)