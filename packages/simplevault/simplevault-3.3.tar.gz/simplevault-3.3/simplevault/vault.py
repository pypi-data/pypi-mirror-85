import json
import os.path

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from fire import Fire


class Vault:
    """
    Vault is a cyphered dict saved on disk in a single file
    If vault does not exist, it is automatically created, and 
    a password is generated.
    """

    def __init__(self, password=None, path="vault.db"):
        self.path = path
        self.password = password
        self.vault = None
        if os.path.exists(path) == False:
            self.password = self.create()
            print(f"Vault didn't exists, create {path} with password {self.password}")

            
        if password is not None:
            self.__load(password, path)

    def __load(self, password, path):
        try:
            b64 = ""
            with open(path, "r") as vault_file:
                b64 = json.load(vault_file)

            nonce = b64decode(b64["nonce"])
            tag = b64decode(b64["tag"])
            data = b64decode(b64["data"])
            cipher = AES.new(b64decode(self.password), AES.MODE_EAX, nonce=nonce)
            raw_data = cipher.decrypt(data)

            cipher.verify(tag)
            self.vault = json.loads(raw_data)

        except FileNotFoundError:
            self.create()

    def view(self):
        print(self.vault)

    def keygen(self):
        return b64encode(get_random_bytes(32)).decode()

    def create(self):
        if self.password is None:
            self.password = self.keygen()

        # add entropy to file
        self.vault = {self.keygen(): self.keygen()}

        self.save()
        return self.password

    def get(self, key, default=None):
        value = self.vault.get(key, default)
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                return value

        return value

    def update(self, key, value):
        self.vault.update({key: value})
        self.save()

    def remove(self, key):
        del self.vault[key]
        self.save()

    def save(self):
        cipher = AES.new(b64decode(self.password), AES.MODE_EAX)
        nonce = cipher.nonce
        to_cipher = json.dumps(self.vault).encode()
        ciphertext, tag = cipher.encrypt_and_digest(to_cipher)
        result = json.dumps(
            {
                "nonce": b64encode(nonce).decode(),
                "tag": b64encode(tag).decode(),
                "data": b64encode(ciphertext).decode(),
            }
        )
        with open(self.path, "w") as vault_file:
            vault_file.write(result)


