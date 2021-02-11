from structure import *
from functions import *


Data = import_data()

try:
    if __name__ == "__main__":
        Data = import_data()
        while True:
            layout()
            print("Select :\n\n1)LOGIN\n\n2)SIGN UP\n\n0)EXIT\n\n")
            choice = int(input('Your Choice : '))
            if choice == 0:
                break
            elif choice == 1:
                Login(Data)
            elif choice == 2:
                Data = create_account(Data)
                layout()
                print("Account Creation Successful! Please Login again!")
                loading(3,"Returning to Home page",3)
            export(Data)
        export(Data)
except Exception as E:
    print("Unexpected Error Occured!",E)   
