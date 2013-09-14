from cornice import Service


Users = Service("users", "/users", description='User management api')
UsersLogin = Service('users-login', '/users/login', description='Login a user in')
UsersLogout = Service('users-logout', '/users/logout')

Accounts = Service("accounts", "/accounts", description='Account management api')

Mail = Service('mail', '/mail', description='Get all MIDs for a user')
MailID = Service('mail-id', '/mail/id/{id}', description='Manage Email via ID')
MailTags = Service('mail-tags', '/mail/{id}/tags/', description='Grab/Edit mail tags')
MailPage = Service('mail-page', '/mail/page/{offset}', description='Grab pages of mail')


Search = Service('search', '/search', description='Search for all the things')
