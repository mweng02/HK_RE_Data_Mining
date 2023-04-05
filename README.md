# HK_RE_Data_Mining

### Objective and DataSet Description 
The objective of this study is to investigate the relationship of MTR station on the property price and compare the accuracy of the ML price prediction with or without train proximity feature. 

Firstly, I had obtained a property transaction information in the period of 2016-2019 from the Land Registry's Memorial Day Book. 

                 
Once obtaining the latitude and longitude of all the unique property address as well as train station, I proceed to calculate the nearest MRT station of each address and map these dataframe back to the ogirinal dataset(via Geocoder.py)
