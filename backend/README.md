# AarogyaJal Backend API

This is the Python backend for the AarogyaJal water quality analyzer app. It provides API endpoints for the Gemini AI service to analyze water quality parameters and provide chatbot responses.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure the environment variables:
   - Create a `.env` file in the root directory
   - Add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

3. Run the server:
   ```
   cd app
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### GET /
- Returns a simple message confirming the API is running

### POST /chat
- Endpoint for chatbot functionality
- Request body: `{"query": "your question here"}`
- Returns: `{"response": "AI response text"}`

### POST /analyze
- Endpoint for water quality analysis
- Request body:
  ```json
  {
    "parameters": {
      "pH": 7.2,
      "turbidity": 5,
      "dissolved_oxygen": 8.5,
      "temperature": 25
    },
    "location": "Sample Location",
    "notes": "Optional notes"
  }
  ```
- Returns:
  ```json
  {
    "analysis": "Detailed analysis text",
    "timestamp": "2023-09-11T12:34:56.789Z"
  }
  ```