# BallBalanceV2
New and improved ball balancing system

Sense: Webcam w/ OpenCV to get ball position  
Reason: Python running on laptop caluclates response angles w/ PID control and sends to arduino  
Act: Arduino controls 2 servo motors w/ arm joints connecting to platform  

Materials:  
  Arduino MKR 1010  
  Logitech WebCam  
  2 MG995 servo motors  
  Surface cut from 3-ring binder  
  Ball to balance  
  3D-printed parts  
    Center joint(2 Pieces)  
    Arm joint (2 pieces each)  
    
Improvements from V1:  
  Computer vision vs unfiltered 4-wire rewsistive touch screen gave more accurate position measurements  
  3D printed joints made struture much stronger, less wiggle room between motor and surface gave more accurate tilt outputs  
    
Limitations:  
  Cheap motors with slow angular velocity made response to large impulses very hard  
  Golf ball used - dimples on surface made fine control hard  
 
