# HK_RE_Data_Mining

### Objective
The objective of this study is to investigate the relationship of MTR station on the property price and compare the accuracy of the ML price prediction with or without train proximity feature. 

### Requirements
Additional Libraries need to import.
```
  Pip install googlemaps
  pip install gmaps 
  pip install streamlit 
```
Need to fill up your own googleMap API Key to run GeoCoder.py
```
    GOOGLE_API_KEY = '' 
```
### Dataset 
1. The main dataset of this study was property transaction information in the period of 2016-2019 from the Land Registry's Memorial Day Book. In the PreProcessing.py, first run Data(SourceFile).DataProcessing() to clean Data and Feature Extraction within the transaction dataset 
```
    SourceFile = glob.glob(os.path.join(sys.path[0], "Data/HK_2016-2019_V2.csv"))
    Data(SourceFile).DataProcessing()
```

                
2.  Next, we proceed to obtain the latitude, longitude as well as the nearest MTR station of each unique address in GeoGoder.py. 
```  
    a = GeoCode()
    a.geoCodePOI()
```
    

3. Finally, run the Data(SourceFile).getDataFrame() and proceed to HK_real_estate_price_analysis.ipynb to further analysis 

### Date Visualisation and Analysis 

### Model Prediction 
