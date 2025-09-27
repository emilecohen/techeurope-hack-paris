import os
from dotenv import load_dotenv
import logging
from supabase import create_client, Client
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from constants import AGENT_CONFIG_ID

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentConfig(BaseModel):
    id: str
    rss_url: str
    newspaper_url: str
    newspaper_name: str
    article_types: List[str]
    instructions: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    supabase_url = os.getenv("SUPABASE_URL") or os.getenv("DATABASE_URL")
    # Try service role key first for read operations, fallback to anon key
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        raise Exception("Supabase URL and key must be configured")
    
    return create_client(supabase_url, supabase_key)

def get_agent_config_by_id(config_id: str = AGENT_CONFIG_ID) -> Dict[str, Any]:
    """Get agent configuration by ID from Supabase"""
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("newspaper_agent_config").select("*").eq("id", config_id).execute()
        
        if not result.data:
            return {
                "status": "error",
                "error": f"No agent configuration found with ID: {config_id}"
            }
        
        config_data = result.data[0]
        agent_config = AgentConfig(**config_data)
        
        logger.info(f"Successfully retrieved agent config with ID: {config_id}")
        
        return {
            "status": "success",
            "config": agent_config,
            "data": config_data
        }
        
    except Exception as e:
        error_message = f"Error retrieving agent config: {str(e)}"
        logger.error(error_message)
        return {
            "status": "error",
            "error": error_message
        }

def get_default_agent_config() -> Dict[str, Any]:
    """Get the default agent configuration using the configured AGENT_CONFIG_ID"""
    return get_agent_config_by_id(AGENT_CONFIG_ID)

def get_agent_instructions(config_id: str = AGENT_CONFIG_ID) -> Dict[str, Any]:
    """Get only the instructions from agent configuration"""
    try:
        config_result = get_agent_config_by_id(config_id)
        
        if config_result["status"] != "success":
            return config_result
        
        return {
            "status": "success",
            "instructions": config_result["config"].instructions,
            "newspaper_name": config_result["config"].newspaper_name
        }
        
    except Exception as e:
        error_message = f"Error getting agent instructions: {str(e)}"
        logger.error(error_message)
        return {
            "status": "error",
            "error": error_message
        }

def get_agent_newspaper_info(config_id: str = AGENT_CONFIG_ID) -> Dict[str, Any]:
    """Get newspaper information from agent configuration"""
    try:
        config_result = get_agent_config_by_id(config_id)
        
        if config_result["status"] != "success":
            return config_result
        
        config = config_result["config"]
        
        return {
            "status": "success",
            "newspaper_name": config.newspaper_name,
            "newspaper_url": config.newspaper_url,
            "rss_url": config.rss_url,
            "article_types": config.article_types
        }
        
    except Exception as e:
        error_message = f"Error getting newspaper info: {str(e)}"
        logger.error(error_message)
        return {
            "status": "error",
            "error": error_message
        }
