# Yoruba Dream Interpreter AI

A lightweight, Vercel-ready web app that turns any dream description into a Yoruba spirituality-inspired interpretation. Users type a dream, submit, and receive symbol-based guidance pulled from Yoruba archetypes such as Oshun, Shango, Ogun, Oya, and more.

## Project Structure

```
.
├── api/
│   └── interpret.py      # Python serverless handler (Vercel)
├── app.js                # Frontend logic (fetch + UI state)
├── index.html            # Minimalist UI markup
├── public/               # Static assets go here (empty placeholder)
├── styles.css            # Yoruba-inspired styling
└── vercel.json           # Runtime configuration (Python 3.11)
```

## Requirements

- Node.js 18+ (for running `vercel dev` locally)
- Python 3.11 runtime provided by Vercel (no local Python dependency needed unless you want to run tests)
- Vercel CLI (`npm i -g vercel`) for local dev or deployment

## Local Development

1. **Install dependencies (only Vercel CLI needed)**
   ```bash
   npm install -g vercel
   ```

2. **Start the dev server**
   ```bash
   cd /Users/macbook/Desktop/chatbot
   vercel dev
   ```
   - Frontend served at `http://localhost:3000`
   - API endpoint lives at `http://localhost:3000/api/interpret`

3. **Use the app**
   - Open the local URL, enter any dream text, click **Interpret dream**.
   - The UI shows a loader while waiting and renders the interpretation response.

## Deployment (Vercel)

1. Log in (first time only):
   ```bash
   vercel login
   ```
2. From the project root:
   ```bash
   vercel deploy --prod
   ```
   Vercel auto-detects the frontend and Python serverless function using `vercel.json` and builds a globally distributed deployment.

## API Details

- **Endpoint**: `POST /api/interpret`
- **Payload**:
  ```json
  {
    "dream": "I was walking through a forest as lightning struck"
  }
  ```
- **Response**:
  ```json
  {
    "interpretation": "In Yoruba spirituality..."
  }
  ```
- Logic: keyword extraction → map to Yoruba archetypes → craft narrative. Missing keywords fall back to a general ori/ancestor message.

## Customizing / Extending

- Add new archetypes by updating `SYMBOLS` in `api/interpret.py`.
- Adjust styling/colors in `styles.css` for different visual themes.
- Enhance frontend messaging or add history/local storage in `app.js` if needed.

## Notes

- No database or external APIs are required; everything runs in-memory.
- All assets are static, making the project ideal for Vercel's free tier.
- Remember to place extra static files (images, favicons) in `public/`.
