import config


def server_start(file, bot):
    users_dict = {}

    with open(file, 'r') as f:
        pairs = f.read().splitlines()
    for pair in pairs:
        buffer = pair.split()
        users_dict.update({str(buffer[0]): buffer[1].split("-")})
    return users_dict

def servef_stop(users_dict):
    with open(config.FILE_WITH_USERS, 'w') as f:
        for key in users_dict.keys():
            buf = users_dict.get(key)
            f.write(str(key) + " " + buf[0] + "-" + buf[1] + "\n")

    return users_dict

def serch_write(users_dict, user_id):
    flag = users_dict.get(str(user_id))
    if flag is None:
        with open(config.FILE_WITH_USERS, 'a') as f:
            f.write(str(user_id) + " English-en\n")
        users_dict.update({str(user_id): ["English", "en"]})
    return users_dict.get(str(user_id))
