# localflaskhighlights


### A flask app that automates the following work tasks:
- Using Selenium, PhantomJS, and Beautiful Soup, finds title, author, citation, and image information for journal articles.
- Creates HTML templates using scraped information for homepage slideshows, and virtual issues.
- Transforms CSVs of journal information into virtual issues.
- Transforms CSVs of podcast information into a javascript media-player.

## Install and run

1. Download ZIP file and extract it

2. While inside of the project folder in terminal:
    - Create a virtual environment. `virtualenv venv`
    - Enter the virtual environment by typing `source venv/bin/activate`

3. Install the requirements `pip install -r requirements.txt`

4. To use the development branch, type `git checkout dev`

4. Run the program `python run.py`

5.  Browse to localhost:8000 to access the web app.
