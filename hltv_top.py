from selenium import webdriver

ALLOWED_PERIODS = ['second', 'seconds', 'minute', 'minutes', 'hour', 'hours', 'day']

def link_dict(a_objects, days_limit):
    result = []
    for element in a_objects:
        l_link = element.get_attribute('href')
        atricle_name = element.find_element_by_class_name('newstext').text
        newstc = element.find_element_by_class_name('newstc').text.split('\n')
        article_age = newstc[0].split()[:2]
        if article_age[1] in ALLOWED_PERIODS or (article_age[1] == 'days' and int(article_age[0]) <= days_limit):
            result.append({"name": atricle_name, "link": l_link, "comments": int(newstc[1].split()[0])})
    return result

driver = webdriver.Chrome()
driver.get("https://www.hltv.org/")
driver.implicitly_wait(200)
links = link_dict(driver.find_elements_by_css_selector('a.newsline.article'), 3)
print(f'Links not later than 3 days - {len(links)}.\n')
links.sort(key=lambda l: l['comments'], reverse=True)
for link in links[:1]:
    print("Link-Name:", link['link'], link['name'])

    print("==================================================================================================")

    driver.get(link['link'])
    driver.implicitly_wait(200)
    print("HEADER - ", driver.find_element_by_css_selector('h1.headline').text)
    print("DATE - ", driver.find_element_by_css_selector('div.date').text)
    print("COMMENTS - ", link['comments'])
    p_elems = driver.find_elements_by_css_selector('p.news-block')
    print(f'\nFound paragraphs - {len(p_elems)}.\n')
    for p in p_elems:
        print(p.text)

    print("==================================================================================================\n")

driver.close()