import selenium.common.exceptions
from selenium import webdriver

def scraping_one(driver, url):
    driver.get(url)

    all_links = driver.find_elements_by_tag_name('a')
    links = []
    for link in all_links:
        try:
            attrib = link.get_attribute("href")
        except selenium.common.exceptions.StaleElementReferenceException:
            continue
        if attrib is None:
            continue
        if "http" in attrib:
            links.append(attrib)
    # links = [link.get_attribute("href") for link in all_links]

    return links

def scrape_web(driver, url, depth, textfile):
    if depth == 0:
        return
    else:
        textfile.write(f'Depth {4 - depth}\n')
        links = scraping_one(driver, url)
        for link in links:
            textfile.write(f'\t {link}\n')
            scrape_web(driver, link, depth - 1, textfile)
    # textfile = open("scraping.txt", "w+", encoding="UTF8")
    # for i in range(depth):
    #     textfile.write(f'Depth {depth + 1}\n')
    #     links = scraping_one(driver, url)

if __name__ == '__main__':
    textfile = open("scraping.txt", "w+", encoding="UTF8")

    options = webdriver.ChromeOptions()

    # Chrome will start in Headless mode
    options.add_argument('headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    driver = webdriver.Chrome()

    scrape_web(driver, "https://memgraph.com", 3, textfile)

    # Send a request to the website and let it load
    # driver.get("https://discourse.memgraph.com")

    # all_links = driver.find_elements_by_tag_name('a')

    # for link in all_links:
    #     print(link.get_attribute("text"), link.get_attribute("href"))



    print("Quitting Selenium WebDriver")
    driver.quit()