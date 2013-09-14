from cornice import Service


Users = Service("users", "/users", description='User management api')
UsersLogin = Service('users-login', '/users/login', description='Login a user in')
UsersLogout = Service('users-logout', '/users/logout')


MailID = Service('mail-id', '/mail/id/{id}', description='Manage Email via ID')
MailTags = Service('mail-tags', '/mail/{id}/tags/', description='Grab/Edit mail tags')
MailPage = Service('mail-page', '/mail/page/{offset}', description='Grab pages of mail')


SearchTags = Service('search', '/search/tags', description='Search for tags')
SearchText = Service('search-fulltext', '/search/text', description='Search by full text')
