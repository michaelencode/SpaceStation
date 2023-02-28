from cryptography.fernet import Fernet

key="JohnstoneSupplyTheWaregroupJacksonvilleMoon="

def encry(passcode):
    fernet=Fernet(key)
    encMessage=fernet.encrypt(passcode.encode())
    return encMessage

def decry(depasscode):
    fernet=Fernet(key)
    decMessage=fernet.decrypt(depasscode).decode()
    return decMessage
