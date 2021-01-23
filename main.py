import discord
import os
from pantheon import pantheon
import asyncio
import json

client = discord.Client()
server = "na1"
api_key = 'RGAPI-7112165c-581b-4678-bf1e-35a28bf55f9f'
json = json.loads(open('champion.json').read())
print(json['data']['Aatrox']['blurb'])

def requestsLog(url, status, headers):
    print(url)
    print(status)
    print(headers)

panth = pantheon.Pantheon(server, api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)

async def getSummonerId(name):
    try:
        data = await panth.getSummonerByName(name)
        return (data['id'],data['accountId'])
    except Exception as e:
        print(e)

async def getRecentMatchlist(accountId):
    try:
        data = await panth.getMatchlist(accountId, params={"endIndex":10})
        return data
    except Exception as e:
        print(e)

async def getRecentMatches(accountId):
    try:
        matchlist = await getRecentMatchlist(accountId)
        tasks = [panth.getMatch(match['gameId']) for match in matchlist['matches']]
        return await asyncio.gather(*tasks)
    except Exception as e:
        print(e)

champs = ["aatrox", "ahri", "akali", "alistar", "amumu", "anivia", "annie", "aphelios", "ashe", "aurelion sol", "azir", "bard", "blitzcrank", "brand", "braum", "caitlyn", "camille", "cassiopeia", "cho'gath", "corki", "darius", "diana", "dr. mundo", "draven", "ekko", "elise", "evelynn", "ezreal", "fiddlesticks", "fiora", "fizz", "galio", "gangplank", "garen", "gnar", "gragas", "graves", "hecarim", "heimerdinger", "illaoi", "irelia", "ivern", "janna", "jarvan iv", "jax", "jayce", "jhin", "jinx", "kai'sa", "kalista", "karma", "karthus", "kassadin", "katarina", "kayle", "kayn", "kennen", "kha'zix", "kindred", "kled", "kog'maw", "leblanc", "lee sin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux", "malphite", "malzahar", "maokai", "master yi", "miss fortune", "mordekaiser", "morgana", "nami", "nasus", "nautilus", "neeko", "nidalee", "nocturne", "nunu and willump", "olaf", "orianna", "orrn", "pantheon", "poppy", "pyke", "qiyana", "quinn", "rakan", "rammus", "rek'sai", "rell", "renekton", "rengar", "riven", "rumble", "Rrze", "samira", "sejuani", "senna", "seraphine", "sett", "shaco", "shen", "shyvana", "singed", "sion", "sivir", "skarner", "sona", "soraka", "swain", "sylas", "syndra", "tahm kench", "taliyah", "talon", "taric", "teemo", "thresh", "tristana", "trundle", "tryndamere", "twisted fate", "twitch", "udyr", "urgot", "varus", "vayne", "veigar", "vel'koz", "vi", "viego", "viktor", "vladimir", "volibear", "warwick", "wukong", "xayah", "xerath", "xin zhao", "yasuo", "yone", "yorick", "yuumi" "zac", "zed", "ziggs", "zilean", "zoe", "zyra"]

quotes = ["So uh, I'm Aatrox. I'm a transcendental being trapped inside cutlery... What's your deal?", "If you'd like to play with me, you'd better be sure you know the game.", "So many noobs, will matchmaking ever find true balance?", "You can't milk those!", "I thought you'd never pick me", "The chicken or the egg? Actually, I came first.", "Ashes, ashes, they all fall down.", "Being good at playing a certain character in a video game is valuable, but I think I'll take the 200+ collective years of professional game design experience.", "How do you like the curves? I was talking about the bow.", "I used to wander the stars. Now I'm stuck down here, with you.", "There is only Shurima. All else is but a mirage.", "*Chime noises*", "The time of man has come to an end.", "I'm on a short fuse.", "You are safe with Braum.", "Wanna see a hat trick?", "Technology and I have a... complicated relationship.", "There is no antidote for me.", "You are such… hideous creatures!", "That just goes to show you you're nothin' but a Whiskey Delta!", "I do not tolerate cowardice.", "They called me a heretic, now they are dead.", "Mundo think you a big sissy! *laughs*", "WELCOME TO THE LEAGUE OF DRAVEN!", "Never had luck. Never needed it.", "I know what lurks in the shadows.", "You know you want me.", "You belong in a museum!", "Come closer. Closer...", "Precision and grace.", "Wanna see a trick?", "I didn't choose to come to life, but I definitely prefer it.", "They took my ship - I'll take their lives", "DEMACIA!!!!", "Gnar gada!", "Don't get pushy!", "Dead man walkin'.", "War is eternal.", "Ah, the sweet smell of science!", "I'm not big on sermons - broken bones teach better lessons.", "Contrary to what you've heard, I have a great sense of humor.", "No-one who wanders is every truly lost.", "Yes, it's true. For only $2.95 a minute, I will leave you breathless.", "For my father, the king.", "Imagine if I had a real weapon!", "Bring down the hammer.", "In carnage, I bloom, like a flower in the dawn.", "Stay still! I'm trying to shoot you!", "Are you the hunter... or the prey?", "Death to all betrayers.", "You know what they say: Karma always catches up to you.", "Do you have a moment to talk about death?", "I tried to silence my mother once. Boy, did I regret that.", "If you run, you won't see me stab you!", "Evil fears only fire! And Yordles, because, what even ARE they?", "I smell death... no, it's you. You smell... bad.", "Yes, they make shurikens this small!", "I ate an optimist once, but I couldn't keep him down.", " Lamb: I'm hungry, I'm hungry, I'm bored, chase chase chase! \nWolf: You get it now!", "I got a joke too! It's called me kicking your teeth in!", "Time to feast!", "For my next trick I'll make their life bar disappear.", "Master yourself, master the enemy.", "I think I broke a nail, good thing it wasn't mine.", "Oh hello bird... what little whisps have you-*sneezes*, oopsie.", "Is it cold in here, or is it just me?", "This is my happy face... see?", "Yup, that tasted purple.", "Well, a double rainbow is a phenomenon of optics that displays a spectrum of light due to the sun shining on droplets of moisture in the atmosphere. Does that explain it?", "Caught between a rock... and a hard place.", "*Burps* I think a Voidling just came out!", "I love all my saplings, especially how they taste.", "The key to immortality? Not dying.", "How do you like my guns... Shock, and Awe!", "Destiny. Domination. Deceit.", "I am your darkness, I am your truth.", "Sometimes you're the catch. Sometimes you're the bait.", "Who let the dogs out? Woof. Woof. Woof.", "You are in the deep end now!", "This place tastes like many emotions. Excitement, anger, joy and... salty? Is salty a feeling?", "Did I mention it's mating season?", "Weather forecast for tonight: dark, with a chance of pain!", "Knock knock. *Willump noises* A Frostguard! *Willump noises* W- Willump! You're not supposed smash him!", "The worth of a man can be measured by the length of his beard, and the girth of his belt buckle.", "I know what makes them tick. I know how to make the ticking stop.", "A day away from my forge is a day wasted.", "We cry out to the heavens... and they answer in wing and flame.", "I'm no hero - just a Yordle with a hammer", "Sink 'em all.", "Those who are 16-bit will soon grovel at the feet of the superior 32-bit.", "Justice takes wing.", "Xayah? Xayah? Crap. What was I supposed to do?", "Alright.", "*growl*", "This 'little girl' is about to crush some heads", "What? Do I have someone in my teeth?", "So much bloodshed... This is my kind of place!", "I knew I should have sprung for the blade warranty.", "Oops, forgot the clutch.", "What? You want to see a magic trick? Fine... tada.", "Ugh. I missed a freakin' cliff-diving trip for this crap?", "Who wants a treat? Bristle wants a treat? Not until we've trampled our foes to dust!", "So this is the terror that waddles in the night. Huh.", "I sing to help them find themselves. The stage just makes it easier.", "", "For my next trick, I'll make you disappear!", "If light travels so fast, how come it's never caught a ninja?", "", "Never underestimate the power of the scout's code!"]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    msg = message.content
    lowerMsg = msg.lower()

    if msg.startswith('$hello'):
      await message.channel.send('Hello!')
    
    
    if any(word in lowerMsg for word in champs):
      if not(msg.startswith('--blurb')):
        wordIndex = 0
        champLeft = True
        msg = msg.lower()
        msgList = msg.split(" ")
        for word in msgList:
          champIndex = 0
          for champ in champs:
            if word == champ:
              if not(any(word in msgList[wordIndex: len(msgList)] for word in champs)):
                champLeft = False
              await message.channel.send(champ.capitalize() + ": " + quotes[champIndex])
              if not(champLeft):
                break 
            champIndex += 1
          if not(champLeft):
            break
          wordIndex += 1


    if msg.startswith('--mh'): 
      name = msg[5:]

      (summonerId, accountId) = await getSummonerId(name)
      
      matchListDto = await getRecentMatches(accountId)
    
    

    #keys: 
    #['gameId', 'platformId', 'gameCreation', 'gameDuration', 'queueId', 'mapId', 'seasonId', 'gameVersion', 'gameMode', 'gameType', 'teams', 'participants', 'participantIdentities']
    
      print("Game ID: " + str(matchListDto[0]['gameId']))
      print("\nPlatform ID: " + str(matchListDto[0]['platformId']))
      print("\nGame Creation: " + str(matchListDto[0]['gameCreation']))
      print("\nGame Duration: " + str(matchListDto[0]['gameDuration']))
      print("\nQueue ID: " + str(matchListDto[0]['queueId']))
      print("\nMap ID: " + str(matchListDto[0]['mapId']))
      print("\nSeason ID: " + str(matchListDto[0]['seasonId']))
      print("\nGame Version: " + str(matchListDto[0]['gameVersion']))
      print("\nGame Mode: " + str(matchListDto[0]['gameMode']))
      print("\nGame Type: " + str(matchListDto[0]['gameType']))
      print("\nTeams: " + str(matchListDto[0]['teams']))
      print("\nParticipants: " + str(matchListDto[0]['participants']))
      print("\nParticipant Identities: " + str(matchListDto[0]['participantIdentities']))
      print(type(matchListDto[0]['participantIdentities'][0]))
      summonerName = ''
      participantId = 0
      championId = 0
      for summoner in matchListDto[0]['participantIdentities']:
        print(summoner['player']['summonerName'].lower())
        print(name.lower())
        if summoner['player']['summonerName'].lower() == name.lower():
          print(name.lower())
          summonerName = summoner['player']['summonerName']
          participantId = summoner['participantId']

      for summoner in matchListDto[0]['participants']:
        if summoner['participantId'] == participantId:
          championId = summoner['championId']


      await message.channel.send(summonerName + " has played " + matchListDto[0]['gameMode'] + " while playing " + str(championId))

    if msg.startswith('--blurb'):
      champName = msg[8:]
      try: 
        await message.channel.send(json['data'][champName.capitalize()]['blurb'])
      except Exception:
        await message.channel.send("Enter a League of Legends champion!")
      
client.run(os.getenv('TOKEN'))