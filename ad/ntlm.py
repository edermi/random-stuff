import hashlib,binascii,sys
hash = hashlib.new('md4', sys.argv[1].encode('utf-16le')).digest()
print('{0}:{1}'.format(sys.argv[1], binascii.hexlify(hash).decode()))
