import csv
import zipcodes


from pyzipcode import ZipCodeDatabase
zcdb = ZipCodeDatabase()

with open('bayareapincodes.csv', mode ='r',encoding='utf-8-sig')as file:
    csvFile = csv.reader(file) 
    next(csvFile)
    for lines in csvFile:
        # print(lines[0])
        # print(zcdb[int(lines[0])])
        a=(zipcodes.matching(lines[0])[0]['county'])
        b=(lines[1])
        if(a!=b):
            print(lines[0],a,b)
