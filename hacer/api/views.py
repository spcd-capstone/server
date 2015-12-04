from . import api

@api.route('/', methods=['GET', 'POST'])
def index():
    return "Nothing"

