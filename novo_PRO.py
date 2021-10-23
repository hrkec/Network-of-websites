import mgclient
from selenium import webdriver

def connect_to_memgraph():
    connection = mgclient.connect(host='127.0.0.1', port=7687)

    # Create a cursor for query execution
    cursor = connection.cursor()

    # Delete all nodes and relationships
    query = "MATCH (n) DETACH DELETE n;"

    # Execute the query
    cursor.execute(query)

    # Execute the query
    # cursor.execute(query)
    #
    # row = cursor.fetchone()

    # query = """
    #                 CREATE (u: URL)
    #                 SET u.text = '{message}'
    #                 RETURN 'Node ' + id(u) + u.text
    #             """.format(message="http://google.com")

    # Execute the query
    # cursor.execute(query)
    #
    # print(cursor.fetchone()[0])
    #
    # print(cursor.description)
    # connection.commit()

    return cursor, connection


def scraping_one(driver, url):
    driver.get(url)

    all_links = driver.find_elements_by_tag_name('a')
    links = set()
    for link in all_links:
        try:
            attrib = link.get_attribute("href")
        except:
            continue
        if attrib is None:
            continue
        if "http" in attrib:
            links.add(attrib)

    return links


def scrape_web(cursor, driver, url, depth, textfile):
    # time.sleep(1)

    if depth == 0:
        return
    else:
        links = scraping_one(driver, url)

        # query = """
        #         CREATE(u: URL)
        #         SET u.text = '{title}'
        #     """.format(title=url)

        query = """
                MATCH(u: URL)
                WHERE u.text = '{title}'
                RETURN u
            """.format(title=url)

        cursor.execute(query)

        row = cursor.fetchone()

        if row is None:
            query = """
                        CREATE(u: URL)
                        SET u.text = '{title}'
                  """.format(title=url)

            cursor.execute(query)

        for link in links:
            textfile.write(f'\t {link}\n')

            query = """
                            MATCH(u: URL)
                            WHERE u.text = '{title}'
                            RETURN u
                        """.format(title=link)

            cursor.execute(query)

            row = cursor.fetchone()

            if row is None:
                query = """
                                        CREATE(u: URL)
                                        SET u.text = '{title}'
                                  """.format(title=link)

                cursor.execute(query)

            # TU SAM ZBTRISAL
            # query = """
            #         MATCH (u1: URL)
            #         WHERE u1.text = '{title1}'
            #         CREATE (u2: URL)<-[:LINKS_TO]-(u1)
            #         SET u2.text = '{title2}';
            # """.format(title1=url, title2=link)
            #
            # cursor.execute(query)

            query = """
                    MATCH (u1: URL), (u2: URL)
                    WHERE u1.text = '{title1}' AND u2.text = '{title2}'
                    CREATE (u1)-[:LINKS_TO]->(u2)
            """.format(title1=url, title2=link)

            cursor.execute(query)

            if row is None:
                scrape_web(cursor, driver, link, depth - 1, textfile)
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

    cursor, connection = connect_to_memgraph()

    scrape_web(cursor, driver, "https://memgraph.com", 3, textfile)
    # scrape_web(cursor, driver, "http://streaming.narodni.hr/stream/player.html", 1, textfile)

    # Send a request to the website and let it load
    # driver.get("https://discourse.memgraph.com")

    # all_links = driver.find_elements_by_tag_name('a')

    # for link in all_links:
    #     print(link.get_attribute("text"), link.get_attribute("href"))



    print("Quitting Selenium WebDriver")
    driver.quit()

    query = """
            MATCH (u: URL)
            RETURN u.text;
        """

    # Execute the query
    # cursor.execute(query)

    # Fetch one row of query results
    # row = cursor.fetchone()

    # Print the first member in row
    # print(row[0])
    connection.commit()