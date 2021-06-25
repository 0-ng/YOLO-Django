import random

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .yolo import yolo_detect
import json


def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    else:
        file_img = request.FILES.get('image')
        data = "statics/" + str(file_img)
        data2 = "static/" + str(file_img)
        with open(data, 'wb') as f:
            for chunk in file_img.chunks():
                f.write(chunk)
        rets = yolo_detect(data, data)

        box = [{
                "x": ret["x"],
                "y": ret["y"],
                "w": ret["w"],
                "h": ret["h"],
                "label": ret["label"],
                "confidence": ret["confidence"]
            } for ret in rets]
        print(box)
        html = render_to_string('formula_details.html', {'formulas': box})
        ret = {
            "data": html,
            "url": data2
        }
        return HttpResponse(json.dumps(ret))
