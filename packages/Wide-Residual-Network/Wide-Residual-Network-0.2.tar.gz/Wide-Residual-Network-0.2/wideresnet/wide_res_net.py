'''
This class is for creating a wide res net convolutional neural network.
'''
import tensorflow as tf
from tensorflow import keras

class WideResNet():
    def __init__(self, input_shape, k = 2, num_layers = 22, num_classes = 4):
        '''
        creates the final keras network
        
        Args:
            input_shape (tuple of image dimensions) : contains shape of image (heigt, width, depth)
            k (integer) : widening factor
            num_layers (integer) : number of layers within the set {10, 16, 22, 28, 34, 40}
            num_classes (integer) : number of classes to classify
        '''
        try:
            img_height, img_width, img_depth = input_shape
        except:
            raise ValueError("Please ensure that input shape has folowwing format: (height, width, depht)")

        self.__input_shape = input_shape
        self.__k = k
        self.__num_layers = num_layers
        self.__num_classes = num_classes
        
    def create_model(self):
        '''
        This function creates the final model based on the values given in the constructor
        '''
         # calculate number of blocks per group
        num_blocks_per_group_float = (self.__num_layers - 4) / (3*2)
        num_blocks_per_group = int(num_blocks_per_group_float)
        
        # check if number of layers is valid and throw error if not (check if N is an integer)
        assert num_blocks_per_group == num_blocks_per_group_float, \
            "num_layers is not valid!"
        
        X_input = keras.Input(self.__input_shape, name = "Input")
        # add input block for wide resnet
        X = self.add_input_block(X_input)
        # add conv2 group -> stride equals 1 because output size shall stay equal to input size
        X = self.add_basic_block(X, 16, self.__k, num_blocks = num_blocks_per_group, stride = (1, 1), group_name = "2")
        # add conv3 group -> stride equals 2 because output size shall be halve the input size
        X = self.add_basic_block(X, 32, self.__k, num_blocks = num_blocks_per_group, stride = (2, 2), group_name = "3")
        # add conv4 group -> stride equals 2 because output size shall be halve the input size
        X = self.add_basic_block(X, 64, self.__k, num_blocks = num_blocks_per_group, stride = (2, 2), group_name = "4")
        # add final output layer
        X = self.add_output_block(X, self.__num_classes)

        model = keras.Model(inputs = X_input, outputs = X)
        return model
    
    def add_input_block(self, X):
        '''
        this function creates one residual basic block for the input

        Args:
            X (tensorflow tensor) : keras input tensor

        Returns:
            X (tensorflow tensor) : keras tensor with new added block
        '''
        X = keras.layers.BatchNormalization(name = "conv1_Bn")(X)
        X = keras.layers.ReLU(name = "conv1_ReLU")(X)
        X = keras.layers.Conv2D(filters = 16, kernel_size = (3,3), padding = "same", name = "conv1_conv")(X)
        return X

    def add_basic_block(self, X, num_filters, k, num_blocks, stride, group_name):
        '''
        this function creates a basic residual block

        Args:
            X (tensorflow tensor) : keras input layer tensor
            num_filters (integer) : number of filters
            k (integer) : widening factor containing stretching factor of number of filters
            num_block (integer) : the number of the blocks used in the current group
            group_name (string) : string containing the name of the current block

        Returns:
            X (tensorflow tensor) : keras tensor with new added block
        '''
        block_prefix = "conv" + group_name + "_block"
        num_block = 1
        
        # create first block seperate (in order to reduce size to the required one)
        X_input = keras.layers.Conv2D(filters = num_filters * k, kernel_size = (1, 1), strides = stride,
                                    name =  block_prefix + str(num_block) + "_identity_resize")(X) # store for later addition

        X = keras.layers.BatchNormalization(name = block_prefix + str(num_block) + "_Bn1")(X)
        X = keras.layers.ReLU(name = block_prefix + str(num_block) + "_ReLU1")(X)
        X = keras.layers.Conv2D(filters = num_filters * k, kernel_size = (3,3), padding = "same", strides = stride,
                                name = block_prefix + str(num_block) + "_conv1")(X)

        X = keras.layers.BatchNormalization(name = block_prefix + str(num_block) + "_Bn2")(X)
        X = keras.layers.ReLU(name = block_prefix + str(num_block) + "_ReLU2")(X)
        X = keras.layers.Conv2D(filters = num_filters * k, kernel_size = (3,3), padding = "same",
                                name = block_prefix + str(num_block) + "_conv2")(X)
        
        X = keras.layers.Add(name = block_prefix + str(num_block) + "_add")([X_input, X])
        
        # add the other blocks
        if num_blocks > 1:
            for num_block in range(2, num_blocks+1):
                X_block = keras.layers.BatchNormalization(name = block_prefix + str(num_block) + "_Bn1")(X)
                X_block = keras.layers.ReLU(name = block_prefix + str(num_block) + "_ReLU1")(X_block)
                X_block = keras.layers.Conv2D(filters = num_filters * k, kernel_size = (3,3), padding = "same",
                                        name = block_prefix + str(num_block) + "_conv1")(X_block)

                X_block = keras.layers.BatchNormalization(name = block_prefix + str(num_block) + "_Bn2")(X_block)
                X_block = keras.layers.ReLU(name = block_prefix + str(num_block) + "_ReLU2")(X_block)
                X_block = keras.layers.Conv2D(filters = num_filters * k, kernel_size = (3,3), padding = "same",
                                        name = block_prefix + str(num_block) + "_conv2")(X_block)

                X = keras.layers.Add(name = block_prefix + str(num_block) + "_add")([X_block, X])
        return X

    def add_output_block(self, X, num_classes):
        '''
        this function adds the output block of the network. It doesn't add additional dense layers, because later we want to 
        compute the class activation maps.
        
        Args:
            X (tensorflow tensor) : tensor output from last convolutional layer
            num_classes (integer) : number of classes to classify

        Returns:
            predictions (tensorflow tensor) : keras tensor with new added block
        '''
        X = keras.layers.GlobalAveragePooling2D()(X)

        # add a flatten layer
        X = keras.layers.Flatten()(X)

        # and a fully connected output/classification layer
        # use the sigmoid function, because we want to use multilabel classification -> proabilities shouldn't depent on each other
        predictions = keras.layers.Dense(num_classes, activation='sigmoid')(X)
        
        return predictions