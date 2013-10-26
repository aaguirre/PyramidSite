def includeme(config):
    config.add_route('add_user', '/admin/add-user')
    config.add_route('delete_user', '/admin/delete-user/{name}/{id}')
    config.add_route('edit_user', '/admin/edit-user/{id}')
    config.add_route('users', '/admin/users')
    config.add_route('set-password', '/set-password/v/{salt}')
