import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import nacl.secret
import nacl.utils
import base64
import json
import paramiko
import nacl.signing
from sshpubkeys import SSHKey



def main():
    myKey = paramiko.Ed25519Key(filename="asd_signing")
    skey = myKey._signing_key
    if isinstance(skey, nacl.signing.SigningKey):
        print("YAY!")

    data = base64.b64encode("blah blah".encode("utf-8"))
    msg = myKey.sign_ssh_data(data)

    print(repr(msg))

    pubKey = myKey.get_base64()
    ssh = SSHKey("ssh-ed25519 " + pubKey, strict=True)


    # ssh = SSHKey("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAVElTgin0grq1T9ppVlIFNJ+8Nxa77dySgvc/6I2ovz m_811862@MACLTUS108302"
    #              "H1pON6P0= ojarva@ojar-laptop", strict=True)
    try:
        ssh.parse()
    except NotImplementedError as err:
        print("Invalid key type:", err)
        sys.exit(1)

    print(ssh.hash_sha256())  # SHA256:xk3IEJIdIoR9MmSRXTP98rjDdZocmXJje/28ohMQEwM




if __name__ == '__main__':
    main()
