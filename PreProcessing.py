import pandas as pd 
import os, pickle, glob , sys 
from geocoder import GeoCode

"""
<---------------------------------------------          Description            --------------------------------------------------------------------->
This class is used to preprocess the raw data file in CSV format into a dataframe by executing the 

if __name__ == "__main__":

    SourceFile = glob.glob(os.path.join(sys.path[0], "Data/Train*.csv")) ---> load the raw transaction dataset 
    HK = Data(SourceFile).DataProcessing() ---> get the clean Data and Feature Extraction within the transaction dataset 
    GeoCode().geoCodePOI() # load the POI data 
    Data(SourceFile).getDataFrame() #merge get the clean dataset 

After running this script, you might proceed to Jupyter Notebook to further analysis (visualization and model prediction)

The Data Class has three main key function: 
a) DataProcessing which has 2 internal Functions to CleanData andFeature Creation
b) getDataFrame() --> get the processed data from Step "a". We have save in pkl format and be further analyze in jupyter notebook
c) Import the geocoder.py getLatLongforTransaction to get the geospatial data (latlong, nearest MRT station) for unique combined_address 
<---------------------------------------------              End            --------------------------------------------------------------------------->

"""
class Data:
    def __init__(self,path_): 
        self.rawdata =  self.ReadSourceFile(path_)

    def ReadSourceFile(self,source):
        df = [] 
        for f in source: 
            rawdata_ = pd.read_csv(f, low_memory=False)
            df.append(rawdata_) 
        df = pd.concat(df)
        return df
    
    # <!---------------------------------------------- Start For Supporting Function------------------------------------------------------------->   
    def Property_Type_(self,df):
        #To create a new column Property_Type_  = 'E' ### major housing estate with a lot of estate  'B' ### 单子楼，normally no facilities 
        return 'E' if (df['EST_E_NAME'] !='') else 'E' if (df['BLOCK']!='' or df['PHASE'] !='') else 'B'

    def project_name(self, df):
        return df['EST_E_NAME'] if df['Property_Type'] == 'E' else df['BLD_E_NAME']
    
        #### Secondary or Resale 
    def sale_type(self,df):
        if df['Completion_Year'] == '':df['Completion_Year'] = 0
        return "NEW" if float(df['Sale_Year'])- float(df['Completion_Year'])<=0 else "RESALE"
    
    def Address (self, df):
        
        estate, building = str(df['EST_E_NAME']) ,str(df['BLD_E_NAME']) 
        block, phase, street  = 'BLOCK '+ str(df['BLOCK']), 'PHASE '+str(df['PHASE']), str(df['ST_NO_FRM']) +' '+ str(df['ST_E_NAME'])
        ###create the more unique address string for geocoder to avoid duplicate of the estate/building name. Eg , There are 3 Fortune Building in HK. 
        if df['Property_Type'] == 'B':
                if (df['BLD_E_NAME'] !='' or df['BLD_C_NAME'] !=''):Address_= df['BLD_E_NAME'] +' '+ df['BLD_C_NAME'] +', '+ street
                else: Address_= street
        elif df['Property_Type'] == "E":
                if (df['BLOCK'] != '') and (df['PHASE'] != ''):Address_= estate+' '+ block +' '+ phase +' '+ building +', '+ street
                elif (df['BLOCK'] != '') and  (df['PHASE'] == ''):Address_= estate+' '+ block +' '+ building +', '+ street
                elif (df['BLOCK'] == '') and  (df['PHASE'] != ''): Address_= estate+' '+ phase+' '+  building +', '+ street
                elif (df['BLOCK'] == '') and  (df['PHASE'] == ''): Address_= estate+' '+ building +', '+ street
        return Address_

    # <!---------------------------------------------- End For Supporting Function------------------------------------------------------------->  
    # <!---------------------------------------------- Start For the ML Prediction -------------------------------------------------------------> 
    ### follow the Rating and Valuation Department Category Standard 
    def area_category(self,df):
        if df['TOTNFA'] < 400:indicator = 1 
        elif df['TOTNFA'] >= 400 and df['TOTNFA'] < 700:indicator = 2 
        elif df['TOTNFA'] >= 700 and df['TOTNFA'] < 1000:indicator = 3 
        elif df['TOTNFA'] >= 1000 and df['TOTNFA'] < 1600:indicator = 4 
        else:indicator = 5 
        return indicator 
    
    #### Floor Premium 
    def floor_type(self,df):
                
        if df['FLOOR'] > 0 and df['FLOOR'] <=10:floor_type = 1
        elif df['FLOOR'] > 10 and df['FLOOR'] <=20:floor_type = 2
        elif df['FLOOR'] > 20 and df['FLOOR'] <=30:floor_type = 3
        elif df['FLOOR'] > 30 and df['FLOOR'] <=40:floor_type = 4
        else:floor_type =0
        return floor_type
    
    #### Age Premium 
    def building_age(self,df):

        year = pd.to_numeric(df['Completion_Year'])
        if df['Sale_Year'] - year <= 0 :building_age = 0 
        elif df['Sale_Year'] - year  > 0 and  df['Sale_Year'] - year  <= 10 :building_age= 1
        elif df['Sale_Year'] - year > 10 and df['Sale_Year'] - year<= 20:building_age = 2 
        else:building_age = 3

        return building_age 
 # <!---------------------------------------------- End For the ML Prediction ----------------------------------------------------------------> 
    
    def DataProcessing(self):  

        def Cleaning(df):
            df = df[(df['TOTNFA']> 0) & (df['CONSIDERTN']> 0) & (df['PUSAGE'] =='RES')]  # Filter the Non Residential Data TYpe and OUTLIER Case such as 0 sqft or 0 in property price 
            df = df.drop(df[(df.BLD_E_NAME == '') & (df.EST_E_NAME == '') & (df.PHASE == '') & (df.BLOCK == '') ].index) # Remove empty cell in Project (ESTATE, BUILDING, BLOCK AND PHASE)
            df['TOTNFA'] = df['TOTNFA'].astype(float) # Convert To Float for Calculation 
            df['Transaction_Price'] =pd.to_numeric(df['CONSIDERTN']*1000000) #  # Convert To Float and multple with million for Calculation
            df['Sale_Year'] = pd.DatetimeIndex(df['INST_DATE']).year
            df['FLOOR'] = df['FLOOR'].fillna("0")
            df['FLOOR'] = df['FLOOR'].str.replace(r'[^\d]+',"",regex=True)
            df = df[df['FLOOR'] !='']
            df['FLOOR'] = pd.to_numeric(df['FLOOR'])
            df['Completion_Year1'] = pd.to_datetime(df['OP_DATE'],errors='coerce') ### CLEAN THE different format of the string in this column 
            df['Completion_Year1'] = pd.DatetimeIndex(df['Completion_Year1']).year
            df['Completion_Year'] = df.apply(lambda x:x['OP_DATE'].str[:4] if x['Completion_Year1']=='' else x['Completion_Year1'],axis = 1)
            df = df.fillna("") ## fill in the blank 
            df.drop_duplicates()
            return df 
        
        def FeatureCreation(df):
            ### Visualisation Feature 
            df['Property_Type'] = df.apply(self.Property_Type_, axis = 1)
            df['Sale_Type'] = df.apply(self.sale_type, axis = 1)
            df['combined_address'] = df.apply(self.Address, axis = 1).str.strip().str.upper()
            df['combined_address'] = df['combined_address'].str.upper()
            df['Project_Name'] = df.apply(self.project_name, axis = 1)
            
            ## Start of ML Prediction Feature 
            df['BuildingAge'] = df.apply(self.building_age, axis = 1) 
            df['FloorType'] = df.apply(self.floor_type, axis =1)
            df['UnitSize'] = df.apply(self.area_category, axis = 1)
            df = df.drop_duplicates(["Project_Name",'TOTNFA','Transaction_Price','combined_address','INST_DATE'])
            
            return df

        def getUniqueAddressforGeoCode(df):
            streets = df.groupby(['combined_address'])['Project_Name'].max().reset_index()
            streets.drop('Project_Name', axis=1, inplace=True)
            return streets 

        def DataFrame():
            df = Cleaning(self.rawdata)
            df = FeatureCreation(df)
            streets = getUniqueAddressforGeoCode(df)
            # first time 
            print(len(streets))
            #streets.set_index('combined_address').to_json('Data/geo-dict.json',orient='index',force_ascii= False)
            return df.to_pickle("Data/Pre_TransactionData.pkl"), streets['combined_address'][:].to_csv("Data/uniqueaddress.csv",encoding='utf-8-sig',index=False,header=True)
        return DataFrame()

    def getDataFrame(self):
        ## so that we can get DATAFRame directly without running the pre-processing 
        df = pd.read_pickle('Data/Pre_TransactionData.pkl')
        streets = pd.read_csv('Data/uniqueaddress.csv')
        print(len(streets))
        latlon = pd.read_pickle('Data/geolocations-all.pkl')
        #print(latlon)
        streets['lat'],streets['long']= latlon['lat'],latlon['lon']
        streets['Distance_TO_MRT'],streets['MRT'] ,streets['CBD']= latlon['distance_to_MRT'], latlon['Station'],latlon['CBD']
        #streets['Distance_TO_MRT'],streets['Distance_TO_MALL'] ,streets['Distance_TO_SCHOOL']  = latlon['distance_to_MRT'],latlon['distance_to_Mall'],latlon['distance_to_school']

        HK = pd.merge(df,streets[['lat','long','Distance_TO_MRT','combined_address','MRT','CBD']],on='combined_address',how='left')
        #'Distance_TO_MRT','lat','long
        HK = HK[['Project_Name','INST_DATE','Sale_Type','Property_Type','Sale_Year','D_CODE',"BuildingAge","UnitSize",'FLOOR','FloorType','combined_address','Distance_TO_MRT','TOTNFA','NET_PSF','lat','long','MRT','CBD','Transaction_Price']]
        HK = HK[(HK['Project_Name'] != "")]
        HK = HK.fillna('')
        HK = HK.set_index(pd.to_datetime(HK['INST_DATE'].values, infer_datetime_format=True))
        HK.drop_duplicates()
        
        HK.to_pickle(r'Data/TransactionData.pkl')
        return HK
    
if __name__ == "__main__":

    SourceFile = glob.glob(os.path.join(sys.path[0], "Data/HK_2016-2019_V2.csv"))
    #Data(SourceFile).DataProcessing()# precleaning 
    #GeoCode().geoCodePOI() # load the POI data 
    Data(SourceFile).getDataFrame() #merge get the clean dataset 




    
 


