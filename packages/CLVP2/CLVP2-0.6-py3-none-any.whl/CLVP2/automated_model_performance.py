import numpy as np
import random
from random import seed
from collections import deque 
from .model import CNN_LSTM_Model
import numpy as np
import random
from tensorflow.keras.layers import *
from tensorflow.keras.applications import *
from tensorflow.keras.models import Model 
from tensorflow.keras.models import *
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
import time
import os
import datetime
from .checks import CheckConditions
from .utils import Utils

#print(random.randint(0,10000))
seed(random.randint(0,1000))

paramter_similarity = deque(maxlen = 100)

Minumum_acceptalple_number = 1
Maxiumum_acceptalple_number = 50
maximum_ratio=2
similar_threshold=Maxiumum_acceptalple_number

maximum_kernel_size = 20
minimum_kernel_size = 1
kernel_size_Weight = 1
maxiumum_Filters = 256
minimum_Filters = 4
maxiumum_Neurons = 500
minimum_Neurons = 10
Filters_Weight =0.4
Neuron_Weight = 0.3
batch_size_weight = 0.8
batch_size_numbers = [4,8,16,32,64,128]



class   automated_parameter_selection():
    
    """The automated_parameter_selection class automates the training process 
    """
    
    def __init__(self,x_train_non_time_series,x_train_time_series,x_validation_non_time_series,x_validation_time_series,x_test_non_time_series,x_test_time_series,y_train,y_validation,y_test):


        """Method for initializing a automated_parameter_selection object

        Args: 
            x_train_non_time_series (array)
            x_train_time_series (array)
            x_validation_non_time_series (array)
            x_validation_time_series (array)
            x_test_non_time_series (array)
            x_test_time_series (array)
            y_train (list)
            y_validation (list)
            y_test (list)


        Attributes:
            x_train_non_time_series (array): train non-time series dataset
            x_train_time_series (array): train time series dataset
            x_validation_non_time_series (array): validation non-time series dataset
            x_validation_time_series (array): validation time series dataset
            x_test_non_time_series (array): test non-time series dataset
            x_test_time_series (array): test time series dataset
            y_train (list): train labels dataset
            y_validation (list): validation labels dataset
            y_test (list): test labels dataset
            
        """

        self.CNN_LSTM_model  = CNN_LSTM_Model(x_train_non_time_series,x_train_time_series,x_validation_non_time_series,x_validation_time_series,x_test_non_time_series,x_test_time_series,y_train,y_validation,y_test)

        self.kernel_size_1 = random.randint(minimum_kernel_size,maximum_kernel_size)
        self.kernel_size_2 = random.randint(minimum_kernel_size,maximum_kernel_size)
        self.kernel_size_3 = random.randint(minimum_kernel_size,maximum_kernel_size)
        self.CNN_Filters_1 =random.randint(minimum_Filters,maxiumum_Filters)
        self.CNN_Filters_2 = 2*random.randint(minimum_Filters,maxiumum_Filters)
        self.CNN_Filters_3 = random.randint(minimum_Filters,maxiumum_Filters)
        self.dense_layer_1 = random.randint(minimum_Neurons,maxiumum_Neurons)
        self.dense_layer_2 = random.randint(minimum_Neurons,maxiumum_Neurons)
        self.dense_layer_3 = random.randint(minimum_Neurons,maxiumum_Neurons)
        self.batch_size = random.choice(batch_size_numbers)

        self.All_parameters = []

        self.parameters_weights =np.array([kernel_size_Weight,kernel_size_Weight,kernel_size_Weight,Filters_Weight,Filters_Weight,Filters_Weight,Neuron_Weight,Neuron_Weight,Neuron_Weight,batch_size_weight])
        self.similar_threshold=50
        self.sum_para=0
        self.final_results = []
        self.train = 1

        self.Time = 1
        
    def  run(self):
        
        """The run method trains deep learning multiple times and returns the best parameters

         Args: None

        Returns: 
            list:  best parameters found

        """
        
        i=1
        new_parameters = [self.kernel_size_1,self.kernel_size_2,self.kernel_size_3,self.CNN_Filters_1,
                           self.CNN_Filters_2,self.CNN_Filters_3,self.dense_layer_1,self.dense_layer_2,self.dense_layer_3,self.batch_size]
        loop=0
        while True:

            start_time = time.time()

            if self.train:
                
                
                #try:
                self.CNN_LSTM_model.reset_model()
                model = self.CNN_LSTM_model.model_architecture(self.kernel_size_1,self.kernel_size_2,self.kernel_size_3,self.CNN_Filters_1,self.CNN_Filters_2,self.CNN_Filters_3,self.dense_layer_1,self.dense_layer_2,self.dense_layer_3)
                results,story =self.CNN_LSTM_model.fit_evaluate_model(model,self.batch_size)
                #print(new_parameters)
                self.All_parameters.append(new_parameters)

                self.final_results.append(results)
                #except:
   
            if story==1:
                loop = loop+1
            if loop>=50:
                break

                                                                                                                                                                                                                                                                        #train
            self.All_parameters_array = np.array(self.All_parameters)
            
            self.kernel_size_1 = random.randint(minimum_kernel_size,maximum_kernel_size)
            self.kernel_size_2 = random.randint(minimum_kernel_size,maximum_kernel_size)
            self.kernel_size_3 = random.randint(minimum_kernel_size,maximum_kernel_size)
            self.CNN_Filters_1 =random.randint(minimum_Filters,maxiumum_Filters)
            self.CNN_Filters_2 = 2*random.randint(minimum_Filters,maxiumum_Filters)
            self.CNN_Filters_3 = random.randint(minimum_Filters,maxiumum_Filters)
            self.dense_layer_1 = random.randint(minimum_Neurons,maxiumum_Neurons)
            self.dense_layer_2 = random.randint(minimum_Neurons,maxiumum_Neurons)
            self.dense_layer_3 = random.randint(minimum_Neurons,maxiumum_Neurons)
            self.batch_size = random.choice(batch_size_numbers)

            new_parameters = [self.kernel_size_1,self.kernel_size_2,self.kernel_size_3,self.CNN_Filters_1,
                           self.CNN_Filters_2,self.CNN_Filters_3,self.dense_layer_1,self.dense_layer_2,self.dense_layer_3,self.batch_size]
            self.new_parameters_array = np.array(new_parameters)
            try :
                similarty = (new_parameters - self.All_parameters_array)*self.parameters_weights
                
            except:
                similarty=np.zeros((10,4))

            absolute = np.absolute(similarty)
            sum_parameters = np.sum(absolute, axis=1)

            minimum = np.min(sum_parameters)
                
            if minimum>self.similar_threshold:
                self.train = 1
                self.sum_para = self.sum_para+1
            else:
                self.train = 0

            paramter_similarity.append(minimum)    
            if i%100==0:
                #print("after " +str(i)+" iterations "  + " with similar_threshold = "+str(similar_threshold)+" no. of paratmers = "+str(sum_para))
                if  self.sum_para<Minumum_acceptalple_number:
                      similar_threshold = max(paramter_similarity)
                      
                elif  self.sum_para>Maxiumum_acceptalple_number:
                      similar_threshold = max(paramter_similarity)*maximum_ratio
                      
                self.sum_para=0

            i=i+1
            
            End_time = time.time()
            run_time =  End_time - start_time

            self.Time = self.Time-run_time
            #print(self.Time)
        #print(self.final_results)    
        best = np.argmin(np.array(self.final_results))
        #print(best)
        #print(np.array(self.All_parameters).shape)
        #print(np.array(self.final_results).shape)
        #print(self.All_parameters[best])
        #print("see first")
        #print(self.All_parameters[best])
        #best_parameters=self.All_parameters[best]
        #model = self.CNN_LSTM_model.model_architecture(best_parameters[0],best_parameters[1],best_parameters[2],best_parameters[3],best_parameters[4],best_parameters[5],best_parameters[6],best_parameters[7],best_parameters[8])
        #results =self.CNN_LSTM_model.fit_evaluate_model(model,best_parameters[9])

        return self.All_parameters[best]


    def train_save_best_model(self,best_parameters):
        
        """The train_save_best_model method trains and saves the best model
         Args: 
            best_parameters(list): the best parameters found

        Returns: 
            str:  full path of the model
 
        """
        
        print("training best model ...")


        model = self.CNN_LSTM_model.model_architecture(best_parameters[0],best_parameters[1],best_parameters[2],best_parameters[3],best_parameters[4],best_parameters[5],best_parameters[6],best_parameters[7],best_parameters[8])
        best_model,best_performance = self.CNN_LSTM_model.fit_best_model(model,best_parameters[9])


        try: 
            model_path = self.CNN_LSTM_model.save_model(best_model,'best','models')
            #print(best_performance)
        
        except Exception as error:
            Utils().with_error(3, 'the model not saved', error)
            
        return Utils().with_success(model_path)



    
