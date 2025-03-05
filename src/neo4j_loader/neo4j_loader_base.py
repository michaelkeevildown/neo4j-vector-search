# neo4j_loader/neo4j_loader_base.py

from neo4j import GraphDatabase

from src.neo4j_loader.loaders.annual_report_cypher import create_annual_report_tx
from src.neo4j_loader.loaders.insurance_policy_cypher import create_insurance_policy_tx
from src.neo4j_loader.loaders.policing_handbook_cypher import create_policing_handbook_tx
from src.utils.env_variables import load_env_variables


class Neo4jBaseLoader:
    def __init__(self):
        self.env_vars = load_env_variables()

        self.uri = self.env_vars['NEO4J_URI']
        self.username = self.env_vars['NEO4J_USER']
        self.password = self.env_vars['NEO4J_PASSWORD']
        self.database = self.env_vars['NEO4J_DATABASE']
        self.vector_index = self.env_vars['NEO4J_DATABASE_VECTOR_INDEX']

        print("NEO4J_URI:", self.uri)
        print("NEO4J_USER:", self.username)
        print("NEO4J_PASSWORD:", self.password)
        print("NEO4J_DATABASE:", self.database)
        print("NEO4J_DATABASE_VECTOR_INDEX:", self.vector_index)

        self.driver = GraphDatabase.driver(self.uri, auth=(
            self.username, self.password))

    def close(self):
        # Close the driver to release resources
        self.driver.close()
        
    def check_vector_index_exists(self):
        """Check if the vector index specified in the .env file exists in the database.
        If it doesn't exist, create it using the specified configuration."""
        query = """
        SHOW INDEXES WHERE name = $index_name
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query, index_name=self.vector_index).single()
            if not result:
                print(f"Vector index '{self.vector_index}' does not exist. Creating it now...")
                create_index_query = f"""
                CREATE VECTOR INDEX {self.vector_index} IF NOT EXISTS
                FOR (n:Page) ON (n.full-page-embeddings)
                """
                session.run(create_index_query)
                print(f"Vector index '{self.vector_index}' created successfully.")
                return True
            print(f"Vector index '{self.vector_index}' exists.")
            return True

    def insert_data(self, title, data, context):
        # Check if vector index exists before inserting data
        self.check_vector_index_exists()
        
        with self.driver.session(database=self.database) as session:
            if context == "Annual Report":
                result = session.write_transaction(create_annual_report_tx, {"data": data, "title": title})
                print("Data Inserted into Neo4j")
            elif context == "Insurance Document":
                result = session.write_transaction(create_insurance_policy_tx, {"data": data, "title": title})
                print("----- Data Inserted into Neo4j")
            elif context == "Policing Handbook":
                result = session.write_transaction(create_policing_handbook_tx, {"data": data, "title": title})
                print("----- Data Inserted into Neo4j")

    def get_last_page(self, title):
        query = """
                MATCH (r:Report {title: $title})-[:CONTAINS]->(p:Page)
                RETURN MAX(p.page_number) AS lastPage
                """
        with self.driver.session(database=self.database) as session:
            result = session.read_transaction(lambda tx: tx.run(query, title=title).single())
            return result['lastPage'] if result['lastPage'] else 0
