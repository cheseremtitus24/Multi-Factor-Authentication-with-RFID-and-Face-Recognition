import cv2
import os

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
#initialize the video cam to default
cap = cv2.VideoCapture(0)
global condition
condition = False
def save(pathh):
    while True:
        # capture frame by frame focus on Region of Interest only
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]  # xcord start, xcord end
            roi_color = frame[y:y + h, x:x + w]

            #import os to change directory to path to save the images


            # save the image as gray scale (save in a loop)


            for i in range(50):
                img_item = str(i) + '.png'

                myCMD = f'cd {pathh}'
                os.system(myCMD)
                cv2.imwrite(img_item, roi_gray)
                color = (255, 0, 0)  # BGR
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                if i == 4:
                    global condition
                    condition = True

            # global condition
            # condition = True


        # display the resulting frame
        # cv2.imshow('frame', frame)

        if condition:
            break
        # if cv2.waitKey(20) & 0xFF == ord('q'):
        #     break


save('test')
cap.release()
cv2.destroyAllWindows()