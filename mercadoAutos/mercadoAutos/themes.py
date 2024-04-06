
yellow_theme = {'css':'/static/owncss/yellowcss.css', 'background': '/static/img/yellowback1.png'}
coral_theme = {'css':'/static/owncss/coralcss.css', 'background': '/static/img/coralback1.png'}
blue_theme = {'css':'/static/owncss/bluecss.css', 'background': '/static/img/blueback1.png'}

def theme(request): return {'theme':get_theme(request)}

def get_theme(request): 
    if not request.session.get('theme'): set_yellow(request)
    return request.session.get('theme')

def set_yellow(request): request.session['theme'] = yellow_theme
def set_coral(request): request.session['theme'] = coral_theme
def set_blue(request): request.session['theme'] = blue_theme