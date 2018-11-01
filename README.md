# Console_Messenger

This project is an easy messenger wrote in python with psql databases. It's based on Active Record attitude so each table in database is an unique class.

## Instalation

* clone repository form github using:
git clone (adress)
* go to database directory and write: 
psql -U postgres -f active.sql -h localhost active_db
* create virtualenvironment in your repository directory: 
virtualenv -p python3 venv
* Install packages used in this project:
pip install -r requirements.txt
* open console and go to project directory 

## Usage 

This project is an messenger that allows to send messages from user1 to user2. We can create many account, edit accounts and removing them. We can show history of messages beetween two users just by writing single command. Every user is stored in users table in our database and every message is stored in messages table in database. 

Flags:
* -p --password
* -u --username 
* -E --email 
* -l --list 
* -d --delete 
* -e --edit
* -f --From 
* -t --to 
* -s --send 
* -H --history 

## Scenarios
1. python3 run.py --username <username> --password <password> --email <email_adress> --edit  
- creating new user/ updating existing user
2. python3 run.py --username <username> --password <password> --delete 
-removing user (if exists in table)
3. python3 run.py --list 
- list of all users 
4. python3 run.py --username <username> --password <password> --send "Message" --to <username2>
- after correct login data user1 sends message to user2 (both users have to exist!)
5. python3 run.py --From <user1> --to <user2> --history 
- shows full history of converation beetween two users. 

## Contribiuting 

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author 
* Michał Kwiatek 
contact: michalkwiatek8@o2.pl

## License 
[MIT](https://choosealicense.com/licenses/mit/)
