import discord

from . import (
    common,
    util,

    user_commands,
    priv_commands,
    admin_commands
)


async def handle(invoke_msg: discord.Message, response_msg: discord.Message):
    await util.send_embed(
        common.log_channel,
        f"Command invoked by {invoke_msg.author} / {invoke_msg.author.id}",
        invoke_msg.content
    )

    cmd_str = invoke_msg.content[len(common.PREFIX):].lstrip()
    cmd_args = cmd_str.split()

    is_admin = False
    is_priv = False

    if invoke_msg.author.id in common.ADMIN_USERS:
        is_admin = True
        is_priv = True
    else:
        for role in invoke_msg.author.roles:
            if role.id in common.ADMIN_ROLES:
                is_admin = True
                is_priv = True
            elif role.id in common.PRIV_ROLES:
                is_priv = True

    try:
        if is_admin:
            if cmd_args[0] in admin_commands.EXPORTED_COMMANDS.keys():
                command = admin_commands.EXPORTED_COMMANDS[cmd_args[0]]
                if command["args"] == -1 or command["args"] == len(cmd_args) - 1:
                    await command["function"](invoke_msg, response_msg, cmd_args[1:],
                                              cmd_str[len(cmd_args[0]):].lstrip())
                    return

        if is_priv:
            if cmd_args[0] in priv_commands.EXPORTED_COMMANDS.keys():
                command = priv_commands.EXPORTED_COMMANDS[cmd_args[0]]
                if command["args"] == -1 or command["args"] == len(cmd_args) - 1:
                    await command["function"](invoke_msg, response_msg, cmd_args[1:],
                                              cmd_str[len(cmd_args[0]):].lstrip())
                    return

        if cmd_args[0] in user_commands.EXPORTED_COMMANDS.keys():
            command = user_commands.EXPORTED_COMMANDS[cmd_args[0]]
            if command["args"] == -1 or command["args"] == len(cmd_args) - 1:
                await command["function"](invoke_msg, response_msg, cmd_args[1:],
                                          cmd_str[len(cmd_args[0]):].lstrip())
                return
    except Exception as exc:
        await util.edit_embed(
            response_msg,
            "An unhandled exception occurred while handling your command!",
            f"{type(exc).__name__}: {', '.join([str(i) for i in exc.args])}"
        )
        return

    await util.edit_embed(
        response_msg,
        "Invalid command!",
        "Have you spelt the command name right or maybe put the appropriate amount of arguments?"
    )
