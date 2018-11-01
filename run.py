from models.user import Users
from models.messages import Messages
from connect import create_connection, close_connection
from clcrypto import generate_salt
import argparse


parser = argparse.ArgumentParser(
    description='Program allows to add/delete user from database')
parser.add_argument(
    '-u', '--username', help="Login/user name")
parser.add_argument('-p', '--password', help="8 signs or more")
parser.add_argument('-E', '--email', help="Set Email")
parser.add_argument('-l', '--list', action="store_true",
                    help="List of all users")
parser.add_argument('-d', '--delete', action="store_true",
                    help="Delete user (if exists)")
parser.add_argument('-e', '--edit', action="store_true",
                    help="Edit user, or add if user doesn't exist")
parser.add_argument('-f', '--From', help="From, sender")
parser.add_argument('-t', '--to', help="Receiver username")
parser.add_argument('-s', '--send', help="Message to send")
parser.add_argument('-H', '--history', action="store_true",
                    help="History of conversation beetween 2 users")
args = parser.parse_args()

# Scenarios:
# 1. -u -p -E -e <-- creating new user/ updating existing user
# 2. -u -p -d    <-- removing user (if exists in TABLE)
# 3. -l          <-- list of all users
# 4. -u -p -s -t <-- send message from logged user to another user (both have to exist)
# 5. -F -t -H    <-- show full history of conversation beetween two users


cnx, cursor = create_connection()
# creating object to work on
user = Users()

# creating new user to database users
if args.username and args.password and args.email and args.edit:
    user.id = user.get_id(args.username, cursor)
    user.save_to_db(args.username, args.password, args.email, cursor)


# removing user(if exists)
if args.username and args.password and args.delete:
    user.id = user.get_id(args.username, cursor)
    user.validate_data(args.username, args.password, cursor)
    if user.id != -1 or user.validate_data(args.username, args.password, cursor):
        user.delete(cursor)
        print("Account has been deleted !")
    else:
        print("Account doesn't exist!")

# list of all users
if args.list:
    for user in Users.load_all_users(cursor):
        print("""
        User name: {}
        E-mail: {}
        """.format(user.username, user.email))

# send message from user1 to user2
if args.username and args.password and args.send and args.to:
    if user.validate_data(args.username, args.password, cursor):
        sender_id = user.get_id(args.username, cursor)
        receiver_id = user.get_id(args.to, cursor)
        if receiver_id == -1:
            print("Receiver doesn't exist !")
        else:
            Messages.send_message(sender_id, receiver_id, args.send, cursor)
            print("Message has been sent!")
    else:
        print("Invalid login data!")

# history of messages
if args.From and args.to and args.history:
    sender_id = user.get_id(args.From, cursor)
    receiver_id = user.get_id(args.to, cursor)
    if sender_id == -1 or receiver_id == -1:
        print("Invalid data!")
    else:
        Messages.load_all_messages(
            sender_id, args.From, receiver_id, args.to, cursor)


close_connection(cnx, cursor)
