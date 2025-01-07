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

def detect_missing_publications(publications, path_to_publications, verbose = True):
    """Loop over publications, and check if they are already present in path_to_publications."""
    for publication in publications:

        To_be_ignored = True # ignore some entry

        title = publication["title"]
        year = publication.get('year', 'Unknown')

        # Extract the first author's last name
        authors = publication.get('author', 'unknown')
        if authors.lower() == "unknown" or not authors.strip():
            family_name = "Unknown_Author"
        else:
            first_author = authors.split(' and ')[0].strip() if ' and ' in authors else authors.split(',')[0].strip()
            family_name = first_author.split()[-1] if first_author else "Unknown_Author"
            journal = publication.get('journal', 'Unknown_Journal').replace(' ', '_')

            if journal == "Med_Sci_(Paris)":
                journal = "Med_Sci"

            if journal.lower() in ["n/a", "unknown", ""]:
                journal = "Unknown_Journal"

            folder_name = str(year)+"_"+family_name+"_"+journal

            # Manage exeptions, such as non-journal article, these manuscript, etc.
            # Adapt to your own case
            if "arXiv" in journal:
                To_be_ignored = True
            elif "Nanofluidics: a theoretical and numerical investigation of fluid transport in nanochannels" in title:
                journal = "These"
            elif "Nanofluidics: a pedagogical introduction" in title:
                journal = "HAL"
            elif os.path.exists(path_to_publications+folder_name):
                To_be_ignored = True
            else:
                To_be_ignored = False

            folder_name = str(year)+"_"+family_name+"_"+journal

        if verbose:
            if To_be_ignored:
                print(f"\033[90m {folder_name} {title} will be ignored\033[0m")
            else:
                print(f"\033[31m{folder_name}  {title} will be created\033[0m")

        if To_be_ignored is False:
            save_to_file(publication, path_to_publications, folder_name)



def save_to_file(pub, path, folder):
    """Save publication to an individual Markdown-like file."""
    if not os.path.exists(path):
        os.makedirs(path)

    year = pub.get('year', 'Unknown')
    
    authors = pub.get('author', 'unknown')
    if authors.lower() == "unknown" or not authors.strip():
        family_name = "Unknown_Author"
    else:
        first_author = authors.split(' and ')[0].strip() if ' and ' in authors else authors.split(',')[0].strip()
        family_name = first_author.split()[-1] if first_author else "Unknown_Author"

    journal = pub.get('journal', 'Unknown_Journal').replace(' ', '_')
    if journal.lower() in ["n/a", "unknown", ""]:
        journal = "Unknown_Journal"

    date_value = pub.get('date', 'N/A') or 'N/A'

    content = f"""---
title: "{pub.get('title', 'N/A')}"
date: {date_value}-01-01
publishDate: {date_value}-01-01
authors: ["{pub.get('author', 'N/A').replace(', ', '", "')}"]
publication_types: ["2"]
abstract: "{pub.get('abstract', 'N/A').replace('\n', ' ')}"
featured: true
publication: "{pub.get('publication', 'N/A')}"
links:
  - icon_pack: fas
    icon: scroll
    name: Link
    url: '{pub.get('url', 'N/A')}'
---
"""
    
    if not os.path.exists(path + folder):
        os.makedirs(path + folder)
    else:
        print("WARNING:", path + folder, " alredy exists")

    with open(path + folder + "/index.md", mode='w', encoding='utf-8') as file:
        file.write(content)

    print("Publications saved to individual files in the 'publications' folder.")

