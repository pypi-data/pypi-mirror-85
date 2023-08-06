from setuptools import setup

def readme():
      with open('README.md') as f:
            README = f.read()
      return README
setup(name="TOPSIS_Dipesh_101803686",
      version="0.1",
      author="Dipesh Jindal",
      packages=["topsis_dipesh_jindal_101803686"],
      description='Package for calculating Topsis Score',
      long_description=readme(),
      long_description_content_type="text/markdown",
      license="MIT",
      include_package_data=True,
      install_requires=['pandas'],
      classifiers=[
        "Programming Language :: Python :: 3    ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3')
