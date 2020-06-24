import pickle
# TODO: This module should contain a parametized function that will take in input of
# the Given probe face we are interested in finding such that once we get a log
# the program returns the name and id to the caller

import cv2

# The Authenticate_user's constructor accepts the rfid card uid
# as the account since the folders during training were given the
# labels of the RFID UID.
# the id is the user_id that bears a foreign key constraint in all
# tables whether the RFID_auth_DB{check titus.db} or the FACE_REC_auth_DB
class Authenticate_User():
    def __init__(self, account, id):
        self.__account = account
        self.__id = id
        self.__status = False
    def set_status(self,value):
       self.__status = value
    def get__status(self):
        return self.__status
    def set_account(self, value):
        self.__account = value

    def get_account(self):
        return self.__account

    def set__id(self, value):
        self.__id = value

    def get_id(self):
        return self.__id

    def opencv(self):
        face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Resources/trainer.yml")
        # TODO: program has to scan while verifying 3 consecutive times with 2-3 second pauses
        # a progress bar should come in handy here
        # pass without error of 2/3 correct classification
        labels = {"person_name": 1}
        with open("Resources/labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v: k for k, v in og_labels.items()}

        cap = cv2.VideoCapture(0)

        # TODO: Program should detect motion such that if there is no motion there is a pop up and it exits if there is
        #  motion it tries to checks for the particular account_number match and it times out after a set wait period say 5
        #  seconds after which there is a retry button pop up alongside an exit there should be a max tries of 3 times on
        #  Exit it should return to Welcome page

        while True:
            # capture frame by frame

            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]  # ycord_start,ycord_end
                roi_color = frame[y:y + h, x:x + w]

                # recognize? deep learned model predict keras tensorflow pytorch scikit learn
                id_, conf = recognizer.predict(roi_gray)
                if conf >= 45:

                    #TODO: db
                    '''
                    Perform a query to the sqldatabase and cross match the given 
                    input {account_number} on the face_rec db and check that the 
                    fed in id matches the user id that was permitted during RFID auth
                    
                    The function should take in the fed in account number and returns
                    a matching userid that is saved to variable uid_Face_DB
                    '''
                    import helper.checkfacedb as facedb
                    uid_Face_DB = facedb.get_status(Authenticate_User.get_account())
                    print("check for value of this id_ " + str(id_))
                    print(labels[id_])  # is the name of the user/account_number
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    account_number = labels[id_]
                    color = (255, 255, 255)
                    stroke = 2
                    cv2.putText(frame, account_number, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                    if account_number == Authenticate_User.get_account() and uid_Face_DB == Authenticate_User.get_id():
                        # Means that the user has been authenticated
                        # Therefore we need to set status to True and then return the status to the calling program
                        Authenticate_User.set_status(True)


            # display the resulting frame
            cv2.imshow('frame', frame)

            # if Authenticate_User.get__status():
            #     break;

            ######################
            # find a way for the opencv prog  to quit when a face is detected

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        # When everyting done resease the camera

        cap.release()
        cv2.destroyAllWindows()

