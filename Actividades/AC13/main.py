from json import JSONEncoder
import pickle
import json
import os
import datetime


class User:
    def __init__(self, name, contacts, phone_number):
        self.name = name
        self.contacts = contacts
        self.phone_number = phone_number


class Message:
    def __init__(self, send_to, content, send_by, last_view_date, date):
        self.send_to = send_to
        self.content = content
        self.send_by = send_by
        self.last_view_date = last_view_date
        self.date = date

    def __getstate__(self):
        new = self.__dict__.copy()
        new_content = ''
        content = new['content']
        for word in content:
            x = ord(word)
            n = new['send_by']
            y = (x + n) % 26
            new_content += chr(y)
        new.update({'content': new_content})
        print(new)
        return new

    def __setstate__(self, state):
        state.update({'last_view_date': datetime.datetime.today().strftime(
                    '%Y-%m-%d %H:%M')})
        self.__dict__ = state


class UserEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return {
                'name': o.name,
                'contacts': o.contacts,
                'phone_number': o.phone_number
            }

        return super(UserEncoder, self).default(o)


class MessageEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(self, Message):
            return {
                'send_to': o.send_to,
                'content': o.content,
                'send_by': o.send_by,
                'last_view_date': o.last_view_date,
                'date': o.date
            }

        return super(MessageEncoder, self).default(o)


def decode_user(dict_obj):
    user = User(**dict_obj)
    return user


def decode_message(dict_obj):
    message = Message(**dict_obj)
    return message


class SecuritySystem:
    def __init__(self):
        self.users = []
        self.messages = []

    def generate_users(self):
        self.users = []
        for filename in os.listdir('./db/usr'):
            with open('./db/usr/' + filename, 'r') as f:
                user = json.load(f, object_hook=lambda json_obj: decode_user(
                    json_obj))
            self.users.append(user)

    def generate_messages(self):
        self.messages = []
        for filename in os.listdir('./db/msg'):
            with open('./db/msg/' + filename, 'r+') as f:
                message = json.load(f, object_hook=lambda json_obj: decode_message(
                    json_obj))
                message.last_view_date = datetime.datetime.today().strftime(
                    '%Y-%m-%d %H:%M')
            self.messages.append(message)

    def add_contacts(self):
        for user in self.users:
            for message in self.messages:
                if message.send_by == user.phone_number and message.send_to \
                        not in user.contacts:
                    user.contacts.append(message.send_to)

    def save_users(self):
        for user in self.users:
            path = './secure_db/usr/' + user.name + '.json'
            with open(path, 'w') as f:
                json.dump(user, f, cls=UserEncoder)

    def save_messages(self):
        for num, message in enumerate(self.messages):
            path = './secure_db/msg/' + str(num)

            with open(path, 'wb') as f:
                pickle.dump(message, f)


if __name__ == '__main__':
    if not os.path.exists('./secure_db/usr'):
        os.makedirs('./secure_db/usr')
    if not os.path.exists('./secure_db/msg'):
        os.makedirs('./secure_db/msg')
    security_system = SecuritySystem()
    security_system.generate_users()
    security_system.generate_messages()
    security_system.add_contacts()
    security_system.save_users()
    security_system.save_messages()
