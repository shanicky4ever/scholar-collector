from utilities import fetch_publications, detect_missing_publications

simongravelle_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl"  # Replace accordingly
path = "publications/"

publications = fetch_publications(simongravelle_url)
print("Publication fetched")

detect_missing_publications(publications, path)
print("Terminated")