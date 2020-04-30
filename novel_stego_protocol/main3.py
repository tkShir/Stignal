from textgenrnn import textgenrnn

textgen = textgenrnn(name="/home/amazonec2/Downloads/textgenrnn-master/alltermscontext")
textgen.train_from_file('/home/amazonec2/Downloads/textgenrnn-master/datasets/r52-test-all-terms.txt',
                        new_model=True,
                        word_level=True,
                        rnn_bidirectional=True,
                        max_length=40,
                        rnn_layers=4,
                        rnn_size=256,
                        max_words=20000,
                        dim_embeddings=300,
                        context=True,
                        num_epochs=10)
textgen.save('/home/amazonec2/Downloads/textgenrnn-master/alltermscontext')
# textgen.train_from_largetext_file(fulltext_path, new_model=True, num_epochs=1,
#                                   word_level=True,
#                                   max_length=10,
#                                   max_gen_length=50,
#                                   max_words=5000)
# textgen = textgenrnn('/home/amazonec2/Downloads/textgenrnn-master/weights/reddit_rarepuppers_politics.hdf5')
# textgen.generate(interactive=True, temperature=2.0, top_n=3)




# stegotext = ""
# for every half-byte in ciphertext:
#     option_num = the number equivalent of the half-byte
#     transformed = T[option_num]
#     # query the model with option_num to get the next T[]
#     stegotext += transformed

# ciphertext = ""
# for every human_word in stegotext:
#     cipher_half_byte = T[human_word] # this will find the option number from the name
#     # query the model with cipher_half_byte to get the next T[]. cipher_half_byte would be the equivalent of option_num from the function above
#     ciphertext += cipher_half_byte
