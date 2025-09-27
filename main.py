import httpx
import os
from dotenv import load_dotenv
import logging
from supabase import create_client, Client
from typing import List, Optional
from pydantic import BaseModel
from constants import PERPLEXITY_MODEL, MAX_TOKENS, PERPLEXITY_PROMPT, TEMPERATURE, TIMEOUT

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewspaperAnalysis(BaseModel):
    newspaper_name: str
    instructions: str

# Initialize Supabase client
def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    supabase_url = os.getenv("DATABASE_URL")
    # Try service role key first for write operations, fallback to anon key
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        raise Exception("Supabase URL and key must be configured")
    
    return create_client(supabase_url, supabase_key)

async def call_perplexity_for_agent_personality(prompt: str, newspaper_url: str) -> NewspaperAnalysis:
    """Call Perplexity API with article content and prompt"""
    perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
    if not perplexity_api_key:
        raise Exception("Perplexity API key not configured")

    full_prompt = prompt.format(newspaper_url=newspaper_url)
    
    try:
        payload = {
            "model": PERPLEXITY_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "schema": NewspaperAnalysis.model_json_schema()
                }
            }
        }
        
        logger.info(f"Sending request to Perplexity API with model: {PERPLEXITY_MODEL}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code != 200:
                error_text = response.text
                logger.error(f"API Error {response.status_code}: {error_text}")
                raise Exception(f"API returned {response.status_code}: {error_text}")
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return NewspaperAnalysis.model_validate_json(content)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP Status Error: {e.response.status_code} - {e.response.text}")
        raise Exception(f"Failed to call Perplexity API: HTTP {e.response.status_code}")
    except Exception as e:
        logger.error(f"Error calling Perplexity API: {e}")
        raise Exception(f"Failed to call Perplexity API: {str(e)}")

async def save_agent_personality_to_supabase(
    rss_url: str,
    newspaper_url: str,
    article_types: List[str],
    perplexity_response: NewspaperAnalysis
) -> dict:
    """Save agent personality data to Supabase"""
    try:
        supabase = get_supabase_client()
        
        data = {
            "rss_url": rss_url,
            "newspaper_url": newspaper_url,
            "newspaper_name": perplexity_response.newspaper_name,
            "article_types": article_types,
            "instructions": perplexity_response.instructions
        }
        
        result = supabase.table("newspaper_agent_config").insert(data).execute()
        
        if result.data:
            logger.info(f"Successfully saved agent personality to Supabase with ID: {result.data[0]['id']}")
            return {
                "status": "success",
                "id": result.data[0]["id"],
                "data": result.data[0]
            }
        else:
            raise Exception("No data returned from insert operation")
            
    except Exception as e:
        error_message = f"Error saving to Supabase: {str(e)}"
        logger.error(error_message)
        return {
            "status": "error",
            "error": error_message
        }

async def get_agent_personality(newspaper_url: str, prompt: str = PERPLEXITY_PROMPT) -> dict:
    """Analyze newspaper article with Perplexity API using custom prompt"""
    try:
        
        # Call Perplexity API with prompt and article
        perplexity_response = await call_perplexity_for_agent_personality(prompt, newspaper_url)
        
        return {
            "status": "success",
            "perplexity_response": perplexity_response,
            "newspaper_name": perplexity_response.newspaper_name,
            "instructions": perplexity_response.instructions
        }
        
    except Exception as e:
        error_message = f"Error analyzing news: {str(e)}"
        logger.error(error_message)
        return {
            "status": "error",
            "error": error_message
        }

async def get_and_save_agent_personality(
    newspaper_url: str,
    rss_url: str,
    article_types: List[str],
    prompt: str = PERPLEXITY_PROMPT
) -> dict:
    """Get agent personality from Perplexity and save to Supabase"""
    try:
        # Get agent personality
        personality_result = await get_agent_personality(newspaper_url, prompt)
        
        if personality_result["status"] != "success":
            return personality_result
            
        # Save to Supabase
        save_result = await save_agent_personality_to_supabase(
            rss_url=rss_url,
            newspaper_url=newspaper_url,
            article_types=article_types,
            perplexity_response=personality_result["perplexity_response"]
        )
        
        if save_result["status"] == "success":
            return {
                "status": "success",
                "message": "Agent personality generated and saved successfully",
                "newspaper_name": personality_result["newspaper_name"],
                "instructions": personality_result["instructions"],
                "supabase_id": save_result["id"],
                "supabase_data": save_result["data"]
            }
        else:
            return save_result
            
    except Exception as e:
        error_message = f"Error in get_and_save_agent_personality: {str(e)}"
        logger.error(error_message)
        return {
            "status": "error",
            "error": error_message
        }


if __name__ == "__main__":
    import asyncio
    
    # Example usage: Get and save agent personality
    result = asyncio.run(get_and_save_agent_personality(
        newspaper_url="https://www.nytimes.com/",
        rss_url="https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        article_types=["news", "politics", "world"]
    ))
    print(result)