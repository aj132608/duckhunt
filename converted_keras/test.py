import numpy as np
import cv2
import tensorflow.keras
from PIL import Image

cap = cv2.VideoCapture(0)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Flip the image
    frame = cv2.flip(frame, 1)

    img = Image.fromarray(frame)

    # Display the resulting frame
    cv2.imshow('Cur frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
