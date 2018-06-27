from models.user import UserModel

# users = [
#     User(1, 'bob', 'asdf'),
#     # User(2,'jas','df')
# ]   

# username_mapping = {u.username: u for u in users}   
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    # print(username)
    # print(password) 
    # print(username_mapping)
    user = UserModel.find_by_username(username) # gives user object
    print(user)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

    # print(userid_mapping)
    # return userid_mapping.get((user_id[0],), None)