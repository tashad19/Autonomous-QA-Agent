from bs4 import BeautifulSoup

def parse_html_text(path: str):
    with open(path, 'r', encoding='utf-8') as fh:
        html = fh.read()
    soup = BeautifulSoup(html, 'lxml')
    texts = [t.strip() for t in soup.stripped_strings]
    return '\n'.join(texts)
