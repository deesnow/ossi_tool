
COMMAND_TIMEOUTS = {
        'default': 1,
        'status': {
            'station': 6
        },
        'list': {
            'station': 2,
            'trunk' : 2,
            'measurement' : 3
        },
        'display': {
            'media-server' : 1,
            'media-gateway' : 1,
            'capacity': 2,
            'node-name': 1
        },
        'clear': {
            'amw': 0.2
        },
        'remove': {
            'station': 0.2
        }
    }

def search_timeout (command):

    words = command.split()
    lng = len(words)
    cmd_found = False
    word_id = 0
    values = COMMAND_TIMEOUTS


    while cmd_found is False:
        values = key_search(words[word_id], values)
        if type(values) is dict:
            word_id += 1
        elif values is None or lng == word_id:
            return  COMMAND_TIMEOUTS['default']

        else:
            return values
        
            
        
def key_search(key, dictionary):
    match_count = 0

    if key in dictionary.keys():
        return dictionary[key]
    else:
        for i in dictionary.keys():
            if i.startswith(key):
                match = dictionary[i]
                match_count += 1
                return match


