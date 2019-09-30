# AnomalyDetection
GitHub repository for the code that accompanies the master thesis project: 'Detecting univariate anomalies in multivariate web analytics time series'. Written in 2018 at Gradient for the completion of the Msc Data Science & Entrepreneurship.

## Abstract
In this study, anomaly detection on web metrics was performed using a recurrent autoencoder.
Previous research suggests a multivariate model could be beneficial for anomaly detection
performance. Therefore a multivariate detection algorithm is tested to see if it could indirectly
detect multiple univariate anomalies in the data. To make these anomalies more interpretable,
a sequential ensemble is used where the multivariate detector is combined with univariate
detectors to find the variable where the anomaly originated. A synthetic dataset is produced to
compare results of different configurations as the real dataset is unlabeled.
### Keywords: 
*Anomaly detection, unsupervised learning, recurrent autoencoder, multivariate time series, web metrics*

Example of the created anomaly detection solution on real data:

![alt text](https://github.com/RynoM/AnomalyDetection/blob/master/pictures/user%20anomalies.JPG)
