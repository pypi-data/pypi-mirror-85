import hashlib

class Hash:

    def __init__(self):
        pass

    def md5(self, obj):
        hash_object = hashlib.md5(obj.encode())
        return(hash_object.hexdigest())

    def sha1(self, obj):
        hash_object = hashlib.sha1(obj.encode())
        return(hash_object.hexdigest())
    
    def sha256(self, obj):
        hash_object = hashlib.sha256(obj.encode())
        return(hash_object.hexdigest())