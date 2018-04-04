# localflaskhighlights


###A flask app that automates the following work tasks:
- Using Beautiful Soup, finds title, author, citation, and image information for journal articles.
- Creates HTML templates using scraped information for homepage slideshows, and virtual issues.
- Downloads TOC images according to user input, example s1 for scheme 1 or f3 for figure 3
- Transforms CSVs of journal information into virtual issues.
- Transforms CSVs of podcast information into a javascript media-player.

##Install and run

1. Download ZIP file and extract it

2. While inside of the project folder in terminal, enter the virtual environment by typing `source venv/bin/activate`

3. Install the requirements `pip install -r requirements.txt` and run the program `python run.py`

4. Type `sudo mongod` in a new terminal window to start the database

5. Browse to localhost:8000 to access the web app.
