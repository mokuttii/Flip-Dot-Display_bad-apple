import cv2
import os

cap = cv2.VideoCapture('V.mp4') # video file name

output_dir = 'frames' #filename
os.makedirs(output_dir, exist_ok=True)

def convert_frame_to_matrix(frame):
    frame = cv2.resize(frame, (28, 7))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    matrix = []
    for row in binary:
        matrix.append(''.join(['1' if pixel == 255 else '0' for pixel in row]))
    return matrix

frame_matrices = []
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % 2 == 0:  
        matrix = convert_frame_to_matrix(frame)
        frame_matrices.append(matrix)
    frame_count += 1

cap.release()
for i, matrix in enumerate(frame_matrices):
    with open(os.path.join(output_dir, f'frame_{i:04}.txt'), 'w') as file:
        for row in matrix:
            file.write(row + '\n')
