# Novel Steganographic Messaging Protocol
###Created by: Anas Hasan, Manan Monga, Michael Korovkin, Samyak Jain, Taka Shirono, Ivan Izhbirdeev

This messaging protocol was created as part of Boston University EC521: Cybersecurity class final project. We created a novel steganographic messaging protocol uses AES-CTR Mode and steganographic methods to allow secure communication between two parties without raising suspicion of an eavesdropper.

## How to use our messaging protcol (Mac)
1. First make sure you have some form of conda installed in your environment. (Refer to: <https://docs.anaconda.com/anaconda/install/>)
2. Open terminal and create a conda environment from our requirements.yml

    `conda env create -f Novel_Stego_Protocol.yml`
    
3. Activate the conda environment

    `conda activate Novel_Stego_Protocol`
    
4. Open one more terminals and activate conda environment

5. On one of the terminal, run the messaging server
    
    `python setup_server.py`

6. On the other terminal open a messaging client

    `python send_receive_stego.py`
    
7. Have your buddy open another client and you can send message to each other securely! Alternatively open another terminal on your own, activate the conda environment, and start messaging yourself...