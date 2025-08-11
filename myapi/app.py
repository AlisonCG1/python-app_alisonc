import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import duckdb
import datetime
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


app = FastAPI()

class QueryRequest(BaseModel):
    query_id: str


PREDEFINED_QUERIES = {
    "penguins_query": "SELECT * FROM my_lake.penguins"
}

def get_duckdb_connection():
    conn = duckdb.connect(database='/Users/alisoncordoba/fir8aug/duckdbdump/lake.duckdb')
    conn.execute("LOAD 'ducklake'")
    conn.execute("""
        ATTACH 'ducklake:/Users/alisoncordoba/fir8aug/duckdbdump/catalog.duckdb' AS my_lake
        (DATA_PATH '/Users/alisoncordoba/fir8aug/duckdbdump/data')
    """)
    conn.execute("USE my_lake")
    return conn


@app.post("/query", response_model=dict)
async def execute_query(request: QueryRequest):
    try:
        logger.info(f"Received query request: {request.query_id}")

        query = PREDEFINED_QUERIES.get(request.query_id)

        if not query:
            logger.error(f"Query ID '{request.query_id}' not found")
            raise HTTPException(status_code=404, detail=f"Query ID '{request.query_id}' not found")

 
        conn = get_duckdb_connection()
        cursor = conn.execute(query)
        columns = [desc[0] for desc in cursor.description]  
        rows = cursor.fetchall()  
        conn.close()

        results = [dict(zip(columns, row)) for row in rows]

        logger.info(f"Query executed successfully: {request.query_id}")
        return {"results": results}

    except Exception as e:
        logger.exception("Error executing query")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")



## endpoint 2 is root and it is a health check that returns the current timestamp in utc time
@app.get("/", response_model=dict)
async def health_check():
    try:
        # Get current UTC timestamp
        utc_timestamp = datetime.now(timezone.utc).isoformat()
        logger.info("Health check requested")
        return {"status": "healthy", "timestamp_utc": utc_timestamp}
    except Exception as e:
        logger.exception("Error in health check")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")