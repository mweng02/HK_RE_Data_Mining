# HK_RE_Data_Mining

### Objective
The objective of this study is to investigate the relationship of MTR station on the property price and compare the accuracy of the ML price prediction with or without train proximity feature. 
### Data
The main dataset of this study was property transaction information in the period of 2016-2019 from the Land Registry's Memorial Day Book. In the PreProcessing.py, first run Data(SourceFile).DataProcessing() to clean Data and Feature Extraction within the transaction dataset 
![image](https://user-images.githubusercontent.com/100345585/229998462-a3dc2b57-9d08-47dd-a775-22ee591911db.png)

2. Additional DataSet                
Once obtaining the latitude and longitude of all the unique property address as well as train station, I proceed to calculate the nearest MRT station of each address and map these dataframe back to the ogirinal dataset(via Geocoder.py)
   #GeoCode().geoCodePOI() # load the POI data 
    #Data(SourceFile).getDataFrame() #merge get the clean dataset 
