# README #
## TextEncryptor - A simple python package for encryting plain text. ##

### What do I do?  ###

This package contains a number of functions which are used for 
encrypting and decrypting text files and plain text. The important
functions for the user are the following

1. textencryptor.encrypt_file() 
2. textencryptor.decrypt_file()
3. textencryptor.encrypt_message()
4. textencryptor.decrypt_message()
5. textencryptor.send_encrypted_email()

Functions 1 & 3 work by encrypting either a user specified 
text file (1.), or a user given message (3.), using a user
given encryption pin/password. 

The encrypted text file or message can be later decrypted
using functions (2.) or (4.), provided that the decryption
pin is identical to the pin used for encryption.  

Function (5.) uses encrypt_message() to encrypt some plain text.
This plain text is then sent in an email. Note that this currently
only works with gmail. Some modifications to your gmail account 
settings will be required. By default gmail will block pythons 
attempts to log in to your gmail account, as it deems it insecure.
    
To allow python access to your gmail, go to the following link
https://myaccount.google.com/lesssecureapps
and switch 'allow less secure apps' to ON. 

**Notes:**

I. No inputs are required for the five main functions, if 
left as, e.g. textencryptor.encrypt_file(), the user will be 
prompted for the required infromation, in this example:

1. The path to the file to be encrypted.
2. The encryption pin. 
3. The path for the encrypted file to be saved to. 

This information can of course be input, then no information
will be required from the user, e.g. 

textencryptor.encrypt_file(load_file_path='example.txt', pin = 123456, save_file_path='encrypted_example.txt')

will create an encrypted file named encrypted_example.txt.
This file is an ecnrypted version of the file example.txt
with encryption pin = 123456. 

II. The algorithms in this package are hard coded in the 
english language. Symbols used in many european languages
(e.g. Å,Ê,Î,Ó,Ù etc...) will be lost in the encryption
and decryption proccess.  

III. send_encrypted_email() ONLY works with gmail. See the 
send_emcrypted_email() function for more information. 


### How do I get set up? ###

**Method one:**
* pip install textencryptor

**Method two:**
* Pull into it's own folder
* Within the folder, run "python3 -m pip install -e ."

