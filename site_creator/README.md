# Static Site Creator

# Setup
```
cd site_creator
mkvirtualenv sedml-site
(sedml-site) pip install -r requirements.txt
(sedml-site) python create_static_html.py
```

# Update content
To update the web pages change the information in the respective 
templates in
```
./templates/
```
and update the HTML via
```
python ./create_static_html.py
```