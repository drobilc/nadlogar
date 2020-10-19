from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from hashlib import md5

class AESCipher(object):

    # This function is used in OpenSSL to get key and initialization vector from
    # string password. The function comes from stackoverflow
    # https://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python
    # The crypto.js module for Javascript uses no salt parameter, so the
    # argument salt is removed. 
    # https://nodejs.org/api/crypto.html#crypto_crypto_createcipher_algorithm_password_options
    @staticmethod
    def EVP_BytesToKey(password, key_length=24, initialization_vector=16):
        """Derive the key and the IV from the given password and salt."""
        dtot = md5(password).digest()
        d = [ dtot ]
        while len(dtot) < (initialization_vector + key_length):
            d.append(md5(d[-1] + password).digest())
            dtot += d[-1]
        return dtot[:key_length], dtot[key_length:key_length+initialization_vector]
    
    @staticmethod
    def encrypt(password, data):
        # Use the function defined above to get key and initialization vector
        # from our password string
        key, initialization_vector = AESCipher.EVP_BytesToKey(password.encode('latin1'))

        # Create a new AES cipher
        aes = AES.new(key, AES.MODE_CBC, iv=initialization_vector)

        # Pad our data using the PKCS#7 padding algorithm
        padded_data = Padding.pad(data.encode('utf-8'), 16, style='pkcs7')

        # Encrypt the padded data
        encrypted = aes.encrypt(padded_data)

        # Return converted bytestring to hex values
        return encrypted.hex()