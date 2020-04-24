# Import matplotlib
import matplotlib.pyplot as plt

# Load the image
data = plt.imread('bricks.png')

# Set the red channel in this part of the image to 1
data[:10, :10, 0] = 1

# Set the green channel in this part of the image to 0
data[:10, :10, 2] = 0

# Set the blue channel in this part of the image to 0
data[:10, :10, 1] = 0

# Visualize the result
plt.imshow(data)
plt.show()