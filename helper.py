from collections import deque

import cv2
import numpy as np
import config

def splitBoxes(img):

    height, width = img.shape[:2]
    

    new_height = (height // config.NUM_QUESTIONS) * config.NUM_QUESTIONS
    new_width = (width // config.NUM_CHOICES) * config.NUM_CHOICES
    
    
    if height != new_height or width != new_width:
        img = cv2.resize(img, (new_width, new_height))
    
    rows = np.vsplit(img, config.NUM_QUESTIONS)
    boxes = [box for r in rows for box in np.hsplit(r, config.NUM_CHOICES)]
    return boxes

def showAnswers(img,myIndex,questions,answers,choices,grading):
    img = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    secW = int(img.shape[1]/choices)  
    secH = int(img.shape[0]/questions) 

    for x in range(0,questions):

        myAns = myIndex[x]
        cX = (myAns*secW) + secW//2
        cY = (x*secH) + secH//2

        if(grading[x] == 1):
            myColor = (0,255,0)
        else:
            myColor = (0,0,255)
            correctAns = answers[x]
            cv2.circle(img, ((correctAns*secW)+secW//2, (x*secH)+secH//2), 10, (0,255,0), cv2.FILLED)

        cv2.circle(img,(cX,cY),10,myColor,cv2.FILLED)
    return img

def countNonZeroPixel(img):
    return np.count_nonzero(img)



def manual_draw_contours(img, contours, color, thickness):
  
    for contour in contours:
        y=contour[1] + 10
        x=contour[0] + 10
        cv2.circle(img, (y,x), radius=1, color=color, thickness=thickness)

def find_corners(contour):


    contour_array = np.array(contour)
    
   
    min_row = int(contour_array[:, 0].min()) + 10  
    max_row = int(contour_array[:, 0].max()) + 10
    min_col = int(contour_array[:, 1].min()) + 10
    max_col = int(contour_array[:, 1].max()) + 10
    
  
    return [
        (min_row, min_col),  # top_left
        (min_row, max_col),  # top_right
        (max_row, min_col),  # bottom_left
        (max_row, max_col)   # bottom_right
    ]
















def dfs(image, sp_x, sp_y, to_replace, replace_with):
   
    height, width = image.shape
    parent_map = {}
    length = 0
    last = None

    stack = [(sp_x, sp_y, 0)]
    parent_map[(sp_x, sp_y)] = None

  
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    while stack:
        x, y, it = stack.pop()
        if image[x, y] != to_replace:
            continue

        image[x, y] = replace_with

        it += 1
        if it > length:
            length = it
            last = (x, y)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and image[nx, ny] == to_replace:
                if (nx, ny) not in parent_map: 
                    parent_map[(nx, ny)] = (x, y)
                    stack.append((nx, ny, it))

    points = []
    current = last
    while current is not None:
        points.append(current)
        current = parent_map[current]
    points.reverse()
    return points




def get_edge_points(image):

    image = image.copy()
    height, width = image.shape
    pad = 10
    image = image[pad:height - pad, pad:width - pad]
    height, width = image.shape
    contours = []

    visited = set()  
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    def bfs(sx, sy):
        to_it = (sx, sy)

        while to_it is not None:
            queue = deque([to_it])
            to_it = None

            while queue:
                x, y = queue.popleft()
                if (x, y) in visited:
                    continue

                image[x, y] = 60
                visited.add((x, y))

                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= height or ny < 0 or ny >= width or image[nx, ny] == 60:
                        continue

                    if image[nx, ny] == 255:
                        to_it = (nx, ny)
                        queue.clear()
                        break
                    if (nx, ny) not in visited:
                        queue.append((nx, ny))

            if to_it is None:
                break

            points = dfs(image, to_it[0], to_it[1], to_replace=255, replace_with=120)
            last_pt = points[-1]

            points = dfs(image, last_pt[0], last_pt[1], to_replace=120, replace_with=60)
            if len(points) > 20:
                contours.append(points)

            to_it = points[-1]

    for x in range(height):
        for y in range(width):
            if (x, y) not in visited:
                bfs(x, y)
    
    return contours

def thresholdImage(img, thres, threshold):
    thres = np.where(img < threshold, 255, 0).astype(np.uint8)
    return thres