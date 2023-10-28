import vk_api
import json


TOKEN = ''


def get_friends(vk, id, fr_dict: dict):
    curr_friends = fr_dict.keys()
    try:
        friends = vk.friends.get(user_id=id)['items']
        for friend in curr_friends:
            if friend in friends:
                fr_dict[id].append(friend)
                fr_dict[friend].append(id)
    except vk_api.exceptions.ApiError:
        fr_dict.pop(id)


vk_session = vk_api.VkApi(token=TOKEN)

vk = vk_session.get_api()
id_root = vk.account.getProfileInfo()['id']

friends = vk.friends.get()

friends_dict = dict()
friends_dict[id_root] = []

for id in friends['items']:
    try:
        _ = vk.friends.get(user_id=id, count=1)
    except vk_api.exceptions.ApiError:
        continue

    friends_dict[id_root].append(id)

    friends_dict[id] = []
    get_friends(vk, id, friends_dict)

    next_friends = vk.friends.get(user_id=id)['items']

    for fr_id in next_friends:
        friends_dict[id].append(fr_id)

        friends_dict[fr_id] = []
        get_friends(vk, fr_id, friends_dict)

friends_json = json.dumps(friends_dict, indent=4, separators=(',', ': '))
with open('friends_big_2.json', 'w') as file:
    file.write(friends_json)

print(len(friends_dict.keys()))
