import tensorflow as tf
# config = tf.C
# config.gpu_options.allow_growth = True
# session = tf.Session(config=config, ...)
from textgenrnn import textgenrnn
print("input hdf5 file directory")
textgendir = input("input hdf5 location: ")
textgen = textgenrnn(textgendir)
from bitstring import BitArray

print("####PLAINTEXT###")
plainbyte = "h3defwed2d2d2ed2d23di".encode()
print(plainbyte)
print("####CIPHERTEXT#####")
inputbyte = "g2d23d2d23d23d221c".encode()
print(inputbyte)
c = BitArray(inputbyte)
print(c.bin)
print("####TRANSFORMED######")
stegotext = textgen.generate(interactive=True, temperature=0.2, top_n=2, ciphertext=inputbyte)
print(stegotext)
print("#######")
print("###SERVER###")
print(stegotext)
print("#####")

print("#######")
print("RECIEVING")
print("#######")
print(stegotext)
inputbyte2 = stegotext.encode()
# print(inputbyte2)
recovered = textgen.generate2(interactive=True, temperature=2.0, top_n=2, stegotext=inputbyte2)
print(recovered)
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])
byte_ciphertext = bitstring_to_bytes(recovered)
print(byte_ciphertext)
print("#DECRYPT#")
print(plainbyte)



print("####PLAINTEXT###")
plainbyte = "HELLO WORLD!".encode()
print(plainbyte)
print("####CIPHERTEXT#####")
inputbyte = "HELLO WORLD!".encode()
print(inputbyte)
c = BitArray(inputbyte)
print(c.bin)
print("####TRANSFORMED######")
stegotext = textgen.generate(interactive=True, temperature=0.2, top_n=2, ciphertext=inputbyte)
print(stegotext)
print("#######")
print("###SERVER###")
print(stegotext)
print("#####")

print("#######")
print("RECIEVING")
print("#######")
print(stegotext)
inputbyte2 = stegotext.encode()
# print(inputbyte2)
recovered = textgen.generate2(interactive=True, temperature=2.0, top_n=2, stegotext=inputbyte2)
print(recovered)
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])
byte_ciphertext = bitstring_to_bytes(recovered)
print(byte_ciphertext)
print("#DECRYPT#")
print(plainbyte)



print("####PLAINTEXT###")
plainbyte = "EC521 rocks".encode()
print(plainbyte)
print("####CIPHERTEXT#####")
inputbyte = "EC521 rocks".encode()
print(inputbyte)
c = BitArray(inputbyte)
print(c.bin)
print("####TRANSFORMED######")
stegotext = textgen.generate(interactive=True, temperature=0.2, top_n=2, ciphertext=inputbyte)
print(stegotext)
print("#######")
print("###SERVER###")
print(stegotext)
print("###SERVER###")
print("#####")

print("#######")
print("RECIEVING")
print("#######")
print(stegotext)
inputbyte2 = stegotext.encode()
# print(inputbyte2)
recovered = textgen.generate2(interactive=True, temperature=2.0, top_n=2, stegotext=inputbyte2)
print(recovered)
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])
byte_ciphertext = bitstring_to_bytes(recovered)
print(byte_ciphertext)
print("#DECRYPT#")
print(plainbyte)
