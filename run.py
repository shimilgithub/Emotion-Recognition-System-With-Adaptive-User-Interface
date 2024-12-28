#This file loads the build CNN model and create adaptive user interface based on emotion
import tkinter as tk
from tkinter import filedialog, Label
from PIL import Image, ImageTk
import numpy as np
import cv2
import tensorflow as tf
import os


# Load the trained model
model = tf.keras.models.load_model('best_model.keras')

# Define emotion categories
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# GUI root
root = tk.Tk()
root.title("Emotion Detection with Adaptive UI")
root.geometry("600x500")

def load_image(file_path):
    '''Function to load and preprocess image'''
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (48, 48))  # Resize to match model input
    img = img / 255.0  # Normalize
    img = np.expand_dims(img, axis=-1)  # Add color channel dimension
    img = np.expand_dims(img, axis=0)   # Add batch dimension
    return img

def get_actual_label(file_path):
    '''Function to get the actual label from the image path'''
    # The label is the last subdirectory in the path (before the image file)
    label = os.path.basename(os.path.dirname(file_path))
    return label

def adaptive_interface(emotion):
    '''Function to handle adaptive UI based on emotion'''
    if emotion == "Happy":
        root.configure(bg="yellow")
        response_label.config(text="You look happy! Share your joy with others!", fg="green")
    elif emotion == "Sad":
        root.configure(bg="lightblue")
        response_label.config(text="It's okay to feel sad. Take a moment for yourself.", fg="blue")
    elif emotion == "Angry":
        root.configure(bg="lightgrey")
        response_label.config(text="Anger is natural. Take a deep breath and let it go.", fg="red")
    elif emotion == "Disgust":
        root.configure(bg="purple")
        response_label.config(text="Disgust can be tough. Focus on something positive.", fg="white")
    elif emotion == "Fear":
        root.configure(bg="orange")
        response_label.config(text="Fear is temporary. You are stronger than you think.", fg="brown")
    elif emotion == "Surprise":
        root.configure(bg="pink")
        response_label.config(text="Surprises can be exciting! Embrace the unexpected.", fg="magenta")
    else:  # Neutral
        root.configure(bg="white")
        response_label.config(text="Feeling neutral is perfectly fine. Stay balanced.", fg="black")

def detect_emotion():
    '''Function to detect emotion from loaded image'''
    file_path = filedialog.askopenfilename()
    if file_path:
        img = load_image(file_path)
        
        # Extract the actual label from the file path
        actual_label = get_actual_label(file_path)
        
        # Make prediction
        predictions = model.predict(img)
        predicted_class_idx = np.argmax(predictions)
        predicted_emotion = emotion_labels[predicted_class_idx]
        prediction_score = predictions[0][predicted_class_idx]  # Get the score for the predicted class
        
        # Display prediction with score
        emotion_label.config(text=f"Detected Emotion: {predicted_emotion} ({prediction_score*100:.2f}%)")
        actual_label_label.config(text=f"Actual Label: {actual_label}")

        # Update adaptive interface
        adaptive_interface(predicted_emotion)

        # Show the selected image in the interface
        display_img = Image.open(file_path)
        display_img = display_img.resize((200, 200))
        tk_img = ImageTk.PhotoImage(display_img)
        image_label.config(image=tk_img)
        image_label.image = tk_img


# UI Components
title_label = Label(root, text="Emotion Detection with Adaptive UI", font=("Helvetica", 16))
title_label.pack(pady=10)

image_label = Label(root)
image_label.pack()

detect_button = tk.Button(root, text="Upload Image for Emotion Detection", command=detect_emotion)
detect_button.pack(pady=20)

emotion_label = Label(root, text="", font=("Helvetica", 14))
emotion_label.pack(pady=10)

actual_label_label = Label(root, text="", font=("Helvetica", 12))
actual_label_label.pack(pady=10)

response_label = Label(root, text="", font=("Helvetica", 12))
response_label.pack(pady=10)

# Run the Tkinter GUI
root.mainloop()
