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
import os
import datetime
from .checks import CheckConditions
from .utils import Utils
import errno, os, stat, shutil

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise


class CNN_LSTM_Model():

    """The CNN_LSTM_Model class for creating, training and saving best deeplearning model 
    """


    def __init__(self,x_train_non_time_series,x_train_time_series,x_validation_non_time_series,x_validation_time_series,x_test_non_time_series,x_test_time_series,y_train,y_validation,y_test):

        
        """Method for initializing a CNN_LSTM_Model object

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
        
        self.x_train_non_time_series= x_train_non_time_series
        self.x_train_time_series = x_train_time_series
        self.x_validation_non_time_series = x_validation_non_time_series 
        self.x_validation_time_series = x_validation_time_series
        self.x_test_non_time_series = x_test_non_time_series
        self.x_test_time_series = x_test_time_series
        self.y_train = y_train
        self.y_validation = y_validation 
        self.y_test = y_test
        
        self.x_non_time_series_shape= x_train_non_time_series.shape[1]
        self.x_time_series_shape = x_train_time_series.shape[1]

    def reset_model(self):
        pass
        

    def model_architecture(self,kernel_size_1,kernel_size_2,kernel_size_3,CNN_Filters_1,CNN_Filters_2,CNN_Filters_3,dense_layer_1,dense_layer_2,dense_layer_3):

        """ The model_architecture method to initialize the deep learning model
         Args: 
            kernel_size_1(int): kernel size for first CNN layer
            kernel_size_2(int):  kernel size for second CNN layer
            kernel_size_3(int): kernel size for third CNN ayer
            CNN_Filters_1(int): number of filters in first CNN layer
            CNN_Filters_2(int): number of filters in second CNN layer
	    CNN_Filters_3(int): number of filters in third CNN layer
            dense_layer_1(int): number of neurons in first dense layer
            dense_layer_2(int): number of neurons in second dense layer
            dense_layer_3(int): number of neurons in third dense layer

        Returns: 
            class:  tensorflow model 

        """
        
        tf.keras.backend.clear_session()
        #tf.random.set_seed(random.randint(0,10000))        
        #np.random.seed(random.randint(0,10000))
        model_CNN = tf.keras.models.Sequential([
            #layer1
            tf.keras.layers.Conv1D(filters= int(CNN_Filters_1), kernel_size=int(kernel_size_1),strides=1, padding="causal",activation="relu",input_shape=[self.x_non_time_series_shape,1]),
            #layer2
            tf.keras.layers.Conv1D(filters=int(CNN_Filters_2), kernel_size=int(kernel_size_2),strides=1, padding="causal",activation="relu"),        

        ])
        LSTM_filters = CNN_Filters_2/2
        model_LSTM = tf.keras.models.Sequential([

        tf.keras.layers.Conv1D(filters=int(CNN_Filters_3), kernel_size=int(kernel_size_3),strides=1, padding="causal",activation="relu",input_shape=[self.x_time_series_shape ,1]),
            #layer2
           tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(int(LSTM_filters))),

        ])

        Merged = Add()([model_CNN.output,model_LSTM.output])
        #concat = concatenate([model_CNN.output, model_LSTM.output], name='Concatenate')

        Merged = Flatten()(Merged)    
        Merged = Dense(dense_layer_1, activation='relu')(Merged)
        Merged = Dense(dense_layer_2, activation='relu')(Merged)
        Merged = Dense(dense_layer_3, activation='relu')(Merged)

        #mergedOut = Dense(128, activation='relu')(mergedOut)

        # output layer
        Merged = Dense(1)(Merged)
        Merged_CNN_LSTM = Model([model_CNN.input,model_LSTM.input], Merged)

        #sgd = optimizers.SGD(lr=0.1e-8,momentum=0.9)

        Merged_CNN_LSTM.compile(loss='mae',  optimizer='adam')
        
        return Merged_CNN_LSTM


    def fit_evaluate_model(self,model,batch_size):

        """The fit_evaluate_model method to initialize the deep learning model
         Args: 
            model(class): Tensorflow model
            batch_size(int):  number of batch size


        Returns: 
            float:  performance on test set

        """
        generate_name = Utils().generate_file_name("test")
        randomness = random.randint(0,1000)
        generate_path = generate_name+'_'+str(randomness)
        path = Utils().save_pipeline('checkpoints')
        path_path = Utils().save_pipeline('checkpoints'+'\\'+generate_path)
        #path_path = Utils().save_pipeline('checkpoints')

        final_name=path_path+'\\'+"test"
        
        checkpoint_filepath = final_name
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_filepath,
            save_weights_only=True,
            monitor='val_loss',
            mode='min',
            verbose=0,
            save_best_only=True)
        try:

            history = model.fit([self.x_train_non_time_series,self.x_train_time_series],self.y_train,epochs=100,verbose=0,callbacks=[model_checkpoint_callback],validation_data=([self.x_validation_non_time_series,self.x_validation_time_series],self.y_validation),batch_size=batch_size)

            model.load_weights(checkpoint_filepath)

            performance = model.evaluate([self.x_test_non_time_series,self.x_test_time_series], self.y_test,verbose=0)
            

            try:
                shutil.rmtree(path_path, ignore_errors=False, onerror=handleRemoveReadonly)
            except :
                pass
            story=1
        except:
            performance=100000000000000000
            story=0
            


        return performance,story

    def fit_best_model(self,model,batch_size):

        """The fit_evaluate_model method to initialize the deep learning model
         Args: 
            model(class): Tensorflow model
            batch_size(int):  number of batch size


        Returns: 
            float:  performance on test set

        """
        generate_name = Utils().generate_file_name("best")
        randomness = random.randint(0,1000)
        generate_path = generate_name+'_'+str(randomness)
        path = Utils().save_pipeline('checkpoints')
        path_path = Utils().save_pipeline('checkpoints'+'\\'+generate_path)
        #path_path = Utils().save_pipeline('checkpoints')

        final_name=path_path+'\\'+"best"
        
        
        checkpoint_filepath = final_name
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_filepath,
            save_weights_only=True,
            monitor='val_loss',
            mode='min',
            verbose=0,
            save_best_only=True)
        
        while True:
            try:
                history = model.fit([self.x_train_non_time_series,self.x_train_time_series],self.y_train,epochs=300,verbose=0,callbacks=[model_checkpoint_callback],validation_data=([self.x_validation_non_time_series,self.x_validation_time_series],self.y_validation),batch_size=batch_size)

                model.load_weights(checkpoint_filepath)

                best_performance = model.evaluate([self.x_test_non_time_series,self.x_test_time_series], self.y_test)
                successful_run=1
            except:
                successful_run=0

            if successful_run==1:
                break
            

        try:
            shutil.rmtree(path_path, ignore_errors=False, onerror=handleRemoveReadonly)
        except :
            pass

        return model,best_performance
    
    def save_model(self,model,model_name,file_name):

        """The save_model method saves the best model
         Args: 
            model(class): Tensorflow model
            model_name(str):  model name
            file_name(str): path folder of the model


        Returns: 
            str:  full path of the model

        """
        

        x = Utils().generate_file_name(model_name)
        y = Utils().save_pipeline(file_name)
        final_name=y+'\\'+x
        model.save(final_name)
        model = tf.keras.models.load_model(final_name)
        #re = model.evaluate([self.x_test_non_time_series,self.x_test_time_series], self.y_test)

        return final_name




