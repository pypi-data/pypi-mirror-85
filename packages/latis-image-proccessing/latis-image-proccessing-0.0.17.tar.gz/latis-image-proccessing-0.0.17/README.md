LATIS image processing utilities for python


## installation

#### Windows
```
pip install latis-gdcm-win
pip install latis-image-proccessing
```
#### Linux
```
sudo apt-get install python3-gdcm
( pip / pip3 ) install latis-image-proccessing
```



### Compiling The Package

```bash
# Build the package 
python setup.py bdist_wheel

# Deploy to pip  
python -m twine upload dist/*
```
