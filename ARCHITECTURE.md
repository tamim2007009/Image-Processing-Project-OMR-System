# 🏗️ Project Architecture

## Overview

This document provides a technical overview of the OMR Answer Sheet Scanner architecture for developers who want to understand or contribute to the codebase.

## 📁 File Structure

```
OMR/
│
├── main.py              # Main application entry point & GUI
├── config.py            # Configuration parameters
├── helper.py            # Image processing utilities
├── README.md            # Project documentation
├── QUICKSTART.md        # Quick start guide
├── CONTRIBUTING.md      # Contribution guidelines
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
├── .gitignore          # Git ignore patterns
│
├── __pycache__/        # Python cache (ignored by git)
└── snapshots/          # Output images (optional)
```

## 🔧 Core Components

### 1. main.py (1007 lines)

**Primary Functions:**

- `processImages(filepath)` - Core OMR processing pipeline
- `print_result()` - Orchestrates batch processing
- `save_to_excel(id_array, score_array)` - Exports results
- `show_result_summary(id_list, score_list)` - Console statistics
- `open_processing_popup()` - Upload/process dialog
- `update_config()` - Updates exam configuration
- `generate_answer_inputs()` - Dynamically creates answer key UI
- `save_answer_key()` - Validates and saves answer key

**Processing Pipeline (in processImages):**

```
1. Load Image
   └─> cv2.imread()

2. Preprocessing
   ├─> Resize (config.IMAGE_WIDTH × IMAGE_HEIGHT)
   ├─> Grayscale conversion
   ├─> Gaussian blur (noise reduction)
   └─> Canny edge detection

3. Contour Detection
   └─> helper.get_edge_points() [Custom algorithm]

4. Corner Detection
   └─> helper.find_corners() for each contour

5. Region of Interest (ROI) Extraction
   ├─> Identify largest contour (answer section)
   ├─> Apply corner offsets
   ├─> Smart filtering (optional edge exclusion)
   └─> Extract answer grid region

6. Answer Detection
   ├─> Binary thresholding
   ├─> Split into grid (questions × choices)
   ├─> Count pixels in each bubble
   └─> Identify maximum (selected answer)

7. Grading
   ├─> Compare with answer key
   ├─> Calculate score percentage
   ├─> Assign letter grade
   └─> Visualize results

8. Grade Section Processing
   └─> Extract and annotate grade region
```

### 2. helper.py (194 lines)

**Core Algorithms:**

#### Custom Contour Detection
```python
get_edge_points(image) -> List[List[Tuple]]
```
- **Purpose**: Detect answer sheet boundaries
- **Algorithm**: BFS for region growing + DFS for edge tracing
- **Advantages**: More accurate than cv2.findContours for OMR sheets
- **Returns**: List of contour point arrays

**Implementation Details:**
```python
# Phase 1: BFS to find connected components
def bfs(sx, sy):
    # Grows regions by exploring 8-connected neighbors
    # Switches to DFS when finding new edge points

# Phase 2: DFS for edge tracing
def dfs(image, sp_x, sp_y, to_replace, replace_with):
    # Traces longest path in connected component
    # Returns edge points representing contour
```

#### Geometric Processing
```python
find_corners(contour) -> List[Tuple]
```
- Extracts 4 corner points from contour
- Returns: [(top_left), (top_right), (bottom_left), (bottom_right)]
- Format: (row, col) coordinates

```python
splitBoxes(img) -> List[np.ndarray]
```
- Divides answer grid into individual bubbles
- Uses: np.vsplit() and np.hsplit()
- Returns: Flattened list of bubble images

```python
showAnswers(img, myIndex, questions, answers, choices, grading) -> np.ndarray
```
- Visualizes grading on answer sheet
- Green circles: Correct answers
- Red circles: Incorrect (with correct answer shown)

#### Utility Functions
```python
countNonZeroPixel(img) -> int
```
- Counts filled pixels in bubble
- Higher count = bubble is filled

```python
thresholdImage(img, thres, threshold) -> np.ndarray
```
- Converts to binary (black/white)
- Optimized implementation using np.where()

```python
manual_draw_contours(img, contours, color, thickness)
```
- Custom contour drawing
- Used for visualization

### 3. config.py (116 lines)

**Configuration Categories:**

#### Image Processing
```python
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 500
BLUR_KERNEL_SIZE = (5, 5)
BLUR_SIGMA = 1
CANNY_THRESHOLD1 = 50
CANNY_THRESHOLD2 = 150
THRESHOLD_VALUE = 170
```

#### Exam Setup
```python
NUM_QUESTIONS = 10
NUM_CHOICES = 5
ANSWER_KEY = [0, 0, 0, ...]  # 0-indexed
```

#### Region Adjustments
```python
ANSWER_CORNER_OFFSET = {...}   # Fine-tune answer ROI
GRADE_CORNER_OFFSET = {...}    # Fine-tune grade ROI
BORDER_PADDING = {...}         # Add margins to ROI
EDGE_EXCLUSION_MARGIN = 0      # Filter corner markers
```

#### Grading System
```python
PASS_MARK = 40.0
GRADE_BOUNDARIES = {'A': 80, 'B': 60, 'C': 40, 'F': 0}
```

#### Validation
```python
validate_config() -> bool
```
- Validates all configuration parameters
- Checks answer key length matches questions
- Ensures answer indices are valid
- Verifies kernel sizes are odd
- Auto-runs on import

## 🔄 Data Flow

```
User Input (GUI)
    ↓
Config Update (config.py)
    ↓
Image Upload
    ↓
processImages() [main.py]
    ├─> Image Loading & Preprocessing
    ├─> get_edge_points() [helper.py]
    ├─> find_corners() [helper.py]
    ├─> ROI Extraction
    ├─> splitBoxes() [helper.py]
    ├─> countNonZeroPixel() [helper.py]
    ├─> Answer Detection
    ├─> Grading Logic
    └─> showAnswers() [helper.py]
    ↓
Results Collection (id[], res[])
    ↓
show_result_summary() [console]
    ↓
save_to_excel() [Excel file]
```

## 🎨 GUI Architecture

Built with **Tkinter** (Python's standard GUI library)

### Main Window Components

1. **Header Section**
   - Title and subtitle
   - Professional branding

2. **Configuration Section**
   - Number of questions input
   - Number of choices input
   - Apply button

3. **Answer Key Section**
   - Dynamically generated grid
   - Scrollable for many questions
   - Individual input fields per question
   - Save button

4. **Status Label**
   - Real-time feedback
   - Color-coded messages

5. **Info Section**
   - Usage instructions
   - Step-by-step guide

### Popup Window (Processing Center)

1. **Configuration Summary**
   - Current settings display

2. **Upload Section**
   - File selection button
   - Thumbnail preview canvas
   - Horizontal scrollbar
   - Status indicator

3. **Action Buttons**
   - Process all images
   - Cancel

## 🧮 Algorithm Complexity

| Function | Time Complexity | Space Complexity |
|----------|----------------|------------------|
| get_edge_points | O(W × H) | O(W × H) |
| find_corners | O(N) | O(1) |
| splitBoxes | O(Q × C) | O(Q × C) |
| countNonZeroPixel | O(pixels) | O(1) |
| processImages | O(W × H) | O(W × H) |

Where:
- W, H = image width and height
- N = contour points
- Q = number of questions
- C = number of choices

## 🔐 Error Handling

### Defensive Programming Patterns

1. **Widget Existence Checks**
```python
try:
    if not widget.winfo_exists():
        return
except tk.TclError:
    return
```

2. **ROI Validation**
```python
if wd <= 0 or ht <= 0:
    # Fallback to original corners
    # Log warning
```

3. **File Operations**
```python
try:
    wb.save(excel_filename)
except Exception as e:
    # Attempt desktop fallback
    # Log error
```

## 🎯 Key Design Decisions

### 1. Custom Contour Detection
- **Why**: OpenCV's findContours sometimes misses boundaries
- **Benefit**: Better accuracy for OMR sheets
- **Trade-off**: More complex code

### 2. Global State Management
```python
uploaded_images = []
thumbnail_images = []
id = []
res = []
```
- **Why**: Simplifies data sharing between functions
- **Trade-off**: Not thread-safe (OK for single-threaded GUI)

### 3. Step-by-Step Visualization
```python
cv2.imshow("Step Name", image)
cv2.waitKey(0)
```
- **Why**: Educational and debugging purposes
- **Future**: Could be toggled via config

### 4. Configuration-Driven Design
- All parameters externalized to config.py
- Easy customization without code changes
- Validation ensures consistency

## 🚀 Performance Optimization Opportunities

1. **Parallel Processing**: Process multiple images concurrently
2. **Caching**: Cache processed thumbnails
3. **GPU Acceleration**: Use cv2.cuda for supported operations
4. **Batch ROI Extraction**: Vectorize bubble analysis
5. **Adaptive Thresholding**: Use cv2.adaptiveThreshold for varying lighting

## 🧪 Testing Strategy

### Current Testing
- Manual visual inspection
- Step-by-step image display
- Console output validation

### Recommended Additions
1. Unit tests for helper functions
2. Integration tests for full pipeline
3. Regression tests with sample images
4. Performance benchmarks

## 📚 Dependencies Rationale

| Library | Purpose | Version |
|---------|---------|---------|
| opencv-python | Image processing & computer vision | 4.5.0+ |
| numpy | Numerical operations & arrays | 1.19.0+ |
| openpyxl | Excel file generation | 3.0.0+ |
| Pillow | GUI thumbnails & image handling | 8.0.0+ |

## 🔮 Extension Points

### Easy to Add
- [ ] Different answer sheet layouts
- [ ] Configurable grading scales
- [ ] Multiple answer keys
- [ ] Student photo extraction
- [ ] QR code support for IDs

### Medium Difficulty
- [ ] Automatic skew correction
- [ ] Machine learning for bubble detection
- [ ] Web interface
- [ ] Database integration
- [ ] Batch report generation (PDF)

### Advanced
- [ ] Real-time processing (webcam)
- [ ] Mobile app
- [ ] Cloud processing
- [ ] Handwriting recognition for IDs

## 📖 Further Reading

- [OpenCV Documentation](https://docs.opencv.org/)
- [NumPy User Guide](https://numpy.org/doc/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [Computer Vision: Algorithms and Applications](http://szeliski.org/Book/)

---

**Last Updated**: November 5, 2025
