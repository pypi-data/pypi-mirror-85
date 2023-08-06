from setuptools import setup

with open("README.md", "r", encoding="utf8") as rm:
    readme = rm.read()
    
with open("requirements.txt") as rq:
    requirements = rq.read().split('\n')

setup(
      name="pytholog",
      version="2.4.1", 
      description="Logic Programming in Python",
      #py_modules=["pytholog"],
      #package_dir={"": "src"},
      packages=["pytholog"],
      install_requires=requirements,
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/mnoorfawi/pytholog",
      author="Muhammad N. Fawi",
      author_email="m.noor.fawi@gmail.com",
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
      )
