import pickle
import zipcodes
from geopy.geocoders import Nominatim

#given area , get list of pincodes that belong that area.
def getpincode(area):
    with open('./storage/pincode_dictionary.pkl', 'rb') as f:
        pincode_dict = pickle.load(f)
    return(pincode_dict[area])


def getaddress(zipcode):
    try:
        zipcode=str(zipcode)
        geolocator = Nominatim(user_agent="png")
        zipInfo=zipcodes.matching(str(zipcode))[0]
        lat=zipInfo['lat']
        long=zipInfo['long']
        
        try:
            with open('./storage/zipcodeAddress.pkl', 'rb') as f:
                zipcodeAddress = pickle.load(f)
            address=(zipcodeAddress[zipcode])
        except Exception as e:
            address=str(zipcode)


    ##Too slow
        # location = geolocator.reverse(str(lat)+","+str(long))
        # if 'road' in location.raw['address']:
        #     if 'town' in location.raw['address']:
        #         address=str(location.raw['address']['road'])+", "+str(location.raw['address']['town'])
        #     elif 'village' in location.raw['address']:
        #         address=str(location.raw['address']['road'])+", "+str(location.raw['address']['village'])
        #     else:
        #         address=str(location.raw['address']['road'])+", "+str(location.raw['address']['city'])
        # elif 'county' in location.raw['address']:
        #     address=str(location.raw['address']['county'])
        # else:
        #     address=str(zipcode)
        return(address,lat,long)

    except Exception as e:
        print(e)
        return str(zipcode)




def getstartpincode(area):
    try:
        pincodeList=getpincode(area)
        with open('./storage/weight.pkl', 'rb') as f:
            weights = pickle.load(f)
        weights=weights[0]
        newdict={}
        for pincode in pincodeList:
            newdict[int(pincode)]=weights[int(pincode)]
        newdict=dict(sorted(newdict.items(), key=lambda item: item[1]))
        newlist=list(newdict.keys())
        print([newlist[-1],newlist[-2],newlist[-3],newlist[-4]])
        return [newlist[-1],newlist[-2],newlist[-3],newlist[-4]]
    except Exception as e:
        return []