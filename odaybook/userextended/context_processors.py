# -*- coding: UTF-8 -*-

def env(request):
    render = {}
    
    render['zombie'] = int(request.COOKIES.get('zombie', 0))

    return render

