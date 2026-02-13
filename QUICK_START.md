# Research Scholar Agent - Quick Start ⚡

## 3-Minute Setup

### Step 1: Activate Virtual Environment
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open Browser
Navigate to: **http://localhost:5000**

---

## Done! ✅

Your Research Scholar Agent is now running!

### Next Steps:
1. **Search a topic** (e.g., "machine learning", "climate change")
2. **Click results** to read full papers on arXiv
3. **Compare papers** using the dropdown selection
4. **View history** to see past searches

---

## Optional: Enable AI Summaries

To get AI-powered 3-4 line summaries (instead of text extraction):

### Get OpenAI API Key:
1. Go to https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key

### Set Environment Variable:

**PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Command Prompt:**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

Then restart the app: `python app.py`

---

## Features Available Now:
✅ Search arXiv papers  
✅ View summaries (text-based)  
✅ Compare papers  
✅ Search history  
✅ Academic UI  

🔄 Optional: AI summaries (with API key)  

---

## Need Help?

- **Port in use?** Change port in `app.py` last line
- **Missing packages?** Run `pip install -r requirements.txt` again
- **API issues?** Check your internet connection
- **Details?** See README.md for full documentation

---

## Keyboard Tips:
- `Enter` = Search
- `Ctrl+C` = Stop server
- Arrow keys = Navigate

**Happy researching! 📚**
