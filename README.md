# I can & I will  VOTE 
## A SOLUTION FOR LOST VOTES TECH SOLUTIONS  CHALLENGE HACKATHON BY TIMES OF INDIA
### A Secure and fair eVoting  System, to ensure correct and  encrypted	election from any  where in India.

Features
--------

  * Public Key Infrastructure and Hyperledger blockchain  Fabric identity technology to ensure a secure voting platform with full  encryption and security
  * government iD proof  verification is including the most accurate Tensorflow and OpenCv caffemodel facial  detection 
  * Fingerprint recognition with SKimage and OpenCV	to match the biometrics  from adhaar without using any	external hardware device to ensure security
  * voice matching	at the time of	voting
  * analyze  behavioural pattern of the voter	during the time of  voting which will analyze behavioural patterns to  predict weather a voter is voting under any wrong  criminal influence or superiors pressure    
  * Live encrypted video chat With 256 Bit AES Encryption  with the election commision employee

## About this repository
* This respository contains 6 Sub folders containing App features, currently for prototype stage of eVoting system is demonstrated in web app format which will be converted into android and ios application in later stages.

### adhaar_authentication__Team_iron_man
* This python package supports biometrics and demographics authentication using the Aadhaar Authentication Service (also known as UID). The library takes care of the details of packaging data and communicating with the Aadhaar authentication server leaving the developer to focus on the application, say Aadhaar-enabled payments.This implementation is basically compliant with Aadhaar authentication API Ver 1.5 (Rev 1) but is WIP.

### audio_classification_Team_iron_man/scripts
* we are converting audio files to spectrograms. Then we are trainning the model with spectrograms of audio files. Instead of inventing something new we are trying to make use, we are using Google's Inception model.

### mental_status__Team_iron_man
*  Effort addresses an automated device for mental status and current behaviour from acoustic features in speech. 

### eVoting_blockchain__Team_iron_man
Architecture of network

![alt tag](https://raw.githubusercontent.com/ngocjr7/voting-blockchain/master/docs/architecture.png)

![alt tag](https://raw.githubusercontent.com/ngocjr7/voting-blockchain/master/docs/network_sample.png)


#### Certificate Authority

It can validate connection when a node ask to join to network and Set permission for each node and validate transaction

#### Orderer

It can hold a list of peers and broadcast to all peer when receive a request broadcast new block or new transaction.
It also have consensus method, which can return the longest blockchain in the network

#### Peer

It hold all data about blockchain, it have some method like mine, validate_transaction, return chain, open surveys, ...





