# Environment Setup Guide

This guide explains how to set up the environment for the AI Textbook RAG backend.

## Environment Variables

### Backend (.env file)

Create a `.env` file in the backend directory with the following variables:

```env
# Backend Environment Variables
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Qdrant Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=textbook_content

# PostgreSQL Database (Neon)
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# LLM Configuration
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7

# API Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### Frontend (.env file)

Create a `.env` file in the textbook directory with the following variables:

```env
# Frontend Environment Variables
API_BASE_URL=http://localhost:8000
PROD_API_URL=https://your-backend-domain.onrender.com

# Analytics (optional)
GA_TRACKING_ID=your_google_analytics_id

# Search Configuration
ALGOLIA_APP_ID=your_algolia_app_id
ALGOLIA_SEARCH_KEY=your_algolia_search_key
ALGOLIA_INDEX_NAME=your_algolia_index_name

# Social Media
SOCIAL_X=your_x_handle
SOCIAL_GITHUB=your_github_handle
```

## Platform-Specific Setup

### Railway Environment Variables

When deploying to Railway, set these variables in the Railway dashboard:

1. `DEBUG`: Set to `False` for production
2. `QDRANT_URL`: Your Qdrant instance URL
3. `QDRANT_API_KEY`: Your Qdrant API key
4. `NEON_DATABASE_URL`: Your Neon PostgreSQL connection string
5. `LLM_API_KEY`: Your LLM provider API key (e.g., OpenAI)

### Render Environment Variables

When deploying to Render, set these variables in the Render dashboard:

1. `DEBUG`: Set to `False` for production
2. `QDRANT_URL`: Your Qdrant instance URL
3. `QDRANT_API_KEY`: Your Qdrant API key
4. `NEON_DATABASE_URL`: Your Neon PostgreSQL connection string
5. `LLM_API_KEY`: Your LLM provider API key

## Required Services

### Qdrant Vector Database

You need a Qdrant instance for vector storage:

- **Local**: Run with Docker (`docker run -p 6333:6333 qdrant/qdrant`)
- **Cloud**: Use Qdrant Cloud or self-hosted instance
- **Railway**: Available as an add-on
- **Render**: Self-hosted or use cloud provider

### PostgreSQL Database (Neon)

For metadata storage:

- **Neon**: Create a new project at https://neon.tech
- **Local**: Use PostgreSQL with `docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15`
- **Railway**: Available as an add-on
- **Render**: Available as an add-on

### LLM Provider

Choose one of these options:

- **OpenAI**: Set `LLM_MODEL=gpt-3.5-turbo` and `OPENAI_API_KEY`
- **Anthropic**: Set `LLM_MODEL=claude-3-haiku` and `ANTHROPIC_API_KEY`
- **Open Source**: Use local models with vLLM or similar

## Security Best Practices

1. **Never commit .env files** - Ensure they're in `.gitignore`
2. **Use strong API keys** - Generate long, random keys
3. **Limit permissions** - Grant minimal required permissions
4. **Enable HTTPS** - Use SSL/TLS in production
5. **Monitor usage** - Track API calls and database queries

## Testing Your Setup

After configuring your environment:

1. Start the backend: `uvicorn main:app --reload`
2. Verify the health endpoint: `GET /api/v1/health`
3. Check that all services are accessible
4. Test the chat endpoint with a sample query

## Troubleshooting

### Common Issues

- **Connection errors**: Verify URLs and credentials
- **Authentication failures**: Check API keys and permissions
- **Rate limiting**: Monitor usage against limits
- **Memory issues**: Adjust embedding batch sizes

### Debugging Tips

- Enable DEBUG mode to see detailed logs
- Check service health endpoints
- Verify network connectivity between services
- Monitor resource usage