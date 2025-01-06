from scholarly import scholarly
import os


def fetch_publications(profile_url):
    """
    Fetch all publications from a Google Scholar profile.

    Args:
        profile_url (str): Google Scholar profile URL.

    Returns:
        list: A list of dictionaries containing publication details.
    """
    try:
        # Extract the user ID from the URL
        user_id = profile_url.split("user=")[1].split("&")[0]

        # Search for the profile
        search_query = scholarly.search_author_id(user_id)
        profile = scholarly.fill(search_query)

        # Collect publications
        publications = []
        for pub in profile.get('publications', []):
            pub_details = scholarly.fill(pub)
            year = pub_details.get('bib', {}).get('pub_year', 'N/A')

            # Debugging missing years
            if year == 'N/A':
                print(f"Missing year for publication: {pub_details.get('bib', {}).get('title', 'Unknown Title')}")
            
            publications.append({
                'title': pub_details.get('bib', {}).get('title', 'N/A'),
                'author': pub_details.get('bib', {}).get('author', 'N/A'),
                'journal': pub_details.get('bib', {}).get('journal', 'N/A'),
                'year': year,
                'citation_count': pub_details.get('num_citations', 0),
                'url': pub_details.get('eprint_url', 'N/A'),
                'abstract': pub_details.get('bib', {}).get('abstract', 'N/A'),
                'publication': pub_details.get('bib', {}).get('journal', 'N/A'),
                'date': year
            })
        return publications

    except Exception as e:
        print(f"Error fetching publications: {e}")
        return []
