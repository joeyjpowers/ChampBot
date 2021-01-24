import discord
import os
from pantheon import pantheon
import asyncio
import json
import config


client = discord.Client()
server = "na1"

champJson = json.loads(open('champion.json').read())
summonerJson = json.loads(open('summoner.json').read())

def requestsLog(url, status, headers):
    print(url)
    print(status)
    print(headers)

panth = pantheon.Pantheon(server, config.api_key, errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)

champQuotes = True

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





champs = ["aatrox", "ahri", "akali", "alistar", "amumu", "anivia", "annie", "aphelios", "ashe", "aurelion sol", "azir", "bard", "blitzcrank", "brand", "braum", "caitlyn", "camille", "cassiopeia", "cho'gath", "corki", "darius", "diana", "dr mundo", "draven", "ekko", "elise", "evelynn", "ezreal", "fiddlesticks", "fiora", "fizz", "galio", "gangplank", "garen", "gnar", "gragas", "graves", "hecarim", "heimerdinger", "illaoi", "irelia", "ivern", "janna", "jarvan iv", "jax", "jayce", "jhin", "jinx", "kai'sa", "kalista", "karma", "karthus", "kassadin", "katarina", "kayle", "kayn", "kennen", "kha'zix", "kindred", "kled", "kog'maw", "leblanc", "lee sin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux", "malphite", "malzahar", "maokai", "master yi", "miss fortune", "mordekaiser", "morgana", "nami", "nasus", "nautilus", "neeko", "nidalee", "nocturne", "nunu and willump", "olaf", "orianna", "orrn", "pantheon", "poppy", "pyke", "qiyana", "quinn", "rakan", "rammus", "rek'sai", "rell", "renekton", "rengar", "riven", "rumble", "Rrze", "samira", "sejuani", "senna", "seraphine", "sett", "shaco", "shen", "shyvana", "singed", "sion", "sivir", "skarner", "sona", "soraka", "swain", "sylas", "syndra", "tahm kench", "taliyah", "talon", "taric", "teemo", "thresh", "tristana", "trundle", "tryndamere", "twisted fate", "twitch", "udyr", "urgot", "varus", "vayne", "veigar", "vel'koz", "vi", "viego", "viktor", "vladimir", "volibear", "warwick", "wukong", "xayah", "xerath", "xin zhao", "yasuo", "yone", "yorick", "yuumi" "zac", "zed", "ziggs", "zilean", "zoe", "zyra"]

quotes = ["So uh, I'm Aatrox. I'm a transcendental being trapped inside cutlery... What's your deal?", "If you'd like to play with me, you'd better be sure you know the game.", "So many noobs, will matchmaking ever find true balance?", "You can't milk those!", "I thought you'd never pick me", "The chicken or the egg? Actually, I came first.", "Ashes, ashes, they all fall down.", "Being good at playing a certain character in a video game is valuable, but I think I'll take the 200+ collective years of professional game design experience.", "How do you like the curves? I was talking about the bow.", "I used to wander the stars. Now I'm stuck down here, with you.", "There is only Shurima. All else is but a mirage.", "*Chime noises*", "The time of man has come to an end.", "I'm on a short fuse.", "You are safe with Braum.", "Wanna see a hat trick?", "Technology and I have a... complicated relationship.", "There is no antidote for me.", "You are such… hideous creatures!", "That just goes to show you you're nothin' but a Whiskey Delta!", "I do not tolerate cowardice.", "They called me a heretic, now they are dead.", "Mundo think you a big sissy! *laughs*", "WELCOME TO THE LEAGUE OF DRAVEN!", "Never had luck. Never needed it.", "I know what lurks in the shadows.", "You know you want me.", "You belong in a museum!", "Come closer. Closer...", "Precision and grace.", "Wanna see a trick?", "I didn't choose to come to life, but I definitely prefer it.", "They took my ship - I'll take their lives", "DEMACIA!!!!", "Gnar gada!", "Don't get pushy!", "Dead man walkin'.", "War is eternal.", "Ah, the sweet smell of science!", "I'm not big on sermons - broken bones teach better lessons.", "Contrary to what you've heard, I have a great sense of humor.", "No-one who wanders is every truly lost.", "Yes, it's true. For only $2.95 a minute, I will leave you breathless.", "For my father, the king.", "Imagine if I had a real weapon!", "Bring down the hammer.", "In carnage, I bloom, like a flower in the dawn.", "Stay still! I'm trying to shoot you!", "Are you the hunter... or the prey?", "Death to all betrayers.", "You know what they say: Karma always catches up to you.", "Do you have a moment to talk about death?", "I tried to silence my mother once. Boy, did I regret that.", "If you run, you won't see me stab you!", "Evil fears only fire! And Yordles, because, what even ARE they?", "I smell death... no, it's you. You smell... bad.", "Yes, they make shurikens this small!", "I ate an optimist once, but I couldn't keep him down.", " Lamb: I'm hungry, I'm hungry, I'm bored, chase chase chase! \nWolf: You get it now!", "I got a joke too! It's called me kicking your teeth in!", "Time to feast!", "For my next trick I'll make their life bar disappear.", "Master yourself, master the enemy.", "I think I broke a nail, good thing it wasn't mine.", "Oh hello bird... what little whisps have you-*sneezes*, oopsie.", "Is it cold in here, or is it just me?", "This is my happy face... see?", "Yup, that tasted purple.", "Well, a double rainbow is a phenomenon of optics that displays a spectrum of light due to the sun shining on droplets of moisture in the atmosphere. Does that explain it?", "Caught between a rock... and a hard place.", "*Burps* I think a Voidling just came out!", "I love all my saplings, especially how they taste.", "The key to immortality? Not dying.", "How do you like my guns... Shock, and Awe!", "Destiny. Domination. Deceit.", "I am your darkness, I am your truth.", "Sometimes you're the catch. Sometimes you're the bait.", "Who let the dogs out? Woof. Woof. Woof.", "You are in the deep end now!", "This place tastes like many emotions. Excitement, anger, joy and... salty? Is salty a feeling?", "Did I mention it's mating season?", "Weather forecast for tonight: dark, with a chance of pain!", "Knock knock. *Willump noises* A Frostguard! *Willump noises* W- Willump! You're not supposed smash him!", "The worth of a man can be measured by the length of his beard, and the girth of his belt buckle.", "I know what makes them tick. I know how to make the ticking stop.", "A day away from my forge is a day wasted.", "We cry out to the heavens... and they answer in wing and flame.", "I'm no hero - just a Yordle with a hammer", "Sink 'em all.", "Those who are 16-bit will soon grovel at the feet of the superior 32-bit.", "Justice takes wing.", "Xayah? Xayah? Crap. What was I supposed to do?", "Alright.", "*growl*", "This 'little girl' is about to crush some heads", "What? Do I have someone in my teeth?", "So much bloodshed... This is my kind of place!", "I knew I should have sprung for the blade warranty.", "Oops, forgot the clutch.", "What? You want to see a magic trick? Fine... tada.", "Ugh. I missed a freakin' cliff-diving trip for this crap?", "Who wants a treat? Bristle wants a treat? Not until we've trampled our foes to dust!", "So this is the terror that waddles in the night. Huh.", "I sing to help them find themselves. The stage just makes it easier.", "Love you, Ma. See ya tomorrow. Mwah.", "For my next trick, I'll make you disappear!", "If light travels so fast, how come it's never caught a ninja?", "What do you get when a dragon sneezes? (chuckles) Out of the way.", "Shaken, not stirred.", "Your puny body is the only joke here.", "Cut purse? No. Cut throat? Yes.", "Eeaugh! Bugs are gross! Ugh!", "Just keep smiling and... Maybe they'll go away.", "Yes, that was a banana. *giggles* No one expects the banana.", "I have to know who has a crush on whom.", "You've traveled across the world to die for someone else's king? Pathetic!", "And they said I lacked balance. Ha!", "The baseness of your appetite repulses me!", "Huh. I guess that's funny where you come from.", "Ugh, I lost another blade. I wonder who it's in this time.", "I've been to the top of the mountain... and the bottom of the gutter. There's much to learn from both.", "Never underestimate the power of the scout's code!", "Screaming won't do you any good, but it's music to my ears.", "A cannonball is the best icebreaker!", "It's alright Clubbems, we'll get to smashing soon.", "My right arm is a lot stronger than my left arm!", "Never lost a fair game... or played one.", "All pipes lead to home.", "If PETA asks, this fur is fake.", "What exactly have I been killing.", "You'd like some real amusement? Come closer.", "Hitting me is like boxing with shadows.", "What's black and blue and is about to show you the definition of pain?!", "Bones are surprisingly inflexible.", "Punch first. Ask questions while punching.", "Humor was better a thousand years ago.", "My opponents need to be upgraded.", "Go ahead, be negative. You'll be just my type.", "You've gone soft, brother. Too much cake.", "Who's a good boy? I am!", "I bet I can hit their base from here!", "I can't wait to burst your bubble.", "Lightning bolt! Lightning bolt! Lightning bolt! Lightning bolt! Lightning bolt! Lightning bolt!", "Find me an immovable object, and I'll put this question to rest!", "There are three certainties in life: honor, death, and hangovers.", "Is that the taste of salt on the wind? Ah, hello brother.", "Ah, would you like some friends? Nope, can't have 'em.", "Zoooooom!", "I hate it when this happens.", "*Zed plays 'rock, paper, scissors' with his shadow. If he wins, his shadow bows and disappears. If he loses, he kills his shadow.*", "Let's blow this joint.", "Time flies like an arrow; fruit flies like banana.", "There are so many weirdos here... It's awesome!", "Our seasons are reversed: my spring, your fall."]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global champQuotes

    if message.author == client.user:
      return

    msg = message.content
    lowerMsg = msg.lower()

    if msg.startswith('$hello'):
      await message.channel.send('Hello!')
    
    if any(word in lowerMsg for word in champs):
      global champQuotes
      if champQuotes:
        if not(msg.startswith('--blurb')) and not(msg.startswith('--title')) and not (msg.startswith('--image')):
          wordIndex = 0
          champLeft = True
          msg = msg.lower()
          msgList = msg.split(" ")
          containsCM = False
          for word in msgList:
            champIndex = 0

            if (word == "dr" and msgList[wordIndex + 1] == "mundo"):
              word = "dr mundo"
            
            if (word == "aurelion" and msgList[wordIndex + 1] == "sol"):
              word = "aurelion sol"
            
            if (word == "jarvan" and msgList[wordIndex + 1] == "iv"):
              word = "jarvan iv"
            
            if (word == "master" and msgList[wordIndex + 1] == "yi"):
              word = "master yi"
            
            if (word == "miss" and msgList[wordIndex + 1] == "fortune"):
              word = "miss fortune"
            
            if (word == "nunu" and msgList[wordIndex + 1] == "and" and msgList[wordIndex + 2] == "willump"):
              word = "nunu and willump"
            
            if (word == "tahm" and msgList[wordIndex + 1] == "kench"):
              word = "tahm kench"
            
            if (word == "twisted" and msgList[wordIndex + 1] == "fate"):
              word = "twisted fate"
            
            if (word == "xin" and msgList[wordIndex + 1] == "zhao"):
              word = "xin zhao"

            if (word == "lee" and msgList[wordIndex + 1] == "sin"):
              word = "lee sin"

            if (word == "--cm"):
              containsCM = True

            for champ in champs:
              if word == champ:
                if not(any(word in msgList[wordIndex: len(msgList)] for word in champs)):
                  champLeft = False
                if not (containsCM):
                  await message.channel.send(champ.capitalize() + ": " + quotes[champIndex])
                else:
                  containsCM = False
                if not(champLeft):
                  break 
              champIndex += 1
          
            if not(champLeft):
              break
            wordIndex += 1

    
    #get most recent game
    if msg.startswith('--mrg'): 
      name = msg[6:]

      try:
        (summonerId, accountId) = await getSummonerId(name)
        
        matchListDto = await getRecentMatches(accountId)
      
        

      #keys: 
      #['gameId', 'platformId', 'gameCreation', 'gameDuration', 'queueId', 'mapId', 'seasonId', 'gameVersion', 'gameMode', 'gameType', 'teams', 'participants', 'participantIdentities']
      
        print("Game ID: " + str(matchListDto[0]['gameId']))
        print("\nPlatform ID: " + str(matchListDto[0]['platformId']))

        print("\nTeams" + str(matchListDto[0]['teams']))

        print("\nParticipants" + str(matchListDto[0]['participantIdentities']))

        print("\nParticipant Identities" + str(matchListDto[0]['participantIdentities']))
        summonerName = ''
        participantId = 0
        championId = 0
        kills = 0
        deaths = 0
        assists = 0
        cs = 0
        visionScore = 0
        win = True
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
            kills = summoner['stats']['kills']
            deaths = summoner['stats']['deaths']
            assists = summoner['stats']['assists']
            cs = summoner['stats']['totalMinionsKilled']
            visionScore = summoner['stats']['visionScore']

        championName = ''

        for champ in champJson['data']:
          if champJson['data'][champ]['key'] == str(championId):
            championName = champJson['data'][champ]['id']
        
        if 1 <= participantId and participantId <= 5:
          if matchListDto[0]['teams'][0]['win'] == 'Win':
            win = True
          else:
            win = False
        else:
          if matchListDto[0]['teams'][1]['win'] == 'Win':
            win = True
          else:
            win = False


        if not summonerName:
          await message.channel.send("Enter a valid valid summoner name on the NA server")
          return

        await message.channel.send(summonerName + " most recently played " + matchListDto[0]['gameMode'] + " as " + championName)
        
        if win:
          await message.channel.send(summonerName + " won the game and had a statline of " + str(kills) + "/" + str(deaths) + "/" + str(assists) + ". They had " + str(cs) + " CS and " + str(visionScore) + " vision score.")
        else:
          await message.channel.send(summonerName + " lost the game and had a statline of " + str(kills) + "/" + str(deaths) + "/" + str(assists) + ". They had " + str(cs) + " CS and " + str(visionScore) + " vision score.")


      except Exception as e:
        print(e)
        await message.channel.send("Enter a  valid summoner name on the NA server")

    #get the blurb of the champion
    if msg.startswith('--blurb'):
      champName = msg[8:]
      try: 
        await message.channel.send(champJson['data'][champName.capitalize()]['blurb'])
      except Exception:
        await message.channel.send("Enter a League of Legends champion!")

    #get title of champion
    if msg.startswith('--title'):
      champName = msg[8:]
      try: 
        await message.channel.send(champJson['data'][champName.capitalize()]['title'].title())
      except Exception:
        await message.channel.send("Enter a League of Legends champion!")
    
    #summoner spell information
    if msg.startswith('--summoner'):
      summonerName = msg[11:]
      try: 
        summonerId = "Summoner" + summonerName.title()
        summonerName = summonerJson['data'][summonerId]['name'].title()
        cooldown = summonerJson['data'][summonerId]['cooldown'][0]
        description = summonerJson['data']["Summoner" + summonerName.title()]['description'].title()
        await message.channel.send("Name: " + summonerName + "\nDescription: " + description +"\nCooldown: " + str(cooldown) + " seconds")
      except Exception as e:
        await message.channel.send("Enter a summoner spell!")

    #turn quotes on or off 
    if msg.startswith('--quotes'):
      choice = msg[9:]
      if choice == 'off':
        champQuotes = False
        await message.channel.send("Quotes turned off")
      elif choice == 'on':
        champQuotes = True
        await message.channel.send("Quotes turned on")
      elif choice == 'status':
        if champQuotes:
          await message.channel.send("Quotes are currently turned on")
        else:
          await message.channel.send("Quotes are currently turned off")
      else:
        await message.channel.send("\"--quotes on\": Turns champion quotes on\n\"--quotes off\": Turns champion quotes off\n\"--quotes status:\": Check whether champion quotes are turned on or off")

    #get champion mastery
    if msg.startswith('--cm'):
      summonerChampName = msg[5:]
      summonerChampName.replace(".", "")
      summonerChampName.replace("'", "")
      names = summonerChampName.split(" ")
      if len(names) < 2 or len(names) > 3:
        await message.channel.send("Enter a summoner name and champion name")
        return
      
      #['championId', 'championLevel', 'championPoints', 'lastPlayTime', 'championPointsSinceLastLevel', 'championPointsUntilNextLevel', 'chestGranted', 'tokensEarned', 'summonerId']

     
      
      summonerName = names[0]
      championName = names[1].capitalize()
      championNameDisplay = championName
      if (len(names) == 3):
        championName += names[2].capitalize()
        championNameDisplay += " " + names[2].capitalize()
      try:
        (summonerId, accountId) = await getSummonerId(summonerName)
        championId = champJson['data'][championName]['key']
        champMastery = await panth.getChampionMasteriesByChampionId(summonerId, championId)
        
        
        champLevel = champMastery['championLevel']
        champPoints = champMastery['championPoints']
        
        

        await message.channel.send(summonerName + " is level " + str(champLevel) + " on " + str(championNameDisplay) + " and has " + str(champPoints) + " champion points")
      
      except Exception:
        await message.channel.send("Either " + summonerName + " has not played " + championNameDisplay + " or " + championNameDisplay + " is not a League of Legends Champion")
        
      else:
        summonerName = names[0]
    
    #help menu
    if msg.startswith('--help'):
      await message.channel.send("All Commands\n--mrg [player_name]: gives information about most recent game from a specified summoner\n--summoner [spell_name]: gives information about a specified summoner spell\n--blurb [champion_name]: gives the official blurb about specified champion\n--title [champion_name]: gives the official title of specified champion\n--quotes [on/off/status]: turns quotes on, off, or gives the status of the quotes\n--image [champion_name]: uploads an image of the specified champion\n--cm [player_name] [champion_name]: shows specified summoner's mastery level and mastery points on specified champion")

    #post image of champion
    if msg.startswith('--image'):
      champName = msg[8:].lower()
      
      
      champName = champName.replace(" ", "")
      champName = champName.replace("'", "")
      champName = champName.capitalize()
      try:
        await message.channel.send(file=discord.File("championImages/" + champName + '.png'))
      except Exception:
        await message.channel.send("Enter a League of Legends champion")

    if msg.startswith('--forjonathan'):
      await message.channel.send(file=discord.File('tenor.gif'))

client.run(os.getenv('TOKEN'))