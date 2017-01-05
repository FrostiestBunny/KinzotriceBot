#!/usr/bin/env python3

from UOBot import bot
import discord
import util
from desires import desires
import cards

@bot.command(name="rps", pass_context=True)
async def rps_challenge(ctx, member : discord.Member, bet : int):
    '''Challenge another user to a rock paper scissors battle! YOU CAN EVEN BET DESIRES.
    '''
    bet = abs(bet)
    challenger = ctx.message.author
    if member == None:
        await bot.say("User doesn't exist.")
        return
    if member.bot or challenger.bot:
        await bot.say("Can't challenge bots, m8.")
        return
    if member.name == challenger.name:
        await bot.say("Can't challenge yourself silly.")
        return
    if desires.get(challenger.id) < bet:
        await bot.say('Nope.')
        return
    if desires.get(member.id) < bet:
        await bot.say("Challenged user doesn't have enough {}.".format(desires.get_emoji()))
        return
    await bot.say('{}, you have been challenged to a rock paper scissors battle by {}. The bet is {} desires. Do you accept? Type yes or no.'.format(member.mention, challenger.name, bet))
    response = await bot.wait_for_message(timeout=120, author=member)
    if response == None:
        await bot.say('Waited for too long, aborting.')
        return
    response = response.content
    if 'no' in response.lower():
        await bot.say('You coward.')
        return
    if 'yes' not in response.lower():
        await bot.say("I don't get it.")
        return

    await bot.say('Alright, the duel has started! Please wait till you receive a prompt from me.')
    tries = 0
    while tries < 3:
        await bot.send_message(challenger, 'Write rock, paper, or scissors.')
        choice1 = await bot.wait_for_message(author=challenger, timeout=60)
        if choice1 is None:
            await bot.say("Waited for too long. Aborting.")
            return
        choice1 = choice1.content
        if 'rock' in choice1.lower() or 'paper' in choice1.lower() or 'scissors' in choice1.lower():
            await bot.send_message(challenger, 'Registered. Please wait.')
            break
        await bot.send_message(challenger, 'Incorrect response.')
        tries += 1
    tries = 0
    while tries < 3:
        await bot.send_message(member, 'Write rock, paper, or scissors.')
        choice2 = await bot.wait_for_message(author=member, timeout=60)
        if choice2 is None:
            await bot.say("Waited for too long. Aborting.")
            return
        choice2 = choice2.content
        if 'rock' in choice2.lower() or 'paper' in choice2.lower() or 'scissors' in choice2.lower():
            await bot.send_message(member, "Accepted.")
            break
        await bot.send_message(member, 'Incorrect response.')
        tries += 1
    choice1_new, choice2_new = util.set_rps(choice1, choice2)
    winner = util.eval_rps(choice1_new, choice2_new)
    if winner == 'p1':
        winner = challenger
        await bot.say('{} uses {} against {}.'.format(challenger.name, choice1_new, choice2_new))
        await bot.say('{} WINS {} {}!'.format(challenger.name, bet, desires.get_emoji()))
        desires.add(challenger.id, bet)
        desires.sub(member.id, bet)
        return
    if winner == 'p2':
        winner = member
        await bot.say('{} uses {} against {}.'.format(member.name, choice2_new, choice1_new))
        await bot.say('{} WINS {} {}!'.format(member.name, bet, desires.get_emoji()))
        desires.add(member.id, bet)
        desires.sub(challenger.id, bet)
        return
    await bot.say('{} uses {} against {}.'.format(member.name, choice2, choice1))
    await bot.say("IT'S A TIE SO NOTHING HAPPENS.")
    return

@bot.command(name="blackjack")
async def cards_blackjack(channel : discord.Channel, *args : discord.Member):
    players = []
    for arg in args:
        if arg.bot:
            await bot.send_message(channel, "No challenging bots, m8.")
            return
        players.append(arg)
    s = "Place your bets "
    for player in players:
        s += player.mention
        s += " "
    await bot.send_message(channel, s)
    bets = {}
    temp_players = players[:]
    for player in temp_players:
        await bot.send_message(channel, "{}'s turn. If you don't want to play, simply respond 'no'.".format(player.mention))
        while True:
            bet = await bot.wait_for_message(timeout=60, author=player)
            if bet is None:
                await bot.send_message(channel, "You didn't bet in time, too bad.")
                players.remove(player)
                break
            if "no" in bet.content:
                await bot.send_message(channel, "{} has quit.".format(player.name))
                players.remove(player)
                break
            try:
                bet = int(bet.content)
                if bet <= 0 or bet > desires.get(player.id):
                    await bot.send_message(channel, "Not enough desires. Or you tried betting 0, what do I know.")
                    continue
                bets[player.id] = bet
                break
            except ValueError:
                await bot.send_message(channel, "Not a number, try again, or just say no.")
    if len(players) == 0:
        await bot.send_message(channel, "EVERYBODY QUIT GG WP NO RE.")
        return
    await bot.send_message(channel, "Participants and their bets.")
    s = ""
    for player in players:
        s += player.name
        s += ": "
        s += str(bets[player.id])
        s += "\n"
    await bot.send_message(channel, s)

    bj = cards.BlackJack()
    hands = {}
    for player in players:
        hands[player.name] = cards.Hand(player.name)
    dealer_hand = cards.Hand("Kinzotrice")

    for hand in hands:
        result = bj.deck.deal([hands[hand]], 1)

    await bot.send_message(channel, "First card dealt to every player.")
    bj.deck.deal([dealer_hand], 1)
    await bot.send_message(channel, "Card dealt to Kinzotrice.")
    await bot.send_message(channel, str(dealer_hand))
    temp_players = players[:]
    for player in temp_players:
        result = bj.deck.deal([hands[player.name]], 1)
        if result == 1:
            await bot.say(str(hands[hand]))
            await bot.say("{}, WOW, NATURAL BLACKJACK. YOU WIN TWICE YOUR BET Hand value(temp for debugging): {}".format(player.name, hands[player.name].total_value()))
            desires.add(player.id, (bets[player.id] * 2))
            players.remove(player)

    await bot.send_message(channel, "Second card dealt to every player.")
    for player in players:
        await bot.send_message(player, str(hands[player.name]))

    bj.deck.deal([dealer_hand], 1)
    await bot.send_message(channel, "Second card dealt to Kinzotrice.")
    await bot.send_message(channel, "THE GAME BEGINS FOR REAL.")
    temp_players_2 = players[:]
    for player in temp_players_2:
        while True:
            await bot.send_message(channel, "Your turn, {}. Take a card (type hit) or not (type stand).".format(player.mention))
            msg = await bot.wait_for_message(author=player, channel=channel)
            msg = msg.content
            if "stop" in msg.lower() or "stand" in msg.lower():
                break
            if "hit" in msg.lower() or "take" in msg.lower():
                dl = bj.deck.deal([hands[player.name]], 1)
                await bot.send_message(player, str(hands[player.name]))
                if dl == 1:
                    await bot.send_message(channel, str(hands[player.name]))
                    await bot.send_message(channel, "{}, WOW, BLACKJACK.".format(player.name))
                    desires.add(player.id, bets[player.id])
                    players.remove(player)
                    break
                if dl == -1:
                    await bot.send_message(channel, str(hands[player.name]))
                    await bot.send_message(channel, "{}, YOU LOSE.".format(player.name))
                    desires.sub(player.id, bets[player.id])
                    players.remove(player)
                    break
                continue
            await bot.send_message(channel, "I don't get you m8, try again.")

    if len(players) == 0:
        await bot.send_message(channel, "Everybody lost, GG WP.")
        return

    dl_turn_result = None
    await bot.send_message(channel, str(dealer_hand))
    await bot.send_message(channel, "Dealer's turn.")
    while dealer_hand.total_value() < 17:
        dl_turn_result = bj.deck.deal([dealer_hand], 1)
    await bot.send_message(channel, "Dealer's hand after his turn.")
    await bot.send_message(channel, str(dealer_hand))
    if dl_turn_result == -1:
        await bot.send_message(channel, "The dealer loses. Every player gets paid their bet.")
        for player in players:
            desires.add(player.id, bets[player.id])
        return
    if dl_turn_result == 1:
        await bot.send_message(channel, "The dealer has a blackjack, every player who doesn't have it loses.")
        for player in players:
            desires.sub(player.id, bets[player.id])
        return

    for player in players:
        if hands[player.name].total_value() > dealer_hand.total_value():
            await bot.send_message(channel, "{0} wins {1} desires. {0}'s hand:\n {2}".format(player.name, bets[player.id], str(hands[player.name])))
            desires.add(player.id, bets[player.id])
        elif hands[player.name].total_value() == dealer_hand.total_value():
            await bot.send_message(channel, "{0} ties with the dealer, so they don't win nor lose anything. {0}'s hand:\n {1}".format(player.name, str(hands[player.name])))
        else:
            await bot.send_message(channel, "{0} loses {1} desires. {0}'s hand:\n {2}".format(player.name, bets[player.id], str(hands[player.name])))
            desires.sub(player.id, bets[player.id])
