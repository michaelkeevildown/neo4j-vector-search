// Migration query to add source property to existing Page nodes
// This concatenates the document title and page number for proper display in the UI

MATCH (r:Report)-[:CONTAINS]->(p:Page)
WHERE p.source IS NULL
SET p.source = r.title + " - Page " + toString(p.page_number)
RETURN count(p) as updated_pages;