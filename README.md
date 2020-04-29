# Novel-Steganographic-Scheme-EC521-Leetz

TODO:

1. Function to send IP packets containing stegotext. [NEARLY DONE]

2. Function to recieve IP packets and extract the stegotext, so that we can operate on it. [NEARLY DONE]

3. Finding a deterministic neural networking model to be exchanged. [DONE]

4. Function to encrypt input. [DONE]

5. Function to decrypt output. [DONE]

6. Function that applies the model to transform the ciphertext into a stegotext. [DONE]

7. Function that applies the model to transform the stegotext into the ciphertext. [DONE]


###Use any ready libraries if available. Make sure to review its contents first##### [ALSO DONE]

for 1 and 2. To set up sending and recieving of packets: https://wiki.python.org/moin/TcpCommunication
We only want to send and recieve packets containing english text. There is no manlipulation of any headers, keep it simple. The code in the wiki is trusted. [DONE]

3. still in testing, any suggestions are welcome and recommended. [DONE]


for 4 and 5. Our choice for the encryption scheme is AES-CTR, python implementation is found here: https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html 
We will apply AES-CTR on the message before it is transformed. So we need to encrypt the message and store it. This library is trusted. [DONE]

6 and 7. this is basic use of dictionaries in python. There are a few steps in 3. that depend on this. [DONE]

