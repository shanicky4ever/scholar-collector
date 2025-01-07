import os

def detect_if_publication_is_missing(publications, verbose = True, path_to_publications = "publications/"):
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
    if not os.path.exists(path):  # Create a folder for the files
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

    filename = f"{year}_{family_name}_{journal}.md"
    filepath = os.path.join('publications', filename)

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

    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write(content)

    print("Publications saved to individual files in the 'publications' folder.")

