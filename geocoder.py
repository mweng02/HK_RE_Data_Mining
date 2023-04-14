import googlemaps,gmaps
import pickle, numpy as np, pandas as pd 

### Need to create your own API key account for google GeoCodingAPI
GOOGLE_API_KEY = ''
REFERENCE_PATH = 'Data/GeoCode/geo-dict.json'

SAVE_REFERENCE_PATH = 'Data/GeoCode/geo-dict.json'
UNIQUE_ADDRESS_PATH = 'Data/GeoCode/uniqueaddress.csv'
DATAFRAME_SOURCE_PATH = 'Data/GeoCode/geolocations-all.pkl'
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

class GeoCode:
    def __init__(self): 
        self.address = self.load_address()
        self.addressdict = self.loadAddressDict()
        self.lat,self.long  = [],[]
        self.st_dict = {}
        self.MRT,self.ShoppingMall,self.school = [],[],[]
        self.MRTName ,self.ShoppingMallName,self.schoolName=[],[],[]
        self.CBD = []

    def Geocoder(self,address,param):
            try:
                if param == "MTR":geocode_result = gmaps.geocode(address+param)
                else:geocode_result = gmaps.geocode(address+"Hong Kong")
                return geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location'] ['lng']
            except AttributeError:
                print('Address not found: {:s}'.format(address))
                return 0, 0
            except Exception as E:
                return 0, 0 

    def calculate_distance(self,x,y):
        return np.sqrt(((x[0]-y[0])*110.574)**2 + ((x[1]-y[1])*111.32)**2)

    def loadAddressDict(self):
        with open(REFERENCE_PATH ,'r+',encoding="utf-8-sig") as f:
            return pd.read_json(f)
    
    def load_address(self):
        with open(UNIQUE_ADDRESS_PATH,'r',encoding="utf-8-sig") as f:
            address = f.read()
            address_ = address.strip().split('\n')
            address_o = pd.Series(address_)
            address_o = address_o.str.strip('"')
            address_o = address_o.str.strip("'")
            address_o = address_o[1:]
        return address_o
    
    def getLatLongfromDict(self, uniqueaddress):
        return uniqueaddress['lat'],uniqueaddress['long']
    
    def getLatLongforTransaction(self):
        count = 0 
        for uniqueaddress in self.address :      
            if not uniqueaddress in self.addressdict:
                    print("Go geoCode",uniqueaddress)
                    lat_,lng_ = 0,0
                    lat_, lng_ = self.Geocoder(uniqueaddress,"Hong Kong")
                    count = count + 1 
                    print("Reading API", count)
            else:
                    print("get from Dict",uniqueaddress)
                    lat_, lng_ = self.getLatLongfromDict(self.addressdict[uniqueaddress])
                
            st = {uniqueaddress: {"lat":lat_,"long":lng_}}
            self.st_dict.update(st)
            self.long.append(lng_)
            self.lat.append(lat_)
        
        updateAddressDict = pd.DataFrame(self.st_dict)
        updateAddressDict.to_json(SAVE_REFERENCE_PATH)

        return self.lat,self.long,self.st_dict   

    def saveGeoLocations(self):
        #'distance_to_Mall': self.ShoppingMall,'distance_to_school': self.school,'distance_to_MRT':self.MRT
        lon_lat = {'lon':self.long, 'lat':self.lat,'distance_to_MRT':self.MRT,'Station':self.MRTName,'CBD':self.CBD,'School':self.school,'mall':self.ShoppingMall}

        with open(DATAFRAME_SOURCE_PATH, 'wb') as file_name:
            pickle.dump(lon_lat, file_name) # for match the correct address
  
        print("Done", len(self.lat),len(self.long),len(self.MRT),len(self.CBD))

    def CalculatePOI(self,path):

        POIList_ = []
        POIDistance = []
        with open(path,'r',encoding="utf-8-sig") as f:
            POI_ = pd.read_json(f)
        
        for _ in self.address:
            Distance = 200
            MRT = 0
            for POI in POI_: 
                x1,x2 = self.addressdict[_]['lat'],self.addressdict[_]['long']
                y1,y2 = POI_[POI]['Lat'],POI_[POI]['Long']
                Dis_Temp = self.calculate_distance([float(x1),float(x2)],[float(y1),float(y2)])
                if Dis_Temp < Distance:
                    Distance = Dis_Temp
                    MRT = POI
                    print(MRT,_)
            POIList_ .append(MRT)
            POIDistance .append(Distance)

        return POIDistance, POIList_
    
    def CalculateCBDistance(self):

        for _ in self.address:

            x1,x2 = self.addressdict[_]['lat'],self.addressdict[_]['long']
            y1,y2 = 22.28199989,114.1576766
            Dis_Temp = self.calculate_distance([float(x1),float(x2)],[float(y1),float(y2)])
            self.CBD.append(Dis_Temp )

        return self.CBD
    
    def getPOIDistance(self):
        #POI = ['MTR']
        POI = ['MTR','shoppingmall','school']
        for POI_ in POI:
            path = "Data/POI/" + POI_ + ".json"
            if POI_ == "shoppingmall": self.ShoppingMall,self.ShoppingMallName= self.CalculatePOI(path)
            elif POI_ == "MTR": self.MRT, self.MRTName= self.CalculatePOI(path)
            elif POI_ == "school":self.school,self.schoolName = self.CalculatePOI(path)
        return self.MRT,self.ShoppingMall, self.school 
    
    def geoCodePOI(self):
        self.getLatLongforTransaction()
        self.CalculateCBDistance()
        self.getPOIDistance()
        self.saveGeoLocations()

if __name__ == "__main__":
   
    a = GeoCode()
    a.geoCodePOI()

  
