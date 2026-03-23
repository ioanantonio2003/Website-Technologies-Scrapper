from bs4 import BeautifulSoup

def make_soup(html_content):
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

if __name__ == "__main__":
    html_test = """
    <!DOCTYPE html>
    <html lang="ro">
    <head>
        <title>It;s Shopify</title>
        <meta name="generator" content="Shopify">
        <script src="https://cdn.shopify.com/s/trekkie.js"></script>
    </head>
    <body>
        <h1 id="header-main">Welcome!</h1>
        <div class="product-list">...</div>
    </body>
    </html>
    """

    soup = make_soup(html_test)

    print(f"{soup.title.string}")
    
    meta_tag = soup.find('meta', attrs={'name': 'generator'})
    if meta_tag:
        print(f"*: {meta_tag['content']}")
        
    scripts = soup.find_all('script')
    for script in scripts:
        if script.get('src'):
            print(f"script:{script['src']}")
