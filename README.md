### Doorbot Python

This is a work in progress of a python API for doorbot.

There is a "full" go implementation at [masom/doorbot](https://github.com/masom/doorbot)

### Multiple Flask apps
Doorbot mounts several applications on Werkzeug:
- Accounts on subdomains which includes a "dashboard" and an "API" app
- Admin subdomain
- Main website

This is accomplished using the Flask app factory pattern. https://github.com/masom/doorbot-api-python/blob/master/doorbot/factory.py

### Middlewares
This project experimented a little bit with route middlewares.

Example in martini (golang):
```golang
m.Group("/books", func(r martini.Router) {
    r.Get("/:id", GetBooks)
    r.Post("/new", NewBook)
    r.Put("/update/:id", UpdateBook)
    r.Delete("/delete/:id", DeleteBook)
}, MyMiddleware1, MyMiddleware2)
```

Flask route middlewares can be implemented like this:

```python
def s(*mw):
    '''s defines a list of route middlewares that will be applied in order.
    '''

    return m(account_scope, auth_secured, *mw)


def m(*mw):
    '''m defines a list of route middlewares that will be applied in order.
    '''

    def wrapped(*args, **kwargs):
        for item in mw:
            rv = item(*args, **kwargs)
            if rv:
                return handle_response(rv)

    return wrapped


bp = Blueprint(__name__)

bp.add_url_rule(
    '/password', 'password',
    m(account_scope, validate('authentication_password'), password),
    methods=['POST']
)

bp.add_url_rule(
    '', 'view', s(view),
    methods=['GET']
)

bp.add_url_rule(
    '/<int:id>', 'update',
    s(auth_manager, validate('door_update'), update),
    methods=['PUT']
)
```

### JSON-Schema validation
JSON-Schema is awesome! It validates JSON payloads allowing you to focus on the business logic vs basic data validation.

Replaces WTForms for the API endpoints.

### TODO

- [ ] Dashboards, admin panels, etc.
- [ ] Tests, this was a quick hack to get things working in python
- [ ] JSON-Schemas
