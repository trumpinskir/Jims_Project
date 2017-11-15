import urllib2
from bs4 import BeautifulSoup as bsoup 
from bs4 import Comment
import re
import csv
import pandas
import time

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, Comment):
        return False
    return True

# scrape full review from host site
# returns string
def get_review_text(link, wait_count=0):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1', 'content-type':'text/html'}
    request = urllib2.Request(link, headers=headers)

    response = None
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        if e.code == 429:
            print "\nERROR 429"
            if wait_count < 5:
                print "Wait "+str(5*wait_count)
                time.sleep(5*wait_count) 
                wait_count += 1
                return get_review_text(link, wait_count)
            return None
        else: 
            return None
    except:
        return None

    if response.getcode() != 200:
        return None

    html = response.read()

    encoding = response.headers.get("Content-Type")
    if encoding is not None:
        encoding = re.search('charset=(([\w_-])*)', encoding)
        if encoding is not None: 
            encoding = encoding.group(1)
        else:
            encoding = None
    if encoding is None:
        encoding = bsoup(html, "html.parser").original_encoding

    soup = bsoup(html.decode(encoding, 'ignore'), "html.parser")

    all_text = soup.findAll(text=True)
    review_text = ""
    for text in all_text:
        if not visible(text): continue

        text = text.encode(encoding, 'ignore')
        if len(re.findall('\w+', text)) > 20:
            review_text = review_text + ' ' + ' '.join(text.split())

    if len(review_text) < 30:
        review_text = None
    return review_text



# scrape starting from critic profile
# returns 5xN rows
def scrape_critic_page(html):

    soup = bsoup(html, "html.parser")

    # get critic name
    critic = soup.find("h1", { "class" : "critic_title" }).getText().encode("utf-8")

    soup = soup.find("ol", { "class" : "reviews critic_profile_reviews" })

    rows = []

    # first review
    first_review = soup.find("li", { "class" : "review critic_review first_review" })
    review_link = first_review.find("li", {"class": "review_action full_review"})
    if review_link is not None:
        title = first_review.find("div", { "class" : "review_product" }).a.getText().encode("utf-8")
        metascore = first_review.find("li", { "class" : "brief_metascore" }).span.getText().encode("utf-8")
        critic_score = first_review.find("li", { "class" : "brief_critscore" }).span.getText().encode("utf-8")		
        review_link = review_link.a['href']
        review_text = get_review_text(review_link)
        if review_text is None:
            print "\nERROR"
            print title
        else: rows.append([critic, title, metascore, critic_score, review_text])

    reviews = soup.findAll("li", { "class" : "review critic_review" })

    for review in reviews:
        
        title = review.find("div", { "class" : "review_product" }).a.getText().encode("utf-8")
        metascore = review.find("li", { "class" : "brief_metascore" }).span.getText().encode("utf-8")
        critic_score = review.find("li", { "class" : "brief_critscore" }).span.getText().encode("utf-8")

        review_link2 = review.find("li", {"class": "review_action full_review"})
        if review_link2 is None:
            print "\nNo Review"
            print title
            continue
        review_link2 = review_link2.a["href"]
        review_text = get_review_text(review_link2)
        if review_text is None:
            print "\nERROR"
            print title
            continue
        rows.append([critic, title, metascore, critic_score, review_text])

        print "\nSUCCESS"
        print title
        print review_link2
        print "TEXT: " + review_text[:15]

    return rows
