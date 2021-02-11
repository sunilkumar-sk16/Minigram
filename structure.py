from numpy.lib.npyio import load
from functions import *
from os import system as sys
import pandas as pd
import numpy as np

Data = pd.DataFrame()

class MiniFeed():
    def __init__(self,Data,indx,feed):
        self.owner = Data.iloc[indx,1]
        self.Feed = feed
        self.index = indx
        self.likes = []
    def read_feed(self):
        layout()
        try:
            self.Feed = input("Enter Your Mini Feed : ")
            print("Your MiniFeed posted Successfully!")
            loading(3,"Returning",2)
        except Exception as E:
            print("Error Occured!",E)
    def modify_feed(self):
        layout()
        try:
            self.Feed = input("Enter Your Mini Feed : ")
            print("Your MiniFeed updated Successfully!")
            loading(3,"Returning",2)
        except Exception as E:
            print("Error Occured!",E)
    def liked(self,index):
        self.likes.append(index)
    def disliked(self,index):
        self.likes.remove(index)
    def display(self,Data,other_ind):
        try:
            while True:
                print('='*50)
                print(self.Feed)
                print("Posted by @{}".format(Data.iloc[self.index,0]))
                print("-"*50)
                print("{} likes".format(len(self.likes)))
                print("="*50)
                choice = int(input("Select: 1) Likes\n2) Comments\n0) Back -> \nYour Choice : "))
                if choice == 0:
                    break
        except Exception as E:
            print("Couldn't Load :( ",E)


class Account():
    Username,Name,Password,Phone,Followers,Following = None,None,None,None,None,None
    def __init__(self,u_name,name,p_word,p_number,flwers,flwing,feed,ind):
        self.index = ind
        self.Username = u_name
        self.Name = name
        self.Password = p_word
        self.Phone = p_word

        self.Feed = list(str(feed).split('$'))
        if self.Feed.count('-'):
            self.Feed.remove('-')
        
        if flwers == '-':
            self.Followers = []
        else:
            self.Followers = [int(i) for i in str(flwers).strip(',') if i!=',']

        if flwing == '-':
            self.Following = []
        else:
            self.Following = [int(i) for i in str(flwing).strip(',') if i!=',']

    def display(self):
        print(self.Name+' '*(92-len(self.Name)-len(self.Username))+'[ @'+self.Username+' ]')
        print('='*97)
        print('Followers :',len(self.Followers),' '*(97-len(str(self.Followers))+11))
        print('Following :',len(self.Following),' '*(97-len(str(self.Following))+11))
        print('Feeds : {}'.format(len(self.Feed)))
        print('='*97)
        print()

    def to_DataFrame(self,Data,index):
        Data.iloc[index,0] = self.Username
        Data.iloc[index,1] = self.Name
        Data.iloc[index,3] = self.Phone
        Data.iloc[index,2] = self.Password
        if len(self.Followers):
            Data.iloc[index,4] = ','.join(str(int(i)) for i in self.Followers)
        else:
            Data.iloc[index,4]= '-'
        if len(self.Following):
            Data.iloc[index,5] = ','.join(str(int(i)) for i in self.Following)
        else:
            Data.iloc[index,5] = '-'
        if len(self.Feed) == 0:
            Data.iloc[self.index]['Feed'] = '-'
        else:
            Data.iloc[self.index]['Feed'] = '$'.join(i for i in self.Feed)
        return Data

    def follow(self,Data,indx):
        new_acc = Account(Data.iloc[indx]['Username'],Data.iloc[indx]['Name'],Data.iloc[indx]['Password'],
        Data.iloc[indx]['Phone'],Data.iloc[indx]['Followers'],Data.iloc[indx]['Following'],Data.iloc[indx]['Feed'],indx)
        
        self.Following.append(indx)
        new_acc.Followers.append(self.index)

        Data = new_acc.to_DataFrame(Data,indx)
        Data = self.to_DataFrame(Data,self.index)
        return Data
    def unfollow(self,Data,indx):
        new_acc = Account(Data.iloc[indx]['Username'],Data.iloc[indx]['Name'],Data.iloc[indx]['Password'],
        Data.iloc[indx]['Phone'],Data.iloc[indx]['Followers'],Data.iloc[indx]['Following'],Data.iloc[indx]['Feed'],indx)
        
        self.Following.remove(indx)
        new_acc.Followers.remove(self.index)

        Data = new_acc.to_DataFrame(Data,indx)
        Data = self.to_DataFrame(Data,self.index)
        return Data
    def view_followers(self,Data):
        layout()
        try:
            if len(self.Followers) == 0:
                print("No Followers to show!!")
                loading(2,"Returning to Home Page",2)
            else:
                while True:
                    layout()
                    F = dict()
                    for i in range(len(self.Followers)):
                        F[i+1] = self.Followers[i]
                        print(i+1,') ',Data.iloc[self.Followers[i],1],' [ @',Data.iloc[self.Followers[i],0],' ]')
                    print("\n0) Back -->")
                    choice = int(input("\nEnter Your Choice : "))
                    if choice==0:
                        break
                    display(Data,self.index,F[choice])
        except Exception as E:
            print("UnExpected Error Occured!!",E)
            loading(2,"Returning to Home Page",2)
    def view_following(self,Data):
        layout()
        try:
            if len(self.Following) == 0:
                print("You are not Following anyone!!")
                loading(2,"Returning to Home Page",2)
            else:
                while True:
                    layout()
                    F = dict()
                    for i in range(len(self.Following)):
                        F[i+1] = self.Following[i]
                        print(i+1,') ',Data.iloc[self.Following[i],1],' [ @',Data.iloc[self.Following[i],0],' ]')
                    print("\n0) Back -->")
                    choice = int(input("\nEnter Your Choice : "))
                    if choice==0:
                        break
                    display(Data,self.index,F[choice])
        except Exception as E:
            print("UnExpected Error Occured!!",E)
            loading(2,"Returning to Home Page",2)
    def view_mutuals(self,Data,other_ind):
        try:
            if self.index==other_ind:
                layout()
                print("You can't have Mutuals with your Own Account!")
                loading(3,"Returning",1)
                return
            while True:
                layout()
                other_acc = Account(Data.iloc[other_ind]['Username'],Data.iloc[other_ind]['Name'],Data.iloc[other_ind]['Password'],
                    Data.iloc[other_ind]['Phone'],Data.iloc[other_ind]['Followers'],Data.iloc[other_ind]['Following'],Data.iloc[other_ind]['Feed'],other_ind)

                S = list(set(self.Followers).intersection(set(other_acc.Following)))

                if len(S)==0:
                    print("You have 0 mutuals to Show!!")
                    loading(2,"Returning",2)
                    return
                D = dict()
                for i in range(len(S)):
                    D[i+1] = S[i]
                    print("{}) {} [ @{} ]".format(i+1,Data.iloc[S[i],1],Data.iloc[S[i],0]))
                print("0) Back -->\n")
                choice = int(input("Enter Your Choice : "))
                if choice == 0:
                    break
                display(Data,self.index,D[choice])
        except Exception as E:
            print("UnExpected Error Occured!",E)
            loading(2,"Returning",2)
    def own_Feed(self,Data):
        try:
            while True:
                layout()
                if len(self.Feed)==0:
                    print("You have No Feed to show!")
                    loading(2,"Returning",3)
                    break
                print("Select Feed to View :\n")
                D = dict()
                for i in range(len(self.Feed)):
                    D[i+1] = self.Feed[i]
                    print("{} ) {}".format(i+1,self.Feed[i]))
                print("\n0) Back -->\n")
                choice = int(input("Your Choice : "))
                if choice == 0:
                    break
                Feed = MiniFeed(Data,self.index,D[choice])
                Feed.display(Data,self.index)
        except Exception as E:
            print("Error Occured!",E)
            loading(2,"Returning",2)

    def add_Feed(self,Data):
        layout()
        try:
            new_feed = input("Enter Your Mini Feed : ")
            self.Feed.append(new_feed)
            print("Your MiniFeed posted Successfully!")
            loading(3,"Returning",2)
        except Exception as E:
            print("Error Occured!",E)
    def delete_Feed(self,Data):
        try:
            while True:
                layout()
                if len(self.Feed)==0:
                    print("You have No Feed to show!")
                    loading(2,"Returning",3)
                    break
                print("Select Feed to Delete :\n")
                D = dict()
                for i in range(len(self.Feed)):
                    D[i+1] = self.Feed[i]
                    print("{} ) {}".format(i+1,self.Feed[i]))
                print("\n0) Back -->\n")
                choice = int(input("Your Choice : "))
                if choice == 0:
                    break
                else:
                    self.Feed.remove(D[choice])
                    print("Feed Succesfully Deleted!")
                    loading(2,"Refreshing",2)
        except Exception as E:
            print("Error Occured!",E)
            loading(2,"Returning",3)
    def settings(self,Data):
        try:
            while True:
                layout()
                print("1) Change Name\n2) Change Password\n3) Change PhoneNumber\n\n0) Back -->\n")
                choice = int(input("Your Choice : "))
                if choice == 0:
                    break
                elif choice == 1:
                    new_name = input("\nEnter New Name : ")
                    print("Are you sure you want to change your name {} to {} <Y/N> ? : ".format(self.Name,new_name))
                    choice1 = input()
                    if choice1[0] == 'y':
                        Data.iloc[self.index,1] = new_name
                        print("Name change successful!!")
                        loading(3,"Returning",1)
                elif choice == 2:
                    def is_password(passwrd):
                        if len(passwrd) < 8:
                            return False
                        up, low, num = False, False, False
                        for i in passwrd:
                            if i.islower():
                                low = True
                            elif i.isupper():
                                up = True
                            elif i.isdigit():
                                num = True
                        return up and low and num
                    while True:
                        new_pass = input('Enter Password <include atleast 8 characters and contain atleast one a-z/A-Z/0-9> : ')
                        if not is_password(new_pass):
                            print("Password is Weak!! <include atleast 8 characters and contain atleast one a-z/A-Z/0-9>")
                            continue
                        new_pass2 = input("\nEnter Password again : ")
                        if new_pass != new_pass2:
                            print("Password Missmatched tryagain!")
                            break
                        choice1 = input("Are you sure you want to change your password").lower()
                        if choice1[0] == 'y':
                            Data.iloc[self.index]['Password'] = new_pass
                            print("Password changed successful!!")
                            loading(2,"Returning",2)
                            break
                        else:
                            loading(0,"Returning",3)
                            break
                elif choice == 3:
                    new_num = input("Enter New Phone Number : ")
                    if new_num == str(self.Phone):
                        print("You are account is already linked with this Phone number!!")
                        loading(3,"Returning",2)
                    elif len(new_num) != 10 and not new_num.isdigit():
                        print("Invalid Phone Number!")
                        loading(2,"Returning",2)
                    else:
                        for i in range(len(Data)):
                            if i == Data.iloc[i]['Phone']:
                                print("Account with {} already exists!".format(new_num))
                                loading(2,"Returning",3)
                                break
                        else:
                            print("Phone number changed from {} to {}!!".format(self.Phone,new_num))
                            Data.iloc[self.index]['Phone'] = int(new_num)
                            loading(3,"Returning",2)
            return Data
        except Exception as E:
            print("UnExpected Error Occured",E)
            loading(2,"Returning to profile",2)
            return Data


def View_feed(Data,ind,other_ind):
    try:
        format()
        curr_acc = Account(Data.iloc[ind]['Username'],Data.iloc[ind]['Name'],Data.iloc[ind]['Password'],
        Data.iloc[ind]['Phone'],Data.iloc[ind]['Followers'],Data.iloc[ind]['Following'],Data.iloc[ind]['Feed'],ind)
        other_acc = Account(Data.iloc[other_ind]['Username'],Data.iloc[other_ind]['Name'],Data.iloc[other_ind]['Password'],            
        Data.iloc[other_ind]['Phone'],Data.iloc[other_ind]['Followers'],Data.iloc[other_ind]['Following'],Data.iloc[ind]['Feed'],other_ind)
        
        other_acc.own_Feed()
    except Exception as E:
        print("UnExpected Error Occured!",E)


def export(Data):
    try:
        Data.to_csv(r'C:\Users\User\Desktop\MiniGram\Accounts.csv',index=False,header=True) 
    except Exception as E:
        print('EXPORT FAILED!',E)

def import_data():
    try:
        Df = pd.read_csv(r'C:\Users\User\Desktop\MiniGram\Accounts.csv',
        header=0)
        Df['Followers'].fillna('-',inplace=True)
        Df['Following'].fillna('-',inplace=True)
        Df['Feed'].fillna('-',inplace=True)

        return Df
    except Exception as E:
        print('IMPORT FAILED!',E)
        return None

def create_account(Data):
    try:
        layout()
        u_name = input('Enter Username : ')
        name = input('Enter Name : ')
        p_word = input('Enter Password <include atleast 8 characters and contain atleast one a-z/A-Z/0-9> : ')
        p_number = int(input('Enter Phone Number : '))

        while True:
            block1, block2, block3 = True, True, True
            if u_name in Data['Username'].unique():
                u_name = input(
                    'Username already exists, Try another Username : ')
                block1 = False
            if p_number in Data['Phone'].unique():
                p_number = int(input(
                    'Account with your PhoneNumber already exists, Try another PhoneNumber : '))
                block2 = False
            if len(str(p_number)) != 10:
                p_number = int(input('Invalid PhoneNumber, Try again : '))
                block3 = False

            if block1 and block2 and block3:
                break

        def is_password(passwrd):
            if len(passwrd) < 8:
                return False
            up, low, num = False, False, False
            for i in passwrd:
                if i.islower():
                    low = True
                elif i.isupper():
                    up = True
                elif i.isdigit():
                    num = True
            return up and low and num

        while not is_password(p_word):
            p_word = input(
                'Enter Strong Password again (with atleast 8 characters & include atleast one a-z/A-Z/0-9): ')

        check = input('Are you sure you want to continue? (Y/N) : ').lower()
        if check[0] == 'n':
            print('Account Creation Denied!!!')
            return
        else:
            new_user = {'Username': u_name, 'Name': name, 'Password': p_word,'Phone':p_number,'Followers':'-','Following':'-','Feed':'-'} 
            Data = Data.append(new_user, ignore_index = True)

            print('Account Creation Succesfull!!!')
            return Data
    except Exception as E:
        print('PLEASE PROVIDE VALID INPUTS ONLY!!!',E)
        return Data

def display(Data,ind,other_ind):
    try:
        while True:
            curr_acc = Account(Data.iloc[ind]['Username'],Data.iloc[ind]['Name'],Data.iloc[ind]['Password'],
                Data.iloc[ind]['Phone'],Data.iloc[ind]['Followers'],Data.iloc[ind]['Following'],Data.iloc[ind]['Feed'],ind)
            other_acc = Account(Data.iloc[other_ind]['Username'],Data.iloc[other_ind]['Name'],Data.iloc[other_ind]['Password'],
                Data.iloc[other_ind]['Phone'],Data.iloc[other_ind]['Followers'],Data.iloc[other_ind]['Following'],Data.iloc[other_ind]['Feed'],other_ind)
            layout()
            print(other_acc.Name+' '*(92-len(other_acc.Name)-len(other_acc.Username))+'[ @'+other_acc.Username+' ]')
            print('='*97)
            print('Followers :',len(other_acc.Followers),' '*(97-len(str(other_acc.Followers))+11))
            print('Following :',len(other_acc.Following),' '*(97-len(str(other_acc.Following))+11))
            print('='*97+'\n')
            if ind == other_ind:
                print('Your are viewing your Profile')
            elif other_acc.Following.count(ind) and curr_acc.Following.count(other_ind):
                print("You are {} are following each other".format(other_acc.Name))
            elif curr_acc.Following.count(other_ind):
                print("You are following {}".format(other_acc.Name))
            elif other_acc.Following.count(ind):
                print("{} is following you".format(other_acc.Name))
            else:
                print("You and {} are not following each other".format(other_acc.Name))
            print("\nSelect :")
            if ind == other_ind:
                print("1) Return to Your Profile")
            elif curr_acc.Following.count(other_ind):
                print("1) UnFollow")
            else:
                print("1) Follow")
            mutuals = len(set(curr_acc.Followers).intersection(set(other_acc.Following)))
            print("You and {} have {} mutual(s)".format(other_acc.Name,mutuals))
            print("2) View Mutuals\n3) View Feed\n4) View Followers\n5) View Following\n\n0) Back -->")
            choice = int(input("Your Choice : "))
            if choice == 0:
                return
            elif choice == 1:
                if ind == other_ind:
                    return
                elif curr_acc.Following.count(other_ind):
                    Data = curr_acc.unfollow(Data,other_ind)
                else:
                    Data = curr_acc.follow(Data,other_ind)
            elif choice == 2:
                curr_acc.view_mutuals(Data,other_ind)
            elif choice == 3:
                View_feed(Data,ind,other_ind)
            elif choice == 4:
                other_acc.view_followers(Data)
            elif choice == 5:
                other_acc.view_following(Data)
    except Exception as E:
        print("An Unexpected Error Occured!",E)
        loading(2,"Returning to Your Profile",3)

def Login(Data):
    layout()
    print("ENTER YOUR CREDENTIALS :")
    try:
        uname = input("Enter UserName : ")
        pword = input("Enter Password : ")
        for i in range(len(Data)):
            if Data.iloc[i]['Username'] == uname and Data.iloc[i]['Password'] == pword:
                layout()
                loading(1,"LOGGING IN TO YOUR ACCOUNT",2)
                Data = Home(Data,i)
                break
        else:
            print("Couldn't Find User, Enter correct Username or Password!!")
            loading(3,"Page redirecting",3)
    except Exception as E:
        print("Login Failed, Please try again!",E)
        loading(3,"Page redirecting",3)

def search(Data,curr_ind):
    try:
        while True:
            layout()
            print("Select :\n")
            print("1) Search All\n2) Search Users\n3) Search Feeds\n\n0) Back -->\n")
            choice = int(input("Your Choice : "))
            if choice == 0:
                break
            elif choice == 1:
                layout()
                key = input("Enter your search : ")
                Acc = dict()
                acc_count = 0
                print("\nRelated Accounts : \n")
                for i in range(len(Data)):
                    if str(Data.iloc[i,0]).lower().count(key.lower()) or str(Data.iloc[i,1]).lower().count(key.lower()):
                        print("{} ) {} [ @{} ]".format(acc_count+1,Data.iloc[i,1],Data.iloc[i,0]))
                        acc_count += 1
                        Acc[acc_count] = i
                if acc_count == 0:
                    print("No related Accounts found! :(")
                Fed = dict()
                feed_count = len(Acc.keys())
                print("\nRelated Feeds : \n")
                for ind in range(len(Data)):
                    curr_acc = Account(Data.iloc[ind]['Username'],Data.iloc[ind]['Name'],Data.iloc[ind]['Password'],
                        Data.iloc[ind]['Phone'],Data.iloc[ind]['Followers'],Data.iloc[ind]['Following'],Data.iloc[ind]['Feed'],ind)
                    for i in curr_acc.Feed:
                        if i.lower().count(key.lower()):
                            print("{} ) {} [ @{} ]".format(feed_count+1,i[:6]+'....',curr_acc.Username))
                            feed_count += 1
                            Fed[feed_count] = i
                if feed_count == acc_count:
                    print("No related Feeds found! :(")
                print("\n0) Back -->\n")
                choice = int(input("Your Choice : "))
                if choice == 0:
                    break
                elif choice <= acc_count:
                    display(Data,curr_ind,Acc[choice])
                elif choice <= feed_count:
                    View_feed(Data,curr_ind,Fed[choice])
            elif choice == 2:
                key = input("Enter Usernames to search : ")
                Acc = dict()
                acc_count = 0
                print("\nRelated Accounts : \n")
                for i in range(len(Data)):
                    if str(Data.iloc[i,0]).lower().count(key.lower()) or str(Data.iloc[i,1]).lower().count(key.lower()):
                        print("{} ) {} [ @{} ]".format(acc_count+1,Data.iloc[i,1],Data.iloc[i,0]))
                        acc_count += 1
                        Acc[acc_count] = i
                if acc_count == 0:
                    print("No related Accounts found! :(")
                print("\n0) Back -->\n")
                choice = int(input("Your Choice : "))
                if choice == 0:
                    break
                elif choice <= acc_count:
                    display(Data,curr_ind,Acc[choice])
            elif choice == 3:
                key = input("Enter Feeds to search: ")
                Fed = dict()
                feed_count = 0
                print("\nRelated Feeds : \n")
                for ind in range(len(Data)):
                    curr_acc = Account(Data.iloc[ind]['Username'],Data.iloc[ind]['Name'],Data.iloc[ind]['Password'],
                        Data.iloc[ind]['Phone'],Data.iloc[ind]['Followers'],Data.iloc[ind]['Following'],Data.iloc[ind]['Feed'],ind)
                    for i in curr_acc.Feed:
                        if i.lower().count(key.lower()):
                            print("{} ) {} [ @{} ]".format(feed_count+1,i[:6]+'....',curr_acc.Username))
                            feed_count += 1
                            Fed[feed_count] = i
                if feed_count == 0:
                    print("No related Feeds found! :(")
                print("\n0) Back -->\n")
                choice = int(input("Your Choice : "))
                if choice == 0:
                    break
                elif choice <= feed_count:
                    View_feed(Data,curr_ind,Fed[choice])
    except Exception as E:
        print("An Error has Occured!",E)

def Home(Data,ind):
    try:
        while True:
            curr_acc = Account(Data.iloc[ind]['Username'],Data.iloc[ind]['Name'],Data.iloc[ind]['Password'],
            Data.iloc[ind]['Phone'],Data.iloc[ind]['Followers'],Data.iloc[ind]['Following'],Data.iloc[ind]['Feed'],ind)
            layout()
            curr_acc.display()
            print("Select :\n\n1)Search\n2)Feed\n3)Followers\n4)Following\n5)Settings\n0)Log Out\n\n")
            choice = int(input("Your Choice : "))
            if choice == 0:
                loading(2,"Loging Out",3)
                break
            elif choice == 1:
                search(Data,ind)
            elif choice == 2:
                while True:
                    layout()
                    print("Select:\n1) Add Feed\n2) Delete Feed\n3) View Feed\n\n0) Exit -->")
                    choice2 = int(input("Your choice : "))
                    if choice2 == 0:
                        break
                    elif choice2 == 1:
                        curr_acc.add_Feed(Data)
                    elif choice2 == 2:
                        curr_acc.delete_Feed(Data)
                    elif choice2 == 3:
                        curr_acc.own_Feed(Data)
            elif choice == 3:
                curr_acc.view_followers(Data)
            elif choice == 4:
                curr_acc.view_following(Data)
            elif choice == 5:
                Data = curr_acc.settings(Data)
            export(Data)
            Data = import_data()
        return curr_acc.to_DataFrame(Data,ind)       
    except Exception as E:
        print("An Unexpected Error Occured!!",E)
        loading(3,"Returning to Home page",3)
        return Data
        
if __name__ == '__main__':

    layout()
    Data = import_data()
    
    export(Data)