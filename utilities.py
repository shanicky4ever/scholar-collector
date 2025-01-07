from scholarly import scholarly
import numpy as np
import time
import os


def fetch_publications(profile_url, verbose = True):
    """Fetch all publications from a Google Scholar profile."""
    try:
        # Extract the user ID from the URL
        user_id = profile_url.split("user=")[1].split("&")[0]
        author = scholarly.search_author_id(user_id)
        author_name = author['name']

        if verbose:
            print(f"\033[35mUser ID = {user_id}\033[0m")
            print(f"\033[35mUser name = {author_name}\033[0m")

        # Search for the profile
        search_query = scholarly.search_author_id(user_id)
        profile = scholarly.fill(search_query)

        # Collect publications
        publications = []
        for pub in profile.get('publications', []):
            pub_details = scholarly.fill(pub)
            title = pub_details.get('bib', {}).get('title', 'N/A')
            journal = pub_details.get('bib', {}).get('journal', 'N/A')
            author = pub_details.get('bib', {}).get('author', 'N/A')
            abstract = pub_details.get('bib', {}).get('abstract', 'N/A')
            url = pub_details.get('eprint_url', 'N/A')
            doi = pub_details.get('pub_url', 'N/A')
            volume = pub_details.get('bib', {}).get('volume', 'N/A')
            issue = pub_details.get('bib', {}).get('number', 'N/A'),
            if isinstance(issue, tuple):  # Check if 'issue' is a tuple
                issue = issue[0] # Extract the first element from the tuple
                
            # Try date-related information
            year = pub_details.get('bib', {}).get('pub_year', 'N/A')
            month = pub_details.get('bib', {}).get('pub_month', 'N/A')
            day = pub_details.get('bib', {}).get('pub_day', 'N/A')
            # Define date
            if year != 'N/A':
                if month != 'N/A' and day != 'N/A':
                    # If month and day are available, use them
                    date_value = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                elif month != 'N/A':
                    # If only month is available, assume the first day
                    date_value = f"{year}-{month.zfill(2)}-01"
                else:
                    # If only year is available, assume January 1st
                    date_value = f"{year}-01-01"
            else:
                # If no year is available, set date as N/A
                date_value = 'N/A'

            is_preprint =  "arXiv" in pub_details.get('bib', {}).get('journal', '') or "bioRxiv" in pub_details.get('bib', {}).get('journal', ''),
            if isinstance(is_preprint, tuple):  # Check if 'issue' is a tuple
                is_preprint = is_preprint[0] # Extract the first element from the tuple

            journal = manage_exception(journal, title)

            # Debugging missing years
            if year == 'N/A':
                print(f"Missing year for publication: {pub_details.get('bib', {}).get('title', 'Unknown Title')}")

            publication_data = {
                'title': title,
                'author': author,
                'journal': journal,
                'year': year,
                'url': url,
                'abstract': abstract,
                'doi': doi,
                'volume': volume,
                'issue': issue,
                'is_preprint': is_preprint,
                'date': date_value,
            }
            if verbose:
                print(f"\033[36m{year}\033[0m {title} \033[36m{journal}\033[0m")

            publications.append(publication_data)
        
        return publications

    except Exception as e:
        print(f"Error fetching publications: {e}")
        return []

def manage_exception(journal, title):
    # Manage exeptions, such as non-journal article, these manuscript, etc.
    # Adapt to your own case
    if "Nanofluidics: a theoretical and numerical investigation of fluid transport in nanochannels" in title:
        journal = "These"
    elif "Nanofluidics: a pedagogical introduction" in title:
        journal = "HAL"
    elif "Med Sci" in journal:
        journal = "Med Sci"
    elif "arXiv" in journal:
        journal = "arXiv"
    elif journal.lower() in ["n/a", "unknown", ""]:
        journal = "Unknown Journal"
    return journal

def define_folder_name(publication):
    """Read publication information and define folder name from it"""
    To_be_ignored = True

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

    journal = manage_exception(journal, title)

    folder_name = str(year)+"_"+family_name+"_"+journal

    return folder_name, title

def add_missing_publications(publications, path_to_publications, verbose = True):
    """Loop over publications, and check if they are already present in path_to_publications."""
    for publication in publications:
        folder_name, title = define_folder_name(publication)
        if folder_name is not None:
            save_to_file(publication, path_to_publications, folder_name, verbose)

def save_to_file(pub, path, folder, verbose):
    """Save publication to an individual Markdown-like file."""
    if not os.path.exists(path):
        os.makedirs(path)

    # Determine publication type
    is_preprint = pub.get('is_preprint', False)
    if is_preprint:
        publication_type = "3"
    else:
        publication_type = "2"

    date = pub.get('date', 'N/A') or 'N/A'
    title = pub.get('title', 'N/A')
    authors = pub.get('author', 'N/A')
    journal = pub.get('journal', 'N/A')
    year = pub.get('year', 'N/A')
    url = pub.get('url', 'N/A')
    abstract = pub.get('abstract', 'N/A')
    doi = pub.get('doi', 'N/A')
    volume = pub.get('volume', 'N/A')
    issue = pub.get('issue', 'N/A')

    content = f"""---
title: "{title}"
date: {date}
publishDate: {date}
authors: ["{authors.replace(', ', '", "')}"]
publication_types: ["{publication_type}"]
abstract: "{abstract.replace('\n', ' ').replace('\"', '\'')}"
featured: true
publication: "{journal}"
doi: "{doi}"
volume: "{volume}"
issue: "{issue}"
links:
  - icon_pack: fas
    icon: scroll
    name: Link
    url: '{url}'
---
"""
    
    if not os.path.exists(path + folder):
        os.makedirs(path + folder)
        with open(path + folder + "/index.md", mode='w', encoding='utf-8') as file:
            file.write(content)
        if verbose:
            print(f"\033[36m{folder}\033[0m {title}\033[36m will be created\033[0m")
    else:
        if verbose:
            print(f"\033[35m{folder}\033[0m {title}\033[36m already exists\033[0m") 
