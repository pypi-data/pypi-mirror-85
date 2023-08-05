from distutils.core import setup

setup(
  name="capmonster_python",
  packages=["python_capmonster"],
  version="1.1",
  license="MIT",
  description="Unofficial capmonster.cloud library for Python",
  author="Alperen Sert",
  author_email="alperenssrt@gmail.com",
  url="https://github.com/alperensert/python_capmonster",
  download_url="https://github.com/alperensert/python_capmonster/archive/v1.1.tar.gz",
  keywords=["RECAPTCHA", "CAPMONSTER", "RECAPTCHAV2", "RECAPTCHAV3", "IMAGETOTEXT", "CAPTCHA", "FUNCAPTCHA"],
  install_requires=["requests"],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
