class ArticleParser(object):
    """
    All of the information scraped from an Article on ACS Publications

    Attributes:
        title: The title as a string
        authors: The list of authors as a string
        citation_year: The citation year as a string
        citation_volume: The volume number as a string
        citation_issue: The issue number as a string
    """

    def __init__(self, title, year, volume, issue):
        self.title = title
        self.authors = authors_joined
        self.year = citation_year
        self.issue = issue_info

    def get_title(soup):
        title = soup.find('span', {'class': 'hlFld-Title'})
        return title.text.encode('utf-8')

    def get_authors(soup):
        authors_soup = soup.select('#authors > span.hlFld-ContribAuthor')
        author_names = []
        for author in authors_soup:
            name_tag = author.find('span', {'class': 'hlFld-ContribAuthor'})
            authors_tag = name_tag.contents[0]
            author_name = authors_tag.contents
            entire_name_symbols = author.text.strip()
            # check to see if a star is in the entire name,
            # then add the star to the name only
            if '*' in entire_name_symbols:
                author_name = author_name[0] + '*'
            else:
                author_name = author_name[0]
            author_name.encode('utf-8')
            author_names.append(author_name)
        return author_names

    def get_citation_year(soup):
        citation_year = soup.find('span', {'class': 'citation_year'})
        citation_year = citation_year.text.encode('utf-8')
        return citation_year

    def get_citation_volume(soup):
        citation_volume = soup.find('span', {'class': 'citation_volume'})
        citation_volume = citation_volume.text.encode('utf-8')
        return citation_volume

    def get_citation_issue(soup):
        issue_info = soup.find("span", class_="citation_volume").next_sibling
        issue_info = issue_info.encode("utf-8")
        return issue_info
