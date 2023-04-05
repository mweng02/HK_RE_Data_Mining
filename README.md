# HK_RE_Data_Mining

### Objective
The objective of this study is to investigate the relationship of MTR station on the property price and compare the accuracy of the ML price prediction with or without train proximity feature. 
### Data
The main dataset of this study was a property transaction information in the period of 2016-2019 from the Land Registry's Memorial Day Book. Firstly, I performed a data cleanising and proprcessing task on these dataset via   

if __name__ == "__main__":
    SourceFile = glob.glob(os.path.join(sys.path[0], "Data/HK_2016-2019*.csv")) ---> load the raw transaction dataset 
    HK = Data(SourceFile).DataProcessing() ---> get the clean Data and Feature Extraction within the transaction dataset 
   
2. Additional DataSet                
Once obtaining the latitude and longitude of all the unique property address as well as train station, I proceed to calculate the nearest MRT station of each address and map these dataframe back to the ogirinal dataset(via Geocoder.py)
   #GeoCode().geoCodePOI() # load the POI data 
    #Data(SourceFile).getDataFrame() #merge get the clean dataset 
