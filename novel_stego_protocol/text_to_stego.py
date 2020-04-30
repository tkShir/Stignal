from textgenrnn import textgenrnn

textgen = textgenrnn('/home/amazonec2/hacker_news.hdf5')

def text_to_stego(ciphertext_to_steg):
    stegotext = textgen.generate(interactive=True, temperature=0.2, top_n=2, ciphertext=ciphertext_to_steg)
    print(stegotext)
    return stegotext

text_to_stego(b'rnaodmdomeodshit')
