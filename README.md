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


## TODO
* migration to github
    * remove content from sourceforge
    * move issues to new tracker

* webpage
    * update references
    * update tools & libraries section
    * SED-ML examples (archives & simulation)
    * favicon
* website added features
    * SED-ML example archives with link to execute them
    
* updated list of feature request & discussions (set of documents)

* implementation
    * implement the data and plotting
    * tesedml webtools (show case for tellurium support)

* specification
    * read and update the specification

* organise community
    * 2 weekly meetings at recurring time to discuss issues (open for community)
    * stickers & flyers for conferences (community outreach)

* example combine archive with full annotations
    

## Information to add
### ontologies
* Ontologies Used Kinetic Simulation Algorithm Ontology (https://bioportal.bioontology.org/ontologies/KISAO)
    * https://www.ebi.ac.uk/ols/ontologies/kisao
* https://www.ebi.ac.uk/ols/ontologies/teddy
    * Terminology for Description of Dynamics
    
