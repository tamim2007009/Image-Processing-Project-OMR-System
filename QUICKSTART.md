# 🚀 Quick Start Guide

Get up and running with OMR Answer Sheet Scanner in under 5 minutes!

## ⚡ Installation (2 minutes)

1. **Download or Clone**
```bash
git clone https://github.com/tamim2007009/Image-Processing-Project-OMR-System.git
cd Image-Processing-Project-OMR-System
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## 🎯 First Run (3 minutes)

### Step 1: Launch the Application
```bash
python main.py
```

### Step 2: Configure Your Exam
- **Number of Questions**: Enter 10 (or your exam's question count)
- **Choices per Question**: Enter 5 (for A, B, C, D, E)
- Click **"✓ Apply Configuration"**

### Step 3: Set Answer Key
- Enter the correct answer for each question:
  - `0` = A
  - `1` = B
  - `2` = C
  - `3` = D
  - `4` = E
- Click **"✓ Save Answer Key"**

### Step 4: Process Answer Sheets
- In the popup window, click **"📁 Select Answer Sheets"**
- Choose your scanned images (PNG, JPG, etc.)
- Click **"🚀 Process All Images"**
- Watch the processing steps (press any key to continue)
- Save results to Excel

## 📋 Answer Sheet Format

Your answer sheets should have:
- ✅ Clear bubbles or boxes for answers
- ✅ Distinct answer section boundary
- ✅ Good contrast and lighting
- ✅ Minimal skew (< 15°)

## 💡 Pro Tips

1. **Scan Quality**: Use 300+ DPI for best results
2. **Lighting**: Ensure even lighting across the sheet
3. **Marks**: Fill bubbles completely with dark ink
4. **Testing**: Start with 1-2 sheets to verify settings

## ⚙️ Quick Configuration Changes

Edit `config.py` for common adjustments:

```python
# More sensitive bubble detection
THRESHOLD_VALUE = 160

# Different edge detection
CANNY_THRESHOLD1 = 30
CANNY_THRESHOLD2 = 100

# Different grading scale
PASS_MARK = 50.0
GRADE_BOUNDARIES = {'A': 90, 'B': 70, 'C': 50, 'F': 0}
```

## ❓ Common Issues

**Problem**: "No contours found"
**Solution**: Adjust `CANNY_THRESHOLD1` and `CANNY_THRESHOLD2`

**Problem**: Wrong answers detected
**Solution**: Increase `THRESHOLD_VALUE` for darker marks

**Problem**: ROI extraction fails
**Solution**: Adjust `ANSWER_CORNER_OFFSET` values

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to improve the project
- Open an issue on GitHub if you need help

## 🎉 That's It!

You're now ready to grade answer sheets automatically. Enjoy! 

For detailed documentation, see [README.md](README.md)
