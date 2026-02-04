# Express.js Welcome Message Server

An Express.js server that generates creative Hebrew welcome messages for new users using OpenAI's API.

## Features

- GET `/welcome-message` endpoint that generates Hebrew welcome messages
- OpenAI GPT-4o-mini integration
- Comprehensive error handling
- CORS enabled for cross-origin requests
- Environment variable configuration

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure your OpenAI API key in `.env`:
```env
OPENAI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

3. Start the server:
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

## API Endpoints

### GET /welcome-message

Generates a short, creative welcome message in Hebrew for a new user.

**Response (Success):**
```json
{
  "success": true,
  "message": "שלום! ברוכים הבאים לפלטפורמה שלנו. אנחנו שמחים שהצטרפת אלינו ואנחנו כאן כדי לעזור לך להצליח.",
  "language": "hebrew",
  "model": "gpt-4o-mini"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "OpenAI API error",
  "message": "Error details here",
  "type": "invalid_api_key"
}
```

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Welcome Message API is running",
  "endpoint": "/welcome-message"
}
```

## Error Handling

The server handles various error scenarios:

- **Missing API Key**: Returns 500 with clear error message
- **OpenAI API Errors**: Returns appropriate status code with error details
- **Network Errors**: Returns 503 for connection issues
- **Generic Errors**: Returns 500 with error message

## Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `PORT` (optional): Server port (defaults to 3000)

## Notes

- The welcome message is generated using GPT-4o-mini model
- Messages are kept short (2-3 sentences) and creative
- The system prompt ensures messages are warm and personal in Hebrew
