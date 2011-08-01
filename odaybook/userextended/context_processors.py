# -*- coding: UTF-8 -*-

def env(request):
    '''
        Специфичные только для этого приложения еременные окружения
    '''
    render = {}
    
    render['zombie'] = int(request.COOKIES.get('zombie', 0))

    return render

