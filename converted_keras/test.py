import numpy as np
import cv2
import tensorflow.keras
from PIL import Image
from time import sleep

cap = cv2.VideoCapture(0)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)

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

    # Slow down the imgages being get
    sleep(0.1)

    # Get the img into PIL
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    # Make sure to resize all images to 224, 224 otherwise they won't fit in the array
    image = image.resize((224, 224))
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)
    # prediction_value = np.where(prediction == np.amax(prediction))[0]
    pred_val = np.argmax(prediction)
    switcher = {
        0: "Nothing",
        1: "Up",
        2: "Down",
        3: "Right",
        4: "Left"
    }
    print(switcher.get(pred_val, "Return Nothing"))
    # print(pred_val)

    # Display the resulting frame
    cv2.imshow('Cur frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
