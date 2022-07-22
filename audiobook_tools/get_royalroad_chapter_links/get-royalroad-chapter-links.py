#!/usr/bin/env python3



#  required:
#      python3
#      BeautifulSoup
#          debian/ubuntu: python3-bs4
#          pip: pip install beautifulsoup4




#####################################################
# CLI Arguments
#
def parse_args():
    """
    CLI Arguments
    """

    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='royalroad web-novels URL')

    args = parser.parse_args()
    
    return args
#END: parse_args())




def get_html(args):

    #  import urllib.request 

    from urllib.request import Request, urlopen

    #  print('  - downloading url...')
    url = args.url
    
    #  print(url)
    #  response = urlopen(url, headers={"User-Agent": "Mozilla/5.0"})
    #  html = str(response.read())
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(request_site).read()


    return html
#End: get html




def get_links(html):
    from bs4 import BeautifulSoup
    #  from lxml import html
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('tr', 'chapter-row')


    for attrib in tags:
        links += ['https://royalroad.com' + str(attrib['data-url'])]
    #  print(tags)
    #  <tr style="cursor: pointer" data-url="/fiction/39408/beware-of-chicken/chapter/950289/v3c26-the-present" data-volume-id="null" class="chapter-row">

    return links 

#End: get_links






def write_links_file(links):

    #  print('  - writing \'links.txt\' file')
    with open('links.txt', 'w') as f:
        for link in links:
            f.write(link + '\n')

#End: write_links_file





def main():

    print('Getting chapters from Royalroad...')
    args = parse_args()

    html = get_html(args)

    links = get_links(html)

    write_links_file(links)
    #  print(links)
    #  save to links.txt

    #  print('  - done')

#End: main




###########################################
# Start it up
#
if __name__ == "__main__":
   main()
