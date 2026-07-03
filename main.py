# -*- coding: utf-8 -*-
"""
PK10 褰╃エ鎶曟敞鍔╂墜 Flet 鐗?v1.1
淇绉诲姩绔樉绀洪棶棰?"""
import flet as ft
import requests
import base64 as b64mod
import io
import re
import json
import os
import time
import datetime
import threading
import sys

if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(_BASE_DIR, "login_config.json")

_EMBEDDED_BALLS = {
    '1': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAACSklEQVR4nO2WvWoUURTHf+fc2XXZDQmS1YghxRIQrLSIip0voI29rcTCRgK+g1jHQrQQfAbfIIIi2vhFzJoYYlK67kzczO49cmcTIyLkTrJ2/uFOc8+d35yPOfcIwFZb5wf4exgNM0wEYQSy/XeliC6cbvlF2VzRm/WGf9DtgjE62J/QsQZkmc7LxgpdFWreUBgt7DeZCt6MXiJCY2D/jrQrGRhOhbp6jx0GZibFipUAgRU8LMULEFVI3DAs3g9XFFSQpCyoWjV6P6D9ucm378eZmd6iOdmJhmocDCpVK7L+/mOVpZdXyPL7nJx+zIdP1wkV7lwcMDnYREgSY+3LGO21C1Sq1zg/d5XZ2dli993bF6QpTEzAYHBEYPDMOaPTqbDcvsHFy3dptWaKvTzvkSRVRPKQm2jpgf4JpJmjVmsVsDTt0M93cC5BClK5GteDDMxDoz5gJ1/m+dIzHj28zdfNVVQjk1YmpMEBbzA+nnOm9YS0+5RaZYp+/xiHVRJj1O/DqaltmmeN1fUTeH/4vqQxRsHTPFe6qUT/b0cCBokYqhZrfnTgqKT/gX+T6n6VlukyQdG3xZ4MIcs829vDAsrzckTZWAmjTATIhErFWFtv8urNOcwc3juak1tcmntNJfFF7x0ZcE9OwYW4hFMybPB5Hn8+KTsW9j30e/IrvBKeEvfNZliiioR+GUss7HYBARYrK4oNUYzMCRFX55FkBcPIVETv1Ou4Ygq2cvmMIoV3GhIYgVVEaKOttxiO+vV/MuoLqUMXplp+8SfgvfMUB1p3OQAAAABJRU5ErJggg==',
    '2': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADpUlEQVR4nLWWXUwcVRTHf/fOzO7OTrrbZNOkSmyS1m20T4pCH1MUK/pkMU9WEGxBKirEBwOtGApFaB9E0Bf/BVEffNIiYizYQpEIbSUba1JsNnbTTTab7iab2Zl7ZWZNDUh2Z3X7Pc3M5Z7vfOec+80Vk5Na3vqB2GqVdw2YEJDSdA4alBRIrbksDMbF6Kg2M1VOWwZn636wHkJ0kDOAlhLhK8oyU+FRIZjwfLxGQh0nCyCUQktIB1J3m5KkbmiTPDgIHSoVoapOtq0ZxJaitsooJYhtO4Ln7e/NYNIGtoJWKx7CqCKMWpir9m0sswvDEJ0jDGrhueCqAgMjqxx+1mdwv4kCZq+X+P6LDPi9LWtlRlXmexpfLPLKO2WOn9iPIHF//egLitlrOeZ/6SFuS7TqgMKau8KxkyVePXEoHOZ8fonLl5ZACQ6MpJDynwSawYyizt1UdPcvcfzkMFpLZmf+5P1TRarLe7HiAttReJs9WLHm6iKfu7pf4bkxjeM4KO3x8bnb/HEzSSrjcW9NUcx3g3YiTarZfFkjhMBXVbKP2+GX32bzJHeVOf3RQwxmFQtzHpcu/s70VD/pdDeqhcJIPfRVjcGh3vC5K2nzwYWnSae6w/cnnoRnXlzjw4kFrl5MkN5t4/s7O2Skkmp84vFGbgP7+riz6PHJhav89OM8rlsnaacYey2DiN/pTA8DBKUNsLJS4uz4HJ9/OsTk2yvM3CgS+PDDj1gcOOSysa6bGkAkQiliLBXKYeD8Qgm30sPw8B7KhT4KC0GfwTQFsRgopZsac2tCDaZ0yP26GgbOHuwns7dKLneXfY8tMzRihIOyVlbcLYjwaDRjbEHY+JVYRppvvvRw3RqJhMNbZ3oZfekWb7znkD24JzTza9P3WJxLkbAbKneM+PJT+rBpcqXu4SF2ntqNWpGxNwu8fmrkX8N943qec+MV1otZLEuGpf/fXmrHM3z1mc98boajx2z6+hzqns/Ut6tMfZ1gvTRMIvDRFn/WSIRBECEFMbOfn79LMT1VBrEJwkC5A1hGCjspWh76tsw7IA165SRtlLbvD4ZoGFAksu2EOiqp3n5DCb+1d+cyt7a3teu/bgEtNZTrPht/G8mDvEzp4Oojl7u4CZw3jfbK2y6ZFAgFZXnkCGqXw/mazxmgEmTRYVItAjLNFWnw/F/MnksQRss1wwAAAABJRU5ErJggg==',
    '3': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAC80lEQVR4nL1WPUsjURQ972UyaGI+JIWgYrUIoiiijVXsVhHsBH+AiIWFu83CbiFbBqy0EksbO1vtxU1rIX6wYApB8FsTjTrjvOVcnOiyaCYk2QsDk/de7nnn3I+5an5+XudyOfv8/PwrgG8A4qiteUopbYz5ZYz5otLptBWNRr/btv3TcRzzckjVGNRorZXneTc6Fot9IjPXdV1u1AGMRjD6TmjXdZPhcDhijJDTqJ+pF6aaSL6U9TblMwoso9YaSr0e5zvXgpoV+GpK4fn5GcVisQTKMPDhe2NjIzzPqx0gnYVCIXR3d2NgYAAtLS0CdHR0hK2tLZycnCASicgFqgYkUD6fR1dXFxYXF//Zn5ycxMLCggAnEglRoipAn2FDQwPOzs6QzWZxdXWFvr4+9PT0IJlMYnp6Gnt7e7i/v4dlWe8yDQTIGzNGuVwOc3NzuLi4kDiurq4ik8mgv79f5GxtbcXu7i5s236XZWCGlPXx8RHX19el5CAw12hPT0/y27btD+NYUZbSaVtbG9rb28HGlE6nMTg4KHubm5s4Pj4WeT/K1ooYFgoFjI2NYXZ2tlR7XFtZWcHa2hqamprKlkZFrYwglPDy8hKnp6cSJ4JMTExgdHQUDw8PZZtAYIaUMB6PY3t7Gzs7OxKnzs5OTE1NicxMJkq6v78vl3gvaSpiSCdkwZJgXa6vr4uUjuNIFvMCd3d3H7IMBOi3r1QqJc4Yt9vbWymFWCwma/6ZcmZV0tZmZmakqDc2NiSWvb29GB8fL5XMwcEBotFo9VnKm9NJc3OzdJahoaG/9inp0tKSAEYikepbGyWj0+XlZYyMjKCjowPhcFjieXh4KDXIJs441qR5y0HLkgwki7dGALKnlOXAKgKkrGzevlM/SfwnyLfwLWCgEeMtAz8j/Y9wUNP+//F/zHCIunFdt/hy43oOU0aGqHw+/1splbGYFa8bNQfjIAzgRg8PD3upVCrjOM4PY0zBnx9rCaaU4iCcDYVCn/8A6yd34uDse8UAAAAASUVORK5CYII=',
    '4': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADP0lEQVR4nLWW34vUVRTAP/fe7+z82tw1pVVYJ0WE7EEk2TajFCGQWgzBzJAMooLoSfxFLxL0FGH/Qr1IDzkPEUXQU2tCJDlUaygWruyubI2t7eTsznydmXvk3vkObtDsfHecDvPl++XOuedzz7nnnnsUgJzkIHAGRQ5BUCh6IRLZEqawHFcfkVdyggMYzgEK20PYUqj2Nt3Xy0pOMoVmGOuRvYX9G+reMxrNhv8VRmS7ydigH2TPxD9ui2KI8ooS+M8uRfmZES4WFRV0iaIhiuuL/SxKkkFT5dHUnVgzg25w1gpnw93YkTdYlU0zX7zJjqsfsD09i0gzdj0B+s3Wwq/lQeSJw7z+2qt+/PJvN/j5p0/YnpnFisIsA9QrgblfuRbwTfAcz+8/iLXWP7WwSuDTsLPEBtrIu/OlYba9+A5DawbRWqG1RqmYmUpMoPPOBELh9gCTW9/m2V27qFYWKBZvRQpxcXQGOlPOs9KCcD69l32H3yQZaPKff8XtubmI10OgcmetDl+HOxh95QS5dWv4/sI4ty7mSWX7W1oYo72ydLAXdNo3l3VflraQfOE0O0dHuPL7JIWz7/NwEFKzUc2QOqVylVpWCIxatgi09bCBRhvh0j9rKY6+y9jYGJVKhR8v/kByaDPpLbtJ9TXXO5BOED62n28TewhrdtnapeTUf6/HAU3Ckp/JkTs1zpOPb0QaNarVCiQyWIF0oNDGcDcMEdPHp5+d46nxI2xdexdbV7hCvaKQOukLFFPFEuuHFv3Cg0QKqdVIG0sqSHkdV//vlBco191pNMvaa+uhrypK+LM+wBcL26jYBDq6oev1BvPZTRw5+h6bN21kYmKCj8+cZueqWfZlfiGjw7Ylrq2HXllgyJR4a/C7pX/4rM2rNCbZ7w+9C/Ezmeu8NHDZh9LNa5evHUPqplm7NLeUP3er7RyXCgX++uMRZiavMWz+ptFwvYR0F9JOUrWaQjXHnDzEOj3PSGo61s0a0KWktOXp7I37AzGXHbSqVzdQlxgtiVm+Rbd6jW6AbmLr6YyieZ0iTEctXFfQFbaJ0+51zA82E6z30PuNsJNjWn1IHsshLFMPEt62sGZP6lr9Q451DzF+Sj/oquBAAAAAAElFTkSuQmCC',
    '5': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAD1ElEQVR4nLVWS28bVRg9353r8dhxPHEc1Y9CcEJF4obKQhWUSIi3QpdFAnXDoxISO1Z0icSKfVCRUH5BN0UIqSAhsQkioCxo0xYlIg+3SW3XoXEak/iBZ+Z+aMYBCaWxRyk+kmXZd+ae73G+cy9NbG5N1S17pkHIsGMrgAT+JzAAnZn7I5Hp8KD5ya9Agx6/W+K/hAA5DnoBxewEhoa0vp0HX45BXaRj6wVF7gqR99UDsAKckGGIYMs+LTye3pG58HrU0nVRtVqGdP+AH7DbkYfAb6zMTAyWvp4VGljQgcgYBFIOSKnum1A7sq6ErGkIbpYRrGz/txZEEI6D2vHHYJmmP1J0ICRmsK5D39jAhYVryJlRWEL8W1rFDIMIP/y+hK9emwJME/Ch9MMzZIYKBmGs38HLw8N49ewbD31s79IlXKlWQfE4YNtde9q5pG6WmoaGbUEphXqjgUI+D1gWHGaEdB2rgQC4r8+bY/YhoM4l1TTotRoSZhJCCFRLJXw2N4fbqeMINZsI1OvYGJ8AxWJgNzsf6Jihq0LNshCWmve7XChgPn8HjdETsAYG0HzyBAK6Dq3Z9D0esuMqEWxmr3zMjNTJk/iiuoP+xh5ubf2Bb9bWcD2XAydT4EdVKUsN9GcVo2Akhp/wxiidSCB97k1vfVIpTC0u4dOf5/DdS69ARqJg9SgqdYdOKZARQnFlBaVKBbu1GmIhA6PjWRimiczTE/igWMCNpUWUzkxCU+0T4miELpmUuJF7Bh/O/wK7eA+2YUBulnH+2gI+vvA+yDDwVDaL0avf4q7joN3pIxLyvpM044NYfuttSCGgEcGSEt9/Po33ymWkR0YQDocRsqyumXUfCwA2EZJrqxhZWsRaKo3NRBID5Xs4DYYZj3tuU7l/H9uRCISrUuYjErovBgJApYKp1RV89Nyz+C2fx/pPszCjUbz+7jsIR6NeUPM3b2E5MwLNtT3VXamH95AI5NiQykEmm0UmlzvwyI+zs5jZ3cXemUkIpXyVVR5KZllQ8SHc1IP4+vJlZE6dwmB/v+c4W5UKZq8v4EoohJUXXoQmpWd9fkCJjeLhgRF5ljWwuoxjhSIie7ue5e3EYrg9Ng4nlfaE5GPobYpGJW/vPN+ZcJ9UaRJKkGd1TIBghnSUd/h6ZN1tzf6HsPuJzwxhtfZnjNuT7WblfvYD8gVuS9gl9LbolmW7DO6Fy9/+B0BETCDpErsT1ONrIkKtlgoG9KYICkEsZc+uiYpZBeJxGbRaM2NkL4uo0M72KV4nzeuSP237hNuGIJEw6/XpaDp58Wo63fgbJxOYa63CNrMAAAAASUVORK5CYII=',
    '6': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADdklEQVR4nLWW0WscVRTGf/fOzO7OTrrbZNOkSmyS1m20T4pCH1MUK/pkMU9WEGxBKirEBwOtGApFaB9E0Bf/BVEffNIiYizYQpEIbSUba1JsNnbTTTab7iab2Zl7ZWZNDUh2Z3X7Pc3M5Z7vfOec+80Vk5Na3vqB2GqVdw2YEJDSdA4alBRIrbksDMbF6Kg2M1VOWwZn636wHkJ0kDOAlhLhK8oyU+FRIZjwfLxGQh0nCyCUQktIB1J3m5KkbmiTPDgIHSoVoapOtq0ZxJaitsooJYhtO4Ln7e/NYNIGtoJWKx7CqCKMWpir9m0sswvDEJ0jDGrgueCqAgMjqxx+1mdwv4kCZq+X+P6LDPi9LWtlRlXmexpfLPLKO2WOn9iPIHF//egLitlrOeZ/6SFuS7TqgMKau8KxkyVePXEoHOZ8fonLl5ZACQ6MpJDynwSawYyizt1UdPcvcfzkMFpLZmf+5P1TRarLe7HiAttReJs9WLHm6iKfu7pf4bkxjeM4KO3x8bnb/HEzSSrjcW9NUcx3g3YiTarZfFkjhMBXVbKP2+GX32bzJHeVOf3RQwxmFQtzHpcu/s70VD/pdDeqhcJIPfRVjcGh3vC5K2nzwYWnSae6w/cnnoRnXlzjw4kFrl5MkN5t4/s7O2Skkmp84vFGbgP7+riz6PHJhav89OM8rlsnaacYey2DiN/pTA8DBKUNsLJS4uz4HJ9/OsTk2yvM3CgS+PDDj1gcOOSysa6bGkAkQiliLBXKYeD8Qgm30sPw8B7KhT4KC0GfwTQFsRgopZsac2tCDaZ0yP26GgbOHuwns7dKLneXfY8tMzRihIOyVlbcLYjwaDRjbEHY+JVYRppvvvRw3RqJhMNbZ3oZfekWb7znkD24JzTza9P3WJxLkbAbKneM+PJT+rBpcqXu4SF2ntqNWpGxNwu8fmrkX8N943qec+MV1otZLEuGpf/fXmrHM3z1mc98boajx2z6+hzqns/Ut6tMfZ1gvTRMIvDRFn/WSIRBECEFMbOfn79LMT1VBrEJwkC5A1hGCjspWh76tsw7IA165SRtlLbvD4ZoGFAksu2EOiqp3n5DCb+1d+cyt7a3teu/bgEtNZTrPht/G8mDvEzp4Oojl7u4CZw3jfbK2y6ZFAgFZXnkCGqXw/mazxmgEmTRYVItAjLNFWnw/F/MnksQRss1wwAAAABJRU5ErJggg==',
    '7': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAACq0lEQVR4nLWWy2oiQRSGT1V3R1tjRBeGkDtZZZOlbnThk7gcMtthniIPMPMOeQmRpMl1k02QEAIJiCCK4N3YVcN/mA5hGNvqGT3QNLbt+er/z6nyCCKii4uLU9/3z7TWSaWUFkIIWkJorbWUEukGlmV9LxaLP4TneV9s2/7Z7/dJCKGJaCmwP7hifX2dptPpqahWq30hRFwpJVcACwJKlVJqYsNGrSFspSGUUhYRJQA0rlnYwkxSaK21bQLDK1LC8fBQSi1alLBNYOPxmFqtFvm+/1clgKytrVEulyPbtkOh0mTVDw8PDEskEhSLxT6ueDzO91QqRd1ul+r1OjsRBpyrED+yLIsTAVSpVEIX1mg06Pz8nCaTCTmOMxc6Fwjr8CPXddlSz/NYCRQH3yWTSdrb22PA29sbzWYzXhyg81ojtIZBbY6Ojuju7o4TIhGUN5tNKhQK/N1oNKKbmxva3t4OdWEhMIBms1nKZDL8GTXq9Xqsolwu8wLu7+/Zhf39fYaHdfTiXv/U7rhD3fPzM52cnNDGxgYDrq6u6Pj4GEcXLdo+RsBAKZKhiQaDAZVKJX6ODobt6XQ6tDv/CYhtgNbP5/PcHNgq19fXXDvTPxhpCoSVqB0aB/Yhnp6e2GbUF/elAaEOG/z19ZXV4ERBPD4+8nNsD6hdGhB2ISFqt7Ozw2qHwyF1Oh3uYFOYMTCwE7YdHh6y4na7zRfUvr+/L7eGUkpWhKS7u7t8hzrsxeD0MQ3b5CUkRK2g9Pb2li18eXnhYw17L8oIZJu8BABmEth3eXnJAHTmwcHBaoAI1G1zc5O2trY+PkdpliAijRiw9jMk6jSpTUeMz/E/I6sQQqBLh1LK6N5EHxN9ZjmO8811Xev3wbuKeZGrBgZY7E+tVvuqlDrD3LjqUf8X7Xp+ZZZZdtoAAAAASUVORK5CYII=',
    '8': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADZElEQVR4nL2WXWgcVRiGnzMz2+yu6TaF7bpJ03SRGq1Goa0BS4VWvGiCYMESUxG8aSCKgjaN5MreiSJetGChN/bnQhQMtfhT7VVLoZBCFVqwWH9QsonRTZtks7Pdnd2ZOeVMZ3EomJ1kt743y5xz5jzn+86733wCQD7CAC4fIehSj4CgOZLeXpJJNA6KG4wLuYm9aHzhQ5oJq6m2p8TlJSG7mQQ6/clmw4JQpSkFlPcpsnvlMbT/CUYtrVpomBCgqeUBqWc1Hl7CCH82SfW2xDSgqgl0KXmg6hJtAXThzYdRKKCUglxFMN+7A6dvkEg6jbNYgAvf0Hr+LO1OCUMPWGMJ1UyzxApBriyZO/ABG98aIxaYcoDs998iRl+hy8rfdUQdLb1E07BLkn+e6Wfjm+94sOkfrnB5/15+OTOOjiTT9zyFfa9hWv49rxToha3pmEVo3bWbqIBC2SJ37H0e+vQ01pF3+XvqL6Rdpe3Zfop+nuRKgTUpP9i3i0jlHNtGzs0Sc4GFm0jXQRgRrHwedYVh9J+m8ZLj2LQmBPZnn2DuGyKRSpEcHuVaSwdrdz1Ne1cXxYJJ5eRh1vhE0bBpNMHiLcmPW7fRfWycjkyGCrAKmM3luDY6xJPffc26pA6uslFDKRWeFW+lk3S+PkZ7JoNlVTD/+J3iQp51qRSPHjjEzce6sS2nCaaJGMznJPbwQTbtGaC0WOCn98b4s6+X62+/ytz0NOu3PEXiwxPMSL0x0wh12orNwoYUbduf8yrJ3MQF4kcOszVWpvPMV8ycOoqUkuTmHszHt4ElEfeWv7BALz2OhHgUEY17G+ttSey2VVizJUoGRNrV9xocx4FItE5s9VLquhCLEP95EvPqhHfytVt6YeQQN3p2Yg4N8+CLL3uZMGemiE1cRP1ZvfdW7FKh4VYlv27YTOvHn7O+5wlvWBUVVbOV8vkC2TcGePjSOVpa6hfxELUUKkXIptOU9uxnTf8LxFYnqFhl5i9dxPjyOB3Xr7I6XutQaBCopGvIssuiC2ZEp4rAEBCv2iRcMOIa1Enl8oAEmgM3sFwFpYWH1UpbuBZD+puqa/KHvJeWASPQYoSLMgASDTRR2cDA/ZL0f7MaLiP+w7IjXQbsbkJcRjTxG+MIBr12vPnQf1t9waBi3QEGgEumGazWJQAAAABJRU5ErJggg==',
    '9': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADl0lEQVR4nL2WXWhcRRTHfzP37lc2ZnHTBqSiUIPSQqnaQiIGRAvRPvTBYqxFYqH4QRFBqWiCL/ZBa6xaHyJ+IQgqFKSCL0qpQioktoYUsZGg0Wizti7ppnGzyTb7cefI3I0Qxey91qR/uJedvTPzn3POf845qucq2pThdQXtHhgFmhWCAkSYBV6KFTl8AMqqp4E/HEXKA1mcs5IQ+4qBKimej83xgupNIgZErTyZDwGjwQAVFLfq1SSzsCGybFFFwvVI6dUk+wekwn8RiFJorf3TKamd0o7t/2F3AHDDTlUiFIuCREBcBZ6gLxkSccusEPH1EYhwhKLJV4Vr7upg484HSF+7jvyFHGeOHmFqYICkGJQSewUCoXqSNekuB60U0wvCtkOvcO+T+/92wirw8WsvM9j7LE2uQqyv/wUC1bjCLXm0142hdhwK88KG7gfpWiQ7l8lw9L13+f7b0/74/qeeYd2OHZQqNpwq0MK6hI7WFByHjq7diDEUikWO9O7n00ce46N9D3Mhl8NRwp2PPs58RULJXS/3QWlNuVihufU6Uutv8MfnJn7m16FBrndhbvwHRk9+7cftxk2bUM0pP4MQYGVdC+1ar1IGYwUhNK1ZQzydZroilEVoSKV8N7rJRlq23EK1JIFuXZbQutCNuxQms2THRv2NWta2sPPFQ7Ts6mL7wVfZenuHP9dxIyjlhFKpW++jESHleRzv7+emO7axtjnNbZ33+I/FzMWLXJ1OY4yHMdVQOUvXJfQ8YknFzMBXvP3QLkZOnOD871kmxn/kg76DDB0/5s+rFufJnRklEq155rIttBAjNCYh99kXfHh6mPT6VgrZHFMzUzz95SAihvO/TFDNTqMagzNOcKYR8CJR3GaXhWyeyeyIX2tu3tvNxs2bUUozcuxzEvbiE4y6hPYqVIqGpvY22vY9weSpIfITGVq3d9LZvcdP3pmzZxnuP0zCCVe/3UAD7T6JBJ33dYF9luC3TIa39uwmOjtHJKJ8kf0vQhsPN2ov+RifvPkGrVu2kmxIUijMMj78DSPvv0PpuzESiXBkoZK3hRVeyfYKEQdRGmWrQ9kjaiAa15gAZcqS5B2qPNk622AXerbV8mr10a5UwWSXVw//ar/8cr9k7CfP0BD70rL44wpARayFtiu5Am0iZeESDnktQt5dbJJXg88aEgVXFH3ROX7SONxt4KS1dIXdW/OaUFgQnovN0XcAzJ+S9nJQFahsRQAAAABJRU5ErJggg==',
    '10': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAEsUlEQVR4nLWWXWxURRTHfzP33l223e0uxdIubY2tpAGCIAWlxo8YEQgNfvKivuiriQ8SYsSQiB8Q5cGoPPigD8YP4oOJGGMgYKDVGCSaILQBpLK2lBKBLct22263u3tnzNyFhaW7hZhyks3emXPm/Gfm/M85IwIHWangIyQdaBQgmUnRpITm/YzkQ7rJCl8XSeEQJotGIGYYTHseQwiR4q2MYLvwd3vnmnmwa6KwUeTJaWiXtxnMiCQLBAkoi7B9MzChC2ot9LT66WwwJuZgebDLGmgQQqClJi8LTLJd4/w6H1f0uSuT5s8y65S3vByotzO77I4dcKVGXobWoVaqslUMtMRI10wgXcAS5LXGiVu0XWjFyTtcDiU4P/c8IgTSFR5fyskUwLxPwwjUxep4Wj/Lc4tfIFRdw5u/bmFP+x5sG+xxi4ePPMj6yJOsWLQCn99H/EKc7r+62DXnCy61JrDMxqYFFKA1NJ1oYvX4Wjobn2DVqlWEaoOeev7eNpTegzPp8OiRx3nnke20P7SsxNm6sXWEd0XYee4DUo2pwm2UAzTXa66w7mwdW6132fD8BkL1Ic/AVS5SSFxcmAX1vzewcemmItip46eIXxxmeUc7gWCAV5/aSM9nR/kuuhu/FlOIVKwqZjo4GmRh60IPLDWcIn4xjiUtjyDYGi7DY9ZqOjoeQClFX28fr/2wiVf+eJlDvxxCa01NfYjOtvXUDoZxfbqExSWAZiOj4VGOxv5k/759bP7kdfpifUVD7WicBNwbWUYgPAspJSdPnuTnuQc5trSXwyd+K9gJzYLoAiLDEZRdmjbFKzWMkgqGo8Ns7d+CGoA7gnN4Ub5UPL6SCt+4j7vqWpC2xM26DEz0o6sVti0YlGcYS4wRmhOiIRylaqIaVaYql0xJLUi0JYivSOD4HIQqTWo7ZzPbX1uIbdYlmUviOoYZmrRIk500JQWq/FU4rlM2MW5IC42dkZiKYOIxrQg8Ml0bikKsbyJT8tCcRMnKYEqbugPSkjjSQWrpxcnRDpZlebr05Dg5K1e2Zt5a7zOnUYKcP0t88mJhp36bJl8zcsLyymTUnUeoNuTx4fzIv6QD4x4v/h+gwXQlmUie3mQPbtr1HC+Zv5RFscU0H2lm+Z33eWQSSnDsbA+J+ktYJjSV8rCcmDhe/cmsQDXA/sRehs4MefFasvIe3r5/G9vq3mNN52pvTepCigP9P5FsHPPW3AhYvlt4eSlxbKdIBMskFdDbcoyv933F5jvfwKq2WNO55toGJzQf/7iTrrsP4EhRlnhTAUWhCIzMTnC87zgKhXQlp8N/e7Ux05Dhy0ufk/w0yTPLN9AYnecRqP+ffr7v2c23kW9INaW8dlaOesLfVaGPaGgYihJJ1nrxGmwZIF2T9lqPa2vECMwfbGNuqgFLS87NPkusOYasMfG+oT2Z1hvEdsfoqAxoktsyQS98m3ZTEg6TrtI08uIQ2wzKMPN6wIoxNGLnp3k+KHDc0kyr+MQogHpK+8pTrmyJmNbBLeiLYswkwjBGeh+V3gMzIwofMMaEdBmRWjOC7zaBFnwKAthCsyMLp6WlWUuew7fhpFdDNSpSbMkIdtCN+g+VT+0F+Aq1/wAAAABJRU5ErJggg=='
}

NUM_COLORS = {
    "1": "#E6DE00", "2": "#0092DD", "3": "#4C4C4C", "4": "#FF8C00",
    "5": "#00CCCC", "6": "#8B00C9", "7": "#BCBCBC", "8": "#E60000",
    "9": "#8B0000", "10": "#00AA00",
}

def _text_color(bg_hex):
    bg_hex = bg_hex.lstrip("#")
    r, g, b = int(bg_hex[0:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
    return "#000000" if (0.299*r + 0.587*g + 0.114*b) > 160 else "#FFFFFF"

class PK10App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PK10 鎶曟敞鍔╂墜"
        self.page.theme_mode = ft.ThemeMode.DARK
        # 绉诲姩绔€傞厤锛氫娇鐢?SafeArea 閬垮厤鐘舵€佹爮閬尅
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.AUTO
        
        # 涓诲鍣紝璁剧疆鑳屾櫙鑹?        self.main_container = ft.Container(
            expand=True,
            bgcolor="#0D1117",
            padding=16,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                spacing=8,
                controls=[]
            )
        )
        
        self.ball_images = {}
        self._load_balls()
        self._build_ui()
        
        # 浣跨敤 SafeArea 鍖呰９涓诲鍣?        self.page.add(ft.SafeArea(content=self.main_container))
        self._log("Flet 鐗堝惎鍔ㄥ畬鎴?v1.1", "SUCCESS")
    
    def _load_balls(self):
        for num, b64_str in _EMBEDDED_BALLS.items():
            try:
                self.ball_images[num] = ft.Image(
                    src_base64=b64_str, width=32, height=32, fit=ft.ImageFit.CONTAIN
                )
            except Exception as e:
                print(f"鍔犺浇鍙风爜鐞?{num} 澶辫触: {e}")
    
    def _build_ui(self):
        content = self.main_container.content
        
        # 鏍囬
        content.controls.extend([
            ft.Text("PK10 鎶曟敞鍔╂墜", size=22, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
            ft.Text("瀹屾暣鐗堬紙鍚?10 寮犲彿鐮佺悆鍥剧墖锛?, size=12, color="#8B949E"),
            ft.Divider(color="#30363D"),
        ])
        
        # 鍙风爜鐞冨睍绀?- 浣跨敤 Row 骞跺厑璁告崲琛?        ball_row = ft.Row(spacing=6, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        for n in range(1, 11):
            ns = str(n)
            if ns in self.ball_images:
                ball_row.controls.append(self.ball_images[ns])
            else:
                ball_row.controls.append(
                    ft.Container(
                        content=ft.Text(ns, size=12, color=_text_color(NUM_COLORS[ns]), weight=ft.FontWeight.BOLD),
                        width=32, height=32,
                        bgcolor=NUM_COLORS[ns],
                        border_radius=16,
                        alignment=ft.alignment.center,
                    )
                )
        content.controls.append(ball_row)
        content.controls.append(ft.Divider(color="#30363D"))
        
        # 鍔熻兘鎸夐挳鍖哄煙
        button_row = ft.Row(
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton(
                    "娴嬭瘯鐧诲綍", 
                    on_click=lambda e: self._log("鐧诲綍鍔熻兘寮€鍙戜腑...", "INFO"),
                    height=40,
                    style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: "#FFFFFF"}, bgcolor="#238636")
                ),
                ft.ElevatedButton(
                    "鍒锋柊寮€濂?, 
                    on_click=lambda e: self._log("鍒锋柊鍔熻兘寮€鍙戜腑...", "INFO"),
                    height=40,
                    style=ft.ButtonStyle(color={ft.ControlState.DEFAULT: "#FFFFFF"}, bgcolor="#1F6FEB")
                ),
            ]
        )
        content.controls.append(button_row)
        content.controls.append(ft.Divider(color="#30363D"))
        
        # 鏃ュ織鍖?        self.log_view = ft.ListView(
            expand=True, 
            spacing=4, 
            auto_scroll=True,
            height=200
        )
        content.controls.extend([
            ft.Text("鎿嶄綔鏃ュ織", size=14, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
            ft.Container(
                content=self.log_view,
                bgcolor="#161B22",
                border_radius=8,
                padding=8,
                expand=True
            )
        ])
    
    def _log(self, msg, level="INFO"):
        colors = {"INFO": "#79C0FF", "SUCCESS": "#3FB950", "ERROR": "#F85149", "WARNING": "#D29922"}
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {msg}"
        self.log_view.controls.append(
            ft.Text(log_line, size=11, color=colors.get(level, "#E6EDF3"), font_family="monospace")
        )
        if len(self.log_view.controls) > 100:
            self.log_view.controls = self.log_view.controls[-100:]
        self.page.update()

def main(page: ft.Page):
    PK10App(page)

if __name__ == "__main__":
    ft.app(target=main)
