# -*- coding: UTF-8 -*-

def env(request):
    render = {}
    
    render['zombie'] = request.COOKIES.get('zombie', False)

    return render

