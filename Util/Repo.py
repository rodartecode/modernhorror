from Util import Default

owners = Default.get("config.json").owners

# Checks to see if the user is "on the list" 
def is_owner(ctx):
    return ctx.author.id in owners

def memb_is_owner(memb_id):
    return memb_id in owners