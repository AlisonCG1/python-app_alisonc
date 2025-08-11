import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import duckdb
import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Pydantic model for request body
class QueryRequest(BaseModel):
    query_id: str

# Predefined queries
PREDEFINED_QUERIES = {
    "penguins_query1": "SELECT * FROM my_lake.penguins"
}

# DuckDB connection function
def get_duckdb_connection():
    return duckdb.connect("my_database.duckdb")

# Endpoint to execute predefined queries
@app.post("/query", response_model=dict)
async def execute_query(request: QueryRequest):
    try:
        logger.info(f"Received query request: {request.query_id}")

        # Retrieve the predefined query
        query = PREDEFINED_QUERIES.get(request.query_id)

        if not query:
            logger.error(f"Query ID '{request.query_id}' not found")
            raise HTTPException(status_code=404, detail=f"Query ID '{request.query_id}' not found")

        # Execute query and fetch results without pandas
        conn = get_duckdb_connection()
        cursor = conn.execute(query)
        columns = [desc[0] for desc in cursor.description]  # Get column names
        rows = cursor.fetchall()  # List of tuples
        conn.close()

        # Convert to list of dicts
        results = [dict(zip(columns, row)) for row in rows]

        logger.info(f"Query executed successfully: {request.query_id}")
        return {"results": results}

    except Exception as e:
        logger.exception("Error executing query")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")



## endpoint 2 is root and it is a health check that returns the current timestamp in utc time