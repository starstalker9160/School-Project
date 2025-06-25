import os
from winHandler import Window

if __name__ == "__main__":
    os.system("cls")
    try:
        Window().mainloop()
    except KeyboardInterrupt: quit(0)
    except Exception as e:
        quit(1)