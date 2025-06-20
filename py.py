# from cryptography.fernet import Fernet

# # ✅ Generate a key (do this ONCE and store it securely)
# key = Fernet.generate_key()
# print(f"Generated Key: {key.decode()}")  # Save this for future use

# # ✅ Create a Fernet cipher object
# cipher = Fernet(key)

# # ✅ Encrypt data
# plaintext = "Sishir Siam".encode()
# encrypted = cipher.encrypt(plaintext)
# print(f"🔐 Encrypted: {encrypted.decode()}")

# # ✅ Decrypt data
# decrypted = cipher.decrypt(encrypted)
# print(f"🔓 Decrypted: {decrypted.decode()}")


# from cryptography.fernet import Fernet
# print(Fernet.generate_key().decode())




sss = b"Sishir Siam"
print(sss)
print(sss.decode())