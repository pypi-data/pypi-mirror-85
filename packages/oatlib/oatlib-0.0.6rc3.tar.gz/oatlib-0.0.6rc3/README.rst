# OAT (Observation Analysis Tool)

A Python library (oatlib) to manage sensor data in Python.
It provides objects and methods to manipulate 
obeservation time series. It support data loading, export and saving
on different format (CSV, sqlite, istSOS).

- lib documentation: https://ist-supsi.gitlab.io/OAT


# Create pipy package
---------------------
python setup.py sdist bdist_wheel
twine upload dist/*

# update library documentation
-------------------------------
pdoc3 --force --html -o html_doc  oatlib