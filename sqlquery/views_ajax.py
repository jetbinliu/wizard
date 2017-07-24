# -*- coding: UTF-8 -*-

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from common.aes_decryptor import Prpcrypt

prpCryptor = Prpcrypt()  # 初始化


@csrf_exempt
def desensitization(request):
    if request.is_ajax():
        encrypted_field = request.POST.get("encrypted_field")
    else:
        encrypted_field = request.POST['encrypted_field']
    _encrypted_field = encrypted_field[14:]
    decrypt_field = prpCryptor.decrypt(_encrypted_field)
    result = {'status':0, 'msg':'ok', 'data':decrypt_field}
    return HttpResponse(json.dumps(result), content_type='application/json')
