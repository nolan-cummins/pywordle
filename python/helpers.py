from collections import defaultdict

# extract game state from NYT Wordle
def extractWordle(soup):
    # get all key states
    key_states=defaultdict(list)
    buttons = soup.find_all("button", {"class":"Key-module_key__kchQI"})
    for button in buttons:
        key = button.get("data-key")
        if not key.isalpha():
            continue
        state = button.get("data-state")
        if state is None:
            key_states["allowed"].append(key)
        else:
            key_states[state].append(key)

    # get the state of the board, previous guesses, etc.
    board_state = soup.find_all("div", {"class":"Tile-module_tile__UWEHN"})
    rows=[[]]
    row=0
    for i, tile in enumerate(board_state):
        tile_info = tile.get("aria-label")
        state = tile.get("data-state")
        letter = tile_info.split(",")[1].strip()
        if letter == "empty":
            rows[row].append(None)
        else:
            rows[row].append((letter, state))
        if "5th letter" in tile_info and i != len(board_state)-1:
            row+=1
            rows.append([])
    return key_states, rows

# extract game state from wordly.org
def extractWordly(soup):
    def convertState(state):
        if state == "letter-elsewhere":
            return "present"
        elif state == "letter-absent":
            return "absent"
        elif state == "letter-correct":
            return "correct"
        return None

    # get all key states
    key_states=defaultdict(list)
    buttons = soup.find_all("div", {"class":"Game-keyboard-button"})
    for button in buttons:
        key = button.text
        state_info = button.get("class")
        if len(key) != 1:
            continue
        if len(state_info) == 1:
            state = "allowed"
        else:
            state = convertState(state_info[1])

        key_states[state].append(key)

    # get the state of the board, previous guesses, etc.
    board_state = soup.find_all("div", {"class":"Row Row-locked-in"})
    rows=[]
    i=0
    for i, row in enumerate(board_state):
        rows.append([])
        for tile in row.find_all("div", {"class":"Row-letter"}):
            letter = tile.text[0]
            state = convertState(tile.get("class")[1])
            rows[i].append((letter, state))
    return key_states, rows

# generate possible characters for each letter given the previous guesses
def generatePossibilites(key_states, rows):
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    ch=[letters.copy() for _ in range(5)]
    for row in rows:
        for i, data in enumerate(row):
            if data is None:
                continue
            letter = data[0].lower()
            state = data[1]
            if state == "correct":
                ch[i] = letter
            elif state == "present" or state == "absent":
                if letter in ch[i]:
                    ch[i].remove(letter)

    for invalid in key_states['absent']:
        for c in ch:
            if invalid in c:
                c.remove(invalid)
    return ch

# find all possible words given the possible characters from the OED-scraped dictionary of 5-letter words
def findMatches(ch, key_states, all_words, dictionary):
    possible_words=[]
    for word in all_words:
        match = True
        for i, word_c in enumerate(word):
            if word_c not in ch[i]:
                match = False
                continue
            for present_c in key_states['present']:
                if present_c in ch[i] and present_c not in word:
                    match = False
        if match:
            possible_words.append((word, dictionary[word]))

    # sort based on frequency from Google Ngram datasets
    best_matches_pair = sorted(possible_words, key=lambda x: x[1], reverse=True)[:5]
    best_matches=[]
    for match in best_matches_pair:
        best_matches.append(match[0])
    return best_matches