from main import *

app.add_api_route('/', login)
app.add_api_route('/index', index)
app.add_api_route('/study', study)