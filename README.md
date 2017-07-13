# SED-ML Website 
This repository contains the SED-ML webpage.

This website is hosted at:  
https://sed-ml.github.io/  
http://www.sed-ml.org/

## Static Site Creator
The webpage is created via a static site creator written in python.

### Setup
To be able to run the site creator you should create a python virtual environment and install
the necessary dependencies.
```
cd site_creator
mkvirtualenv sedml-site
(sedml-site) pip install -r requirements.txt
```

### Update content
To update the web pages change the information in the respective templates in
```
./templates/
```
and update the static HTML via
```
(sedml-site) cd site_creator
(sedml-site) python ./create_static_html.py
```    
