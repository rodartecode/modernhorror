from Util import Default

owners = Default.get("config.json").owners


def is_owner(ctx):
    return ctx.author.id in owners