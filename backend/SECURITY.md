# Security Guide for AI Textbook RAG Chatbot

This guide explains how to properly secure your project before deploying to public repositories.

## Security Measures Implemented

### 1. Environment Variables Protection
- All sensitive credentials are stored in `.env` files
- `.env` files are included in `.gitignore` and will not be committed to the repository
- Example environment variables are provided in `.env.example` with placeholder values

### 2. Credential Placeholders
All sensitive information in example files has been replaced with generic placeholders:
- Database URLs: `your_neon_database_url_here`
- API Keys: `your_cohere_api_key_here`, `your_openai_api_key_here`
- API Keys: `your_qdrant_api_key_here`
- Secret Keys: `your_secret_key_here`

### 3. Secure Configuration
- The application properly reads credentials from environment variables via the settings module
- No hardcoded credentials in source code
- Configuration is handled through the `config/settings.py` module

## How to Set Up Securely

### For Development
1. Create a `.env` file in the backend directory
2. Add your actual credentials to this file (do NOT commit this file)
3. Use the `.env.example` file as a template for required variables

### For Production Deployment
1. Set environment variables through your hosting platform's interface (e.g., Vercel, Netlify, Railway, etc.)
2. Never store actual credentials in version control
3. Use your platform's secret management features

## Files Protected from Commit

The following file patterns are included in `.gitignore`:
- `.env` - Environment variables file
- `.env.local` - Local environment variables
- `*.db` - Database files
- `*.log` - Log files that might contain sensitive information

## API Security Best Practices

1. **API Key Rotation**: Regularly rotate your API keys
2. **Environment Isolation**: Use different keys for development and production
3. **Access Restrictions**: Where possible, restrict API keys to specific domains/IPs
4. **Monitoring**: Monitor API usage for unusual patterns

## Frontend Security

1. **Backend Communication**: The frontend communicates with the backend via API calls
2. **No Direct API Access**: The frontend does not directly access external APIs (Cohere, Qdrant, etc.)
3. **Secure Transmission**: All API calls are made over HTTPS in production

## Verification Checklist

Before committing to a public repository, verify:
- [x] No `.env` files are committed
- [x] No actual credentials exist in source code
- [x] `.gitignore` properly excludes sensitive files
- [x] Example files use only placeholder values
- [x] README uses generic examples without real credentials

## Additional Security Recommendations

1. **Use Secrets Management**: Consider using a secrets management solution for production
2. **Regular Audits**: Periodically audit your codebase for accidentally committed secrets
3. **Environment Variables**: Always use environment variables for sensitive data
4. **Principle of Least Privilege**: Ensure API keys have minimal required permissions

Your project is now secure and ready for public deployment on Git repositories.