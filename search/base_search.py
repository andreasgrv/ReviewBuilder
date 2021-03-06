import re
from db.data import Paper

MAX_RESULTS = 100


class Searcher:
    def __init__(self, paperstore):
        self.paperstore = paperstore

    def search(self, query, min_year=None, max_year=None, max_results=MAX_RESULTS):
        pass


class SearchResult(Paper):
    def __init__(self, index, bib, source, extra_data):
        super().__init__(bib, extra_data)
        self.index = index
        self.source = source
        self.paper = None

    def __getitem__(self, item):
        return self.extra_data.get(item, self.bib.get(item))

    def __repr__(self):
        return f"<#%d: %s - %s - %s> \n %s" % (
            self.index, self.bib.get("title", ""),
            self.bib.get("author", ""),
            self.bib.get("year", ""), str(self.bib))


def getSearchResultsFromBib(bib_entries, max_results=100000000):
    results = []
    for index, bib in enumerate(bib_entries[:max_results]):
        res = SearchResult(index, bib, 'bibfile', {})
        if bib.get('note'):
            match = re.search('(\d+)\scites:\s.+?scholar\?cites\=(\d+)', bib['note'])
            if match:
                res.source = 'scholar'
                res.extra_data['scholarid'] = match.group(2)
                res.extra_data['citedby'] = match.group(1)
        results.append(res)

    return results
