def isUserAdmin(user):
    return user.groups.filter(name='library_admins').exists()

