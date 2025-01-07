from utilities import fetch_publications, add_missing_publications

 # Replace accordingly
simongravelle_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl" 
path = "publications/"

# Read publication from Google Scholar
publications = fetch_publications(simongravelle_url)
print("\033[35mPublication fetched\033[0m")

add_missing_publications(publications, path)
print("\033[35mAdded missing\033[0m")
