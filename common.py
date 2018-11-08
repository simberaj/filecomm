
'''Common filecomm functionality.'''

PORT = 1711
CHUNK_SIZE = 8192
TIMEOUT = 60

def transfer(instream, outstream, chunk_size=CHUNK_SIZE):
    print('commencing reading')
    chunk = instream.read(chunk_size)
    totsize = len(chunk)
    while chunk:
        print(len(chunk))
        outstream.write(chunk)
        chunk = instream.read(chunk_size)
        totsize += len(chunk)
    return totsize