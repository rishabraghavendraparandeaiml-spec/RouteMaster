## ✅ Matrix Input Feature Added

### 📝 NEW UI Components

You can now enter start and targets as **matrix coordinates** directly in input fields!

#### Input Fields Added:
1. **Start Position**: `[row, col]`
2. **Targets**: `[[row, col], [row, col], ...]`
3. **Apply Matrix Input** button

### 📋 How to Use

#### Example 1: Single Target
```
Start:    [0, 0]
Targets:  [[2, 1]]
```
Click "Apply Matrix Input" → Start at (0,0), target at (2,1) will appear on grid

#### Example 2: Multiple Targets
```
Start:    [0, 0]
Targets:  [[2, 1], [3, 4], [5, 7]]
```
Click "Apply Matrix Input" → 3 home icons (🏠) will appear on grid

#### Example 3: Different Start
```
Start:    [1, 3]
Targets:  [[4, 2]]
```

### ⚠️ Important Notes

1. **0-indexed coordinates**: 
   - First row = 0, First column = 0
   - For 6x8 grid: rows are 0-5, columns are 0-7

2. **JSON format required**:
   - Start: `[0, 0]` ← square brackets, comma separated
   - Targets: `[[2, 1]]` ← double brackets for array of arrays
   - Multiple: `[[2, 1], [3, 4]]` ← comma between targets

3. **Validation**:
   - Checks if coordinates are within grid bounds
   - Prevents placing on obstacles
   - Shows error messages if invalid

### 🎯 Workflow

1. *(Optional)* Adjust grid size (Rows/Cols)
2. *(Optional)* Click "Create New Grid"
3. **Type start position**: e.g., `[0, 0]`
4. **Type targets**: e.g., `[[2, 1], [3, 5]]`
5. **Click "Apply Matrix Input"** ✅
6. *(Optional)* Add obstacles by clicking cells
7. **Click "Optimize Route"**
8. See results!

### 🔄 Refresh Browser

**Press Ctrl+F5** at http://localhost:8000 to see the new matrix input fields!

You'll see a yellow/amber box with:
- Start input field
- Targets input field  
- "Apply Matrix Input" button
