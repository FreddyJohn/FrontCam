# FrontCam
FrontCam is python code that detects motion and uploads the captured motion to an s3 bucket. 
It achieves this by taking the standard deviation of the absolute difference between two grayscaled 
regions of interest within two consecutive frames. This is a very simple and effective motion
detection algorithm all found in getVOSD() of FrontCam.py , if you want you can take the std
of n regions of x,y size and extrapolate close from far motion. The Graph is the upper-right corner
displays the output of this process


![alt text](https://qwertyuikmnbvcdrt67890126987mngf.s3-us-west-2.amazonaws.com/FrontCamExample.PNG)
