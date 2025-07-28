from fastapi import FastAPI, Query
from pydantic import HttpUrl
from scraper import scrape_url
import asyncio

app = FastAPI()

@app.get("/scrape")
async def scrape_endpoint(url: HttpUrl = Query(..., description="URL to scrape")):
    html = await scrape_url(str(url))
    return {"url": url, "html": html}
