import discord
import os
from pantheon import pantheon
import asyncio
import json
import random

client = discord.Client()
server = "na1"

champJson = json.loads(open('champion.json').read())
summonerJson = json.loads(open('summoner.json').read())
champsQuotesJson = json.loads(open('champsQuotes.json').read())

def requestsLog(url, status, headers):
    print(url)
    print(status)
    print(headers)

panth = pantheon.Pantheon(server, os.getenv('API_KEY'), errorHandling=True, requestsLoggingFunction=requestsLog, debug=True)

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

#list of champions
champs = champsQuotesJson["champs"]

#list of champion quotes lined up with champion
quotes = champsQuotesJson["quotes"]

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


      except Exception:
        await message.channel.send("Enter a  valid summoner name on the NA server")

    #get the blurb of the champion
    if msg.startswith('--blurb'):
      champName = msg[8:]
      if champName != 'random':
        try: 
          await message.channel.send(champJson['data'][champName.capitalize()]['blurb'])
        except Exception:
          await message.channel.send("Enter a League of Legends champion!")
      else:
        champName = champs[random.randrange(0, len(champs) - 1)]
        try: 
          await message.channel.send(champJson['data'][champName.capitalize()]['blurb'])
        except Exception:
          await message.channel.send("Enter a League of Legends champion!")
      

    #get title of champion
    if msg.startswith('--title'):
      champName = msg[8:]
      if champName == 'random':
        champName = champs[random.randrange(0, len(champs) -1)]
      splitChamp = champName.split(" ")
      if len(splitChamp) == 2 or len(splitChamp) == 3:
        if (splitChamp[0] == "dr" and splitChamp[1] == "mundo"):
            champName = "Dr Mundo"
              
        if (splitChamp[0] == "aurelion" and splitChamp[1] == "sol"):
          champName = "Aurelion Sol"
        
        if (splitChamp[0] == "jarvan" and splitChamp[1] == "iv"):
          champName = "Jarvan IV"
        
        if (splitChamp[0] == "master" and splitChamp[1] == "yi"):
          champName = "Master Yi"
        
        if (splitChamp[0] == "miss" and splitChamp[1] == "fortune"):
          champName = "Miss Fortune"
        
        if (splitChamp[0] == "nunu" and splitChamp[1] == "and" and splitChamp[2] == "willump"):
          champName = "Nunu"
        
        if (splitChamp[0] == "tahm" and splitChamp[1] == "kench"):
          champName = "Tahm Kench"
        
        if (splitChamp[0] == "twisted" and splitChamp[1] == "fate"):
          champName = "Twisted Fate"
        
        if (splitChamp[0] == "xin" and splitChamp[1] == "zhao"):
          champName = "Xin Zhao"

        if (splitChamp[0] == "lee" and splitChamp[1] == "sin"):
          champName = "Lee Sin"

      
      try: 
        champName = champName.replace("'", "")
        champName = champName.title()
        champName = champName.replace(" ", "")
        
        print(champName)
        await message.channel.send(champJson['data'][champName]['title'].title())
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
      except Exception:
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
      await message.channel.send("All Commands\n--mrg [player_name]: gives information about most recent game from a specified summoner\n--summoner [spell_name]: gives information about a specified summoner spell\n--blurb [champion_name]: gives the official blurb about specified champion\n--title [champion_name]: gives the official title of specified champion\n--quotes [on/off/status]: turns quotes on, off, or gives the status of the quotes\n--image [champion_name]: uploads an image of the specified champion\n--cm [player_name] [champion_name]: shows specified summoner's mastery level and mastery points on specified champion\n--title random, --blurb random, or --image random gives a random title, blurb, or image")

    #post image of champion
    if msg.startswith('--image'):
      champName = msg[8:].lower()
      if champName != 'random':
        champName = champName.replace(" ", "")
        champName = champName.replace("'", "")
        champName = champName.capitalize()
        try:
          await message.channel.send(file=discord.File("championImages/" + champName + '.png'))
        except Exception:
          await message.channel.send("Enter a League of Legends champion")

    if msg.startswith('--forjonathan'):
      await message.channel.send(file=discord.File('tenor.gif'))

    if msg.startswith('--swag'):
      await message.channel.send(file=discord.File('Swag.jpg'))

    if msg.startswith('--200years'):
      await message.channel.send(file=discord.File('championImages/Aphelios.png'))

    if msg.startswith('--cancer'):
      await message.channel.send(file=discord.File('championImages/teemo.gif'))
    
    if msg.startswith('--scouts code'):
      await message.channel.send("https://www.youtube.com/watch?v=KDIAGsCOWD8")

    if msg.startswith('--image random'):
      try:
        champName = champs[random.randrange(0, len(champs))]
        champName = champName.replace(" ", "")
        champName = champName.replace("'", "")
        champName = champName.capitalize()
        await message.channel.send(file=discord.File("championImages/" + champName + '.png'))
      except Exception:
        await message.channel.send("Enter a League of Legends champion")


client.run(os.getenv('TOKEN'))
