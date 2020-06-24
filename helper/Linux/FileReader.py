def reader():
    try:
        f = open('/tmp/out.ready',mode='r')
        sentence = f.read()
        return sentence
    except:
        print("REading failed")
    finally:
        f.close()
# print(reader())