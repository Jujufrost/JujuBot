import datetime as dt
import os
import random
import requests

import discord
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(intents=intents, command_prefix='$')

@bot.command(name='rolldice', help='Simulates rolling dice. Ex: $rolldice 3 20')
async def roll(ctx, number_of_dice: int=1, number_of_sides: int=6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='coinflip', help='Flips a coin')
async def coinflip(ctx):
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(result)

@bot.command(name='rps', help='Rock, Paper, Scissors game. Ex: $rps paper')
async def rps(ctx, usr_choice):
    usr_choice = usr_choice.capitalize()
    bot_choice = random.choice(['Rock', 'Paper', 'Scissors'])

    if usr_choice == bot_choice:
        await ctx.send("It's a tie!")
    
    elif usr_choice == 'Rock':
        if bot_choice == 'Scissors':
            await ctx.send(f'{usr_choice} beats {bot_choice}, {ctx.author.name} wins!')
        else:
            await ctx.send(f'{bot_choice} beats {usr_choice}, {bot.user.name} wins!')

    elif usr_choice == 'Paper':
        if bot_choice == 'Rock':
            await ctx.send(f'{usr_choice} beats {bot_choice}, {ctx.author.name} wins!')
        else:
            await ctx.send(f'{bot_choice} beats {usr_choice}, {bot.user.name} wins!')

    elif usr_choice == 'Scissors':
        if bot_choice == 'Paper':
            await ctx.send(f'{usr_choice} beats {bot_choice}, {ctx.author.name} wins!')
        else:
            await ctx.send(f'{bot_choice} beats {usr_choice}, {bot.user.name} wins!')


### WEATHER ###
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.getenv('WEATHER_KEY')

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = round(kelvin - 273.15, 1)
    fahrenheit = round(celsius * (9/5) + 32, 1)
    return celsius, fahrenheit

@bot.command(name='weather', help='Provides weather for a city. Ex: $weather "New York"')
async def weather(ctx, city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    
    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = response['main']['temp']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    humidity = response['main']['humidity']
    description = response['weather'][0]['description'].capitalize()
    wind_speed = response['wind']['speed']
    wind_speed_mph = round(wind_speed * 2.237, 1)
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
     

    
    await ctx.send(f"Temperature in {city}: {temp_fahrenheit}˚F/{temp_celsius}˚C\n"
                   f"General weather: {description}\n"
                   f"Feels like: {feels_like_fahrenheit}˚F/{feels_like_celsius}˚C\n"
                   f"Humidity: {humidity}%\n"
                   f"Wind speed: {wind_speed_mph}mph\n"
                   f"Sun rises: {sunrise_time}\n"
                   f"Sun sets: {sunset_time}"
    )
#################
    



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)