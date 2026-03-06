# Python Installation Guide for RouteMaster AI

## ❌ Current Status: Python NOT Found

The system has a **Microsoft Store Python alias** that blocks real Python installation.

---

## ✅ Solution: Install Real Python 3.11

### Option 1: Direct Download (Recommended)

1. **Download Python 3.11** from: https://www.python.org/downloads/windows/
   - Choose: **Windows installer (64-bit)** for modern systems
   
2. **Run the Installer**
   - ✅ **IMPORTANT**: Check the box: `Add Python 3.11 to PATH`
   - Choose: "Customize Installation"
   - Verify pip, IDLE, and other tools are selected
   - Install for: "All Users" (recommended)

3. **Verify Installation**
   ```powershell
   python --version
   pip --version
   ```
   Both should show version numbers without errors.

### Option 2: Download with winget

```powershell
# Remove blocking alias first
Remove-Item "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe" -Force -ErrorAction Ignore

# Install Python
winget install Python.Python.3.11

# Verify
python --version
```

### Option 3: Download with Chocolatey

```powershell
# Install Chocolatey if you don't have it
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python -y

# Verify
python --version
```

---

## 🔧 After Installation

Once Python is installed, run:

```powershell
cd e:\HACKATHON

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_compatibility.py

# Start server
python app.py

# Open browser to http://localhost:8000
```

---

## 🆘 Troubleshooting

### Still Getting "Python was not found"

**Solutions:**

1. **Restart PowerShell/Terminal** - Close and reopen completely
2. **Restart Computer** - Sometimes PATH needs system restart
3. **Check PATH Environment Variable**
   ```powershell
   $env:PATH -split ";" | Select-String -Pattern "Python"
   # Should show something like: C:\Users\[User]\AppData\Local\Programs\Python\Python311
   ```

4. **Manually Add to PATH** (if needed)
   - Hit Windows key, search: "Environment Variables"
   - Click: "Edit the system environment variables"
   - Click: "Environment Variables" button
   - Under "User variables", click "New"
   - Variable name: PATH
   - Variable value: `C:\Users\Rishab\AppData\Local\Programs\Python\Python311`
   - Click OK, close dialogs, **restart PowerShell**

### Pip not found after Python installs

```powershell
# Try:
python -m pip --version

# If that works, you can use:
python -m pip install -r requirements.txt
```

---

## 📥 Direct Download Links

- **Python 3.11.8** (64-bit): https://www.python.org/downloads/release/python-3118/
- **Python 3.12** (latest): https://www.python.org/downloads/

**Select file**: `Windows installer (64-bit)`

---

## ✅ Verification Checklist

After installation, these commands should work:

```powershell
# Check Python
python --version
# Should show: Python 3.x.x

# Check Pip
pip --version
# Should show: pip x.x.x from ...

# Test import
python -c "import sys; print(sys.executable)"
# Should show: C:\Users\...\Python\python.exe
```

---

## 🎯 Next Steps

1. **Install Python 3.11** from: https://www.python.org/downloads/
2. **Restart PowerShell**
3. **Run from e:\HACKATHON**:
   ```powershell
   pip install -r requirements.txt
   python test_compatibility.py
   python app.py
   ```
4. **Open**: http://localhost:8000

---

**Status**: Waiting for Python installation  
**Action Required**: Download and install Python 3.11+  
**Estimated Time**: 5-10 minutes
