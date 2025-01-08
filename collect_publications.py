from utilities import fetch_publications, add_missing_publications
import sys


def main(path="publications/"):
    # Replace accordingly
    simongravelle_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl"
    
    # Read publication from Google Scholar
    publications = fetch_publications(simongravelle_url)
    print("\033[35mPublication fetched\033[0m")
    
    add_missing_publications(publications, path)
    print("\033[35mAdded missing\033[0m")

if __name__ == "__main__":
    """Allow the path to be passed as an argument when the script is executed directly"""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path ="publications/"
    main(path)