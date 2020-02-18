filename = "isifile.txt"
f = open(filename,'rb')
l = f.read(64)
while(l):
    print(repr(l))
    l = f.read(64)
f.close()