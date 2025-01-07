from fetch_from_scholar import fetch_publications
from save_to_file import detect_if_publication_is_missing

if __name__ == "__main__":
    simongravelle_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl"  # Replace accordingly
    publications = fetch_publications(simongravelle_url)
    print("Publication fetched")
    detect_if_publication_is_missing(publications)
    print("Terminated")