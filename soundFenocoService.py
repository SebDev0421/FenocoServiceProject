import serial
import json 
""" from dotenv import load_dotenv
import os
import redis """

from time import sleep

import csv
from datetime import datetime


import pymongo
#database connecttion

""" load_dotenv()
redis_password=os.getenv('REDIS_PASSWORD')
redis_client=redis.StrictRedis(host='137.184.82.147',port=6379,db=0 , password=redis_password) """



myclient = pymongo.MongoClient("mongodb+srv://doadmin:47Q8t9l1Ts2S5ad6@db-mongodb-nyc3-25731-31725688.mongo.ondigitalocean.com/?authMechanism=DEFAULT")

mydbMongo = myclient["proyecto1111"]

serialDevice = '326610'
port = '/dev/ttyUSB0'



sleep(1)

print("Esperando dispositivo.....")
while True:
    try:
        ser = serial.Serial(port,115200)
        break
    except:
        print('Device no found')
        pass
        

print('Device connect')



print("Cargando......")
sleep(0.5)

commands = ["AWA0"]


while True:

    ser.write(commands[0].encode(encoding='ascii'))
    ser.flush()
    while ser.in_waiting:
     
     #print(trame_read)
     trame_read = ser.readline()
     
     #print(dbM)
     try:
      dbM = trame_read.decode('cp850').split(';')
      if(dbM[1] == "[data]"):
        dateTime =  dbM[2]
        year = dateTime[6:10]
        month =  dateTime[3:5]
        day = dateTime[0:2]
        hour = dateTime[11:13]
        minutes = dateTime[14:16]
        seconds = dateTime[17:19]
        dateTime_out = year+month+day+hour+minutes+seconds

        #print(dateTime_out)
        powers = dbM[4]
        
        """ print(dateTime)
        print(powers) """

        arrayPowers = powers.split(',')
        
        result = []
        result.append(dateTime_out)
        #print(val)

        for x in arrayPowers:
           result.append(x)
           
        #print(result[44])
        
        record = {
            "sonometer":int(serialDevice),
            "register":int(result[0]),
            "SPLZ":float(result[1]),
            "SPLC":float(result[2]),
            "SPLA":float(result[3]),
            "SPLI":float(result[4]),
            "SPLD":float(result[5]),
            "SPLT":float(result[6]),
            "SPLU":float(result[7]),
            "20kHz":float(result[8]),
            "16kHz":float(result[9]),
            "12k5Hz":float(result[10]),
            "10kHz":float(result[11]),
            "8kHz":float(result[12]),
            "6k3Hz":float(result[13]),
            "5kHz":float(result[14]),
            "4kHz":float(result[15]),
            "3k15Hz":float(result[16]),
            "2k5Hz":float(result[17]),
            "2kHz":float(result[18]),
            "1k6Hz":float(result[19]),
            "1k25Hz":float(result[20]),
            "1kHz":float(result[21]),
            "800Hz":float(result[22]),
            "630Hz":float(result[23]),
            "500Hz":float(result[24]),
            "400Hz":float(result[25]),
            "315Hz":float(result[26]),
            "250Hz":float(result[27]),
            "200Hz":float(result[28]),
            "160Hz":float(result[29]),
            "125Hz":float(result[30]),
            "100Hz":float(result[31]),
            "80Hz":float(result[32]),
            "63Hz":float(result[33]),
            "50Hz":float(result[34]),
            "40Hz":float(result[35]),
            "31Hz5":float(result[36]),
            "25Hz":float(result[37]),
            "20Hz":float(result[38]),
            "16Hz":float(result[39]),
            "12Hz5":float(result[40]),
            "10Hz":float(result[41]),
            "8Hz":float(result[42]),
            "6Hz3":float(result[43])
        }
        print(record)
        #collection = mydbMongo[serialDevice]
        #x = collection.insert_one(record)
        jsonDict=json.dumps(record)
        redis_client.lpush('milista',jsonDict)
        redis_client.lpush('sonometers',serialDevice)
        
        print("data was load....")
     except Exception as error:
      print(error)
      pass
      

     #trame_read.split(';')

    


    """ try:
        dataRecive = ser.read()
        responseDevice = responseDevice + dataRecive.decode('utf-8')
    except:
        print(responseDevice)
        break """

    sleep(0.5)

