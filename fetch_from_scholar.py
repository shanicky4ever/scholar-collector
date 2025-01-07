from scholarly import scholarly
import numpy as np
import time
import os


def fetch_publications(profile_url, verbose = True):
    """Fetch all publications from a Google Scholar profile."""
    try:
        # Extract the user ID from the URL
        user_id = profile_url.split("user=")[1].split("&")[0]
        if verbose:
            print("User ID =", user_id)

        # Search for the profile
        search_query = scholarly.search_author_id(user_id)
        profile = scholarly.fill(search_query)

        # Collect publications
        publications = []
        for pub in profile.get('publications', []):
            pub_details = scholarly.fill(pub)
            year = pub_details.get('bib', {}).get('pub_year', 'N/A')
            title = pub_details.get('bib', {}).get('title', 'N/A')
            journal = pub_details.get('bib', {}).get('journal', 'N/A')

            # Debugging missing years
            if year == 'N/A':
                print(f"Missing year for publication: {pub_details.get('bib', {}).get('title', 'Unknown Title')}")

            publication_data = {
                'title': pub_details.get('bib', {}).get('title', 'N/A'),
                'author': pub_details.get('bib', {}).get('author', 'N/A'),
                'journal': pub_details.get('bib', {}).get('journal', 'N/A'),
                'year': year,
                'citation_count': pub_details.get('num_citations', 0),
                'url': pub_details.get('eprint_url', 'N/A'),
                'abstract': pub_details.get('bib', {}).get('abstract', 'N/A'),
                'publication': pub_details.get('bib', {}).get('journal', 'N/A'),
                'date': year
            }
            if verbose:
                print(f"\033[36m{year}\033[0m {title} \033[36m{journal}\033[0m")

            publications.append(publication_data)
        
        return publications

    except Exception as e:
        print(f"Error fetching publications: {e}")
        return []

if __name__ == "__main__":
    simongravelle_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl"  # Replace accordingly
    ti = time.time()
    publications = fetch_publications(simongravelle_url, verbose = True)
    tf = time.time()
    print("Elapsed time: ", np.round((tf-ti),2), "s")
    print(len(publications), "publications found")