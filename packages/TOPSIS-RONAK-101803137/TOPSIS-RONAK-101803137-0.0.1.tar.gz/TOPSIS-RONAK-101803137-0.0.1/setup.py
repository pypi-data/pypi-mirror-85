from setuptools import setup
with open("README.txt", 'r') as fh:
    long_description = fh.read()
setup(name='TOPSIS-RONAK-101803137',
      version='0.0.1',
      description='This package takes a .csv file as input and calculate topsis score of all entries and rank them according to the topsis score',
      author='Ronak',
      author_email='ronaka2328@gmail.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type="text/plain",
      keywords=['topsis', 'rank', 'data science'],
      packages=['TOPSIS-RONAK-101803137'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
