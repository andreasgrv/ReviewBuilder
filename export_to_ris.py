from base.general_utils import loadEntriesAndSetUp

from argparse import ArgumentParser
from db.ris import writeBibToRISFile


def main(conf):
    paperstore, papers_to_add, papers_existing, all_papers = loadEntriesAndSetUp(conf.input, conf.cache)

    if conf.missing_abstract:
        all_bibs = []
        for paper in all_papers:
            if not paper.has_pdf and not paper.has_abstract:
                all_bibs.append(paper.bib)
    elif conf.missing_pdf:
        all_bibs = []
        for paper in all_papers:
            if not paper.has_pdf:
                all_bibs.append(paper.bib)
    else:
        all_bibs = [p.bib for p in all_papers]

    writeBibToRISFile(all_bibs, conf.output)


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Exports a bibliography to RIS (EndNote) for further gathering of PDFs')

    parser.add_argument('-i', '--input', type=str,
                        help='Input Bibtex file with the previously cached search results')
    parser.add_argument('-o', '--output', type=str,
                        help='Output RIS file')
    parser.add_argument('-x', '--missing-pdf', type=bool, default=False,
                        help='Export *only* papers missing a PDF')
    parser.add_argument('-a', '--missing-abstract', type=bool, default=False,
                        help='Export *only* papers that are also missing an abstract')
    parser.add_argument('-c', '--cache', type=bool, default=True,
                        help='Use local cache for results')

    conf = parser.parse_args()

    main(conf)
