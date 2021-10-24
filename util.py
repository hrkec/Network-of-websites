import mgclient
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from errors import *


def connect_to_memgraph():
    connection = mgclient.connect(host='127.0.0.1', port=7687)

    # Create a cursor for query execution
    cursor = connection.cursor()

    return cursor, connection


def delete_network(cursor):
    # Delete all nodes and relationships
    query = "MATCH (n) DETACH DELETE n;"

    # Execute the query
    cursor.execute(query)


def scrape_website(driver, url):
    try:
        driver.get(url)
    except WebDriverException:
        raise WebsiteNotFoundNetError(f"{url} doesn't exist!")

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


def check_if_node_exists(cursor, url):
    query = """
                MATCH(u: URL)
                WHERE u.text = '{title}'
                RETURN u
            """.format(title=url)
    cursor.execute(query)
    row = cursor.fetchone()
    return row


def create_node(cursor, url):
    query = """
                CREATE(u: URL)
                SET u.text = '{title}'
            """.format(title=url)

    cursor.execute(query)

def scrape(cursor, driver, url, depth):
    if depth != 0:
        links = scrape_website(driver, url)

        row = check_if_node_exists(cursor, url)
        if row is None:
            create_node(cursor, url)

        for link in links:
            row = check_if_node_exists(cursor, link)
            if row is None:
                create_node(cursor, link)

            query = """
                        MATCH (u1: URL), (u2: URL)
                        WHERE u1.text = '{title1}' AND u2.text = '{title2}'
                        CREATE (u1)-[:LINKS_TO]->(u2)
                    """.format(title1=url, title2=link)

            cursor.execute(query)

            if row is None:
                scrape(cursor, driver, link, depth - 1)
    else:
        return


def create_network(start_url, depth):
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
    delete_network(cursor)

    scrape(cursor, driver, start_url, depth)

    print("Quitting Selenium WebDriver")
    driver.quit()

    connection.commit()


def shortest_path(start_url, end_url):
    cursor, connection = connect_to_memgraph()

    start = "(u: URL {text:" + f'"{start_url}"' + "})"
    end = "(u2: URL {text:" + f'"{end_url}"' + "})"

    query = f"""MATCH {start}
            RETURN u;
        """

    cursor.execute(query)
    if cursor.fetchone() is None:
        raise WebsiteNotFoundInDBError(f"There is no {start_url} in Memgraph database!")

    query = f"""
                MATCH {end}
                RETURN u2;
            """

    cursor.execute(query)
    if cursor.fetchone() is None:
        raise WebsiteNotFoundInDBError(f"There is no {end_url} in Memgraph database!")

    query = f"""
                MATCH p = {start}
                -[r:LINKS_TO * bfs]-
                {end}
                UNWIND (nodes(p)) AS rows
                RETURN rows.text;
            """
    cursor.execute(query)

    websites = cursor.fetchall()
    websites = [website[0] for website in websites]

    num_of_clicks = len(websites) - 1

    if num_of_clicks == -1:
        raise ShortestPathNotFoundError(f"There is no path between {start_url} and {end_url}")

    print(f"Shortest Path: {num_of_clicks}")
    for i, website in enumerate(websites):
        print(f'{i} - {website}')