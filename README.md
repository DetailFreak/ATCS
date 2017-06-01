# ATCS
Amity Traffic Control System

Objective:
To reduce time wasted at railway crossings By:
- Providing real time information on the status of crossing.
- Estimating of time for the crossing to change status (open/close).
- Providing the traffic status at the crossing.

Methodology :
The methodology adopted uses machine learning and Image processing as well as additional hardware sensors to improve accuracy and make the system robust.

Summary : 
The project aims to alleviate the suffering of commuters to Amity Lucknow campus by providing a website as well as an android app to tell them the exact time they should leave their home to reach with least stoppage. 

The project consists of three modules
    1. Sensing mechanism.( Hardware )
    2. Image processing
           - crossing detection ( using LeNet over a pre processed image database )
           - traffic counting
    3. Android app and website.

1. The sensing mechanism consists of hardware deployed near the crossing which includes a battery, a solar panel, 2 video cameras, a laser trap, a GSM module and a raspberry pi 3, all these components are placed in a weatherproof housing near the railway crossing. These devices have the responsibility of sensing, processing and sending the status 	of the crossing to the server.
2. This part of the system consists of python scripts which run on the raspberry pi, they will process the video feeds and the laser sensor to produce the status of the crossing, the laser sensor will provide the initial training data to train the neural network which is used to detect the crossing status. The traffic counter estimates the traffic density around the crossing area using moments method of contours formed by moving vehicles. The foreground detection is done by using adaptive background subtraction.
3. The web server and the application will get prior information about trains approaching the crossing using the IndianRailwaysAPI. The data is stored and improved upon using our previous data on the crossing status over there, you can see realtime status of the crossing on the application.
