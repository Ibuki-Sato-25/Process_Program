import re

class SingletonMeta(type):
    _instance = {}
    '''Singleton implementation metaclass'''

    def __call__(cls, *args, **kwds):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwds)
        return cls._instance[cls]

class UserManager(metaclass=SingletonMeta):
    '''User management class'''

    def __init__(self):
        self.login_id = []

    def add_user(self, username, password):
        self.login_id.append([username, password])
    '''Add a user'''

    def exists_user(self, username, password):
        return [username, password] in self.login_id
    '''Check if user exists'''

    def check_user(self, username):
        return any(user[0] == username for user in self.login_id)
    '''Check if user ID is already taken'''


class Authenticator:
    '''User authentication class'''
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.current_user = None

    def check(self):
        '''User authentication and registration'''
        print('''
    ------------------------------------------------------------
    If you are already registered, please enter "username password".
    If you are not registered, please enter "register": 
    ------------------------------------------------------------
        ''') 
        while True:
            User_Varification = input('\nEnter: ')
            if User_Varification == "register":
                if self.register():
                    break
            else:
                if self.login_check(User_Varification):
                    break

    def register(self):
        '''User registration method'''
        print("""
    ------------------------------------------------------------
    Please enter "username password" to register.
    To return to the login screen, enter "login".

    Please follow these rules for setting a password:
    - Japanese characters cannot be used.
    - Include both English letters and numbers.
    - Passwords are generally 6 characters long: 
    ------------------------------------------------------------
            """)
        while True:
            User_New = input('\nEnter: ')
            if User_New == "login":
                print('''
    ------------------------------------------------------------
    If you are already registered, please enter "username password".
    If you are not registered, please enter "register": 
    ------------------------------------------------------------
        ''') 
                break
            try:
                username, password = User_New.split()
                if self.user_manager.check_user(username):
                    print('\nNote: Username is already in use')
                elif len(password) < 6:
                    print('\nNote: Password must be at least 6 characters long. Please check.')
                elif re.search(r'[^\x00-\x7F]', password):
                    print('\nNote: Password cannot include Japanese characters')
                elif not (re.search(r'[a-zA-Z]', password) and re.search(r'[0-9]', password)):
                    print('\nNote: Password must include both letters and numbers')
                else:
                    self.user_manager.add_user(username, password)
                    print('\nRegistration successful')
                    self.current_user = username
                    print(f'Thank you for registering {self.current_user}')
                    return True
            except ValueError:
                print('\nNote: Incorrect input format')

    def login_check(self, User_Varification):
        '''Login authentication method'''
        try:
            username, password = User_Varification.split()
            if self.user_manager.exists_user(username, password):
                print("\nLogin successful")
                self.current_user = username
                print(f'Welcome back {self.current_user}')
                return True
            else:
                print("\nLogin failed: ")
        except ValueError:
            print('\nNote: Incorrect input format')

class EventManager:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.save_events = {}

    def initialize_user(self):
        if self.authenticator.current_user not in self.save_events:
            self.save_events[self.authenticator.current_user] = {}

    def define_event(self, user_action):
        try:
            mode, event, process = user_action.split(maxsplit=2)
            user_events = self.save_events[self.authenticator.current_user]
            if event in user_events:
                print('\nEvent already exists, overwriting.')
            user_events[event] = process
            print(f'\nEvent "{event}" has been saved')
        except ValueError:
            print('\nNote: Incorrect input format')

    def check_event(self, user_action):
        try:
            mode, event = user_action.split()
            if event in self.save_events[self.authenticator.current_user]:
                process = self.save_events[self.authenticator.current_user][event]
                print(f'\nProcess for {event}:')
                process_list = process.split()
                for number, i_process in enumerate(process_list, start=1):
                    print(f'{number}: {i_process}')
            else:
                print('\nSpecified event does not exist')
        except ValueError:
            print('\nNote: Incorrect input format')

    def list_events(self):
        try:
            user_events = self.save_events[self.authenticator.current_user]
            if not user_events:
                print('\nNo events found')
            else:
                for number, (event, process) in enumerate(user_events.items(), start=1):
                    print(f'{number}: {event}')
        except ValueError:
            print('\nNote: Incorrect input format')

    def delete_event(self, user_action):
        try:
            mode, event = user_action.split()
            if event in self.save_events[self.authenticator.current_user]:
                del self.save_events[self.authenticator.current_user][event]
                print(f'{event} has been deleted.')
            else:
                print('Event not found')
        except ValueError:
            print('\nNote: Incorrect input format')

    def display_help(self):
        print('''
    --------------------------------------------------------------------------------
    This demo is designed to optimize human actions.
    Define the appropriate action process according to the situation = event.
    Once defined, you can check the process to be followed by entering the event name when you encounter the event.

    To define an event and its process: 1 EventName Process Process...
    To check the process for a defined event: 2 EventName
    To check all defined event names: 3
    To delete a registered event: 4 EventName
    To display help: 5
    To log in again: 6
    To exit the program: 7
    --------------------------------------------------------------------------------
        ''')

    def handle_user_action(self):
        while True:
            user_action = input("\nEnter: ")
            try:
                if '1' in user_action:
                    self.define_event(user_action)
                elif '2' in user_action:
                    self.check_event(user_action)
                elif '3' in user_action:
                    self.list_events()
                elif '4' in user_action:
                    self.delete_event(user_action)
                elif '5' in user_action:
                    self.display_help()
                elif '6' in user_action:
                    self.authenticator.check()
                    self.initialize_user()
                    self.display_help()
                elif '7' in user_action:
                    print('Program has ended.')
                    break
                else:
                    print('\nNote: Please select a mode.')
            except ValueError:
                print('\nInput format may not be correct.')
                continue

user_manager = UserManager()
authenticator = Authenticator(user_manager)
event_manager = EventManager(authenticator)

if __name__ == "__main__":
    authenticator.check()
    event_manager.initialize_user()
    event_manager.display_help()
    event_manager.handle_user_action()