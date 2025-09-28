# TechEurope Hack Paris - NewsCaster

Famous news publishers are suing big AI Labs (OpenAI, Perplexity) for indexing their paywalled data. They are passive in the AI wave, and cannot impose their tone, voice, opinion feed. Newscaster gives back the control to the news publishers: they can meet their audience where there are, creating a branded, controlled, multi channel MCP that subscribers can use anywhere.

 
Newscaster is an AI-powered news aggregation and interaction platform that combines RSS ingestion, vector search, and multiple interaction modalities including text, voice, and video conferencing with AI agents.

## 🏗️ Architecture Overview

The platform consists of four main components:

1. **RSS News Aggregator** - Ingests and processes news articles from RSS feeds
2. **Weaviate Vector Database** - Stores and searches articles using semantic embeddings
3. **MCP Server** - Model Control Protocol server for AI agent tools (you will find the MCP server in the `mcp-main` branch)
4. **Multi-Modal UI** - React-based interfaces for different interaction types


ARCHITECTURE DIAGRAM:

https://excalidraw.com/#room=476e064b6fe75928da53,2LZI0iVtJairnX2UP-Ck7g
<img width="1135" height="652" alt="Screenshot 2025-09-28 at 1 03 14 PM" src="https://github.com/user-attachments/assets/6de05c21-6d16-4827-8d0a-84ec9d84d330" />

## 📥 1. Ingestion (Articles + Config through RSS + Perplexity)

### RSS News Aggregator (`rss_news_aggregator/`)

The ingestion pipeline fetches articles from RSS feeds, processes them, and stores them in Weaviate for semantic search.

**Key Features:**

- RSS feed parsing and article extraction
- HTML content cleaning and full-text fetching
- Duplicate detection and prevention
- Batch processing with configurable limits
- Multi-language support
- Category extraction from RSS tags

**Components:**

- `main.py` - FastAPI server with `/posting` endpoint
- `parser/fetcher.py` - RSS parsing and article processing
- `parser/cleaner.py` - HTML cleaning and content extraction
- `parser/saver.py` - Weaviate database integration
- `models/articles.py` - Article data structure definition

**Usage:**

```bash
cd rss_news_aggregator
pip install -r requirements.txt
uvicorn main:app --reload
```

**API Endpoint:**

```http
POST /posting
Content-Type: application/json

{
  "companyName": "BBC News",
  "language": "en",
  "maxArticles": 50,
  "rssLink": "http://feeds.bbci.co.uk/news/rss.xml"
}
```

## 🗄️ 2. Weaviate Vector Database (`weaviate/`)

Semantic search and storage for news articles using OpenAI embeddings.

**Features:**

- Vector embeddings using `text-embedding-3-large`
- Semantic search capabilities
- Batch import with error handling
- Multi-language article support

**Setup:**

```bash
cd weaviate
python create_newspaper.py  # Create schema
python newspaper_insert.py  # Insert articles
python newspaper_read.py    # Query examples
```

**Environment Variables:**

```env
WEAVIATE_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key
COHERE_APIKEY=your_cohere_api_key
```

## 🔧 3. MCP (Model Control Protocol) Creation (`agent/mcp/`)

FastMCP server providing tools and functions for AI agents.

**Current Tools:**

- Mathematical operations (`add`, `subtract`)
- Speech control (`speak_faster`)

**Setup:**

```bash
cd agent/mcp
docker build -t mcp-server .
docker run -d -p 8000:8000 mcp-server
```

**API Endpoints:**

- `GET /mcp` - MCP protocol endpoint
- Tools available for AI agent integration

## 🎯 4. Multiple Ways to Interact

### Text-Based Interaction (`ui/`)

React-based dashboard for managing news agents and articles.

**Features:**

- News agent registration form
- Article browsing and filtering
- Agent configuration management
- Real-time article updates

**Setup:**

```bash
cd ui
npm install
npm run dev
```

**Key Pages:**

- `/` - Agent registration form
- `/dashboard` - Article management and agent configuration
- `/playground` - Interaction mode selection

### Voice Interaction

LiveKit-based voice agents with real-time speech processing.

**Agent Files:**

- `agent/agent.py` - Basic voice agent
- `agent/agent1.py` - Enhanced voice agent with Bey avatar
- `agent/agent_final.py` - Full-featured agent with weather lookup

**Setup:**

```bash
cd agent
conda env create -f environment.yml
conda activate paris
python agent_final.py
```

**Features:**

- Real-time speech-to-text
- Voice activity detection
- Noise cancellation
- Bey avatar integration
- MCP tool integration

### Video Conferencing (`agent-ui/`)

Next.js-based video conferencing interface with LiveKit integration.

**Features:**

- Video conferencing with AI agents
- Screen sharing capabilities
- Recording functionality
- Custom video backgrounds
- Real-time audio/video processing

**Setup:**

```bash
cd agent-ui
npm install
npm run dev
```

**Key Components:**

- Video conference rooms
- Custom video backgrounds
- Recording controls
- Audio/video settings

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker
- Weaviate Cloud account
- OpenAI API key
- Cohere API key

### Environment Setup

1. **Clone and setup environment:**

```bash
git clone <repository>
cd techeurope-hack-paris
```

2. **Configure environment variables:**

```bash
# Create .env files in relevant directories
cp .env.example agent/.env
cp .env.example rss_news_aggregator/.env
```

3. **Start the ingestion service:**

```bash
cd rss_news_aggregator
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

4. **Setup Weaviate database:**

```bash
cd weaviate
python create_newspaper.py
```

5. **Start MCP server:**

```bash
cd agent/mcp
docker build -t mcp-server .
docker run -d -p 8000:8000 mcp-server
```

6. **Start the main UI:**

```bash
cd ui
npm install
npm run dev
```

7. **Start video conferencing UI:**

```bash
cd agent-ui
npm install
npm run dev
```

8. **Run voice agent:**

```bash
cd agent
conda env create -f environment.yml
conda activate paris
python agent_final.py
```

### Usage Flow

1. **Register a News Source:** Use the main UI to register RSS feeds and configure agents
2. **Ingest Articles:** The system automatically fetches and processes articles
3. **Search Articles:** Use the dashboard to browse and filter articles
4. **Interact with AI:**
   - **Text:** Use the playground to chat with AI agents
   - **Voice:** Run the voice agent for real-time speech interaction
   - **Video:** Join video conferences with AI agents

## 🛠️ Development

### Project Structure

```
techeurope-hack-paris/
├── rss_news_aggregator/     # RSS ingestion service
├── weaviate/               # Vector database setup
├── agent/                  # AI agents and MCP server
├── ui/                     # Main React dashboard
├── agent-ui/              # Video conferencing interface
└── README.md              # This file
```

### Key Technologies

- **Backend:** Python, FastAPI, LiveKit, Weaviate
- **Frontend:** React, Next.js, TypeScript, Tailwind CSS
- **AI/ML:** OpenAI GPT, Embeddings, Real-time Speech
- **Infrastructure:** Docker, Conda, npm

## 📝 API Documentation

### RSS Aggregator API

- `POST /posting` - Submit RSS feed for processing

### MCP Server

- `GET /mcp` - MCP protocol endpoint
- Tools: `add`, `subtract`, `speak_faster`

### LiveKit Integration

- Real-time audio/video streaming
- Voice activity detection
- Noise cancellation
- Avatar integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the TechEurope Hack Paris event.

---

**Built with ❤️ for TechEurope Hack Paris**
