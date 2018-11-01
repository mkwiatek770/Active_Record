from clcrypto import password_hash, check_password, generate_salt
import re


class Users:
    '''Table users in active_db'''
    id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def hashed_password(self):
        '''This getter allows us to have access to hashed_password of current user-object'''
        return self.__hashed_password

    def set_password(self, password):
        '''This method allows us to set password of current object user, 
        lenght of the password must be greater or equal than 8 signs.'''
        while True:
            if len(password) >= 8:
                self.__hashed_password = password_hash(
                    password, generate_salt())
                break
            else:
                password = input(
                    "Password must have 8 signs or more enter another one: ")

    def set_username(self, username, cursor):
        '''This method allows user to set username,
        it's used while creating new user, before appending user to database users'''
        while True:
            sql = '''
            SELECT username FROM users
            WHERE username = %s
            '''
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result == None:
                self.username = username
                break
            else:
                username = input("Username is taken try another one: ")

    def set_email(self, email):
        '''This method is used to set email, email has to match requirement pattern like: sampleuser1@gmail.com'''
        email_pattern = r"\w+@[a-zA-Z]+\.com"
        while True:
            match = re.search(email_pattern, email)
            if match != None:
                self.email = email
                break
            else:
                email = input(
                    "Niepoprawny adres email przykładowy email to user2@.gmail.com\nWprowadź jeszcze raz:  ")

    def get_id(self, username, cursor):
        '''This methods returns user id, if username passed as a parameter exists in database, 
        then method will return ID of this username in database, if username doesn't exist, the method returns -1'''
        sql = '''
        SELECT id FROM users
        WHERE username = %s
       '''
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result != None:
            return result[0]
        else:
            return -1

    def validate_data(self, username, password, cursor):
        '''Validation data by passing username and password,
        sql query checks if there is a user with password passed as an argument, if yes method returns True,
        otherwise-False'''
        sql = """
        SELECT hashed_password from users
        WHERE username = %s
        """
        cursor.execute(sql, (username,))
        passw = cursor.fetchone()
        if passw != None:
            return check_password(password, passw[0])
        return False

    def save_to_db(self, username, password, email, cursor):
        """This method has two uses:
        if user doesn't exists, and passed data are valid - creates an user in database
        else - update users data like password and email, user can't change it's username it's the 
        uchangable part of the user"""
        if self.id == -1:
            self.set_username(username, cursor)
            self.set_email(email)
            self.set_password(password)
            sql = """INSERT INTO Users(username, email, hashed_password)
                VALUES(%s, %s, %s) RETURNING id;
                """
            values = (self.username, self.email, self.__hashed_password)
            cursor.execute(sql, values)
            self.id = cursor.fetchone()[0]
            print("Account has been succesfully created!")
        else:
            sql = """
            UPDATE Users SET
            email=%s,
            hashed_password=%s
            WHERE id=%s AND username = %s
            """
            values = (self.set_email(email), self.set_password(
                password), self.id, username)
            cursor.execute(sql, values)
            print("Account has been succesfully updated !")

    @staticmethod
    def load_user_by_id(cursor, user_id):
        """This method loads one single user by its id"""
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id, ))
        data = cursor.fetchone()
        if data:
            loaded_user = Users()
            loaded_user.id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        '''This method loads all users by printing list which contains information about objects(users)'''
        sql = """
        SELECT id, username, email, hashed_password
        FROM Users
        """
        list_of_users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            user = Users()
            user._id = row[0]
            user.username = row[1]
            user.email = row[2]
            user.__hashed_password = row[3]
            list_of_users.append(user)
        return list_of_users

    def delete(self, cursor):
        """Removing user from database. The object is now with id = -1 it means its not added"""
        sql = """DELETE FROM Users WHERE id=%s"""
        cursor.execute(sql, (self.id, ))
        self.id = -1
        return True
