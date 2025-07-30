import os
from random import choice

import discord
import pandas as pd

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

lines1 = [
    "A thrill chills the blood",
    "Whatever to do?",
    "Teach me, O Master",
    "From that day onward",
    "I bring you a gift",
    "Mom's a gorilla",
    "Wait a moment, please",
    "Bow down, oh bow down",
    "Stand with pride, young one",
    "Oh, magnificent",
    "They know who they are",
    "In these environs",
    "Just a fleeing gag",
    "To no one's surprise",
    "Yesterday, I saw",
    "A cloud-covered moon",
    "Part-time employment",
    "Down on the seafloor",
    "Deep contemplation",
    "More stalwart than stone",
    "Softer than fresh clay",
    "Miserable wretch",
    "Ere a restful night",
    "Repent and atone",
    "Life is thus, you know",
    "Appetites most odd",
    "Most exceptional",
    "When the lights are out",
    "With vim and vigor",
    "Perambulation",
    "One must read the room",
    "A stroke of genius",
    "Til the bitter end",
]

lines2 = [
    "ever needlessly anxious",
    "this, that, or another one",
    "covered in a cake of dust",
    "shadows hide what eyes should see",
    "distance beyond reckoning",
    "overcome with emotion",
    "no matter what you may say",
    "every hair standing on end",
    "from one winter to the next",
    "this, that, or another one",
    "heavy with the flab of age",
    "refusing not once, but twice",
    "borrowed money spends just fine",
    "the latest exercise trend",
    "one shot booms like a barrage",
    "footing lost, ne'er to be found",
    "undefeated and unmatched",
    "walking hand in hand with you",
    "resolved to face down my fate",
    "leave, nevermore to return",
    "warriors stand proud and true",
    "all things must pass in the end",
    "make my hair stand up on end",
    "ignorant of what it means",
    "eyes strain to hold back the tears",
    "the moment I turn around",
    "take heart and be strong, dear one",
    "on your cheek, like fine whiskers",
    "every spot, from head to tail",
    "a pedigreed delinquent",
    "battle-worn but unbroken",
    "grandma's a gorilla, too",
    "say you'll be true forever",
]

lines3 = [
    "pectoral muscles.",
    "filing bankruptcy.",
    "the touch of a pro.",
    "mutual feelings.",
    "lady of leisure.",
    "begging for your life.",
    "so on and so forth.",
    "no word of reply.",
    "alabaster skin.",
    "wear your Sunday best.",
    "throw in the towel.",
    "tremendous blunder.",
    "says the oil baron.",
    "constant rematches.",
    "I remove my clothes.",
    "love lost forever.",
    "sighs the luchador.",
    "bags under the eyes.",
    "I'm a gorilla.",
    "a hug from behind.",
    "together we fall.",
    "major surgery.",
    "shaking off the mud.",
    "the fisherman sings.",
    "I love you, my dear.",
    "deserted at sea.",
    "a winning ticket.",
    "crushing loneliness.",
    "like a growing fish.",
    "unsinkable ship.",
    "total overkill.",
    "combine for battle.",
    "I love you, my dear.",
]


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.casefold() == "!quote".casefold():
        await message.channel.send(await slayerbot())

    if message.content.casefold() == "!gorilla".casefold():
        gorilla_quote, attemps, counter = await gorilla()
        # make a txt file with the attempts
        with open("attempts.txt", "w") as f:
            f.write(f"Number of attempts: {counter}\n")
            f.write("\n".join(attemps))
        try:
            await message.channel.send(gorilla_quote, file=discord.File("attempts.txt"))
        except discord.errors.HTTPException as exc:
            await message.channel.send(
                f"{gorilla_quote}\nToo many attempts for discord's file size limit. Number of attempts: {counter}"
            )
        new_player_score, new_general_score = await update_scores(message, counter)
        match new_player_score:
            case 1:
                await message.channel.send(
                    f"New low score for <@{message.author.id}>: {counter} attempts"
                )
            case 2:
                await message.channel.send(
                    f"New high score for <@{message.author.id}>: {counter} attempts"
                )

        match new_general_score:
            case 1:
                await message.channel.send(
                    f"<@{message.author.id}> HAS OBTAINTED THE LOWEST SCORE OF ALL TIME: {counter} attempts"
                )
            case 2:
                await message.channel.send(
                    f"<@{message.author.id}> HAS OBTAINTED THE HIGHEST SCORE OF ALL TIME: {counter} attempts"
                )

    if message.content.casefold() == "!odds".casefold():
        await message.channel.send(
            "There are %d quote combinations"
            % (len(lines1) * len(lines2) * len(lines3))
        )

    if message.content.casefold() == "!scores".casefold():
        if not os.path.exists(f"scores_{message.guild.id}.md"):
            with open(f"scores_{message.guild.id}.md", "w+") as f:
                f.write("No scores yet")
        with open(f"scores_{message.guild.id}.md", "r") as f:
            print(f.read())
            f.seek(0)
            await message.channel.send(f.read())

    if message.content.startswith("!help"):
        await message.channel.send(
            "Use !quote to get a random quote, !gorilla to get a gorilla quote, !odds to get the number of possible quotes, !scores to get the scores and !help to get this message"
        )

    if message.content.startswith("!goat"):
        role: discord.role.Role = discord.utils.get(
            message.guild.roles, name="Dandy GOAT"
        )
        print(role.members)
        print(message.author)
        print(role.members[0].id == message.author.id)


async def slayerbot():
    return f"{choice(lines1).strip()}... {choice(lines2).strip()}... {choice(lines3).strip()}"


async def gorilla():
    line1, line2, line3 = "", "", ""
    attempts = []
    counter = 0
    while "gorilla" not in line1 or "gorilla" not in line2 or "gorilla" not in line3:
        line1 = choice(lines1).strip()
        line2 = choice(lines2).strip()
        line3 = choice(lines3).strip()

        counter += 1
        attempts.append(f"{line1}... {line2}... {line3}")

    return (f"{line1}... {line2}... {line3}", attempts, counter)


async def update_scores(message: discord.Message, counter: int):
    if not os.path.exists(f"scores_{message.guild.id}.csv"):
        scores = pd.DataFrame(columns=["user", "low", "high"])
        scores.to_csv(f"scores_{message.guild.id}.csv", index=False)

    scores = pd.read_csv(
        f"scores_{message.guild.id}.csv",
        dtype={"user": "int64", "low": "int64", "high": "int64"},
    )
    user = message.author.id
    # Wether the user has a new high or low score
    new_player_score = 0
    # wether there is a new general high or low score
    new_general_score = 0

    if user not in scores["user"].values:
        new_row = pd.DataFrame(
            [
                {
                    "user": user,
                    "low": counter,
                    "high": counter,
                }
            ]
        )
        scores = pd.concat([scores, new_row], ignore_index=True)
    else:
        if counter < scores.loc[scores["user"] == user, "low"].values[0]:
            new_player_score = 1
        if counter > scores.loc[scores["user"] == user, "high"].values[0]:
            new_player_score = 2

        if counter < scores["low"].min():
            new_general_score = 1
            role = discord.utils.get(message.guild.roles, name="Dandy GOAT")
            if not role:
                await message.guild.create_role("Dandy GOAT")
                await message.author.add_roles(role)
            if role.members:
                if message.author.id != role.members[0].id:
                    await role.members[0].remove_roles(role)
                    await message.author.add_roles(role)
            else:
                await message.author.add_roles(role)

        if counter > scores["high"].max():
            new_general_score = 2
            role = discord.utils.get(message.guild.roles, name="Dandy TOAD")
            if not role:
                await message.guild.create_role("Dandy TOAD")
                await message.author.add_roles(role)
            if role.members:
                if message.author.id != role.members[0].id:
                    await role.members[0].remove_roles(role)
                    await message.author.add_roles(role)
            else:
                await message.author.add_roles(role)

        scores.loc[scores["user"] == user, "low"] = min(
            scores.loc[scores["user"] == user, "low"].values[0], counter
        )
        scores.loc[scores["user"] == user, "high"] = max(
            scores.loc[scores["user"] == user, "high"].values[0], counter
        )

    scores.to_csv(f"scores_{message.guild.id}.csv", index=False)
    await update_scores_markdown(scores, message.guild.id)

    return new_player_score, new_general_score


async def update_scores_markdown(scores: pd.DataFrame, server_id: int):
    low_scores = scores.nsmallest(5, "low").sort_values("low")[["user", "low"]]
    high_scores = scores.nlargest(5, "high").sort_values("high", ascending=False)[
        ["user", "high"]
    ]
    with open(f"scores_{server_id}.md", "w+") as f:
        f.write(f"# Gorilla Quote Scores\n")
        f.write(f"## Lowest number of attempts:\n")
        i = 0
        for index, row in low_scores.iterrows():
            f.write(f"{i+1}. <@{row['user']}>: {row['low']} attempts\n")
            i += 1
        f.write(f"## Highest number of attempts:\n")
        i = 0
        for index, row in high_scores.iterrows():
            f.write(f"{i+1}. <@{row['user']}>: {row['high']} attempts\n")
            i += 1
        f.write("## Players scores:\n")
        for i, row in scores.iterrows():
            f.write(
                f"<@{row['user']}>: Lowest: {row['low']} attempts, Highest: {row['high']} attempts\n"
            )


client.run(os.environ.get("DISCORD_KEY"))
