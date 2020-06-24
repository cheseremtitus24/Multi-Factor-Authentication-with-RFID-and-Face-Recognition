import cv2
'''
This code detects probe images and locks onto the ROI and 
saves the training data into the ../images/<new_user>/ folder
'''
face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
cap = cv2.VideoCapture(0)


while True:
    # capture frame by frame

    ret, frame = cap.read()


    ### no capture image available

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]  # ycord_start,ycord_end
        roi_color = frame[y:y + h, x:x + w]

        # save the image as gray scale (save in a loop)
        for i in range(30):
            img_item = str(i) + '.png'
            cv2.imwrite(img_item, roi_gray)

        color = (255,0,0) #BGR
        stroke = 2
        end_cord_x = x+w
        end_cord_y = y + h
        cv2.rectangle(frame,(x,y),(end_cord_x,end_cord_y),color,stroke)

        

    # display the resulting frame
    cv2.imshow('frame', frame)
cap.release()
cv2.destroyAllWindows()
    
