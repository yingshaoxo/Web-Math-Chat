class Auth():
    def __init__(self, my_session):
        self.s = my_session
    
    def random_token(self):
        import secrets
        return secrets.token_hex(32)

    def get_token(self, id):
        one = self.s.find_one(id)
        if one != None:
            return one.token
        else:
            return None

    def set_token(self, id, *args):
        user = self.s.find_one(id)
        if user == None:
            return None
        if len(args) == 1:
            user.token = args[0]
        else:
            user.token = self.random_token()
        self.s.commit()
        return user.token
        
        
