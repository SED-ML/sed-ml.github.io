# SED-ML Website 
This repository contains the SED-ML website:
- http://www.sed-ml.org/
- https://sed-ml.github.io/

## Static Site Creator
The website is created via a static site creator written in Python.

### Setup
To run the site creator, install Python 3 and the necessary dependencies for the site creator.
```
cd site_creator
pip install -r requirements.txt
```

### Update content
Updates should be performed in a separate branch and merged via a pull request to `master` branch. 

First, cloning the repository via
```
git clone https://github.com/SED-ML/sed-ml.github.io.git
cd sed-ml.github.io
```

Second, checkout a branch for the fix or new feature via
```
git checkout -b <name>
```

Third, to update the web pages, change the information in their respective templates and data files in
```
./site_creator/templates/
```

## Compile the static website
Run
```
cd site_creator
python create_static_html.py
```   

## Deploying updates
1. Commit your changes to the templates and data files (`git commit ...`). It is not necessary to commit the static generated HTML files.
2. Push these changes (to a branch other than `master`) (`git push`).
3. A GitHub action will perform a few automated actions:
   - Validate the example COMBINE archives.
   - Bundle the example COMBINE archives into a zip archive.
   - Compile the static HTML files.
   - Commit and push the static HTML files and bundled examples to the repository.
4. Open a pull request to merge your branch into `master` .
5. Assign review of the pull request to another SED-ML editor.
6. Another editor will review and merge the pull request.
7. The updated site will be deployed once its merged into the `master` branch.
