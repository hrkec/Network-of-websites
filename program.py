import mgclient

# Make a connection to the database
connection = mgclient.connect(host='127.0.0.1', port=7687)

# Create a cursor for query execution
cursor = connection.cursor()

# Delete all nodes and relationships
query = "MATCH (n) DETACH DELETE n"

# Execute the query
cursor.execute(query)

# Create a node with the label FirstNode and message property with the value "Hello, World!"
query = """
            CREATE (u: URL), (u2: URL)
            CREATE (u)-[r:LINKS_TO]->(u2)
            RETURN r
        """

# Execute the query
cursor.execute(query)

# Fetch one row of query results
row = cursor.fetchone()

# Print the first member in row
print(row[0])