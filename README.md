# datacamp-image-processing-with-keras
Repository for all notes and solutions to challenges in the course Image Processing with Keras in Python offered by DataCamp.

# Image Processing with Neural Networks

## Images as data

* Images can be read using the matplotlib library and displayed using a plot function.
* However, the computer does not see the image. It is interpreted as an array/matrix of numbers.
* Colored images are read in 3 dimensions:

        data.shape
        # Prints: (2850, 3000, 3)
    
    Here, the first two dimensions correspond to the heights and width of the image (number of pixels). The third dimension corresponds to the color (RGB). Here, 3 corresponds to Red color.

* A particular pixel can be read by using the spatial dimensions and can be modified.

        data[:10, :10, 0] = 1

    Here, we set the red channel of the first 10x10 pixels to 1, making a red square. The green and blue channels are denoted by 1 and 2 respectively.

## Classifying images

* For example, you have images related to fashion items - Shoes, T-shirts, Dresses. These images can be classified into their respective categories.
* A classifier is trained with the images and their labels.
* While specifying the class labels - Neural networks expect the labels of classes in a dataset to be organized in a one-hot encoded manner: each row in the array contains zeros in all columns, except the column corresponding to a unique label, which is set to 1.
* To evaluate the classifier, images that are not used during training are used.
* The output of the classifier is one-hot encoded. This can be used to find the correct number of predictions.
* Number of correct predictions can be obtained as follows:

        number_correct = (test_labels * predictions).sum()


# Using Convolutions

In the above section, we just used pixels in the images for classification.
However, natural images often contain correlations, such as, some pixels may represent edges or a contour. Such correlations are of great use in classification.

## Convolutions

* Each image can be assumed to be made up of pixels that represent one mathematical operation called Convolution. This is a basic operation that is used by Convolutional Neural Networks to process images.

### Convolution Example

Consider the following data:

        array = np.array([0,0,0,0,0,1,1,1,1,1])

    Here, the above data represents an edge where the values go from 0 to 1.

* A kernel represents the feature we are looking for:

        kernel = [-1, 1]

* A convolution of an one-dimensional array with a kernel comprises of taking the kernel, sliding it along the array, multiplying it with the items in the array that overlap with the kernel in that location and summing this product.

* Similarly, a convolution in two dimensions can be created. Here, the kernel and the window of the image pixels is a 2D matrix.

* Examples:

    A kernel that identifies vertical lines in an image:
    ```
    [-1, 1, -1
     -1, 1, -1
     -1, 1, -1]
    ```

    A kernel that identifies horizontal lines in an image:
    ```
    [-1, -1, -1
      1,  1,  1
     -1, -1, -1]
    ```

    A kernel that identifies a bright spot surrounded by dark spots:
     ```
    [-1, -1, -1
     -1,  1, -1
     -1, -1, -1]
    ```

## Convolutions in Keras

Keras provides functions to create convolutional neural networks.

    from keras.models import Sequential
    from keras.layers import Conv2D, Dense, Flatten
    
    model = Sequential()
    model.add(Conv2D(10, kernel_size=3, activation='relu', input_shape=(img_rows, img_cols, 1)))
    model.add(Flatten())
    model.add(Dense(3, activation='softmax'))

Here, the Flatten layer is a connector between the convolutional layer and the Dense layer. It takes the output of the convolutional layer which is in the form of a feature map and flattens it into a one dimensional array.

![](images/cnn.PNG)

### Tweaking Convolutions

1. Padding

* In cases as above, the output has less dimensions as compared to the input. To avoid this, the input can be zero padded.
* Padding allows a convolutional layer to retain the resolution of the input into this layer.
* This is done by adding zeros around the edges of the input image, so that the convolution kernel can overlap with the pixels on the edge of the image.

![](images/zero_pad.PNG)

* In keras, this can be done by adding a 'padding' keyword argument to the keras Conv2D function.

    Conv2D(10, kernel_size=3, activation='relu', input_shape=(img_rows, img_cols, 1), padding='same')

The default behavior is no padding applied and can be specified by padding='valid'.

2. Size of the Stride

* The size of the strides of the convolution kernel determines whether the kernel will skip over some of the pixels as it slides along the image.
* This affects the size of the output because when strides are larger than one, the kernel will be centered on only some of the pixels.
* For example, although padding is applied, the size of the output can be smaller than the input if the step size is 2 pixels.
* Stride can be specified using the *strides* keyword argument to Conv2D. The default value is 1.

3. Dilated Convolutions

You can also control which pixels get affected by the kernel. Such convolutions are called *Dilated Convolutions*.

In keras, this can be achieved by passing a parameter *dilation_rate* to the Conv2D method.

![](images/dilated_cnn.PNG)

### Calculating the size of the output

The size of the output can be calculated with the help of a simple formula:

    O = ((I - K + 2P) / S) + 1

    where,
    I = Size of the Input
    K = Size of the Kernel
    P = Size of the zero padding
    S = Strides

# Building Deeper CNNs

* Networks with more convolution layers are called "deep" networks, and they may have more power to fit complex data, because of their ability to create hierarchical representations of the data that they fit.
* Multiple convolutional layers can be added to build deeper CNNs.

![](images/deep_cnn.PNG)

* Deeper CNNs are needed to gradually build up representation of objects in the images.
* The first layers can capture features such as oriented lined, the last few layers can capture complex objects based on the outputs of these layers. Hence, deeper networks are more useful in image processing.
* Hence, deep networks may require more data and more computations to fit.

## Counting Parameters

* We need to know how many parameters a CNN has, so we can adjust the model architecture, to reduce this number or shift parameters from one part of the network to another. 
* Number of parameters in a model can be calculated as follows:

* For a model layer with 10 units and input_shape of (784, )

        No. of parameters = 784*10 + 10

Number of pixels times the number of units and 10 added for the bias terms.

Similarly, number of parameters can be calculated for rest of the layers. 

In keras, these details can be obtained using

        model.summary()

## Pooling Operations

* One challenge with deep CNNs is reducing the number of parameters. 
* To mitigate this, we can summarise the output of the convolutional layers. For example, we can summarise the output of a group of pixels by their maximal value. This is called *Max Pooling*.
* This ensures that the output has only about a quarter of the features and shows only the brightest values.
* Pooling can help us if we want to train the network more rapidly, or if we don't have enough data to learn a very large number of parameters.

![](images/max_pooling.PNG)

* In keras, Max Pooling can be done with the help of MaxPool2D object.

        from keras.models import Sequential
        from keras.layers import Dense, Conv2D, Flatten, MaxPool2D

        model = Sequential()
        model.add(Conv2D(...))
        model.add(MaxPool2D(2))

    After each convolutional layer, we add a pooling layer. Here, 2 indicates the size of the Pooling window, i.e. Pooling will take max over a window of 2 x 2 pixels.

# Improving Deep Convolutional Networks

## Regularisation

Deep CNNs often tend to overfit the data. To avoid overfitting, regularisation can be used.
There are two techniques of Regularisation:

**1.Dropout**

* In each learning step, we select a subset of the units.
* This subset is ignored in the forward pass.
* and also ignored in the backpropagation of errors.

![](images/dropout.PNG)

* This method tends to work well because if some nodes in the network become too sensitive to noise in the data, the other nodes compensate for it.

In keras, Dropout is implemented as a layer. We add this layer after the layer in which we want to ignore subsets.

        model.add(Conv2D(...))
        model.add(Dropout(0.25))

Here, 0.25 indicates the proportion of the units to be ignored.

**2.Batch Normalization**

* In this technique, the output of a particular layer is rescaled so that it always has zero mean and a standard deviation of 1 in every batch of training.
* It solves the problems that arise when different layers produce extremely different distributions of the output.

In keras, Batch Normalization is implemented as a layer. We add this layer after the layer which we want to normalise.

        model.add(Conv2D(...))
        model.add(BatchNormalization())

**Using Dropout and Batch Normalization together**

* Dropout tends to slow down the learning process by making learning more careful in the subsequent layers, while Batch Normalization fastens the learning speed.
* When both these methods are used together, their effects may counter each other. This may lead to a worsened model performance.
* This is called the disharmony between Dropout and Batch Normalization. You must be careful while using them together.

## Interpreting Models

* On major criticism of deep CNNs is that they are a black box, although they work well, it is hard to understand why they work well.
* Interpreting the model is important and this can be done by visualising what certain parts of the model do.

In keras, parts of the model can be selected and analyzed.

        model.layers
        conv1=model.layers[0]   # first layer
        weights = conv1.get_weights()

get_weights() returns an array of two elements - kernels and

        kernel1 = weights[0]
        kernel1_1 = kernel1[:, :, 0, 0]

This kernel can be visualised using:

        plt.imshow(kernel1_1)

It is hard to identify what the kernel emphasized by visualising it alone. We can convolve the kernel with an image from the test set.

        filtered_image = convolution(test_image, kernel1_1)
        plt.imshow(filtered_image)

The result of this image is:
    ![](images/filtered_image.PNG)

We can see that this kernel depicts the edges of an object in the image.

# Links
* [Keras Cheatsheet](https://datacamp-community-prod.s3.amazonaws.com/94fc681d-5422-40cb-a129-2218e9522f17)