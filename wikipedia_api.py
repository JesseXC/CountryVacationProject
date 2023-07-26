import wikipediaapi

def get_summary(query):
    wiki_wiki = wikipediaapi.Wikipedia('VacationProject (jcruz2@oberlin.com)', 'en')
    try:
        page_py = wiki_wiki.page(f'{query}')
        if page_py.exists():
            return page_py.summary
        else:
            return None
    except:
        print("failwiki")
    
print(get_summary('Casa Batllo'))