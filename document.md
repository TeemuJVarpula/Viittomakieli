# Work Estimates

    # Maybe this section could be removed.

# Change Log

| Version | Changes made                           | Date      |
| ------- | -------------------------------------- | --------- |
| 1.0     | First version of document              | 14.2.2024 |
| 1.3     | Table of contents added                | 23.2.2024 |
| 1.7     | Flowchart diagram of the program added | 29.2.2024 |

# Project Version and Deadline

| Version | Deadline  | Relevant Dates | Scope and Deliverables                               |
| ------- | --------- | -------------- | ---------------------------------------------------- |
| 1.0     | 1.3.2024  | 26.2.2024      | Raspberry Pi setup                                   |
| 1.1     | 6.3.2024  | 26.2.2024      | Raspberry Pi image recognition                       |
| 1.2     | 8.3.2024  | 8.3.2024       | Raspberry Pi working display                         |
| 1.3     | 15.3.2024 | 15.3.2024      | 3 character identification                           |
| 1.4     | 22.3.2024 | 22.3.2024      | Whole alphabet identification and control characters |

# Introduction

The aim of this project is to develop a real-time system that can detect hand gestures of Finnish sign language alphabet capture by the camera using OpenCV and Tensorflow running on Raspberry Pi. The system will use our own image collection to train the recognition model.The system can recognize Finnish Sign Language alphabet from A-Y and control signs such as "enter", "space","delete" and "backsapce.

# Project overview

Software is running on Raspberry Pi and signs to be recognized are taken with camera connected to it. Image is taken by pressing space button from key board. Each alphabet has 100 images. Recognition level will be shown in the screen in percentage level and sign recognized accuracy level has to be 30% is recognized, it will be display in LCD screen for the recipient.

## Hardware Requirements

- Raspberry Pi
- Camera module Breadboard
- LCD Display for recognized letters

## Software Requirements

- Python
- OpenCV
- TensorFlow

## System Architecture

The system architecture consists of the following components:

- Raspberry Pi: The main computing platform and interfaces with the camera module for capturing frames.
- Python Script(Sign Detector)The core component responsible for processing captured frames, detecting hand gestures, and classifying them into predefined signs.
- MediaPipe Library: Used for hand landmark detection in real-time frames.
- Scikit-Learn Library: Used for training a Random Forest classifier to classify hand gestures.
- OpenCV: Used for image processing tasks such as frame cature, color conversion.
- CameraWrapper.py: This program provides cross-platform compatibility to use camera for image capture.

# Functional requirements

## General description

System needs to recognize atleast one Finnish sign alphabet character and display it on the screen. The state of accuracy of recognizion must be shown to the screen.

## Components and functions

### Image Capturing

User presses space button from keyboard to capture image from camera attached to Raspberry. 

### Image recognition

- Project uses machine learning to train the recognition model and computer vision to identify signs from images. The main steps how the recognition works.
- OpenCV to preprocess the images to get better suited data for this task Images need to be labelled for sign detection.
- Training will be done with TensorFlow
- Sign detection from the image.

### Show state of recognition of image

Recognition level is shown in the frame display with the percentage.

### Show recognized characters to recipient

Recognized characters are diplayed in the screen frame and 1602 LCD display. New characters are appended to the end when recognized.

# Non-functional requirements

## Training of the model

Training the AI model can take quite a long time and should be done on more powerfull pc than Raspberry Pi.

## Raspberry Pi cooling

Considering image prosessing is quite a demanding task, processor might get hot without proper heatsink. Temperature should be monitored during use and specially during live video recognition.

# FlowChart

# Limitations

The Sign Language Detector has several potential limitations to consider:

- Limited Gesture Vocabulary: The system is only limited to Finnish sign language letters.
  are recognized and only stationary signs are supported.
- Recognition Accuracy: Despite of trained model with sufficient data, the recognition accuracy of hand gestures may vary depending on factors such as lighting conditions, hand alignment,and occlusions.
- Processing Power: The computational resources of the Raspberry Pi may limit the sytem´s real-time performance, especially when processing high-resolution frames.

## Conclusion

The Sign Detector for Raspberry Pi project successfully developed a real-time system for reconiging Finnish Sign Alphabet hand gestures and enabling user interaction with Raspberry Pi.
