import sys

import pymysql
from pymysql.constants import ER


class DatabaseMenu:
    def __init__(self):
        import sepe_interface.Secret as Auth  # login details used for database connection - stored in sepearte python file because they should be hidden
        try:
            self.conn = pymysql.connect('localhost', Auth.user, Auth.pswrd, Auth.db, charset='utf18')  # mySQL database connection object
            self.c = self.conn.cursor()  # cursor object used for mySQL queries
            login = input('Login: ')
            password = input('Password: ')
            self.login = login
            self.password = password
        except pymysql.InternalError as err:
            if err == ER.ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                sys.exit()
            elif err == ER.BAD_DB_ERROR:
                print("Database does not exist")
                sys.exit()
            else:
                print(err)
                sys.exit()

    def login(self):
        print('Please type your login and password')
        self.c.execute('SELECT Uprawnienia FROM logowanie where User = {login} and Pass = {pswrd}'.format(login=self.login, pswrd=self.password))  # Getting permission level for the user from queries execution
        permission = self.c.fetchall()  # Setting the permission level value to a new variable. The variable type is table/matrix
        if permission[0][0] == 0:
            print('Welcome root {login}'.format(login=self.login))  # the highest level of privileges
            pass
        elif permission[0][0] == 1:
            print('Welcome admin {login}'.format(login=self.login))  # medium level of privileges
            pass
        elif permission[0][0] == 2:
            print('Welcome user {login}'.format(login=self.login))  # the lowest level of privileges
            pass
        else:
            print('login error. There is no username {login} or username and password does not match'.format(login=self.login))

    def selectRoot(self):
        self.c.execute('select * from users')
        wynik = self.c.fetchall()
        print('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}'.format('LP', 'LOGIN', 'HASLO', 'E-MAIL', 'TYP'))
        for i in wynik:
            print('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}'.format(i[0], i[1], i[2], i[3], i[4]))

    def selectAdmin(self):
        self.c.execute('select * from users where login = %s and passwrd = %s', (self.login, self.passwrd))
        wynik = self.c.fetchall()
        print('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}'.format('LP', 'LOGIN', 'HASLO', 'E-MAIL', 'TYP'))
        for i in wynik:
            print('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}'.format(i[0], i[1], i[2], i[3], i[4]))

    def selectUser(self):
        self.c.execute('select * from users where login = %s and passwrd = %s', (self.login, self.passwrd))
        wynik = self.c.fetchall()
        print('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}'.format('LP', 'LOGIN', 'HASLO', 'E-MAIL', 'TYP'))
        for i in wynik:
            print('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}'.format(i[0], i[1], i[2], i[3], i[4]))

    def insertRoot(self):
        try:
            login = input('Podaj login:')
            passwrd = input('Podaj hasło:')
            mail = input('Podaj e-mail:')
            permission = input('Podaj uprawnienia:')
            self.c.execute(
                'Insert into users (login, passwrd, mail, permission) values ("{:s}", "{:s}", "{:s}", "{:s}")'.format(login, passwrd, mail, permission))
            potwierdzenie = input('Potwierdź wprowadzenie nowego uzytkownika T/N').upper()
            if potwierdzenie == 'T':
                self.conn.commit()
                print('dodano poprawnie uzytkownika')
            else:
                self.conn.rollback()
                print('nie dodano rekordu')
            self.select()
        except:
            print('taki uzytkownik juz istnieje')

    def update(self):
        try:
            self.select()
            wybor = int(input('Wybierz LP uzytkownika do podmiany'))
            while True:
                self.select()
                zmiana = input('atrybut do zmiany L - login, H - hasło, E - e-mail, U - uprawnienia, * - wyjście').upper()
                if zmiana == 'L':
                    nowyLogin = input('podaj nowy login:')
                    self.c.execute('update users set login = "{:s}"  where id = {}'.format(nowyLogin, wybor))
                    print('poprawnie zmieniono login')
                    potwierdzenie = input('Potwierdź wprowadzenie nowego uzytkownika T/N').upper()
                    if potwierdzenie == 'T':
                        self.conn.commit()
                        print('zmieniono poprawnie uzytkownika')
                    else:
                        self.conn.rollback()
                        print('nie zmieniono rekordu')
                elif zmiana == 'H':
                    nowyHaslo = input('podaj nowe hasło:')
                    self.c.execute('update users set passwrd = "{:s}"  where id = {}'.format(nowyHaslo, wybor))
                    print('poprawnie zmieniono hasło')
                    potwierdzenie = input('Potwierdź wprowadzenie nowego uzytkownika T/N').upper()
                    if potwierdzenie == 'T':
                        self.conn.commit()
                        print('zmieniono poprawnie uzytkownika')
                    else:
                        self.conn.rollback()
                        print('nie zmieniono rekordu')
                elif zmiana == 'E':
                    nowyMail = input('podaj nowy e-mail:')
                    self.c.execute('update users set mail = "{:s}"  where id = {}'.format(nowyMail, wybor))
                    print('poprawnie zmieniono e-mail')
                    potwierdzenie = input('Potwierdź wprowadzenie nowego uzytkownika T/N').upper()
                    if potwierdzenie == 'T':
                        self.conn.commit()
                        print('zmieniono poprawnie uzytkownika')
                    else:
                        self.conn.rollback()
                        print('nie zmieniono rekordu')
                elif zmiana == 'U':
                    nowyUpr = input('podaj nowe uprawnienia:')
                    self.c.execute('update users set permission = "{:s}"  where id = {}'.format(nowyUpr, wybor))
                    print('poprawnie zmieniono uprawnienia')
                    potwierdzenie = input('Potwierdź wprowadzenie nowego uzytkownika T/N').upper()
                    if potwierdzenie == 'T':
                        self.conn.commit()
                        print('zmieniono poprawnie uzytkownika')
                    else:
                        self.conn.rollback()
                        print('nie zmieniono rekordu')
                else:
                    print('bład')
                    break
            self.select()
        except:
            print('taki uzytkownik nie isnitenieje')

    def delete(self):
        try:
            self.select()
            while True:
                wybor = int(input('Wybierz LP uzytkownika do usunięcia'))
                if wybor == 1:
                    print('nie można usunąć roota')
                    break
                else:
                    self.c.execute('delete from users where id = {}'.format(wybor))
                    potwierdzenie = input('Potwierdź usunięcie T/N').upper()
                    if potwierdzenie == 'T':
                        self.conn.commit()
                        print('usunięto użytkownika')
                        break
                    else:
                        self.conn.rollback()
                        print('nie wykonano akcji')
                        break
            self.select()
        except:
            print('taki uzytkownik nie isnitenieje')

    # def report(self):
    #     from os import getcwd, chdir, listdir
    #     from time import time
    #     chdir('..')
    #     chdir(getcwd() + '\\' + 'reports')
    #     raport = input('Podaj nazwę pliku:')
    #     if ((raport + '.csv') in listdir(getcwd())):
    #         raport = raport + str(time())
    #     pathFile = str(getcwd()) + '\\' + raport
    #     r = open(pathFile + '.csv', 'w')
    #     self.c.execute('select * from users')
    #     wynik = self.c.fetchall()
    #     r.write('Author:{}'.format(self.login + '\n'))
    #     r.write('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}\n'.format('LP', 'LOGIN', 'HASLO', 'E-MAIL', 'TYP'))
    #     for i in wynik:
    #         r.write('{:>4}|{:>20s}|{:>20s}|{:>20s}|{:>4s}\n'.format(i[0], i[1], i[2], i[3], i[4]))
    #     chdir('..')
    #     r.close()