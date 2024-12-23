import threading

def foo():
    print("Hello threading!")


my_thread = threading.Thread(target=foo)

print(type(my_thread))

my_thread.start()
