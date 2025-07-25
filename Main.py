import re

def clean_duplicate_authors(bibtex_entry):
    """
    Clean the duplicate authors :
    1. Find the author match (if no match skip)
    2. See unique authors by stripping them 
    3. If norm_author is not seen, append then clean.
    """

    author_match = re.search(r'author\s*=\s*{(.+?)}', bibtex_entry, re.DOTALL)
    if not author_match:
        return bibtex_entry 

    author_block = author_match.group(1)
    authors = [a.strip() for a in author_block.split(' and ')]

    seen = set()
    unique_authors = []
    for author in authors:
        norm_author = author.lower().replace('.', '').replace(' ', '')
        if norm_author not in seen:
            seen.add(norm_author)
            unique_authors.append(author)

    new_author_block = ' and '.join(unique_authors)
    cleaned_entry = re.sub(r'author\s*=\s*{(.+?)}', f'author = {{{new_author_block}}}', bibtex_entry, flags=re.DOTALL)

    return cleaned_entry

def process_bib_file(input_file, output_file):
    """"
    This is the main working block that will reference our other helpers.
    1. Open the file and read it
    2, Split entries 
    3. Run helper block -> Clean split entries
    4. Output write and print OK message
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split entries (naively assumes @ starts a new entry)
    entries = re.split(r'(?=@\w+{)', content)

    cleaned_entries = [clean_duplicate_authors(entry) for entry in entries if entry.strip()]
    cleaned_content = '\n\n'.join(cleaned_entries)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    print(f"Cleaned BibTeX written to {output_file}")


process_bib_file("references.bib", "references_cleaned.bib")
