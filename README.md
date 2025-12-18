# Auto Parts Request Website 🚗

A bilingual (English/Spanish) customer-facing website for managing auto parts requests.

## Features

### Customer Side
- 📱 **iPhone-style language selector** (English/Spanish)
- 📝 **Simple request form** with vehicle & part details
- ✅ **Instant confirmation** after submission
- 🌐 **Fully bilingual** interface

### Admin Side
- 📊 **Dashboard** with statistics
- 💰 **Send quotes** to customers
- 📸 **Track deposit requirements**
- ✅ **Mark requests as completed**
- 🗂️ **Filter by status** (New, Quoted, Completed)

## How to Run Locally

### 1. Install Python
Make sure you have Python 3.8+ installed

### 2. Install Dependencies
```bash
cd Parts_Request_Website
pip install -r requirements.txt
```

### 3. Run the Website
```bash
python app.py
```

The website will start on:
- **Customer Page:** http://localhost:5001
- **Admin Panel:** http://localhost:5001/admin

## How It Works

### For Customers:
1. Visit your website
2. Select language (English or Español)
3. Fill out the part request form:
   - Name, Phone, Email
   - Vehicle Year, Make, Model, Color
   - Part needed
   - Additional notes
4. Submit and receive confirmation
5. Wait for your quote via phone/email

### For You (Admin):
1. Go to `/admin`
2. View all incoming requests
3. Click "Send Quote" on any request
4. Enter:
   - Quote amount
   - Deposit amount required
   - Message to customer
5. Send the quote (you'll need to contact them via phone with the details)
6. Mark as complete when done

## Deploying Online (Making it Public)

### Option 1: Render.com (FREE)

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub (upload this folder to GitHub first)
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Deploy!

You'll get a free URL like: `https://your-parts-website.onrender.com`

### Option 2: PythonAnywhere (FREE)

1. Sign up at https://www.pythonanywhere.com
2. Upload your files
3. Set up a Flask app in their dashboard
4. Free URL: `https://yourusername.pythonanywhere.com`

### Option 3: Heroku (Paid, but simple)

1. Install Heroku CLI
2. Create `Procfile`:
```
web: python app.py
```
3. Deploy:
```bash
heroku create your-parts-site
git push heroku main
```

## Database

All customer requests are stored in `customer_requests.json`

**IMPORTANT:** Back this file up regularly! It contains all your customer data.

## Customization

### Change Port
In `app.py`, change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Add Your Business Info
Edit the templates to add:
- Your business name
- Phone number
- Location
- Photos

### Translations
All text is in the HTML templates. Search for `{% if language == 'en' %}` to find and edit translations.

## Security Notes

⚠️ **Before going live:**

1. **Change the secret key** in `app.py`:
```python
app.config['SECRET_KEY'] = 'create-a-random-long-string-here'
```

2. **Add admin password protection** (optional but recommended)
3. **Set up HTTPS** (most hosting platforms do this automatically)

## File Structure

```
Parts_Request_Website/
├── app.py                      # Main application
├── customer_requests.py        # Database handler
├── customer_requests.json      # Data storage (auto-created)
├── requirements.txt            # Dependencies
├── templates/
│   ├── index.html             # Language selector
│   ├── request_form.html      # Customer form
│   ├── thank_you.html         # Confirmation page
│   └── admin.html             # Admin dashboard
└── README.md                  # This file
```

## Support

Need help? Common issues:

### "Port already in use"
Change the port in `app.py` to 5002 or 5003

### "Module not found"
Run: `pip install -r requirements.txt`

### Can't access admin panel
Make sure you're going to: `http://localhost:5001/admin`

## Future Enhancements (Ideas)

- 📧 Email notifications when new request comes in
- 💬 SMS integration (Twilio)
- 📷 Allow customers to upload photos
- 💳 Accept deposits online (Stripe, PayPal)
- 📱 Mobile app version
- 🔐 Admin login with password

---

Built with ❤️ for your auto parts business!
