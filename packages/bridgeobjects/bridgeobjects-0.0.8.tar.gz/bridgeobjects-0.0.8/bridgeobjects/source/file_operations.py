"""Provide file load and save functionality for PBN, RBN and lin formats."""

__all__ = ['load_pbn', 'save_pbn', 'load_lin', 'load_rbn', 'parse_pbn', 'parse_lin', 'save_rbn', 'BoardAsString']

import os
import datetime
import re

from .event import Event
from .board import Board
from .hand import Hand
from .card import Card
from .call import Call
from .suit import Suit
from .trick import Trick
from .contract import Contract
from .auction import Auction
from .constants import SUIT_NAMES, RANKS, CALLS, SEATS, CONTRACTS, CARD_NAMES

PBN_VULNERABILITY_CONVERSION = {'Z': 'None', 'N': 'NS', 'E': 'EW',
                                'B': 'Both', '?': None,
                                'None': 'Z', 'NS': 'N', 'EW': 'E',
                                'Both': 'B', None: '?'}

LIN_VULNERABILITY_CONVERSION = {'0': 'None', 'N': 'NS', 'E': 'EW',
                                'B': 'Both', '?': None,
                                'None': '0', 'NS': 'N', 'EW': 'E',
                                'Both': 'B', None: '?'}

PBN_CALL_CONVERSION = {'P': 'Pass', 'D': 'X', 'R': 'XX', 'A': 'AP',
                       'Pass': 'P', 'X': 'D', 'XX': 'R', 'AP': 'A'}

PBN_VERSION_TEXT = '% PBN 2.1'
PBN_FORMAT_TEXT = '% EXPORT'
PBN_CONTENT_TEXT = '% Content-type: text/pbn; charset=ISO-8859-1'
PBN_CREATOR_TEXT = '% Creator: bridgeobjects'

RBN_VERSION_TEXT = '% RBN version 3.2'
RBN_CREATOR_TEXT = '% Created by bridgeobjects'

DEFAULT_EVENT_NAME = 'BfG default event name'
DEFAULT_EVENT_DATE = datetime.date(1980, 1, 1)


def load_pbn(path):
    """Load a pbn file to a list of events."""
    events = []
    file_text = _get_file_text(path)
    if file_text:
        events = parse_pbn(file_text)
    return events


def save_pbn(events, path, append=False):
    """Save a list of events in pbn format."""
    success = False
    output = _create_pbn_list(events, path)
    if output:
        success = bool(_write_file(output, path, append))
    return success


def load_rbn(path):
    """Load a rbn file to a list of events."""
    events = []
    file_text = _get_file_text(path)
    if file_text:
        events = parse_rbn(file_text)
    return events


def save_rbn(events, path, append=False):
    """Save a list of events in rbn format."""
    success = False
    output = _create_rbn_list(events)
    if output:
        success = bool(_write_file(output, path, append))
    return success


def load_lin(path):
    """Load a lin file to a list of events."""
    events = []
    file_text = _get_file_text(path)
    if file_text:
        events = parse_lin(file_text)
    return events


def _get_file_text(path):
    """Return the file text lines as a list."""
    file_text = ""
    try:
        with open(path, "r") as pbn_file:
            raw_text = pbn_file.read()
            raw_text = raw_text.replace(chr(13), '')
            raw_text = raw_text.replace('\r', '')
            file_text = raw_text.split('\n')
    except FileNotFoundError:
        raise
    return file_text


def parse_pbn(file_lines):
    """Populate bridgeobjects objects from a pbn file."""
    current_name = None
    current_board_identifier = ""
    auction_state = False
    play_state = False
    board_state = False
    events = []
    event = None
    board = None
    value = None
    for line in file_lines:
        if line:
            tag = ""
            if line.startswith("%"): # Comments
                pass
            elif line.startswith("[") or line.startswith("{"):
                tag, value = _parse_pbn_line(line)
                if auction_state and tag != 'Note':
                    auction_state = False
                elif play_state and tag != 'Note':
                    play_state = False
                elif line.startswith('{'):
                    if board_state and tag == 'Description':
                        board.description = value
                        board_state = False

            # Event event
            if tag == "Event":
                if current_name != value:
                    current_name = value
                    current_board_identifier = ""
                    if value and value != DEFAULT_EVENT_NAME:
                        event = Event(value)
                        events.append(event)

            # Event location
            elif tag == "Site":
                event.location = value

            # Event date
            elif tag == "Date":
                event.date = _parse_pbn_date(value)

            # Scoring method
            elif tag == "Scoring":
                event.scoring_method = value

            # Board identifier
            elif tag == "Board":
                board_state = True
                board_identifier = value
                if current_board_identifier != board_identifier:
                    current_board_identifier = board_identifier
                    board = Board(board_identifier)
                    if not event:
                        event = Event(DEFAULT_EVENT_NAME)
                        events.append(event)
                    event.boards.append(board)
                    trick_index = 0

            # Board West
            elif tag == "West":
                board.west = value

            # Board North
            elif tag == "North":
                board.north = value

            # Board East
            elif tag == "East":
                board.east = value

            # Board South
            elif tag == "South":
                board.south = value

            # Board Dealer
            elif tag == "Dealer":
                board.dealer = value

            # Board Vulnerable
            elif tag == "Vulnerable":
                board.vulnerable = value

            # Board hands
            elif tag == "Deal":
                board.hands = _parse_pbn_deal(board, value)
                # board.hands_by_seat = {
                #     'N': board.hands['N'],
                #     'E': board.hands['E'],
                #     'S': board.hands['S'],
                #     'W': board.hands['W'],
                # }
                # board.hands_by_index = {
                #      0: board.hands[0],
                #      1: board.hands[1],
                #      2: board.hands[2],
                #      3: board.hands[3],
                # }

            # Declarer
            elif tag == "Declarer":
                if value == '?':
                    value = None
                board.contract.declarer = value
                board.declarer = value

            # # Description
            # elif tag == "Description":
            #     board.description = value

# TODO sort out modifiers
            # Contract
            elif tag == "Contract":
                if value and value[-1] == 'X':
                    if value[-2] == 'X':
                        board.contract.modifier = 'R'
                        value = value[:-2]
                    else:
                        board.contract.modifier = 'D'
                        value = value[:-1]
                if value in CONTRACTS:
                    board.contract.name = value

            # Auction
            elif tag == "Auction":
                if value != 'None':
                    board.auction.first_caller = value
                auction_state = True
            elif auction_state:
                _parse_pbn_auction(board, tag, value, line)

            # Play section
            elif tag == "Play":
                first_player = value
                play_state = True
            elif play_state:
                trick = _parse_pbn_play_section(board, tag, value, line, first_player)
                if trick:
                    board.tricks[trick_index] = trick
                    trick_index += 1
    return events


def _parse_pbn_line(line):
    """Return the tag and value from a pbn text line."""
    # example pbn line: [Site "Amsterdam, The Netherlands NLD"]
    space_at = line.find(" ")
    tag = line[1:space_at]
    value = line[space_at + 1:]
    value = value[:-1]
    value = value.replace('"', "")
    return tag, value


def _parse_pbn_date(value):
    """Return a datetime date object from a pbn date string."""
    # example date value: 2018.02.26
    is_valid = re.search("[0-9]{4}.[\0-9]{2}.[0-9]{2}", value)
    if is_valid:
        date = value.split('.')
        date = list(map(int, date))
        return datetime.date(date[0], date[1], date[2])
    else:
        return DEFAULT_EVENT_DATE


def _parse_pbn_deal(board, deal):
    """Return a list of hands from a pbn deal string."""
    # example deal value:
    # N:K87.Q642.AJ6.K73 T5.85.Q752.Q6542 AQJ96.73.T843.JT 432.AKJT9.K9.A98
    hands = {}
    # Assign hands to board in correct seat; 0 and 'N, 1 and 'E' etc..
    raw_hands = deal[2:].split(" ")
    first_seat = SEATS.index(deal[0])
    for index, card_list in enumerate(raw_hands):
        seat_index = (first_seat + index) % 4
        seat_name = SEATS[seat_index]
        hand = Hand(card_list)
        hands[seat_index] = hand
        hands[seat_name] = hand
    return hands


def _parse_pbn_auction(board, tag, value, line):
    """Use the tag and value to update the board's auction attributes."""
    if tag == 'Note':
        note_line = value.split(':', 1)
        board.auction.notes[note_line[0]] = note_line[1]
    else:
        line = ' '.join(line.split())
        auction_line = line.split(' ')
        call_index = len(board.auction.calls) - 1
        for index, element in enumerate(auction_line):
            if element in PBN_CALL_CONVERSION:
                element = PBN_CALL_CONVERSION[element]
            if element == '-':
                pass  # Dummy value in PBN. No bid has been made.
            elif element == 'A':
                passes = [Call('P')]*4
                board.auction.calls = passes
            elif element in CALLS:
                board.auction.calls.append(Call(element))
                board.auction.note_keys.append('')
                call_index += 1
            elif element[0] == '=':
                board.auction.note_keys[call_index] = element.replace('=', '')
            else:
                assert False, 'invalid element in calls: %s' % element


def _parse_pbn_play_section(board, tag, value, line, first_player):
    """Use the tag and value to update the board's Tricks."""
    trick = None
    note_found = False
    note_found = False
    trick_index = 0
    if tag == 'Note':
        note_line = value.split(':', 1)
        board.play_notes[note_line[0]] = note_line[1]
    else:
        line = ' '.join(line.split())
        trick = Trick(trick_index)
        trick_index += 1
        play_line = line.split(' ')
        trick_note_keys = []
        card_index = 0
        for element in play_line:
            if len(element) == 2:
                element = ''.join([element[1], element[0]])
            if element[0] == '=':
                note_found = True
                trick_note_keys[card_index-1] = element.replace('=', '')
                card.play_note_index = element.replace('=', '')
            elif element in CARD_NAMES:
                card = Card(element)
                trick.cards.append(card)
                trick_note_keys.append('')
                card_index += 1
        trick.leader = first_player
        if len(trick.cards) == 4:
            trick.complete(board.contract.trump_suit)
            first_player = trick.winner
        if note_found:
            trick.note_keys = [key for key in trick_note_keys]
    return trick


def _get_pbn_dealer_index(board, deal):
    """
        Return the first hand index to ensure that the first hand
        assigned to the board's hands list is that of the board dealer.
    """
    # first_hand is the seat index of the first hand given in the deal
    first_hand = SEATS.index(deal[0])

    # dealer_index is the seat index of the dealer
    dealer_index = SEATS.index(board.dealer)

    # rotate the hand index to ensure that the
    # first hand created is the dealer's
    hand_index = (first_hand - dealer_index) % 4
    return hand_index


def parse_rbn(file_text):
    """Populate bridgeobjects objects from a rbn file."""
    events = []
    current_name = ""
    current_board_identifier = ""
    create_event = True
    board = None
    north, south, west, east = "", "", "", ""
    for line in file_text:
        if line:
            tag = ""

            # Comments
            if line[0] == "%":
                pass

            # Notes
            if line[0] == "{":
                pass
            else:
                tag = line[0]
                value = line[2:]
                if tag in "EDL":
                    if create_event:
                        event = Event()
                        events.append(event)
                        create_event = False

                # Event name
                if tag == "E":
                    event.name = value

                # Event date
                elif tag == "D":
                    event.date = _parse_rbn_date(value)

                # Event location
                elif tag == "L":
                    event.location = value

                # Event Scoring
                elif tag == "F":
                    event.scoring_method = value

                # Board identifier
                elif tag == "B":
                    board_identifier = value
                    if current_board_identifier != board_identifier:
                        current_board_identifier = board_identifier
                        board = Board(board_identifier)
                        event.boards.append(board)
                        board.north, board.south, board.west, board.east = north, south, west, east
                    create_event = True

                # Board dealer and hands
                elif tag == "H":
                    board.dealer = value[0]
                    board.hands = _parse_rbn_deal(board, value)

                # Board auction and vulnerable
                elif tag == "A":
                    board.vulnerable = _get_rbn_vulnerable(value)
                    board.auction = _parse_rbn_auction(value)

                # Board contract and declarer
                elif tag == "C":
                    raw_data = value.split(':')
                    board.contract = _get_rbn_contract(raw_data[0])
                    if raw_data[1] == '?':
                        declarer = None
                    else:
                        declarer = raw_data[1]
                    board.contract.declarer = declarer

                # Board players
                elif tag == "N":
                    north, south, west, east = _parse_rbn_seats(value)
                    if board:
                        board.north, board.south, board.west, board.east = \
                            north, south, west, east
        else:
            create_event = True
    return events


def _parse_rbn_deal(board, deal):
    """Return a list of hands from a rbn deal string."""
    # example deal value:
    # W:A8765.QT.K9.AT87:J42.AJ7632.J.632:QT3.85.Q86.KQJ54:
    hands = {}
    raw_hands = deal[2:].split(":")
    if len(raw_hands[3]) == 0:
        raw_hands = _build_fourth_rpn_hand(raw_hands)
    first_seat = SEATS.index(deal[0])
    for index, card_list in enumerate(raw_hands):
        seat_index = (first_seat + index) % 4
        seat_name = SEATS[seat_index]
        hand = Hand(card_list)
        hands[seat_index] = hand
        hands[seat_name] = hand
    return hands


def _parse_rbn_date(value):
    """Return a datetime date object from a pbn date string."""
    # example date value: 19930512
    year = int(value[:4])
    month = int(value[4:6])
    day = int(value[6:])
    return datetime.date(year, month, day)


def _parse_rbn_seats(value):
    """Return, north, south, west, east for a rbn file."""
    north, south, west, east = "", "", "", ""
    if value:
        pairs = value.split(":")
        if len(pairs) >= 1:
            north_south = pairs[0].split("+")
            if len(north_south) >= 1:
                north = north_south[0]
            if len(north_south) >= 2:
                south = north_south[1]
        if len(pairs) >= 2:
            west_east = pairs[1].split("+")
            if len(west_east) >= 1:
                west = west_east[0]
            if len(west_east) >= 2:
                east = west_east[1]
    return north, south, west, east


def _build_fourth_rpn_hand(raw_hands):
    """Build the fourth hand based on the other three hands."""
    used_cards = [[], [], [], []]
    last_hand = [[], [], [], []]
    # Create a list of cards used by other three hands.
    for hand in raw_hands[:-1]:
        suit_cards = hand.split('.')
        for suit, cards in enumerate(suit_cards):
            for card in cards:
                used_cards[suit].append(card)
    # Build a hand (as a list) from the cards not already used.
    for suit in range(4):
        for rank in reversed(RANKS[1:]):
            if rank not in used_cards[suit]:
                last_hand[suit].append(rank)
    # Convert list to string form.
    suit_names = []
    for suit in last_hand:
        suit_names.append(('').join(suit))
    fourth_hand = ('.').join(suit_names)
    raw_hands[3] = fourth_hand
    return raw_hands


def _get_rbn_vulnerable(value):
    """Return the auction vulnerability as a string."""
    return PBN_VULNERABILITY_CONVERSION[value[1]]


def _parse_rbn_auction(value):
    """Return the auction as a list of board.CALLS."""
    auction = Auction()
    pointer = 0
    calls = []
    while pointer < len(value):
        if value[pointer] == 'P':
            calls.append(Call('P'))
            pointer += 1
        elif value[pointer].isdigit():
            calls.append(Call(value[pointer:pointer + 2]))
            pointer += 2
        elif value[pointer] in 'XD':
            calls.append(Call('D'))
            pointer += 1
        elif value[pointer] == 'R':
            calls.append(Call('R'))
            pointer += 1
        elif value[pointer] == 'A':
            calls.extend([Call('P'), Call('P'), Call('P')])
            pointer += 1
        else:
            pointer += 1
    auction.calls = list(calls)
    return auction


def _get_rbn_contract(value):
    """Return the contract vulnerability as a list of CALLS."""
    contract = Contract(name=value)
    # if len(value) > 3:
    #     value = value[:3]
    # if value in CONTRACTS:
    #     contract.name = value
    return contract


def _create_pbn_list(events, path=''):
    """Create a list of strings for events in pbn format."""
    output = []
    if path:
        if not os.path.isfile(path):
            output = _append_pbn_header()
        else:
            with open(path, 'r') as pbn_file:
                for line in pbn_file.readlines():
                    line = line.replace('\n', '')
                    if len(line.replace(' ', '')) > 0:
                        if line[1] != '%':
                            output = _append_pbn_header()
                            break
                contents = pbn_file.readlines()
                if len(contents) == 0:
                    output = _append_pbn_header()
    for event in events:
        output.extend(_create_pbn_event(event))
    return output


def _append_pbn_header():
    """Create a list containing the pbn file header."""
    output = []
    output.append(PBN_VERSION_TEXT)
    output.append(PBN_FORMAT_TEXT)
    output.append(PBN_CONTENT_TEXT)
    output.append(PBN_CREATOR_TEXT)
    output.append('')
    return output


def _create_pbn_event(event):
    """Return an event as string in pbn format as a list."""
    output = []
    output.append('[Event "%s"' % event.name)
    output.append('[Site "%s"' % event.location)
    if event.date:
        output.append('[Date "%s"' % event.date.strftime('%Y.%m.%d'))
    output.append('')
    for board in event.boards:
        output.extend(BoardAsString.create_pbn_board(event, board))
    return output
#
#
# def create_pbn_board(event, board):
#     """Return a board as a list of strings in pbn format."""
#     output = ['[Board "%s"]' % board.identifier,
#               '[West "%s"]' % board.west,
#               '[North "%s"]' % board.north,
#               '[East "%s"]' % board.east,
#               '[South "%s"]' % board.south,
#               '[Dealer "%s"]' % board.dealer]
#     if board.description:
#         output.append('{Description "%s"}' % board.description)
#     if board.vulnerable:
#         output.append('[Vulnerable "%s"]' % board.vulnerable.replace('Both', 'All'))
#     output.append('[Deal "{}:{}"]'.format(board.dealer, _get_pbn_deal(board)))
#     if event:
#         output.append('[Scoring "%s"]' % _question_from_null(event.scoring_method))
#     output.append('[Declarer "%s"]' % _question_from_null(board.contract.declarer))
#     if board.contract.call:
#         question = _question_from_null(board.contract.call.name)
#         output.append('[Contract "%s"]' % question)
#     if board.auction.calls:
#         output.extend(_create_pbn_auction(board))
#     output.append('[Result "%s"]' % _question_from_null(board.result))
#     if board.tricks:
#         output.extend(_create_pbn_play_section(board))
#     output.append('')
#     if board.play_notes:
#         for key in board.play_notes:
#             note = '[Note "{}:{}"]'.format(key, board.play_notes[key])
#             output.append(note)
#         output.append('')
#     return output


def _create_pbn_auction(board):
    """Return an auction as a pbn list."""
    auction_list = ['[Auction "{}"]'.format(board.contract.declarer)]
    dealer_index = SEATS.index(board.dealer)
    line = []
    for index in range((dealer_index - SEATS.index('W')) % 4):
        line.append('-')
    for call in board.auction.calls:
        if call.name in PBN_CALL_CONVERSION:
            pbn_call = PBN_CALL_CONVERSION[call.name]
        else:
            pbn_call = call.name
        line.append(pbn_call)
        if len(line) == 4:
            auction_list.append(' '.join([bid for bid in line]))
            line = []
    auction_list.append(' '.join([bid for bid in line]))
    return auction_list


def _create_pbn_play_section(board):
    """Return board's tricks as a pbn list."""
    trick_list = []
    player = board.tricks[0].leader
    trick_list.append('[Play "{}"]'.format(player))
    for index, trick in sorted(board.tricks.items()):
        if trick.leader:
            line = []
            for index, card in enumerate(trick.cards):
                if card:
                    line.append(''.join([card.name[1], card.name[0]]))
                    if trick.note_keys[index]:
                        line.append('={}='.format(trick.note_keys[index]))
            trick_list.append(' '.join([card for card in line]))
    return trick_list


def _question_from_null(value):
    """Return a question mark if value is None or ''."""
    if not value:
        return "?"
    else:
        return value


def _get_pbn_deal(board, delimiter=' '):
    """Return a board's hands as a string in pbn format."""
    hands_list = []
    dealer_index = SEATS.index(board.dealer)
    for index in range(4):
        seat = (dealer_index + index) % 4
        hand = board.hands[seat]
        hand_list = []
        for suit_name in reversed(SUIT_NAMES):
            suit_cards = []
            for rank in reversed(RANKS[1:]):
                for card in hand.cards:
                    if card.name == ''.join([rank, suit_name]):
                        suit_cards.append(card.rank)
            hand_list.append(''.join(suit_cards))
        hands_list.append('.'.join(hand_list))
    return delimiter.join(hands_list)


def _create_rbn_list(events):
    """Create a list of strings for events in rbn format."""
    output = []
    output.append(RBN_VERSION_TEXT)
    output.append(RBN_CREATOR_TEXT)
    for event in events:
        output.extend(_create_rbn_event(event))
    return output


def _create_rbn_event(event):
    """Return an event as string in rbn format as a list."""
    output = []
    output.append('E %s' % event.name)
    output.append('L %s' % event.location)
    if event.date:
        output.append('D %s' % event.date.strftime('%Y%m%d'))
    output.append('M %s' % _question_from_null(event.scoring_method))
    for board in event.boards:
        output.extend(_create_rbn_board(event, board))
    return output


def _create_rbn_board(event, board):
    """Return a board as a list of strings in pbn format."""
    output = ['B %s' % board.identifier]

    #  names
    names = _create_rbn_names(board)
    if names:
        output.append('N %s' % names)

    # hands
    deal = _get_pbn_deal(board, ':')
    output.append('H {}:{}'.format(board.dealer, deal))

    # auction
    vulnerable = PBN_VULNERABILITY_CONVERSION[board.vulnerable]
    output.append('A {}{}:'.format(board.dealer, vulnerable))

    # contract
    board_contract = _question_from_null(board.contract)
    board_declarer = _question_from_null(board.declarer)
    contract = ':'.join([board_contract.name, board_declarer])
    if contract != "?:?":
        output.append('C %s' % contract)

    # result
    result = _question_from_null(board.result)
    if result != "?":
        output.append('[R %s' % result)
    output.append('')
    return output


def _create_rbn_names(board):
    """Return the boards players in rbn format."""
    names = '{}+{}:{}+{}'.format(board.north, board.south, board.west, board.east)
    if names == "+:+":
        names = ""
    if names[:3] == "+:":
        names = names.replace("+:", ";")
    if names[-3:] == ":+":
        names = names.replace(":+", ";")
    return names


def _write_file(output, path, append):
    """Write the list 'ouput' to a text file defined by path."""
    if not os.path.isfile(path):
        with open(path, "w") as pbn_file:
            pbn_file.write('')
    try:
        if append:
            mode = 'a'
        else:
            mode = 'w'
        with open(path, mode) as pbn_file:
            pbn_file.write('\n'.join(output))
        success = True
    except FileNotFoundError:
        logger.warning('invalid file path: %s. File not written', path)
        success = False
    return success


def parse_lin(file_text):
    """Populate bridgeobjects objects from a lin file."""
    events = []
    event = Event()
    events.append(event)
    for line in file_text:
        if line:
            if '[Date]' in line:
                value = line.split(' ')[-1]
                event.date = _parse_pbn_date(value)
            elif '[Location]' in line:
                value = line.split(' ', 2)[-1]
                event.location = value
            elif '[Event]' in line:
                value = line.split(' ', 2)[-1]
                event.session = value
            if line[0:2] == 'qx':
                board = _parse_lin_board(line)
                event.boards.append(board)
    return events


def _parse_lin_board(line):
    """Return a board object from a lin line."""
    board = Board()
    line_list = line.split('|')
    board.identifier = line_list[7]
    board.vulnerable = LIN_VULNERABILITY_CONVERSION[line_list[9]]
    dealer_index = int(line_list[3][0]) - 1
    board.dealer = ['S', 'W', 'N', 'E'][dealer_index]
    board.hands = _parse_lin_hands(line_list[3][1:], board.dealer)
    return board


def _parse_lin_hands(line_list, dealer):
    """Return a list of hands from lin text."""
    hands = {}
    dealer_index = SEATS.index(dealer)
    hand_index = (2 - dealer_index) % 4
    hand = Hand()
    for character in line_list:
        if character in Suit.SHORT_NAMES:
            suit_name = character
        elif character == ',':
            hands[hand_index] = hand
            hands[SEATS[hand_index]] = hand
            hand = Hand()
            hand_index += 1
            hand_index %= 4
        else:
            card = Card(character, suit_name)
            hand.cards.append(card)
    hands[hand_index] = hand
    hand = Hand()
    hand_index += 1
    hand_index %= 4

    hand = Board.build_fourth_hand(hands)
    hands[hand_index] = hand
    hands[SEATS[hand_index]] = hand
    return hands


class BoardAsString(object):
    def __init__(self):
        pass

    @staticmethod
    def create_pbn_board(event, board):
        """Return a board as a list of strings in pbn format."""
        output = ['[Board "%s"]' % board.identifier,
                  '[West "%s"]' % board.west,
                  '[North "%s"]' % board.north,
                  '[East "%s"]' % board.east,
                  '[South "%s"]' % board.south,
                  '[Dealer "%s"]' % board.dealer]
        if board.description:
            output.append('{Description "%s"}' % board.description)
        if board.vulnerable:
            output.append('[Vulnerable "%s"]' % board.vulnerable.replace('Both', 'All'))
        output.append('[Deal "{}:{}"]'.format(board.dealer, _get_pbn_deal(board)))
        if event:
            output.append('[Scoring "%s"]' % _question_from_null(event.scoring_method))
        output.append('[Declarer "%s"]' % _question_from_null(board.contract.declarer))
        if board.contract.call:
            question = _question_from_null(board.contract.call.name)
            output.append('[Contract "%s"]' % question)
        if board.auction.calls:
            output.extend(_create_pbn_auction(board))
        output.append('[Result "%s"]' % _question_from_null(board.result))
        if board.tricks:
            output.extend(_create_pbn_play_section(board))
        output.append('')
        if board.play_notes:
            for key in board.play_notes:
                note = '[Note "{}:{}"]'.format(key, board.play_notes[key])
                output.append(note)
            output.append('')
        print(output)
        return output
