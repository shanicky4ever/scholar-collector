from save_to_file import save_to_file
from fetch_from_scholar import fetch_publications

if __name__ == "__main__":
    simongravelle_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl"  # Replace accordingly
    publications = fetch_publications(simongravelle_url)
    
    # Debug: Check for missing years
    for pub in publications:
        if pub['year'] == '2024':
            print(f"Found 2024 publication: {pub['title']}")
    
    print("Publication fetched")
    save_to_file(publications)
