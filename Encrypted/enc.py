from cryptography.fernet import Fernet as en
from cryptography.fernet import Fernet as dek

text = "My super secret message"
textb = bytes(text, 'utf-8')

#выработка ключа
cipher_key = en.generate_key()
#установка ключа
cipher = en(cipher_key)
#шифрование
encrypted_text = cipher.encrypt(textb)

print(textb)
print(f"Ключ: {cipher_key}")
print(f"Шифртекст: {encrypted_text}")
print("################################")

sendline = cipher_key + encrypted_text
print(sendline)

print("################################")
#выработка ключа
cipherdek = dek(sendline)
#разшифрование
decrypted_text = cipherdek.decrypt(encrypted_text)
print(decrypted_text.decode("utf-8") ) # 'My super secret message'