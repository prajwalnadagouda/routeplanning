import pickle

#given area , get list of pincodes that belong that area.
def getpincode(area):
    with open('pincode_dictionary.pkl', 'rb') as f:
        pincode_dict = pickle.load(f)
    return(pincode_dict[area])

def getstartpincode():
    return 95110