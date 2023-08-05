from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
  name = 'TOPSIS_Atinder_101803176',         # How you named your package folder (MyLib)
  packages = ['TOPSIS_Atinder_101803176'],   # Chose the same as "name"
  description="A Python package for topsis analysis.",
  long_description=readme(),
  long_description_content_type="text/markdown",
  url="",
  author="Atinderpal Kaur",
  author_email="kaur.atinder01@gmail.com",
  license="MIT",
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
  include_package_data=True,
  install_requires=["requests"],
  entry_points={
        "console_scripts": [
            "TOPSIS_Atinder_101803176=TOPSIS_Atinder_101803176.TOPSIS:main",
        ]
   },
)
