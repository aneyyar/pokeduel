
import discord
from discord.ext import commands
import requests
from io import BytesIO
client = commands.Bot(command_prefix = '.')
import pickledb
import sqlite3
import random
import time
in_duel = [1]
pokemons={'https://cdn.discordapp.com/attachments/725671584005619725/733951073366048789/pokemon.png':'mewtwo'}
z = []
colors = [0x9400D3, 0x4B0082, 0x0000FF, 0x00FF00, 0xFFFF00, 0xFF7F00, 0xFF0000]
db = sqlite3.connect('pokemonstats.db')
cur = db.cursor()

q = ''

@client.event
async def on_ready():
    print("im ready")
@client.command()
async def dex(ctx,arg):
    cur.execute("SELECT field4, field5, field6, field7, field8, field9, field10, field11 FROM Pokemonstats WHERE field3 = ?; ",(arg,))
    rows = cur.fetchall()
    for row in rows:
        embed = discord.Embed(
          title=arg.capitalize(),
          description="\n**TYPE: ** "+str(row[6])+"**\nHP: **"+str(row[0])+"**\nATK: **"+str(row[1])+"**\nDEF: **"+str(row[2])+"**\nSPATK: **"+str(row[2])+"**\nSPDEF: **"+str(row[4])+"**\nSPEED: **"+str(row[5]),
          color=discord.Color(random.choice(colors))
        )
        embed.set_image(url = "https://projectpokemon.org/images/normal-sprite/"+arg+".gif")
        await ctx.send(embed=embed)
@client.command()
async def moveinfo(ctx,*,args):       
  cur.execute("SELECT field20, field21, field24, field25 FROM Pokemonstats WHERE field19 = ?; ",(str(args),))
  
  rows = cur.fetchall()
  mv = discord.Embed(
    title =args.capitalize(),
    
    color=discord.Color(random.choice(colors))
  )
  if not rows:
    return
  print(rows)
  for row in rows:
      mv.add_field(name='Type ', value=row[0], inline=False)
      mv.add_field(name='Category ', value=row[1], inline=False)
      mv.add_field(name = '\nPower ', value = row[2], inline=False)
      mv.add_field(name = 'Accuracy ', value = row[2], inline=False)
  await ctx.send(embed = mv)
@client.command()
async def select(ctx, arg):
  cur.execute("SELECT field2, field3, field4, field5 FROM userdata WHERE field1 = ?; ",(ctx.author.id,))
  rows = cur.fetchone()
  
  if not rows:
    cur.execute("INSERT INTO userdata (field1, field2, field3, field4) VALUES(?,?,?,?)",(str(ctx.author.id),arg,"tackle, tackle, tackle, tackle","adamant"))
    db.commit()
    await ctx.send(arg+" has been selected!")
    print(db.total_changes)

  else:
    cur.execute("Update userdata set field2 = ?, field3 = ?, field4 = ? WHERE field1 = ?",(arg,"tackle, tackle, tackle, tackle","adamant",str(ctx.author.id)))
    db.commit()
    await ctx.send(arg+" has been selected!")
    print(db.total_changes)
  
   
@client.command()   
async def info(ctx):
  cur.execute("SELECT field2, field3, field4 FROM userdata WHERE field1 = ?; ",(str(ctx.author.id),))
  row = cur.fetchone() 
  print(ctx.author.id)
  
  if not row:
    await ctx.send("you havent selected a pokemon yet")
    return
  
  
  name = row[0]
  print(row)
  cur.execute("SELECT field4, field5, field6, field7, field8, field9, field10, field11 FROM Pokemonstats WHERE field3 = ?; ",(name,))
  pokemon = cur.fetchone()
  
  hpstat = ((((float(pokemon[0])*2)+31)*100)/100)+100+10
  atkstat = ((((float(pokemon[1])*2)+31)*100)/100)+5
  defstat = ((((float(pokemon[2])*2)+31)*100)/100)+5
  spatkstat = ((((float(pokemon[3])*2)+31)*100)/100)+5
  spdefstat = ((((float(pokemon[4])*2)+31)*100)/100)+5
  speedstat = ((((float(pokemon[5])*2)+31)*100)/100)+5
  user = pokemon
  if row[2] == "adamant":
    atkstat = int(float(atkstat*1.1))
    spatkstat = int(float(spatkstat*0.9))
  if row[2] == "lonely": 
    atkstat = int(float(atkstat*1.1))
    defstat = int(float(defstat*0.9))
  if row[2] == "brave":
    atkstat = int(float(atkstat*1.1))
    speedstat = int(float(speedstat*0.9))
  if row[2] == "naughty":
    atkstat = int(float(atkstat*1.1))
    spdefstat = int(float(spdefstat*0.9))
  if row[2] == "bold":
    defstat = int(float(defstat*1.1))
    atkstat = int(float(atkstat*0.9))
  if row[2] == "relaxed":
    defstat = int(float(defstat*1.1))
    speedstat = int(float(speedstat*0.9))
  if row[2] == "impish":  
    defstat = int(float(defstat*1.1))
    spatkstat = int(float(spatkstat*0.9))
  if row[2] == "lax": 
    defstat = int(float(defstat*1.1))  
    spdefstat = int(float(spdefstat*0.9))  
  if row[2] == "timid":      
    speedstat = int(float(speedstat*1.1))
    atkstat = int(float(atkstat*0.9))
  if row[2] == "hasty":      
    speedstat = int(float(speedstat*1.1)) 
    defstat = int(float(defstat*0.9)) 
  if row[2] == "jolly":      
    speedstat = int(float(speedstat*1.1))   
    spatkstat = int(float(spatkstat*0.9))
  if row[2] == "naive":      
    speedstat = int(float(speedstat*1.1))  
    spdefstat = int(float(spdefstat*0.9)) 
  if row[2] == "modest": 
    spatkstat = int(float(spatkstat*1.1))   
    atkstat = int(float(atkstat*0.9))    
  if row[2] == "mild": 
    spatkstat = int(float(spatkstat*1.1)) 
    defstat = int(float(defstat*0.9)) 
  if row[2] == "quiet": 
    spatkstat = int(float(spatkstat*1.1))   
    speedstat = int(float(speedstat*0.9))
  if row[2] == "rash": 
    spatkstat = int(float(spatkstat*1.1)) 
    spdefstat = int(float(spdefstat*0.9))
  if row[2] == "calm":  
    spdefstat = int(float(spdefstat*1.1))  
    atkstat = int(float(atkstat*0.9))
  if row[2] == "gentle":  
    spdefstat = int(float(spdefstat*1.1))  
    defstat = int(float(defstat*0.9)) 
  if row[2] == "sassy":  
    spdefstat = int(float(spdefstat*1.1))
    speedstat = int(float(speedstat*0.9))
  if row[2] == "sassy":  
    spdefstat = int(float(spdefstat*1.1))      
    spatkstat = int(float(spatkstat*0.9))
  embed = discord.Embed(
    title="Level 100 "+name.capitalize(),
    description="**Nature:** "+row[2].capitalize()+"\n**TYPE: ** "+str(pokemon[6])+"**\nHP: **"+str(hpstat)+"**\nATK: **"+str(atkstat)+"**\nDEF: **"+str(defstat)+"**\nSPATK: **"+str(spatkstat)+"**\nSPDEF: **"+str(spdefstat)+"**\nSPEED: **"+str(speedstat),
    color=discord.Color(random.choice(colors))
  )
  embed.set_image(url = "https://projectpokemon.org/images/normal-sprite/"+name+".gif")  
  await ctx.send(embed = embed)
@client.command()
async def test(ctx):
  data = ['sampletext',42]

  cur.execute("CREATE TABLE IF NOT EXISTS t1(link TEXT,story_id INTEGER)")
  cur.execute("INSERT INTO t1 (link, story_id) VALUES (?,?)", data)

  db.commit()
@client.command()
async def moves(ctx):
  cur.execute("SELECT field2, field3, field4, field5 FROM userdata WHERE field1 = ?; ",(ctx.author.id,))
  row = cur.fetchone()
  if not row:
    await ctx.send("you havent selected a pokemon yet")
    return
  mvs = row[1].split(", ")  
  name = row[0]
  string = ""
  
  string2 = ""
  cur.execute("SELECT field12 FROM Pokemonstats WHERE field3 = ?; ",(name,))
  pokemon = cur.fetchone()
  learnset = pokemon[0].split(", ")
  for i in mvs:
    string = string+"\n"+i
  for i in learnset:
    string2 = string2+"\n"+i
  
  embed = discord.Embed(
    title ="Moves for "+name,
    description = string +"\n\n**Available Moves**\n```"+string2+"```",
    color=discord.Color(random.choice(colors))
  )
  embed.set_footer(text="do .learn <move1>, <move2>, <move3>, <move4> to learn new moves")
  await ctx.send(embed = embed)

@client.command()
async def learn(ctx,*,args):
  cur.execute("SELECT field2, field3, field4, field5 FROM userdata WHERE field1 = ?; ",(ctx.author.id,))
  row = cur.fetchone()
  name = row[0]
  mvset = args.split(", ")
  cur.execute("SELECT field12 FROM Pokemonstats WHERE field3 = ?; ",(name,))
  pokemon = cur.fetchone()
  learnset = pokemon[0].split(", ")
  print(learnset)
  if len(mvset) != 4:
    await ctx.send("please enter four moves to learn in the format: move1, move2, move3, move4")
    return
  for i in mvset:
    if i.lower() not in str(learnset):
      await ctx.send(name +" cant learn "+i)
      return
  cur.execute("Update userdata set field3 = ? WHERE field1 = ?",(args,str(ctx.author.id)))
  db.commit()    
  await ctx.send("moveset updated")

@client.command()
async def ping(ctx):
   """ Pong! """
   before = time.monotonic()
   message = await ctx.send("Pong! API response time: `" +str(round(client.latency*1000,2))+"ms`.")
   ping = (time.monotonic() - before) * 1000
   await message.edit(content=f"Pong! API response time: `" +str(round(client.latency*1000,2))+"ms`. Sending response time: `"+str(int(ping))+"ms`") 
@client.command()
async def duel(ctx,user:discord.Member):
  cur.execute("SELECT field2, field3, field4 FROM userdata WHERE field1 = ?; ",(ctx.author.id,))
  author = cur.fetchone()
  cur.execute("SELECT field2, field3, field4 FROM userdata WHERE field1 = ?; ",(user.id,))
  member = cur.fetchone()
  if not author:
    await ctx.send("you havent selected a pokemon yet")
    return
  elif not member:
    await ctx.send("the person you are challenging hasnt selected a pokemon yet")
    return
  elif user.id == ctx.author.id:
    await ctx.send("you cannot challenge yourself")
    return  
  await ctx.send(ctx.author.mention+" challenges you to a duel, "+user.mention+" type .accept to accept the duel")
  def check(author, message):
      return message.author == author  
  timeout = 10
  timeout_start = time.time()
  type = {
    'water':{
      'fire':0.5,'electric':2.0,'grass':2.0,'steel':0.5,'water':0.5,'normal':1,'poison':1,'fighting':1,'dragon':1,'rock':1,'ghost':1,'bug':1,'flying':1,'dark':1,'ground':1,'psychic':1,'fairy':1,'ice':0.5
      },
    'fire':{
      'water':2.0,'rock':2.0,'ground':2.0,'bug':0.5,'steel':0.5,'fire':0.5,'grass':0.5,'fairy':0.5,'ice':0.5,'normal':1,'poison':1,'electric':1,'fighting':1,'dragon':1,'ghost':1,'flying':1,'dark':1,'psychic':1
      },
    'grass':{
      'water':0.5,'ground':0.5,'grass':0.5,'electric':0.5,'fire':2.0,'flying':2.0,'poison':2.0,'bug':2.0,'ice':2.0,'normal':1,'steel':1,'fighting':1,'dragon':1,'rock':1,'ghost':1,'dark':1,'psychic':1,'fairy':1
      },
    'electric':{
      'flying':0.5,'steel':0.5,'electric':0.5,'ground':2,'normal':1,'poison':1,'ice':1,'fighting':1,'dragon':1,'water':1,'rock':1,'ghost':1,'bug':1,'grass':1,'dark':1,'fire':1,'psychic':1,'fairy':1
    },
    'psychic':{
      'fighting':0.5,'psychic':0.5,'':0.5,'bug':2.0,'ghost':2.0,'dark':2.0,'normal':1,'steel':1,'poison':1,'electric':1,'ice':1,'dragon':1,'water':1,'rock':1,'grass':1,'flying':1,'fire':1,'ground':1,'fairy':1
      },
    'ice':{
      'fighting':2.0,'steel':2.0,'rock':2.0,'fire':2.0,'ice':0.5,'normal':1,'poison':1,'electric':1,'dragon':1,'water':1,'ghost':1,'bug':1,'grass':1,'flying':1,'dark':1,'ground':1,'psychic':1,'fairy':1
      },
    'dragon':{
      'fire':0.5,'water':0.5,'grass':0.5,'electric':0.5,'ice':2.0,'dragon':2.0,'fairy':2.0,'normal':1,'steel':1,'poison':1,'fighting':1,'rock':1,'ghost':1,'bug':1,'flying':1,'dark':1,'ground':1,'psychic':1
    },
    'fairy':{
      'dragon':0,'steel':2.0,'fighting':0.5,'bug':0.5,'poison':2.0,'dark':0.5,'normal':1,'electric':1,'ice':1,'water':1,'rock':1,'ghost':1,'grass':1,'flying':1,'fire':1,'ground':1,'psychic':1,'fairy':1
      },
    'dark':{
      'fighting':2.0,'psychic':0,'bug':2.0,'ghost':0.5,'fairy':2.0,'normal':1,'steel':1,'poison':1,'electric':1,'ice':1,'water':1,'rock':1,'grass':1,'flying':1,'fire':1,'ground':1,'dragon':1
      },
    'normal':{
      'fighting':2.0,'ghost':0,'normal':1,'steel':1,'poison':1,'electric':1,'ice':1,'dragon':1,'water':1,'rock':1,'bug':1,'grass':1,'flying':1,'dark':1,'fire':1,'ground':1,'psychic':1,'fairy':1
      },
    'fighting':{
      'flying':2.0,'bug':0.5,'rock':0.5,'dark':0.5,'psychic':2.0,'fairy':2.0,'normal':1,'steel':1,'poison':1,'electric':1,'ice':1,'fighting':1,'dragon':1,'water':1,'ghost':1,'grass':1,'fire':1,'ground':1
      },
    'flying':{
      'rock':2.0,'ground':0,'grass':0.5,'bug':0.5,'fighting':0.5,'electric':2.0,'ice':2.0,'normal':1,'steel':1,'poison':1,'dragon':1,'water':1,'ghost':1,'flying':1,'dark':1,'fire':1,'psychic':1,'fairy':1
      },
    'poison':{
      'fighting':0.5,'poison':0.5,'ground':2.0,'psychic':2.0,'grass':0.5,'bug':0.5,'fairy':0.5,'fire': 1,'normal':1,'steel':1,'electric':1,'ice':1,'dragon':1,'water':1,'rock':1,'ghost':1,'flying':1,'dark':1,'fire':1
      },
    'ground':{
      'ice':2.0,'poison':0.5,'rock':0.5,'electric':0,'grass':2.0,'water':2.0,'normal':1,'steel':1,'fighting':1,'dragon':1,'ghost':1,'bug':1,'flying':1,'dark':1,'fire':1,'ground':1,'psychic':1,'fairy':1
      },
    'rock':{
      'steel':2.0,'fighting':2.0,'ground':2.0,'grass':2.0,'water':2.0,'normal':0.5,'flying':0.5,'poison':0.5,'fire':0.5,'electric':1,'ice':1,'dragon':1,'rock':1,'ghost':1,'bug':1,'dark':1,'psychic':1,'fairy':1
      },
    'bug':{
      'fire':2.0,'rock':2.0,'fighting':0.5,'ground':0.5,'flying':2.0,'grass':0.5,'normal':1,'steel':1,'poison':1,'electric':1,'ice':1,'dragon':1,'water':1,'ghost':1,'bug':1,'dark':1,'psychic':1,'fairy':1
      },
    'ghost':{
      'normal':0,'fighting':0,'ghost':2.0,'dark':2.0,'bug':0.5,'poison':0.5,'steel':1,'electric':1,'ice':1,'dragon':1,'water':1,'rock':1,'grass':1,'flying':1,'ground':1,'psychic':1,'fairy':1
      },
    'steel':{'normal':0.5,'fighting':2.0,'poison':0.5,'flying':0.5,'ground':2.0,'rock':0.5,'bug':0.5,'steel':0.5,'fire':2.0,'grass':0.5,'psychic':0.5,'ice':0.5,'dragon':0.5,'fairy':0.5,'electric':1,'water':1,'ghost':1,'dark':1}
  }  
  
  while time.time() < timeout_start + timeout:
    response = await client.wait_for('message', check = lambda message: message.author == user, timeout=300) 
    if(response.content == ".accept"):
      in_duel.append(ctx.author.id)
      in_duel.append(user.id)
      
      await ctx.send("duel accepted")
      name = author[0]
      cur.execute("SELECT field4, field5, field6, field7, field8, field9, field10, field11 FROM Pokemonstats WHERE field3 = ?; ",(name,))
      pokemon = cur.fetchone()
              
      
      hpstat = ((((float(pokemon[0])*2)+31)*100)/100)+100+10
      atkstat = ((((float(pokemon[1])*2)+31)*100)/100)+5
      defstat = ((((float(pokemon[2])*2)+31)*100)/100)+5
      spatkstat = ((((float(pokemon[3])*2)+31)*100)/100)+5
      spdefstat = ((((float(pokemon[4])*2)+31)*100)/100)+5
      speedstat = ((((float(pokemon[5])*2)+31)*100)/100)+5
      
      
      #await ctx.send(embed = duel)
      name2 = member[0]
      cur.execute("SELECT field4, field5, field6, field7, field8, field9, field10, field11 FROM Pokemonstats WHERE field3 = ?; ",(name2,))
      pokemon2 = cur.fetchone()
              
      
      hpstat2 = ((((float(pokemon2[0])*2)+31)*100)/100)+100+10
      atkstat2 = ((((float(pokemon2[1])*2)+31)*100)/100)+5
      defstat2 = ((((float(pokemon2[2])*2)+31)*100)/100)+5
      spatkstat2 = ((((float(pokemon2[3])*2)+31)*100)/100)+5
      spdefstat2 = ((((float(pokemon2[4])*2)+31)*100)/100)+5
      speedstat2 = ((((float(pokemon2[5])*2)+31)*100)/100)+5
      if author[2] == "adamant":
        atkstat = int(float(atkstat*1.1))
        spatkstat = int(float(spatkstat*0.9))
      if author[2] == "lonely": 
        atkstat = int(float(atkstat*1.1))
        defstat = int(float(defstat*0.9))
      if author[2] == "brave":
        atkstat = int(float(atkstat*1.1))
        speedstat = int(float(speedstat*0.9))
      if author[2] == "naughty":
        atkstat = int(float(atkstat*1.1))
        spdefstat = int(float(spdefstat*0.9))
      if author[2] == "bold":
        defstat = int(float(defstat*1.1))
        atkstat = int(float(atkstat*0.9))
      if author[2] == "relaxed":
        defstat = int(float(defstat*1.1))
        speedstat = int(float(speedstat*0.9))
      if author[2] == "impish":  
        defstat = int(float(defstat*1.1))
        spatkstat = int(float(spatkstat*0.9))
      if author[2] == "lax": 
        defstat = int(float(defstat*1.1))  
        spdefstat = int(float(spdefstat*0.9))  
      if author[2] == "timid":      
        speedstat = int(float(speedstat*1.1))
        atkstat = int(float(atkstat*0.9))
      if author[2] == "hasty":      
        speedstat = int(float(speedstat*1.1)) 
        defstat = int(float(defstat*0.9)) 
      if author[2] == "jolly":      
        speedstat = int(float(speedstat*1.1))   
        spatkstat = int(float(spatkstat*0.9))
      if author[2] == "naive":      
        speedstat = int(float(speedstat*1.1))  
        spdefstat = int(float(spdefstat*0.9)) 
      if author[2] == "modest": 
        spatkstat = int(float(spatkstat*1.1))   
        atkstat = int(float(atkstat*0.9))    
      if author[2] == "mild": 
        spatkstat = int(float(spatkstat*1.1)) 
        defstat = int(float(defstat*0.9)) 
      if author[2] == "quiet": 
        spatkstat = int(float(spatkstat*1.1))   
        speedstat = int(float(speedstat*0.9))
      if author[2] == "rash": 
        spatkstat = int(float(spatkstat*1.1)) 
        spdefstat = int(float(spdefstat*0.9))
      if author[2] == "calm":  
        spdefstat = int(float(spdefstat*1.1))  
        atkstat = int(float(atkstat*0.9))
      if author[2] == "gentle":  
        spdefstat = int(float(spdefstat*1.1))  
        defstat = int(float(defstat*0.9)) 
      if author[2] == "sassy":  
        spdefstat = int(float(spdefstat*1.1))
        speedstat = int(float(speedstat*0.9))
      if author[2] == "sassy":  
        spdefstat = int(float(spdefstat*1.1))      
        spatkstat = int(float(spatkstat*0.9))
      if member[2] == "adamant":
        atkstat2 = int(float(atkstat2*1.1))
        spatkstat2 = int(float(spatkstat2*0.9))
      if member[2] == "lonely": 
        atkstat2 = int(float(atkstat2*1.1))
        defstat2 = int(float(defstat2*0.9))
      if member[2] == "brave":
        atkstat2 = int(float(atkstat2*1.1))
        speedstat2 = int(float(speedstat2*0.9))
      if member[2] == "naughty":
        atkstat2 = int(float(atkstat2*1.1))
        spdefstat2 = int(float(spdefstat2*0.9))
      if member[2] == "bold":
        defstat2 = int(float(defstat2*1.1))
        atkstat2 = int(float(atkstat2*0.9))
      if member[2] == "relaxed":
        defstat2 = int(float(defstat2*1.1))
        speedstat2 = int(float(speedstat2*0.9))
      if member[2] == "impish":  
        defstat2 = int(float(defstat2*1.1))
        spatkstat2 = int(float(spatkstat2*0.9))
      if member[2] == "lax": 
        defstat2 = int(float(defstat2*1.1))  
        spdefstat2 = int(float(spdefstat2*0.9))  
      if member[2] == "timid":      
        speedstat2 = int(float(speedstat2*1.1))
        atkstat2 = int(float(atkstat2*0.9))
      if member[2] == "hasty":      
        speedstat2 = int(float(speedstat2*1.1)) 
        defstat2 = int(float(defstat2*0.9)) 
      if member[2] == "jolly":      
        speedstat2 = int(float(speedstat2*1.1))   
        spatkstat2 = int(float(spatkstat2*0.9))
      if member[2] == "naive":      
        speedstat2 = int(float(speedstat2*1.1))  
        spdefstat2 = int(float(spdefstat2*0.9)) 
      if member[2] == "modest": 
        spatkstat2 = int(float(spatkstat2*1.1))   
        atkstat2 = int(float(atkstat2*0.9))    
      if member[2] == "mild": 
        spatkstat2 = int(float(spatkstat2*1.1)) 
        defstat2 = int(float(defstat2*0.9)) 
      if member[2] == "quiet": 
        spatkstat2 = int(float(spatkstat2*1.1))   
        speedstat2 = int(float(speedstat2*0.9))
      if member[2] == "rash": 
        spatkstat2 = int(float(spatkstat2*1.1)) 
        spdefstat2 = int(float(spdefstat2*0.9))
      if member[2] == "calm":  
        spdefstat2 = int(float(spdefstat2*1.1))  
        atkstat2 = int(float(atkstat2*0.9))
      if member[2] == "gentle":  
        spdefstat2 = int(float(spdefstat2*1.1))  
        defstat2 = int(float(defstat2*0.9)) 
      if member[2] == "sassy":  
        spdefstat2 = int(float(spdefstat2*1.1))
        speedstat2 = int(float(speedstat2*0.9))
      if member[2] == "sassy":  
        spdefstat2 = int(float(spdefstat2*1.1))      
        spatkstat2 = int(float(spatkstat2*0.9))

  
      if speedstat>=speedstat2:
        duel = discord.Embed(description=ctx.author.name+"'s turn",color=discord.Color(random.choice(colors)))
        duel.set_image(url = "https://projectpokemon.org/images/sprites-models/normal-back/"+name+".gif")
        duel.set_thumbnail(url = str(pokemon2[7]))
        turn = True
        health = discord.Embed(description = name.capitalize()+"'s health: "+str(hpstat)+"              "+name2.capitalize()+"'s health: "+str(hpstat2),color=discord.Color(random.choice(colors)))
      else:
        duel = discord.Embed(description=user.name+"'s turn",color=discord.Color(random.choice(colors)))
        duel.set_image(url = "https://projectpokemon.org/images/sprites-models/normal-back/"+name2+".gif")
        duel.set_thumbnail(url = str(pokemon[7]))
        turn = False
        health = discord.Embed(description = name2.capitalize()+"'s health: "+str(hpstat2)+" \n"+name.capitalize()+"'s health: "+str(hpstat),color=discord.Color(random.choice(colors)))
      await ctx.send(embed = duel)
      
        
      
        
      
      
            
      #await ctx.send(str(name2))
      health = discord.Embed(description = name.capitalize()+"'s health: "+str(hpstat)+"\n"+name2.capitalize()+"'s health: "+str(hpstat2),color=discord.Color(random.choice(colors)))
      health.set_footer(text="type .use 1-4 to use a move")
      await ctx.send(embed = health)
      def calculate_damage(base_damage, attack, defense):
        return (((((2*100)/5)+2)*base_damage*(attack/defense))/50)+2
      while hpstat2>0 and hpstat>0:
        
        
        

        
          if turn:
            move = await client.wait_for('message', check = lambda message: message.author == ctx.author, timeout=300) 
          else:
            move = await client.wait_for('message', check = lambda message: message.author == user, timeout=300) 
        
          
        
          use = move.content.split(" ")
          
          if len(use) != 2:
            
            continue
          elif use[1] != "1" and use[1] != "2" and use[1] != "3" and use[1] != "4":
            
            continue
          if turn:
            moves = author[1].split(", ")
          else:
            moves = member[1].split(", ")
          cur.execute("SELECT field1, field2, field3, field4, field5, field6, field7, field8, field9, field10, field11, field12, field13, field14, field15, field16, field17, field18, field19, field20, field21, field22, field23, field24, field25, field26 FROM Pokemonstats WHERE field19 = ?; ",(str(moves[int(use[1])-1]),))
          value = ""
          movestats = cur.fetchone()
          print(movestats)
          bp = movestats[23]
          dmg = 0
          stab = 1
          effectiveness = 1
          missed = False
          probability = random.uniform(0, 1)
          rand =  random.uniform(0.85, 1)
          types1 = pokemon[6].split(", ")
          types2 = pokemon2[6].split(", ")
          if movestats[24] == '100':
            accuracy = 1
          else: 
            accuracy = float("0."+movestats[24])
          if probability < accuracy:
            missed = True
          
          
          if missed:
            if turn:
              if movestats[19] in types1:
                stab = 1.5
              for i in types2:
                
              
                print(type[str(i.lower())][str(movestats[19].lower())])
                effectiveness = effectiveness*float(type[str(i.lower())][str(movestats[19].lower())])
              
                
              if str(movestats[20]) == "Physical":
                dmg = calculate_damage(int(bp),int(atkstat),int(defstat2))*stab*rand
              else:
                dmg = calculate_damage(int(bp),int(spatkstat),int(spdefstat2))*stab*rand
              dmg = int(float(dmg)*float(effectiveness))
              hpstat2 = hpstat2-dmg
              
            else:
              
              if movestats[19] in types2:
                stab = 1.5
              for i in types1:
                effectiveness = effectiveness*float(type[str(i).lower()][str(movestats[19]).lower()])
              if str(movestats[20]) == "Physical":
                dmg = calculate_damage(int(bp),int(atkstat2),int(defstat))*stab*rand
              else:
                dmg = calculate_damage(int(bp),int(spatkstat2),int(spdefstat))*stab*rand
              dmg = int(float(dmg)*float(effectiveness))
            
              hpstat = hpstat-dmg
          
          
          if turn:
            value = value+"\n"+ ""+name.capitalize()+" used "+str(moves[int(use[1])-1])+""
            if not missed:
              value = value+"\n"+"it missed"
            elif effectiveness>1:
              value = value+"\n"+"its super effective!"
            elif effectiveness == 0:
              value = value+"\n"+"it did nothing"  
            elif effectiveness < 1:
              value = value+"\n"+"its not very effective"
            value = value+"\n**"+"-"+str(int(dmg))+"**"
            duel = discord.Embed(description=user.name+"'s turn",color=discord.Color(random.choice(colors)))
            duel.set_image(url = "https://projectpokemon.org/images/sprites-models/normal-back/"+name2+".gif")
            duel.set_thumbnail(url = str(pokemon[7]))
            
            health = discord.Embed(description = name2.capitalize()+"'s health: "+str(int(hpstat2))+"\n"+name.capitalize()+"'s health: "+str(int(hpstat)),color=discord.Color(random.choice(colors)))
          else:
            value = value+"\n"+ ""+name2.capitalize()+" used "+str(moves[int(use[1])-1])+""
            if not missed:
              value = value+"\n"+"it missed"
            elif effectiveness>1:
              value = value+"\n"+"its super effective!"
            elif effectiveness == 0:
              value = value+"\n"+"it did nothing"
            elif effectiveness < 1:
              value = value+"\n"+"its not very effective"
            
            value = value+"\n"+"-**"+str(int(dmg))+"**"
            duel = discord.Embed(description=ctx.author.name+"'s turn",color=discord.Color(random.choice(colors)))
            duel.set_image(url = "https://projectpokemon.org/images/sprites-models/normal-back/"+name+".gif")
            duel.set_thumbnail(url = str(pokemon2[7]))
          
            health = discord.Embed(description = name.capitalize()+"'s health: "+str(int(hpstat))+"\n"+name2.capitalize()+"'s health: "+str(int(hpstat2)),color=discord.Color(random.choice(colors)))
          if hpstat <= 0:
            value = value+"\n"+""+name.capitalize()+" fainted"
            
            in_duel.remove(ctx.author.id)
            in_duel.remove(user.id)
            return
          if hpstat2 <= 0:
            value = value+"\n"+""+name2.capitalize()+" fainted"
            in_duel.remove(ctx.author.id)
            in_duel.remove(user.id)
            return
          notif = discord.Embed(description=""+value+"",color=discord.Color(random.choice(colors)))  
          await ctx.send(embed = notif)
          await ctx.send(embed = duel)
          await ctx.send(embed = health)
          turn = not turn
          
        
      await ctx.send("duel ended")
      in_duel.remove(ctx.author.id)
      in_duel.remove(user.id)
      return

    
   
        
        	
      
client.run('NzM1NTU5OTQ1MTM0NTM4OTIz.XxiBmQ.ZdDe-YIl7wO4E_nD92Ndz0CXkcc')