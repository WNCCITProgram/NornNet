# Cloudflare Turnstile Setup

This guide explains how to integrate Cloudflare Turnstile bot protection with NornNet.

## What is Turnstile?

Cloudflare Turnstile is a CAPTCHA alternative that helps prevent bots from accessing your site. It runs in the background with minimal user friction.

## Setup Steps

### 1. Get Your Turnstile Keys

1. Log in to your Cloudflare dashboard: https://dash.cloudflare.com/
2. Navigate to **Turnstile** (or go directly to: `https://dash.cloudflare.com/?to=/:account/turnstile`)
3. Create a new site/widget:
   - **Site name**: NornNet (or any name you prefer)
   - **Domain**: `lab.wncc.edu` (or your actual domain)
   - **Widget mode**: Managed (recommended) or Non-Interactive
4. Copy your **Site Key** and **Secret Key**

### 2. Configure Environment Variables

Edit the `.env` file in the project root and add your keys:

```bash
TURNSTILE_SITE_KEY=your-site-key-from-cloudflare
TURNSTILE_SECRET=your-secret-key-from-cloudflare
```

**Important:** Never commit the `.env` file to git! It's already in `.gitignore`.

### 3. Install Dependencies

Install the required Python packages:

```powershell
# Activate your virtual environment first
.\.venv\Scripts\Activate.ps1

# Install/update packages
pip install -r requirements.txt
```

### 4. Restart the Application

```powershell
# Recycle the IIS app pool
.\recycle.ps1
```

## How It Works

### Frontend (User Side)
- A Turnstile widget appears above the chat input box
- Users complete the challenge (usually automatic/invisible)
- A token is generated and sent with each chat message

### Backend (Server Side)
- Flask receives the message + Turnstile token
- Validates the token with Cloudflare's API
- Only processes the message if validation succeeds
- Returns an error if token is missing or invalid

## Testing

### With Turnstile Enabled
1. Set both `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET` in `.env`
2. Restart the app
3. Visit the site - you should see the Turnstile widget
4. Complete the challenge and send a message

### Without Turnstile (Development)
1. Leave `TURNSTILE_SECRET` empty or remove it from `.env`
2. The widget won't appear and validation is skipped
3. Useful for local testing without needing Cloudflare keys

## Troubleshooting

### Widget doesn't appear
- Check that both keys are set in `.env`
- Verify `.env` is being loaded (check logs for any errors)
- Ensure `load_dotenv()` is called before accessing `os.getenv()`

### Validation fails
- Verify your **Secret Key** is correct
- Check that the domain matches what you registered in Cloudflare
- Look at `logs/main_app.log` for detailed error messages
- Ensure `requests` package is installed

### Token missing error
- The Turnstile widget may not have loaded yet
- Try refreshing the page
- Check browser console for JavaScript errors

## Security Notes

- **Site Key**: Public, visible in HTML source code (safe to expose)
- **Secret Key**: Private, used server-side only (never expose in frontend)
- The `.env` file is in `.gitignore` to prevent accidental commits
- Use `.env.example` as a template for other developers

## Cloudflare Turnstile Modes

- **Managed**: Adaptive challenge based on threat level (recommended)
- **Non-Interactive**: Invisible, runs automatically
- **Invisible**: Programmatically triggered (requires code changes)

For more information, see: https://developers.cloudflare.com/turnstile/
