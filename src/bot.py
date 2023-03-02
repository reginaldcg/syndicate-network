import discord
import os
from discord import app_commands
from src import responses
from src import log

logger = log.setup_logger(__name__)

isPrivate = False
isReplyAll = False

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /help")


async def send_message(message, user_message):
    global isReplyAll
    if not isReplyAll:
        author = message.user.id
        await message.response.defer(ephemeral=isPrivate)
    else:
        author = message.author.id
    try:
        response = '> **' + user_message + '** - <@' + \
            str(author) + '> \n\n'
        response = f"{response}{await responses.handle_response(user_message)}"
        char_limit = 1900
        if len(response) > char_limit:
            # [discord limit = 2000/chunk]
            if "```" in response:
                # if the code block exists, split the response.

                parts = response.split("```")

                for i in range(0, len(parts)):
                    if i%2 == 0: # [even indices ≠ code blocks]
                        if isReplyAll:
                            await message.channel.send(parts[i])
                        else:
                            await message.followup.send(parts[i])

                    # send seperate messages
                    else: # [odd indices = code blocks]
                        code_block = parts[i].split("\n")
                        formatted_code_block = ""
                        for line in code_block:
                            while len(line) > char_limit:
                                # 50 characters per line
                                formatted_code_block += line[:char_limit] + "\n"
                                line = line[char_limit:]
                            formatted_code_block += line + "\n"  # add and seperate with a new line

                        # send seperate messages
                        if (len(formatted_code_block) > char_limit+100):
                            code_block_chunks = [formatted_code_block[i:i+char_limit]
                                                 for i in range(0, len(formatted_code_block), char_limit)]
                            for chunk in code_block_chunks:
                                if isReplyAll:
                                    await message.channel.send("```" + chunk + "```")
                                else:
                                    await message.followup.send("```" + chunk + "```")
                        else:
                            if isReplyAll:
                                await message.channel.send("```" + formatted_code_block + "```")
                            else:
                                await message.followup.send("```" + formatted_code_block + "```")

            else:
                response_chunks = [response[i:i+char_limit]
                                   for i in range(0, len(response), char_limit)]
                for chunk in response_chunks:
                    if isReplyAll:
                        await message.channel.send(chunk)
                    else:
                        await message.followup.send(chunk)

        else:
            if isReplyAll:
                await message.channel.send(response)
            else:
                await message.followup.send(response)
    except Exception as e:
        if isReplyAll:
            await message.channel.send("> **Sorry, Gup went to the bathroom. Try again later.**")
        else:
            await message.followup.send("> **Sorry, Gup went to the bathroom. Try again later.**")
        logger.exception(f"ERROR: LOG FAILURE: {e}")


async def send_start_prompt(client):
    import os.path

    config_dir = os.path.abspath(__file__ + "/../../")
    prompt_name = 'starting-prompt.txt'
    prompt_path = os.path.join(config_dir, prompt_name)
    discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
    try:
        if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
            with open(prompt_path, "r") as f:
                prompt = f.read()
                if (discord_channel_id):
                    logger.info(f"Sending Prompt-Response with Size. {len(prompt)}")
                    responseMessage = await responses.handle_response(prompt)
                    channel = client.get_channel(int(discord_channel_id))
                    await channel.send(responseMessage)
                    logger.info(f"Prompt-Response:{responseMessage}")
                else:
                    logger.info("Missing Channel. Dropping Send-Response.")
        else:
            logger.info(f"Missing {prompt_name}. Dropping Send-Response.")
    except Exception as e:
        logger.exception(f"ERROR: SENDING RESPONSE FAILURE: {e}")


def run_discord_bot():
    client = aclient()

    @client.event
    async def on_ready():
        await send_start_prompt(client)
        await client.tree.sync()
        logger.info(f'{client.user} has been turned on. Beep-Boop.')

    @client.tree.command(name="chat", description="Talk to Gup about your problems. Beep-Boop.")
    async def chat(interaction: discord.Interaction, *, message: str):
        global isReplyAll
        if isReplyAll:
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send(
                "> **WARNING: To stop Gup from replying to all server messages, use the command: `/replyall`.**")
            logger.warning("\x1b[31mHaha, nice one. We're already in replyall mode though.\x1b[0m")
            return
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        user_message = message
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
        await send_message(interaction, user_message)

    @client.tree.command(name="private", description="Talk privately to Gup about your problems. Beep-Boop.")
    async def private(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if not isPrivate:
            isPrivate = not isPrivate
            logger.warning("\x1b[31mPRIVATE MODE ON\x1b[0m")
            await interaction.followup.send(
                "> **INFO: The next response will be made in private.**")
        else:
            logger.info("Haha, nice one. We're already in private mode though.")
            await interaction.followup.send(
                "> **WARNING: To leave private mode, use the command: `/public`.**")

    @client.tree.command(name="public", description="Talk publicly to Gup about your problems. Beep-Boop.")
    async def public(interaction: discord.Interaction):
        global isPrivate
        await interaction.response.defer(ephemeral=False)
        if isPrivate:
            isPrivate = not isPrivate
            await interaction.followup.send(
                "> **INFO: The next response will be made in public.**")
            logger.warning("\x1b[31mPUBLIC MODE ON\x1b[0m")
        else:
            await interaction.followup.send(
                "> **WARNING: To leave public mode, use the command: `/private`.**")
            logger.info("Haha, nice one. We're already in public mode though.")

    @client.tree.command(name="replyall", description="Toggle between Gup's reply methods.")
    async def replyall(interaction: discord.Interaction):
        global isReplyAll
        await interaction.response.defer(ephemeral=False)
        if isReplyAll:
            await interaction.followup.send(
                "> **INFO: Gup will only reply to commands.**")
            logger.warning("\x1b[31mREPLYALL OFF\x1b[0m")
        else:
            await interaction.followup.send(
                "> **INFO: Gup will reply to all server messages.**")
            logger.warning("\x1b[31mREPLYALL ON\x1b[0m")
        isReplyAll = not isReplyAll

    @client.tree.command(name="reset", description="Clear Gup's chat history. Beep-Boop.")
    async def reset(interaction: discord.Interaction):
        responses.chatbot.reset_chat()
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("> **INFO: Huh.. Where am I—? I can't seem to remember anything.**")
        logger.warning(
            "\x1b[31mHISTORY CLEARED\x1b[0m")
        await send_start_prompt(client)

    @client.tree.command(name="help", description="Ask Gup for some help. Beep-Boop.")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(""":star:**BOT COMMANDS** \n
        - `/chat [message]` Chat with Gup.
        - `/private` Set message mode to private.
        - `/public` Set message mode to public.
        - `/replyall` Toggle between Reply to all, or Reply to all commands.
        - `/reset` Clear ChatGPT conversation history""")
        logger.info(
            "\x1b[31mBOT COMMANDS\x1b[0m")

    @client.event
    async def on_message(message):
        if isReplyAll:
            if message.author == client.user:
                return
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
            logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
            await send_message(message, user_message)

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    client.run(TOKEN)