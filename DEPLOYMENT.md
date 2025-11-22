# How to Deploy to Streamlit Cloud ☁️

Follow these steps to put your app online so your mom can use it from anywhere!

## Prerequisites
1.  **GitHub Account**: You already have this since the code is in a repo.
2.  **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io/) (connect it with your GitHub).

## Step 1: Push Code to GitHub
Make sure your latest changes (including the new download button) are pushed to your GitHub repository.

```bash
git add .
git commit -m "Prepare for cloud deployment"
git push
```

## Step 2: Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  **Repository**: Select your repo (`tts_mae`).
4.  **Branch**: `main` (or `master`).
5.  **Main file path**: `app.py`.
6.  Click **"Deploy!"**.

## Step 3: Configure Secrets (API Key) 🔑
The app will fail initially because it doesn't have the Google API Key. You need to add it securely.

1.  On your deployed app's dashboard, click the **"Manage app"** button (bottom right) or the **Settings** menu (three dots).
2.  Go to **"Settings"** -> **"Secrets"**.
3.  Paste the following into the text box (replace `YOUR_API_KEY` with your actual key from your `.env` file):

```toml
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
```

4.  Click **"Save"**.

## Step 4: Share! 🚀
1.  The app should automatically restart and work.
2.  Copy the URL (e.g., `https://tts-mae-yourname.streamlit.app`).
3.  Send it to your mom! She can use it on her phone or computer.
