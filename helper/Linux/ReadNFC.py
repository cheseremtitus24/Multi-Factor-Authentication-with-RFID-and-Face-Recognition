import os

'''
Linux/Macintosh : This program calls the system and runs the nfc utility in a loop to query the UID of the card
        and saves it to the file /tmp/out.ready

Windows : Need to replace this with a call that will use arduino to read the UID 
        instead and save it to the same path
        
        
        
N/B Need to implementation that will check the platform of execution and be able to choose


:TO DO 
        1. Arduino setup to read uid and save it to a local file
        


'''

myCmd = "nfc-anticol |grep UID > /tmp/cheserem.key && cat /tmp/cheserem.key |cut -d ' ' -f 3 > /tmp/out.ready && rm " \
        "/tmp/cheserem.key "
global lloop
lloop = False
hold = os.system(myCmd)
if hold == 256:
    lloop = True
    print("Waiting for CardSwipe!!!!!!")
else:
    lloop = False


def getvalue():
    return  lloop




while lloop:
    hold = os.system(myCmd)
    if hold == 256:
        lloop = True
        print("Waiting for CardSwipe!!!!!!")
    else:
        lloop = False

        getvalue()
        print()
        print("Card Read Success (:")
        # get_value()
        print("Have Fun")



