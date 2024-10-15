import binascii,sys
from Crypto.Hash import MD4

hash_obj = MD4.new()
hash_obj.update(sys.argv[1].encode('utf-16le'))
hash_digest = binascii.hexlify(hash_obj.digest()).decode()
print(f'{sys.argv[1]}:{hash_digest}')

