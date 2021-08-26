from base64 import urlsafe_b64encode
from os.path import isfile

from cryptography.fernet import Fernet
from cryptography import exceptions
from json import dump, load

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from hash import hashString

DataBaseFile = 'PW.json'


class Crypto:
    def __init__(self):
        self.personalStr = ''
        self.PWs = {}
        self.PWDigit = 20
        self.key = None
        self.fernet = None
        if not isfile(DataBaseFile):
            with open(DataBaseFile, 'w', encoding='utf-8') as database:
                print('make a new file!')
                dump({}, database)

    def setKey(self, personalStr):
        with open(DataBaseFile, 'r', encoding='utf-8') as database:
            tempPW = load(database)
            if len(tempPW) == 0:
                self.salt = Fernet.generate_key()
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=self.salt,
                    iterations=100000, )
                self.key = urlsafe_b64encode(kdf.derive(personalStr.encode()))
                self.fernet = Fernet(self.key)
                self.personalStr = personalStr
                return
            if hashString(personalStr, 40) == tempPW['VerifyKey']:
                self.salt = tempPW['Salt'].encode()
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=self.salt,
                    iterations=100000, )
                self.key = urlsafe_b64encode(kdf.derive(personalStr.encode()))
                self.fernet = Fernet(self.key)
                self.personalStr = personalStr
                return
            raise exceptions.InvalidKey

    def EncryptWithHash(self, text):
        return hashString(text, self.PWDigit)

    def makePW(self, siteName, ID):
        if siteName not in self.PWs:
            self.PWs[siteName] = {self.fernet.encrypt(ID.encode()).decode(): self.fernet.encrypt(
                self.EncryptWithHash(siteName + ID + self.personalStr + self.salt.decode()).encode()).decode()}
        else:
            for storedID in list(self.PWs[siteName].keys()):
                if ID == self.fernet.decrypt(storedID.encode()).decode():
                    return
            self.PWs[siteName][self.fernet.encrypt(ID.encode()).decode()] = self.fernet.encrypt(
                self.EncryptWithHash(siteName + ID + self.personalStr + self.salt.decode()).encode()).decode()

    def decrypt(self, siteName, ID):
        if siteName in self.PWs:
            for storedID in list(self.PWs[siteName].keys()):
                if ID == self.fernet.decrypt(storedID.encode()).decode():
                    return self.fernet.decrypt(self.PWs[siteName][storedID].encode()).decode()
            raise NameError('there is no ' + ID + ' in PWs[' + siteName + '].')
        raise NameError('there is no ' + siteName + ' in PWs.')

    def savePW(self):
        with open(DataBaseFile, 'w', encoding='utf-8') as database:
            decryptedSiteName = list(self.PWs.keys())
            for dsn in decryptedSiteName:
                self.PWs[self.fernet.encrypt(dsn.encode()).decode()] = self.PWs.pop(dsn)
            savingSlat = self.salt.decode()
            print(savingSlat)
            dump({'VerifyKey': hashString(self.personalStr, 40), 'Salt': savingSlat, 'Data': self.PWs}, database, indent=4,
                 ensure_ascii=False)

    def loadPW(self):
        with open(DataBaseFile, 'r', encoding='utf-8') as database:
            temp = load(database)
            if 'Data' in temp:
                self.PWs = temp['Data']
            else:
                self.PWs = {}
            encryptedSiteNameList = list(self.PWs.keys())
            for esn in encryptedSiteNameList:
                self.PWs[self.fernet.decrypt(esn.encode()).decode()] = self.PWs.pop(esn)

    def delSite(self, siteName):
        if siteName in self.PWs:
            self.PWs.pop(siteName)

