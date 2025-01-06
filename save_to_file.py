import os

def save_to_file(publications):
    """
    Save each publication to an individual Markdown-like file.

    Args:
        publications (list): List of publication dictionaries.
    """
    try:
        if not os.path.exists('publications'):  # Create a folder for the files
            os.makedirs('publications')

        for pub in publications:
            year = pub.get('year', 'Unknown')
            
            # Extract the first author's last name
            authors = pub.get('author', 'unknown')
            if authors.lower() == "unknown" or not authors.strip():
                family_name = "Unknown_Author"
            else:
                first_author = authors.split(' and ')[0].strip() if ' and ' in authors else authors.split(',')[0].strip()
                family_name = first_author.split()[-1] if first_author else "Unknown_Author"

            # Replace spaces with underscores in the journal name, and handle missing journal
            journal = pub.get('journal', 'Unknown_Journal').replace(' ', '_')
            if journal.lower() in ["n/a", "unknown", ""]:
                journal = "Unknown_Journal"

            # Construct the filename
            filename = f"{year}_{family_name}_{journal}.md"
            filepath = os.path.join('publications', filename)

            # Handle missing date fields
            date_value = pub.get('date', 'N/A') or 'N/A'

            # Markdown-like content
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

    except Exception as e:
        print(f"Error saving individual files: {e}")


if __name__ == "__main__":
    scholar_url = "https://scholar.google.fr/citations?user=9fD2JlYAAAAJ&hl"  # Replace accordingly
    publications = fetch_publications(scholar_url)
    
    # Debug: Log all fetched publications to check for missing fields
    for pub in publications:
        if not pub.get('journal') or not pub.get('author'):
            print(f"Incomplete publication data: {pub}")
    
    # Debugging for 2024 publications
    for pub in publications:
        if pub.get('year') == '2024':
            print(f"Found 2024 publication: {pub['title']}")
    
    print("Publication fetched")
    save_to_individual_files(publications)
