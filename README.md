# HK_RE_Data_Mining

### Objective
The objective of this study is to investigate the relationship of MTR station on the property price and compare the accuracy of the ML price prediction with or without train proximity feature. 
### Dataset 
1. The main dataset of this study was property transaction information in the period of 2016-2019 from the Land Registry's Memorial Day Book. In the PreProcessing.py, first run Data(SourceFile).DataProcessing() to clean Data and Feature Extraction within the transaction dataset 
![image](https://user-images.githubusercontent.com/100345585/229998462-a3dc2b57-9d08-47dd-a775-22ee591911db.png)
                
2.  Next, we proceed to obtain the latitude, longitude as well as the nearest MTR station of each unique address in GeoGoder.py 
![image](https://user-images.githubusercontent.com/100345585/230000180-369f0ac7-46b5-4772-a371-8200a9a87d8e.png)

3. Finally, run the Data(SourceFile).getDataFrame() and proceed to HK_real_estate_price_analysis.ipynb to further analysis 

### Date Visualisation and Analysis 

### Model Prediction 
