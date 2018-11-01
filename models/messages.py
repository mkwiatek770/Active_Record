import re


class Messages:
    '''Table messages in active_db'''
    message_id = None
    sender_id = None
    receiver_id = None
    message = None

    @staticmethod
    def send_message(sender_id, receiver_id, messsage, cursor):
        '''This method is used to send message from one user(sender) 
        to another(receiver)'''
        sql = '''
        INSERT INTO messages (sender_id, receiver_id, message)
        values (%s, %s, %s)
        '''
        cursor.execute(sql, (sender_id, receiver_id, messsage))

    @staticmethod
    def load_all_messages(sender_id, sender_name, receiver_id, receiver_name, cursor):
        '''This method shows the history of conversation beetween two users,
        To execute this method we need parameters like:
        sender_id, receiver_id, sender_name, receiver_name and cursor to execute sql queries'''
        sql = '''
        SELECT message_id, message, date, username FROM messages JOIN users
        ON messages.sender_id = users.id 
        WHERE sender_id = %s AND receiver_id = %s
        OR sender_id = %s AND receiver_id = %s
        ORDER BY message_id ASC
        '''
        date_pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})"
        cursor.execute(sql, (sender_id, receiver_id, receiver_id, sender_id))
        for message in cursor:
            months = {'01': 'jan', '02': 'feb', '03': 'mar',
                      '04': 'apr', '05': 'may', '06': 'jun',
                      '07': 'jul', '08': '', '09': 'aug',
                      '10': 'oct', '11': 'nov', '12': 'dec'}
            text = message[1]
            match = re.search(date_pattern, str(message[2]))
            print("""
            {}: {}
            {} {}   {}:{}:{}
            """.format(message[3], text, match['day'], months[match['month']], match['hour'], match['minute'], match['second']))
