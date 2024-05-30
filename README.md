# Drowsiness_Detection_System

## Project Overview
Driver drowsiness is a significant cause of road accidents, responsible for over 30% of incidents. This project aims to develop a non-intrusive system to detect driver fatigue and issue timely warnings, thereby reducing the risk of accidents caused by drowsiness.

## Features
Real-time Monitoring: Utilizes a camera to monitor the driver's eyes.
Fatigue Detection Algorithm: Detects symptoms of driver fatigue by analyzing eye closure and facial landmarks.
Alert Mechanism: Issues an audible alarm and applies brakes to reduce vehicle speed when drowsiness is detected.
## Project Components
Hardware
Camera for real-time monitoring
Servo motor for brake application
Buzzer for alarm
Software
Image processing using Dlib library
Fatigue detection algorithm based on Eye Aspect Ratio (EAR)
Integration with vehicle control systems
System Architecture
The system continuously captures video frames of the driver’s face, processes these frames to detect eye closure, and calculates the Eye Aspect Ratio (EAR). If the EAR indicates prolonged eye closure, the system triggers an alarm and applies brakes.

## Methodology
Data Collection: Capturing video data of the driver.
Processing: Using Dlib to identify facial landmarks and calculate EAR.
Detection: Analyzing EAR over time to detect drowsiness.
Response: Activating the alarm and applying brakes.
Results
The system was tested under various conditions and successfully detected drowsiness, issuing timely warnings and controlling the vehicle's speed to enhance safety.

## Future Work
Improving detection accuracy under different lighting conditions.
Enhancing the algorithm to reduce false positives.
Integrating with advanced driver-assistance systems (ADAS).
## Conclusion
This Driver Drowsiness Detection System provides a practical solution to enhance road safety by detecting driver fatigue and issuing timely alerts, potentially saving lives and reducing accident rates.
