from text_importer.importers.rero.classes import ReroNewspaperIssue
from text_importer.importers.rero.detect import detect_issues as rero_detect_issues, select_issues as rero_select_issues
from text_importer.importers import generic_importer

if __name__ == '__main__':
    generic_importer.main(ReroNewspaperIssue, rero_detect_issues, rero_select_issues)
