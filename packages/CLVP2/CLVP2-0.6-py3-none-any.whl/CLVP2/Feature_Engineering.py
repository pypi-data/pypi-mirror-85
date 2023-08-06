import numpy as np
import pandas as pd
import re
import random
from sklearn.preprocessing import MinMaxScaler
from .utils import Utils
import pickle



class CleaningData():
    
    """The CleaningData class cleans data before training process 
    """


    def __init__(self,Most_frequent_threshold = 0.9,null_threshold=0.1, remove_columns=[]):
        


        """Method for initializing a CleaningData object

        Args: 
            Most_frequent_threshold (float)
            null_threshold (float)
            remove_columns (list)

        Attributes:
            Most_frequent_threshold (float):  frequent threshold to accept a certain feature 
            null_threshold (float): null threshold to accept a certain row
            remove_columns (list): columns user want to remove
        """

        self.Most_frequent_threshold = Most_frequent_threshold
        self.remove_columns = remove_columns
        self.null_threshold = null_threshold

        
    def Remove_Columns(self,data):
        

        """The Remove_Columns method remove specific columns

        Args: 
            data (data frame): input data

        Returns:
            data frame: data after removing selected columns

        """
        
        for i in self.remove_columns:
            try:
                data.drop([i], axis=1, inplace=True)
            except:
                #print("there is no column called ",i)
                pass

        return data

    def Remove_Nulls(self,data):

        """The Remove_Nulls method remove nulls data

        Args: 
            data (data frame): input data

        Returns: 
	    data frame: data after removing null data

        """

        #data = data.dropna(axis=1, how='all')
        #data = data.dropna(axis=0, how='all')
        #print(data.shape)
        minumum_values = int(data.shape[0]*self.null_threshold)
        #print(minumum_values)
        data = data.dropna(axis=1,thresh=minumum_values)
        #print(data.shape)
        minumum_values = int(data.shape[1]-data.shape[1]*self.null_threshold)
        #print(minumum_values)
        data = data.dropna(axis=0,thresh=minumum_values)
        #print(data.shape)
        x= [i for i in data.columns]
        #print(x)
        data = data.fillna(0)

        return data

        
    def Remove_Most_Frequent(self,data):

        """The Remove_Most_Frequent method remove data with high repetitive frequency

        Args: 
            data (data frame): input data

        Returns: 
	    data frame: data after removing data with high frequency

        """
 
        for i in data:
            unique_percentage = ((data[i].value_counts().max())/data.shape[0])
            if unique_percentage>self.Most_frequent_threshold:
                del data[i]
                #print(i)

        return data
                
    def Reset_Index(self,data):
        """The Reset_Index method to reset the data frame index 

        Args: 
            data (data frame): input data

        Returns: 
	    data frame: data after resetting data frame index

        """
        data=data.reset_index()
        data.drop(['index'], axis=1, inplace=True)

        return data


    

class Splitting_Data():

    """The Splitting_Data class create, sperate, normalize and split the dataset
    """

    def __init__(self,windows=5,shift=1,minimum = 0,maximum=1):

        """Method for initializing a Splitting_Data object

        Args: 
            windows (int)
            shift (int)
            minimum (int)
            maximum (int)


        Attributes:
            windows (int):  windows size in time series data
            shift (int): shift rate in time series data
            minimum (float): minimum number in dataset after normalization process
            maximum (float): maximum number in dataset after normalization process

        """


        self.windows = windows
        self.shift = shift
        self.minimum = minimum
        self.maximum = maximum

    def Dividing_Data(self,mixed_data,train=0):

        """The Dividing_Data method to divide the dataset into time series and non-time-series datasets 
        Args: 
            data (data frame): input data

        Returns: 
	    data frame: non time series dataset
	    data frame: time series dataset
	    list: non time series features
	    list: time series features


        """
        
        time_series = pd.DataFrame({})
        non_time_series = pd.DataFrame({})
        columns_number = []
        x= [i for i in mixed_data.columns]

        for i in range(0,len(x)):
            clv = re.findall(r'clv|CLV|Clv',x[i])
            #print(clv)
            order = re.findall(r'\d',x[i])
            if len(clv)>0:
                columns_number.append((int(order[0]),x[i]))

        sort = sorted(columns_number, key = lambda x: x[0])
        
        for i in sort:
            time_series[i[1]] = mixed_data[i[1]]
            del mixed_data[i[1]]

            
        non_time_series = mixed_data

        features_non_time_series= [i for i in non_time_series.columns]
        #print(features_non_time_series)
        features_time_series= [i for i in time_series.columns[-1-self.windows:-1]]
        #print(fetures_time_series)
        if train==1:
            if (len(features_time_series)+1)< 6:
                #print((features_time_series))
                return Utils.with_error(error_code=2,error_message="missing clv columns")
        else:
            if (len(features_time_series)+1)< 5:
                #print((features_time_series))
                return Utils.with_error(error_code=2,error_message="missing clv columns")
            return Utils.with_success([non_time_series,time_series.iloc[:,-5:]])
            
        
        return Utils.with_success([non_time_series,time_series,features_non_time_series,features_time_series])

    def Creating_Dataset(self,non_time_series,time_series):

        """The Creating_Dataset method to create two datasets: time series and non-time-series datasets 
        Args: 
            non_time_series(data frame): non-time series dataset
           time_series(data frame): time series dataset

        Returns: 
	    list: contain time, non time series and labels dataset

        """

        row_lenght = time_series.shape[1]
        data_per_row=0
        row_lenght = row_lenght-self.windows
        while True:
            if row_lenght > 0:
                data_per_row=data_per_row+1
            else:
                break
            
            row_lenght = row_lenght-self.shift

        time_series_array = time_series.values
        non_time_series_array = non_time_series.values

        data = []
        
        for z in range(0,time_series.shape[0]):
    
          begin=0
          for i in range(0,data_per_row):
              
              x_ntts = non_time_series_array[z]
              x_tts = time_series_array[z][begin:begin+self.windows]
              y_t = time_series_array[z][begin+self.windows]

              data.append([x_ntts,x_tts,y_t])
              begin = begin+self.shift
              
        return data
                

    def Shuffling_Seprating_Data(self,data):
        
        """The Shuffling_Seprating_Data method shuffle the dataset

        Args: 
            data(list): datasets

        Returns: 
	    array: non time series dataset
	    array: time series dataset
	    list: labels

        """

        x_non_time_series = []
        x_time_series = []
        y_train = []

        random.shuffle(data)

        for i,j,k in data:

            x_non_time_series.append(i)
            x_time_series.append(j)
            y_train.append(k)

        x_non_time_series = np.array(x_non_time_series)
        x_time_series = np.array(x_time_series)
        #y_train = np.array(y_train)

        return x_non_time_series,x_time_series,y_train
    
    def Split_Data(self,non_time_series,time_series,lables , traing_percentage=0.8,validation_percentage=0.1):

        """The Split_Data method split the dataset into training, validation and test sets

        Args: 
            non_time_series(array): non time series dataset
            time_series(array): time series dataset
            labels (list): labels dataset
            training_percentage(float): precenatge of training portion 
            validation_percentage: precenatge of validation 	         portion
        Returns: 
	    array: x_train_non_time_series dataset
	    array: x_validation_non_time_series dataset
	    array: x_test_non_time_series dataset
	    array: x_train_time_series dataset
	    array: x_test_time_series dataset
	    list: y_train dataset
	    list: y_validation dataset
	    list: y_test dataset
        """
        
        training_size = int(len(non_time_series)*traing_percentage)
        validation_size = int(len(non_time_series)*validation_percentage)
        #testing_percentage = 1- traing_percentage - validation_percentage    
        
        x_train_non_time_series = non_time_series[:training_size]    
        x_validation_non_time_series =   non_time_series[training_size:training_size+validation_size]    
        x_test_non_time_series = non_time_series[training_size+validation_size:]  
        
        x_train_time_series = time_series[:training_size] 
        x_validation_time_series =  time_series[training_size:training_size+validation_size]
        x_test_time_series  = time_series[training_size+validation_size:]
        
        y_train = lables[:training_size]
        y_validation = lables[training_size:training_size+validation_size]
        y_test = lables[training_size+validation_size:]

        return  x_train_non_time_series,x_validation_non_time_series,x_test_non_time_series,x_train_time_series,x_validation_time_series,x_test_time_series,y_train,y_validation,y_test

                
    def Normalize_train_data(self,data):

        """The Normalize_train_data method normalize the input train dataset
        Args: 
            data(array): input dataset

        Returns: 
	    array: normalized features 
	    function: scaler that used to normailze dataset
	   
        """

        #converting Pandas data to Numpy array
        #data = data.values
        scaler = MinMaxScaler(feature_range=(self.minimum , self.maximum))
        scaler.fit(data)
        normalized_features = scaler.transform(data)
        
        return normalized_features,scaler

    def Normalize_test_data(self,data,scaler):
        
        """The Normalize_test_data method normalize the input test or validation dataset
        Args: 
            data(array): input dataset
	    scaler (function): used to normailze test dataset

        Returns: 
	    array: normalized features 
	
        """
        #converting Pandas data to Numpy array
        #data = data.values

        normalized_features = scaler.transform(data)
        
        return normalized_features

    def Normalize_data(self,x_train_non_time_series,x_validation_non_time_series,x_test_non_time_series,x_train_time_series,x_validation_time_series,x_test_time_series):

        """The Normalize_data method normalize the input  datasets
        Args: 
            x_train_non_time_series(array):  train non-time series dataset
            x_validation_non_time_series(array):  validation non-time series dataset
            x_test_non_time_series(array): test non-time series dataset
            x_train_time_series(array): train time series dataset
            x_validation_time_series(array): x validation time series dataset

        Returns: 
            array:  train non-time series dataset
            array:  validation non-time series dataset
            array: test non-time series dataset
            array: train time series dataset
            array: x validation time series dataset
            function: scalar to normalize non-time series dataset
            function: scalar to normalize time series dataset
        """
        x_train_non_time_series,scaler1 = self.Normalize_train_data(x_train_non_time_series)
        x_train_time_series,scaler2 = self.Normalize_train_data(x_train_time_series)
        x_validation_non_time_series = self.Normalize_test_data(x_validation_non_time_series,scaler1)
        x_validation_time_series = self.Normalize_test_data(x_validation_time_series,scaler2)
        x_test_non_time_series = self.Normalize_test_data(x_test_non_time_series,scaler1)
        x_test_time_series = self.Normalize_test_data(x_test_time_series,scaler2)

        
        return x_train_non_time_series,x_train_time_series,x_validation_non_time_series,x_validation_time_series,x_test_non_time_series,x_test_time_series,scaler1,scaler2
    

    def save_model(self,scaler,model_name,file_name):

        """The save_model method saves the best model
         Args: 
            model(class): normalizing class
            model_name(str):  model name
            file_name(str): path folder of the model


        Returns: 
            str:  full path of the model

        """
        

        x = Utils().generate_file_name(model_name)
        y = Utils().save_pipeline(file_name)
        final_name=y+'\\'+x
        
        try:
            pickle_out = open(final_name+'.pickle',"wb")
            pickle.dump(scaler, pickle_out)
            pickle_out.close()
        
        except Exception as error:
            Utils().with_error(4, 'the scaler file not saved', error)
        

        #re = model.evaluate([self.x_test_non_time_series,self.x_test_time_series], self.y_test)

        return Utils().with_success(final_name)
 


