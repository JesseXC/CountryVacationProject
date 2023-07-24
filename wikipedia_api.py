import wikipediaapi

def get_summary(query):
    wiki_wiki = wikipediaapi.Wikipedia('VacatiionProject (jcruz2@oberlin.com)', 'en')
    page_py = wiki_wiki.page(f'{query}')
    print(page_py)
    if page_py.exists():
        return page_py.summary
    else:
        return  "Wiki Page Does Not Exist"
    