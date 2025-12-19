# PostgreSQL Database Setup for Railway

## What Changed?
Your app now saves customer requests to a PostgreSQL database instead of a JSON file. This means:
- ✅ Customer data persists forever (won't be deleted on redeploy)
- ✅ No more data loss when pushing updates
- ✅ Professional, scalable storage

## How to Set Up on Railway (5 minutes)

### Step 1: Add PostgreSQL to Your Railway Project
1. Go to https://railway.app
2. Open your project (carparts)
3. Click "New" → "Database" → "Add PostgreSQL"
4. Railway will create a PostgreSQL database and automatically add the `DATABASE_URL` environment variable

### Step 2: Connect the Database to Your App
Railway automatically connects the database to your app via the `DATABASE_URL` environment variable. Nothing else needed!

### Step 3: Deploy
1. Push your code (already done)
2. Railway will automatically redeploy with PostgreSQL
3. The database table will be created automatically on first run

### Step 4: Verify It's Working
1. Go to your website and submit a test request
2. Refresh the page - the request should still be there
3. Go to Railway dashboard → PostgreSQL → Data tab to see your data

## Local Development
When running locally (without DATABASE_URL), the app automatically falls back to using the JSON file. This means:
- Local testing still works normally
- No PostgreSQL needed on your computer
- Production uses PostgreSQL, local uses JSON

## Troubleshooting
**If requests aren't saving:**
1. Check Railway dashboard → PostgreSQL → Make sure it's running
2. Check your app logs for database connection errors
3. Make sure DATABASE_URL is set in environment variables

**If you see old test data:**
The old JSON data won't be automatically migrated. Once PostgreSQL is set up, new requests will go to the database.

## Need Help?
Check Railway docs: https://docs.railway.app/databases/postgresql
