
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 500


BLUR_KERNEL_SIZE = (5, 5)  
BLUR_SIGMA = 1

CANNY_THRESHOLD1 = 50
CANNY_THRESHOLD2 = 150

THRESHOLD_VALUE = 170


NUM_QUESTIONS = 10
NUM_CHOICES = 5


ANSWER_KEY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


ANSWER_CORNER_OFFSET = {
    'top_left_x': 0,      
    'top_left_y': 0,       
    'bottom_right_x': 0,   
    'bottom_right_y': 0    
}


CROP_RATIO = 1.0  



BORDER_PADDING = {
    'top': 0,       
    'bottom': 0,    
    'left': 0,     
    'right': 0      
}


EDGE_EXCLUSION_MARGIN = 0  



PASS_MARK = 40.0

GRADE_BOUNDARIES = {
    'A': 80,  
    'B': 60,  
    'C': 40,  
    'F': 0    
}



SHOW_INTERMEDIATE_STEPS = True


GRADE_CORNER_OFFSET = {
    'top_left_x': 0,        
    'top_left_y': 0,        
    'bottom_right_x': 0,    
    'bottom_right_y': 0     
}


GRADE_TEXT_POSITION = (240, 390)
GRADE_TEXT_FONT = 1  
GRADE_TEXT_SCALE = 1.5
GRADE_TEXT_COLOR = (0, 255, 0) 
GRADE_TEXT_THICKNESS = 3



GUI_WIDTH = 600
GUI_HEIGHT = 400

GUI_BG_COLOR = "#1E8F91"
GUI_BUTTON_COLOR = "#4CAF50"
GUI_TEXT_COLOR = "#ffffff"

THUMBNAIL_SIZE = (100, 100)


def validate_config():
    
    errors = []
    
    if len(ANSWER_KEY) != NUM_QUESTIONS:
        errors.append(f"ANSWER_KEY length ({len(ANSWER_KEY)}) doesn't match NUM_QUESTIONS ({NUM_QUESTIONS})")
    
    for idx, ans in enumerate(ANSWER_KEY):
        if not (0 <= ans < NUM_CHOICES):
            errors.append(f"ANSWER_KEY[{idx}] = {ans} is invalid. Must be between 0 and {NUM_CHOICES-1}")
    
    if BLUR_KERNEL_SIZE[0] % 2 == 0 or BLUR_KERNEL_SIZE[1] % 2 == 0:
        errors.append(f"BLUR_KERNEL_SIZE must have odd dimensions, got {BLUR_KERNEL_SIZE}")
    
    if not (0 < CROP_RATIO <= 1):
        errors.append(f"CROP_RATIO must be between 0 and 1, got {CROP_RATIO}")
    
    if errors:
        print(" Configuration Errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("Configuration validated successfully!")
    return True


# Run validation when imported
if __name__ != "__main__":
    validate_config()
