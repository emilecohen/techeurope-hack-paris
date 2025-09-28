from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser.fetcher import latest_articles, auto_fetch_rss

# Define the request body schema
class ArticleRequest(BaseModel):
    companyName: str
    language: str
    maxArticles: int
    rssLink: str

app = FastAPI()

# Allow any origin for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/posting")
async def upload_articles(request: ArticleRequest):

    # Call your backend logic
    auto_fetch_rss(
        request.companyName,
        request.language,
        request.maxArticles,
        request.rssLink
    )

    return {"status": "success"}
