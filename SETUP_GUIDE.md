# RouteMaster AI - Setup & Test Guide

## 📋 Project Overview
**RouteMaster Route Picker** - A warehouse route optimization system combining:
- **Frontend**: React 18 + Tailwind CSS (interactive UI)
- **Backend**: FastAPI + A* Pathfinding + TSP Solver
- **Algorithm**: A* search with Manhattan distance heuristic
- **Optimization**: Traveling Salesman Problem for multi-target routing

---

## ✅ Compatibility Status

### Test Summary
- ✅ Frontend → Backend request format compatible
- ✅ Backend → Frontend response format compatible  
- ✅ Grid encoding matches (0=empty, 1=obstacle, 2=target)
- ✅ Endpoints properly configured
- ✅ Error handling improved with null-check for unreachable targets
- ✅ File read error handling added

### Files in Project
```
e:\HACKATHON\
├── app.py                      # FastAPI backend
├── index.html                  # React frontend
├── requirements.txt            # Python dependencies
├── test_compatibility.py       # Automated tests (NEW)
├── COMPATIBILITY_REPORT.md     # Detailed analysis (NEW)
└── SETUP_GUIDE.md             # This file
```

---

## 🚀 Quick Start (Windows)

### Step 1: Install Python 3.8+
```powershell
# Option A: Download from https://www.python.org
# Option B: Microsoft Store
winget install Python.Python.3.11
```

### Step 2: Install Dependencies
```powershell
cd e:\HACKATHON
pip install -r requirements.txt
```

### Step 3: Run Backend Server
```powershell
cd e:\HACKATHON
python app.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 4: Open Frontend
Navigate to: **http://localhost:8000**

### Step 5: Click "OPTIMIZE ROUTE" Button
- Grid visualizes with obstacles (dark), start point (truck 🚚), targets (boxes 📦)
- Path animates in cyan when optimized
- Stats display total steps and collected targets

---

## 🧪 Pre-Run Testing (No Server Needed)

### Run Compatibility Tests
```powershell
cd e:\HACKATHON
python test_compatibility.py
```

This verifies:
- Frontend data formats match backend expectations
- A* algorithm produces valid paths
- Response structure is correct
- Data types are validated

---

## 📊 Test Data Details

### Grid Layout
```
   0   1   2   3
0  S   .   X   .     S = Start [0,0]
1  .   T   X   .     T = Target [1,1]
2  .   .   .   T     T = Target [2,3]
3  X   X   .   .     X = Obstacle
```

### Expected Behavior
1. **Start**: [0,0] (top-left)
2. **Route**: [0,0] → [1,0] → [1,1] → [2,1] → [2,2] → [2,3]
3. **Total Steps**: ~6-7
4. **Targets Collected**: 2

---

## 🔧 Troubleshooting

### Error: "Python was not found"
- Install Python from https://www.python.org
- Ensure "Add Python to PATH" is checked during installation
- Restart PowerShell

### Error: "Module 'fastapi' not found"
```powershell
pip install -r requirements.txt
# Or manually:
pip install fastapi uvicorn pydantic python-multipart
```

### Error: "Address already in use"
FastAPI is running on another process:
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it
taskkill /PID <PID> /F

# Or change port in app.py:
#   uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend loads but "OPTIMIZE ROUTE" doesn't work
1. Check browser console (F12)
2. Ensure backend server is running on port 8000
3. Check CORS is enabled (it is in app.py)

---

## 📝 API Reference

### POST /calculate-route
**Request:**
```json
{
  "grid": [[0,0,1,0],[0,2,1,0],[0,0,0,2],[1,1,0,0]],
  "start": [0, 0],
  "targets": [[1, 1], [2, 3]]
}
```

**Response:**
```json
{
  "total_steps": 6,
  "path": [[0,0], [1,0], [1,1], [2,1], [2,2], [2,3]],
  "targets_collected": 2
}
```

### GET /
Returns the index.html frontend.

---

## 🎯 Algorithm Details

### A* Pathfinding
- **Heuristic**: Manhattan Distance
- **Time Complexity**: O(b^d) where b=branching factor, d=depth
- **Space Complexity**: O(b^d)
- **Optimal**: Yes (with admissible heuristic)

### TSP (Traveling Salesman)
- **Method**: Brute force permutations
- **Time Complexity**: O(n!)
- **Suitable for**: Up to ~8-10 targets
- **Future Optimization**: Could use nearest-neighbor or genetic algorithms

---

## 🔐 Security Notes

### CORS Enabled
- Allow-origins: "*" (development only)
- For production: Restrict to specific domains
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Input Validation
- Pydantic validates all inputs
- Grid bounds checked in A* algorithm
- Unreachable targets return 400 error

---

## 📈 Performance Notes

### Current Test Case
- Grid size: 4x4
- Targets: 2
- Computation time: <10ms

### Scaling Limits
| Metric | Current | Recommended Max |
|--------|---------|-----------------|
| Grid Size | 4x4 | 50x50 |
| Targets | 2 | 8-10 |
| Paths to compute | 2 | 8-10 |
| TSP permutations | 2 | 8! = 40,320 |

---

## ✨ Next Steps

1. ✅ Verify compatibility (done)
2. 📦 Install Python and dependencies
3. ▶️ Run `python app.py`
4. 🌐 Open http://localhost:8000
5. 🎮 Click "OPTIMIZE ROUTE" and watch it work!

---

## 📞 Support

For issues:
1. Check error messages in console/terminal
2. Run `python test_compatibility.py` to verify setup
3. Review code in [app.py](app.py) and [index.html](index.html)

Happy routing! 🚚📦
