# HK_RE_Data_Mining

### Objective
The objective of this study is to investigate the relationship of MTR station on the property price and compare the accuracy of the ML price prediction with or without train proximity feature. 
### Dataset 
1. The main dataset of this study was property transaction information in the period of 2016-2019 from the Land Registry's Memorial Day Book. In the PreProcessing.py, first run Data(SourceFile).DataProcessing() to clean Data and Feature Extraction within the transaction dataset 
![image](https://user-images.githubusercontent.com/100345585/229998462-a3dc2b57-9d08-47dd-a775-22ee591911db.png)
                
2.  Next, we proceed to obtain the latitude, longitude as well as the nearest MTR station of each unique address after 
![image](https://user-images.githubusercontent.com/100345585/229999099-3bbd32e8-b6e3-4cc3-afd1-aaaa9d4dcb33.png)
