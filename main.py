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


# def check_friends(friends, potential_friends):
#     result = list(map(lambda x: x in friends, potential_friends))
#     if len(result) != 0:
#         return True, result
#     else:
#         return False, None


vk_session = vk_api.VkApi(token=TOKEN)
# vk_session.auth()

vk = vk_session.get_api()

friends = vk.friends.get()

friends_dict = dict()

for id in friends['items']:
    friends_dict[id] = []
    get_friends(vk, id, friends_dict)

    # начало для настройки глубины и количества друзей
    # next_friends = vk.friends.get(user_id=id, count=10)['items']
    # same, people = check_friends(friends=friends_dict.keys(),
    #                       potential_friends=next_friends)
    # if same:
    #     next_friends.remove(people)

friends_json = json.dumps(friends_dict, indent=4, separators=(',', ': '))
with open('friends.json', 'w') as file:
    file.write(friends_json)

# print(friends_json)
# print(len(friends_dict.keys()))
