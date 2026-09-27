# TgImg - Free Telegram Image Server

A lightweight, self-hosted image hosting solution that uses the Telegram Bot API as an unlimited free cloud storage backend.

## Features
- **Unlimited Storage**: Uses your personal Telegram Private Channel to store images.
- **Drag & Drop UI**: A beautiful, modern interface built with Tailwind CSS.
- **Direct Image Streaming**: Serves images directly to users without exposing your Telegram chat IDs or API tokens.
- **Fast Caching**: Images are cached in the browser for up to 1 year for maximum performance.
- **Custom Links**: Generates clean, short URLs for your images.

## Setup Instructions
1. Clone this repository.
2. Run python -m venv venv and activate it.
3. Install dependencies: pip install -r requirements.txt (Contains django, requests, python-dotenv).
4. Rename .env.example to .env and add your Telegram Bot Token and Channel ID.
5. Run migrations: python manage.py migrate.
6. Start the server: python manage.py runserver.
