def runtest():
    text = input(">> ")
    if ("'" in text):
        print("Not allowed!")
        exit(1)
    if('"' in text):
        print("Not allowed!")
        exit(1)
    try:
        print(exec(text, {'__builtins__': None, 'print':print}))
    except:
        print("ERROR!")

while True:
    runtest()
    
