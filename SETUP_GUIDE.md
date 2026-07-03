# 📥 How to Extract & Setup GARUDA on Your Laptop

Complete step-by-step guide to download, extract, and run GARUDA on **Windows**, **macOS**, or **Linux**.

---

## 🖥️ Prerequisites (All Platforms)

Before you start, download and install these:

### 1. Git
- **Windows/macOS/Linux**: Download from [git-scm.com](https://git-scm.com/downloads)
- Verify installation:
  ```bash
  git --version
  ```

### 2. Python 3.11+
- **Windows/macOS**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: 
  ```bash
  sudo apt-get update
  sudo apt-get install python3 python3-pip python3-venv
  ```
- Verify installation:
  ```bash
  python --version
  # or
  python3 --version
  ```

### 3. Node.js & npm
- Download from [nodejs.org](https://nodejs.org/) (LTS version recommended)
- Verify installation:
  ```bash
  node --version
  npm --version
  ```

### 4. Code Editor (Optional but Recommended)
- **VS Code**: [Download here](https://code.visualstudio.com/)
- **PyCharm**: [Download here](https://www.jetbrains.com/pycharm/)

---

## 📋 Step-by-Step Setup Guide

### STEP 1: Clone/Download the Repository

#### Option A: Using Git (Recommended)

**Windows (Command Prompt or PowerShell):**
```bash
git clone https://github.com/parthg2106/GARUDA-agent.git
cd GARUDA-agent
```

**macOS/Linux (Terminal):**
```bash
git clone https://github.com/parthg2106/GARUDA-agent.git
cd GARUDA-agent
```

#### Option B: Download as ZIP

1. Go to: https://github.com/parthg2106/GARUDA-agent
2. Click **Code** → **Download ZIP**
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt and navigate to the extracted folder:

**Windows (Command Prompt):**
```cmd
cd path\to\GARUDA-agent
```

**macOS/Linux (Terminal):**
```bash
cd path/to/GARUDA-agent
```

---

### STEP 2: Backend Setup (Python)

#### For Windows:

```cmd
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt
```

Your prompt should now show `(venv)` at the beginning, like:
```
(venv) C:\Users\YourName\GARUDA-agent>
```

#### For macOS/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

Your prompt should now show `(venv)` at the beginning, like:
```
(venv) user@computer GARUDA-agent %
```

**✅ If you see `(venv)` in your terminal, you're good to go!**

---

### STEP 3: Frontend Setup (React/Node.js)

#### For All Platforms (Windows/macOS/Linux):

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Go back to root directory
cd ..
```

**Note:** The `npm install` command may take 2-5 minutes. Don't close the terminal.

---

### STEP 4: Create Environment Configuration File

#### For Windows (Command Prompt):
```cmd
REM Create .env file in the root directory
echo # Backend Configuration > .env
echo BACKEND_URL=http://localhost:8000 >> .env
echo FASTAPI_ENV=development >> .env
echo LOG_LEVEL=INFO >> .env
echo. >> .env
echo # Frontend Configuration >> .env
echo REACT_APP_API_URL=http://localhost:8000/api/v1 >> .env
echo REACT_APP_WS_URL=ws://localhost:8000/ws >> .env
```

#### For Windows (PowerShell):
```powershell
@"
# Backend Configuration
BACKEND_URL=http://localhost:8000
FASTAPI_ENV=development
LOG_LEVEL=INFO

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
"@ | Out-File -FilePath .env -Encoding UTF8
```

#### For macOS/Linux:
```bash
cat > .env << EOF
# Backend Configuration
BACKEND_URL=http://localhost:8000
FASTAPI_ENV=development
LOG_LEVEL=INFO

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
EOF
```

---

### STEP 5: Start the Application

You need **2 terminal windows** (or tabs) open.

#### Terminal 1: Start Backend Server

**Windows:**
```cmd
REM Activate virtual environment (if not already activated)
venv\Scripts\activate

REM Start FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**macOS/Linux:**
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Start FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**✅ Backend is ready when you see `Application startup complete`**

---

#### Terminal 2: Start Frontend Server

**All Platforms:**
```bash
# Navigate to frontend folder
cd frontend

# Start React development server
npm start
```

**Expected output:**
```
  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

**✅ Frontend is ready when you see the local URL message**

---

## 🌐 Access the Application

Once both servers are running, open your web browser:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend Dashboard** | http://localhost:3000 | Main UI/dashboard |
| **API Documentation** | http://localhost:8000/api/docs | Interactive API explorer |
| **Health Check** | http://localhost:8000/api/v1/health | Backend status |

---

## ⚠️ Troubleshooting

### Problem: "Python not found" or "Python is not recognized"

**Solution:**
- Make sure Python is installed: Download from [python.org](https://www.python.org/downloads/)
- **Windows**: Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

**Verify:**
```bash
python --version
python3 --version
```

---

### Problem: "npm not found" or "Node is not recognized"

**Solution:**
- Make sure Node.js is installed: Download from [nodejs.org](https://nodejs.org/)
- Restart your computer after installation

**Verify:**
```bash
node --version
npm --version
```

---

### Problem: Virtual environment won't activate

**Windows:**
```cmd
REM Try this instead:
python -m venv venv
python venv\Scripts\activate.bat
```

**If still not working:**
```cmd
REM Use PowerShell instead of Command Prompt
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

---

### Problem: "ModuleNotFoundError" when starting backend

**Solution:**
1. Make sure virtual environment is activated (you should see `(venv)` in terminal)
2. Try reinstalling dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### Problem: "Cannot find module" errors on frontend

**Solution:**
```bash
cd frontend
npm install
npm start
```

---

### Problem: Port 8000 or 3000 already in use

**Use different ports:**

**Terminal 1 (Backend on different port):**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 (Frontend on different port):**
```bash
cd frontend
PORT=3001 npm start
```

---

## 🎓 Quick Reference Commands

### Windows

```cmd
REM Initial Setup
git clone https://github.com/parthg2106/GARUDA-agent.git
cd GARUDA-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd frontend && npm install && cd ..

REM Starting Application
REM Terminal 1:
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

REM Terminal 2:
cd frontend
npm start
```

### macOS/Linux

```bash
# Initial Setup
git clone https://github.com/parthg2106/GARUDA-agent.git
cd GARUDA-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Starting Application
# Terminal 1:
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2:
cd frontend
npm start
```

---

## 📊 Verify Everything is Working

### 1. Check Backend API

Open browser and visit: **http://localhost:8000/api/docs**

You should see the Swagger UI documentation.

### 2. Check Frontend Dashboard

Open browser and visit: **http://localhost:3000**

You should see the GARUDA dashboard interface.

### 3. Test API Health

Open terminal and run:

**Windows:**
```cmd
curl http://localhost:8000/api/v1/health
```

**macOS/Linux:**
```bash
curl http://localhost:8000/api/v1/health
```

**Expected response:**
```json
{"status": "healthy", "timestamp": "2024-01-01T12:00:00"}
```

---

## 🚀 Next Steps

Once everything is running:

1. **Explore the Dashboard**: http://localhost:3000
2. **Read API Documentation**: http://localhost:8000/api/docs
3. **Train AI Models** (optional):
   ```bash
   python training/train_models.py
   ```
4. **Run Tests**:
   ```bash
   pytest tests/ -v
   ```
5. **Read Main README** for more details: `README.md`

---

## 💡 Pro Tips

### Tip 1: Use VS Code for Development
- Download [VS Code](https://code.visualstudio.com/)
- Install extensions: Python, REST Client, Thunder Client
- Open the GARUDA folder in VS Code

### Tip 2: Keep Terminal Windows Organized
- Use different tabs/windows for backend and frontend
- Name them clearly (e.g., "GARUDA Backend", "GARUDA Frontend")

### Tip 3: Check Logs
- Backend logs appear in Terminal 1
- Frontend logs appear in Terminal 2
- Look for errors starting with `ERROR:` or `Traceback`

### Tip 4: Stop the Application
- Press `Ctrl + C` in both terminals to stop the servers

### Tip 5: Database/Cache Issues
If you encounter strange errors:
```bash
# Remove cache files
rm -rf __pycache__ .pytest_cache
cd frontend && rm -rf node_modules .next && npm install && cd ..
```

---

## 📞 Need Help?

If you get stuck:

1. **Check error messages** - Read the full error in terminal
2. **Google the error** - Most Python/Node errors have solutions online
3. **Check GitHub Issues**: https://github.com/parthg2106/GARUDA-agent/issues
4. **Check Prerequisites** - Make sure Git, Python, and Node are installed correctly

---

## ✅ Setup Checklist

- [ ] Installed Git
- [ ] Installed Python 3.11+
- [ ] Installed Node.js
- [ ] Cloned/Downloaded repository
- [ ] Created Python virtual environment
- [ ] Installed Python dependencies
- [ ] Installed Node dependencies
- [ ] Created `.env` file
- [ ] Started backend server (Terminal 1)
- [ ] Started frontend server (Terminal 2)
- [ ] Accessed dashboard at http://localhost:3000
- [ ] Verified API at http://localhost:8000/api/docs

---

**Congratulations! 🎉 You're all set to explore GARUDA!**

For more information, see the main [README.md](README.md)
