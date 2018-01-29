import pdb
# debugging
# import pdb #use pdb.set_trace() to break


class Article(object):
    def __init__(self,
        title = None,
        authors = None,
        year = None,
        volume = None,
        journal = None,
        issue = None,
        toc_gif = None,
        fig_urls = None
        ):
        #set everything to self. whatever
        self.title = title
        self.authors = authors
        self.year = year
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.toc_gif = toc_gif
        self.fig_urls = fig_urls

    # @staticmethod
    # def choose_alt_figure(fig_id):
    #     alt_figure = fig_urls[fig_id]
    #     return alt_figure


class ArticleParser(object):
    """
    All of the information scraped from an Article on ACS Publications

    Attributes:
        title: The title as a string
        authors: The list of authors as a string
        year: The citation year as a string
        volume: The volume number as a string
        issue: The issue number as a string
        toc_gif: The toc GIF image URL as a string
        other_gif: a string that is part of a URL
    """

    # sets soup as instance variable
    def __init__(self, soup):
        self.soup = soup

    # parse the soup and return an article
    def parse_article(self):
        # create an article instance using named parameters
        article = Article(
            title = self.get_title(),
            authors = self.get_authors(),
            year = self.get_citation_year(),
            journal = self.get_citation_journal(),
            volume = self.get_citation_volume(),
            issue = self.get_citation_issue(),
            toc_gif = self.get_toc_gif(),
            fig_urls = self.get_all_figs(),
        )
        return article

    def get_title(self):
        title = self.soup.find('span', {'class': 'hlFld-Title'})
        # title = title.text.encode('utf-8')
        title = title.decode_contents(formatter="none").encode('utf-8')
        return title

    def get_authors(self):
        authors_soup = self.soup.select('#authors > span.hlFld-ContribAuthor')
        author_names = []
        for author in authors_soup:
            name_tag = author.find('span', {'class': 'hlFld-ContribAuthor'})

            # skip hlFld-ContribAuthor spans that contain no names
            # continue the program if name_tag is empty.
            if not name_tag or not name_tag.contents:
                continue

            # find the first item in the scraped author tag, their Name.
            # (symbols are after the name in the array)
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

    def get_citation_journal(self):
        citation_journal = self.soup.select('#citation > cite')[0].text
        return citation_journal

    def get_citation_year(self):
        try:
            citation_year = self.soup.find('span', {'class': 'citation_year'})
            citation_year = citation_year.text.encode('utf-8')
            return citation_year
        except:
            try:
                # for old format articles
                citation_year = self.soup.select('#citation')[0].text
                return citation_year
            except:
                # for Articles ASAP
                return citation_year == ''

    def get_citation_volume(self):
        try:
            citation_volume = self.soup.find('span', {'class': 'citation_volume'})
            citation_volume = citation_volume.text.encode('utf-8')
            return citation_volume
        except:
            try:
                citation_volume = self.soup.select('#citation')[1].text
                return citation_volume
            except:
                return citation_volume == ''


    def get_citation_issue(self):
        try:
            issue_info = self.soup.find("span", class_="citation_volume").next_sibling
            issue_info = issue_info.encode("utf-8")
            return issue_info
        except:
            issue_info = ''
            return issue_info

    def get_toc_gif(self):
        try:
            toc_gif = self.soup.select('#abstractBox > .figure > a > img')[0]['src']
            return toc_gif
        except:
            toc_gif = ''
            return toc_gif

    def get_all_figs(self):
        '''Loop through all figures and get the URLs for all images'''
        figures = self.soup.select('.figure')
        fig_urls = {}
        for figure in figures:
            fig_urls[str(figure.get('id'))] = str(figure.find('img')['src'])
        return fig_urls
