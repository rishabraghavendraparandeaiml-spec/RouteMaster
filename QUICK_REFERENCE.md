# RouteMaster AI - Quick Reference

## 🚀 Getting Started (30 seconds)

### Windows Quick Start
1. Install Python: https://www.python.org
2. Run: `start.bat` in the HACKATHON folder
3. Choose option [4] to install + start
4. Open: http://localhost:8000

### Command Line Quick Start
```powershell
cd e:\HACKATHON
pip install -r requirements.txt
python app.py
```

---

## 📋 Common Commands

### Installation
```powershell
# Install all dependencies
pip install -r requirements.txt

# Install individual packages
pip install fastapi uvicorn pydantic
```

### Testing
```powershell
# Run compatibility tests (no server needed)
python test_compatibility.py

# This verifies:
# - Frontend/backend format compatibility
# - A* algorithm correctness
# - Data serialization
# - Response structure
```

### Running the Application
```powershell
# Start the server
python app.py

# Server should respond with:
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Then open: http://localhost:8000 in your browser
```

### Stopping the Server
```powershell
# Press CTRL+C in the terminal running the server
```

---

## 🔌 API Endpoints

### Interactive UI
- **GET** `/` → Opens web interface

### Route Calculation
- **POST** `/calculate-route` → Calculate optimal route
  
**Request Example:**
```bash
curl -X POST http://localhost:8000/calculate-route \
  -H "Content-Type: application/json" \
  -d '{
    "grid": [[0,0,1,0],[0,2,1,0],[0,0,0,2],[1,1,0,0]],
    "start": [0,0],
    "targets": [[1,1],[2,3]]
  }'
```

**Response Example:**
```json
{
  "total_steps": 6,
  "path": [[0,0], [1,0], [1,1], [2,1], [2,2], [2,3]],
  "targets_collected": 2
}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python from https://python.org, restart terminal |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Address in use" | Another app uses port 8000, kill it or use different port |
| "Connection refused" | Backend not running, execute `python app.py` |
| "CORS error" | Already configured in app.py, check browser console |
| "Grid not loading" | Clear browser cache (Ctrl+Shift+Del), hard refresh (Ctrl+F5) |

---

## 📊 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | FastAPI backend server |
| `index.html` | React frontend UI |
| `requirements.txt` | Python dependencies |
| `test_compatibility.py` | Automated testing suite |
| `start.bat` | Windows quick-start script |
| `SETUP_GUIDE.md` | Complete setup instructions |
| `COMPATIBILITY_REPORT.md` | Technical analysis |
| `VERIFICATION_SUMMARY.md` | Compatibility check results |

---

## ⚡ Performance Tips

### Optimize for Large Grids
- Increase memory: Use larger machines
- Reduce targets: Limit to 8-10 maximum
- Cache paths: Store computed A* paths

### Debug Slow Routes
```python
# Add timing to app.py:
import time
start = time.time()
# ... calculation ...
print(f"Route took {time.time() - start}s")
```

---

## 🎮 Frontend Features

### Controls
- **OPTIMIZE ROUTE** - Calculates best path
- **Grid Display** - 4x4 interactive grid
  - 🚚 = Start position
  - 📦 = Targets
  - ⬛ = Obstacles
  - 🟦 = Calculated path

### Real-time Stats
- Total Steps (number of moves)
- Targets Collected (how many reached)

---

## 📈 Algorithm Details

### A* Pathfinding
```
Heuristic: Manhattan Distance
Formula: cost = g(n) + h(n)
         g(n) = actual cost from start
         h(n) = estimated distance to goal
```

### TSP Solver
```
Method: Brute force permutations
Time: O(n!) where n = number of targets
Example: 8 targets = 40,320 permutations
```

---

## 🔐 Security

### Production Checklist
- [ ] Change CORS to specific domains
- [ ] Add authentication/API keys
- [ ] Use HTTPS/SSL
- [ ] Validate grid size limits
- [ ] Rate limit requests
- [ ] Add logging/monitoring
- [ ] Use environment variables for config

---

## 📞 Support Resources

- **Python.org**: https://www.python.org
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com

---

## ✅ Verification Checklist

Before going live:
- [ ] Ran `python test_compatibility.py`
- [ ] Verified backend starts with `python app.py`
- [ ] Opened http://localhost:8000 in browser
- [ ] Clicked "OPTIMIZE ROUTE" button
- [ ] Path animates correctly
- [ ] Stats display correctly
- [ ] No console errors

---

Last Updated: March 6, 2026
Status: ✅ VERIFIED
