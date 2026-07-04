# -*- coding: utf-8 -*-
"""
PK10 Lottery Betting Assistant - Flet v1.6
Fixed: Widget lifetime - all page widgets stored as page attributes
Fixed: Removed scroll complexity for mobile
"""
import flet as ft
import base64

# ===== Embedded Ball Images (base64, 28x28) =====
_EMBEDDED_BALLS = {
    '1': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAACSklEQVR4nO2WvWoUURTHf+fc2XXZDQmS1YghxRIQrLSIip0voI29rcTCRgK+g1jHQrQQfAbfIIIi2vhFzJoYYlK67kzczO49cmcTIyLkTrJ2/uFOc8+d35yPOfcIwFZb5wf4exgNM0wEYQSy/XeliC6cbvlF2VzRm/WGf9DtgjE62J/QsQZkmc7LxgpdFWreUBgt7DeZCt6MXiJCY2D/jrQrGRhOhbp6jx0GZibFipUAgRU8LMULEFVI3DAs3g9XFFSQpCyoWjV6P6D9ucm378eZmd6iOdmJhmocDCpVK7L+/mOVpZdXyPL7nJx+zIdP1wkV7lwcMDnYREgSY+3LGO21C1Sq1zg/d5XZ2dli993bF6QpTEzAYHBEYPDMOaPTqbDcvsHFy3dptWaKvTzvkSRVRPKQm2jpgf4JpJmjVmsVsDTt0M93cC5BClK5GteDDMxDoz5gJ1/m+dIzHj28zdfNVVQjk1YmpMEBbzA+nnOm9YS0+5RaZYp+/xiHVRJj1O/DqaltmmeN1fUTeH/4vqQxRsHTPFe6qUT/b0cCBokYqhZrfnTgqKT/gX+T6n6VlukyQdG3xZ4MIcs829vDAsrzckTZWAmjTATIhErFWFtv8urNOcwc3juak1tcmntNJfFF7x0ZcE9OwYW4hFMybPB5Hn8+KTsW9j30e/IrvBKeEvfNZliiioR+GUss7HYBARYrK4oNUYzMCRFX55FkBcPIVETv1Ou4Ygq2cvmMIoV3GhIYgVVEaKOttxiO+vV/MuoLqUMXplp+8SfgvfMUB1p3OQAAAABJRU5ErkJggg==',
    '10': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAEsUlEQVR4nLWWXWxURRTHfzP33l223e0uxdIubY2tpAGCIAWlxo8YEQgNfvKivuiriQ8SYsSQiB8Q5cGoPPigD8YP4oOJGGMgYKDVGCSaILQBpLK2lBKBLct22263u3tnzNyFhaW7hZhyks3emXPm/Gfm/M85IwIHWangIyQdaBQgmUnRpITm/YzkQ7rJCl8XSeEQJotGIGYYTHseQwiR4q2MYLvwd3vnmnmwa6KwUeTJaWiXtxnMiCQLBAkoi7B9MzChC2ot9LT66WwwJuZgebDLGmgQQqClJi8LTLJd4/w6H1f0uSuT5s8y65S3vByotzO77I4dcKVGXobWoVaqslUMtMRI10wgXcAS5LXGiVu0XWjFyTtcDiU4P/c8IgTSFR5fyskUwLxPwwjUxep4Wj/Lc4tfIFRdw5u/bmFP+x5sG+xxi4ePPMj6yJOsWLQCn99H/EKc7r+62DXnCy61JrDMxqYFFKA1NJ1oYvX4Wjobn2DVqlWEaoOeev7eNpTegzPp8OiRx3nnke20P7SsxNm6sXWEd0XYee4DUo2pwm2UAzTXa66w7mwdW6132fD8BkL1Ic/AVS5SSFxcmAX1vzewcemmItip46eIXxxmeUc7gWCAV5/aSM9nR/kuuhu/FlOIVKwqZjo4GmRh60IPLDWcIn4xjiUtjyDYGi7DY9ZqOjoeQClFX28fr/2wiVf+eJlDvxxCa01NfYjOtvXUDoZxfbqExSWAZiOj4VGOxv5k/759bP7kdfpifUVD7WicBNwbWUYgPAspJSdPnuTnuQc5trSXwyd+K9gJzYLoAiLDEZRdmjbFKzWMkgqGo8Ns7d+CGoA7gnN4Ub5UPL6SCt+4j7vqWpC2xM26DEz0o6sVti0YlGcYS4wRmhOiIRylaqIaVaYql0xJLUi0JYivSOD4HIQqTWo7ZzPbX1uIbdYlmUviOoYZmrRIk500JQWq/FU4rlM2MW5IC42dkZiKYOIxrQg8Ml0bikKsbyJT8tCcRMnKYEqbugPSkjjSQWrpxcnRDpZlebr05Dg5K1e2Zt5a7zOnUYKcP0t88mJhp36bJl8zcsLyymTUnUeoNuTx4fzIv6QD4x4v/h+gwXQlmUie3mQPbtr1HC+Zv5RFscU0H2lm+Z33eWQSSnDsbA+J+ktYJjSV8rCcmDhe/cmsQDXA/sRehs4MefFasvIe3r5/G9vq3mNN52pvTepCigP9P5FsHPPW3AhYvlt4eSlxbKdIBMskFdDbcoyv933F5jvfwKq2WNO55toGJzQf/7iTrrsP4EhRlnhTAUWhCIzMTnC87zgKhXQlp8N/e7Ux05Dhy0ufk/w0yTPLN9AYnecRqP+ffr7v2c23kW9INaW8dlaOesLfVaGPaGgYihJJ1nrxGmwZIF2T9lqPa2vECMwfbGNuqgFLS87NPkusOYasMfG+oT2Z1hvEdsfoqAxoktsyQS98m3ZTEg6TrtI08uIQ2wzKMPN6wIoxNGLnp3k+KHDc0kyr+MQogHpK+8pTrmyJmNbBLeiLYswkwjBGeh+V3gMzIwofMMaEdBmRWjOC7zaBFnwKAthCsyMLp6WlWUuew7fhpFdDNSpSbMkIdtCN+g+VT+0F+Aq1/wAAAABJRU5ErkJggg==',
    '2': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADpUlEQVR4nLWWXUwcVRTHf/fO7JfL8lGXUoirKEFpoo2aUoQaYxNSP5qaPjQm+tAH40OND0YT25g+NDFRw6N99cHERKMxMZpqwcZanpRUoYqAhlCoFvkoFFg+lmV35x4zs4Amsuw0wHmYzM49O//7P/P/n3sUZ0VTez1IMvcGWp8GStneMCilEfkRR72uoVMzL6eIlr8DEkNEthlQI0awg81o+VZxbqQBRTdKBTGO9hJ2IkQEbblUs+WES+7AyeV3s1OhlMI4YmPcEhpBqdvZLqrgr01CKWWv3fnKdy9aI+5nWQdxP7lBGePdFYtVQD+hEKVheYmy1Dg1K+NYYpgK3slkSS0SLvGAKaI5n4AK7eSoT/ZxiGGa791Nfd192AGL0b/HuPxbBxfmEoxU7fdYylYA3cKJtojPXeNszRjHT7xKIBReX28Ejj69ROMnH/Pm8FUmEwfRmUWMW40Nwrcqw5l57q7f64H1dv/ExW/O82tPN5lMBjsS5djRIxwMTkMqiVh2QZ7+SipCOlzOwNAI3//+EV8MLzMTS1A1dYlzL6Rpam4hWlnN49UhvpqYxInUoYyzIWRRQO9P4nCztJbTE4oVHSKVqIZoGTPzC8zcmvYs5jrLiFnT8naoFGYr6jwluv3Cmb9FkzXO3vsPe00kvTjPn4uCCUZBClvktjqLcjKgLJzlBVrGOnj7yMPcU9/gMRzs76V9QiNle9C5TEGmvhkqBLHDVEwN0Jrt563nW3iksclbG7s+xPsXuhiNH/LKvyVbrIFhBYlP/sJJu5fXTr5I/K5ab22ot4e2zzr4PPoE6Vg1KreCbNK4fAGKDsDiLMf4g1OvvEQsvsd73n6pk3e/vsLP1YdJlyYgm9oUzL/xRWhYGODlZx7zwIwxtF/8jjNfXmGq8kEqV26ix24wHUuwFIl7otkSQ/fo2i+j7Nv3LI7J98uQrXnvuUexdX5DAaP4tK+HD1IHkOguMLktAApUqhSRkn+nj9bW1v+lDU58iL4xixPbjTLZDY8tf4BaM6ir6On6gSzKe41ZZeo1a6UISo6rSQsT2YUyuYJK9ddptOJy7AAnzvdhZGNRuFr5q+wBJFrusduaD8WQClfQX/NkkTxn1YdFbeFjUhODcl+4WQrFBwebQCBfMxeziId8zy6FQkQ0JpQkvbCMe4Zt/0zKf8HyY+JDNUM4po1Q1F53+Q6gEQgpjElqOjGUWW0sz51B1GL+cPM1gPnF8piRy3Rhqaf+ARxEfqpayEYNAAAAAElFTkSuQmCC',
    '3': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAC80lEQVR4nL1WPUsjURQ972UyaGI+JIWgYrUIoiiijVXsVhHsBH+AiIWFu83CbiFbBqy0EksbO1vtxU1rIX6wYApB8FsTjTrjvOVcnOiyaCYk2QsDk/de7nnn3I+5an5+XudyOfv8/PwrgG8A4qiteUopbYz5ZYz5otLptBWNRr/btv3TcRzzckjVGNRorZXneTc6Fot9IjPXdV1u1AGMRjD6TmjXdZPhcDhijJDTqJ+pF6aaSL6U9TblMwoso9YaSr0e5zvXgpoV+GpK4fn5GcVisQTKMPDhe2NjIzzPqx0gnYVCIXR3d2NgYAAtLS0CdHR0hK2tLZycnCASicgFqgYkUD6fR1dXFxYXF//Zn5ycxMLCggAnEglRoipAn2FDQwPOzs6QzWZxdXWFvr4+9PT0IJlMYnp6Gnt7e7i/v4dlWe8yDQTIGzNGuVwOc3NzuLi4kDiurq4ik8mgv79f5GxtbcXu7i5s236XZWCGlPXx8RHX19el5CAw12hPT0/y27btD+NYUZbSaVtbG9rb28HGlE6nMTg4KHubm5s4Pj4WeT/K1ooYFgoFjI2NYXZ2tlR7XFtZWcHa2hqamprKlkZFrYwglPDy8hKnp6cSJ4JMTExgdHQUDw8PZZtAYIaUMB6PY3t7Gzs7OxKnzs5OTE1NicxMJkq6v78vl3gvaSpiSCdkwZJgXa6vr4uUjuNIFvMCd3d3H7IMBOi3r1QqJc4Yt9vbWymFWCwma/6ZcmZV0tZmZmakqDc2NiSWvb29GB8fL5XMwcEBotFo9VnKm9NJc3OzdJahoaG/9inp0tKSAEYikepbGyWj0+XlZYyMjKCjowPhcFjieXh4KDXIJs441qR5y0HLkgwki7dGALKnlOXAKgKkrGzevlM/SfwnyLfwLWCgEeMtAz8j/Y9wUNP+//F/zHCIunFdt/hy43oOU0aGqHw+/1splbGYFa8bNQfjIAzgRg8PD3upVCrjOM4PY0zBnx9rCaaU4iCcDYVCn/8A6yd34uDse8UAAAAASUVORK5CYII=',
    '4': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADP0lEQVR4nLWW34vUVRTAP/fe7+z82tw1pVVYJ0WE7EEk2TajFCGQWgzBzJAMooLoSfxFLxL0FGH/Qr1IDzkPEUXQU2tCJDlUaygWruyubI2t7eTsznydmXvk3vkObtDsfHecDvPl++XOuedzz7nnnnsUgJzkIHAGRQ5BUCh6IRLZEqawHFcfkVdyggMYzgEK20PYUqj2Nt3Xy0pOMoVmGOuRvYX9G+reMxrNhv8VRmS7ydigH2TPxD9ui2KI8ooS+M8uRfmZES4WFRV0iaIhiuuL/SxKkkFT5dHUnVgzg25w1gpnw93YkTdYlU0zX7zJjqsfsD09i0gzdj0B+s3Wwq/lQeSJw7z+2qt+/PJvN/j5p0/YnpnFisIsA9QrgblfuRbwTfAcz+8/iLXWP7WwSuDTsLPEBtrIu/OlYba9+A5DawbRWqG1RqmYmUpMoPPOBELh9gCTW9/m2V27qFYWKBZvRQpxcXQGOlPOs9KCcD69l32H3yQZaPKff8XtubmI10OgcmetDl+HOxh95QS5dWv4/sI4ty7mSWX7W1oYo72ydLAXdNo3l3VflraQfOE0O0dHuPL7JIWz7/NwEFKzUc2QOqVylVpWCIxatgi09bCBRhvh0j9rKY6+y9jYGJVKhR8v/kByaDPpLbtJ9TXXO5BOED62n28TewhrdtnapeTUf6/HAU3Ckp/JkTs1zpOPb0QaNarVCiQyWIF0oNDGcDcMEdPHp5+d46nxI2xdexdbV7hCvaKQOukLFFPFEuuHFv3Cg0QKqdVIG0sqSHkdV//vlBco191pNMvaa+uhrypK+LM+wBcL26jYBDq6oev1BvPZTRw5+h6bN21kYmKCj8+cZueqWfZlfiGjw7Ylrq2HXllgyJR4a/C7pX/4rM2rNCbZ7w+9C/Ezmeu8NHDZh9LNa5evHUPqplm7NLeUP3er7RyXCgX++uMRZiavMWz+ptFwvYR0F9JOUrWaQjXHnDzEOj3PSGo61s0a0KWktOXp7I37AzGXHbSqVzdQlxgtiVm+Rbd6jW6AbmLr6YyieZ0iTEctXFfQFbaJ0+51zA82E6z30PuNsJNjWn1IHsshLFMPEt62sGZP6lr9Q451DzF+Sj/oquBAAAAAAElFTkSuQmCC',
    '5': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAD1ElEQVR4nLVWS28bVRg9353r8dhxPHEc1Y9CcEJF4obKQhWUSIi3QpdFAnXDoxISO1Z0icSKfVCRUH5BN0UIqSAhsQkioCxo0xYlIg+3SW3XoXEak/iBZ+Z+aMYBCaWxRyk+kmXZd+ae73G+cy9NbG5N1S17pkHIsGMrgAT+JzAAnZn7I5Hp8KD5ya9Agx6/W+K/hAA5DnoBxewEhoa0vp0HX45BXaRj6wVF7gqR99UDsAKckGGIYMs+LTye3pG58HrU0nVRtVqGdP+AH7DbkYfAb6zMTAyWvp4VGljQgcgYBFIOSKnum1A7sq6ErGkIbpYRrGz/txZEEI6D2vHHYJmmP1J0ICRmsK5D39jAhYVryJlRWEL8W1rFDIMIP/y+hK9emwJME/Ch9MMzZIYKBmGs38HLw8N49ewbD31s79IlXKlWQfE4YNtde9q5pG6WmoaGbUEphXqjgUI+D1gWHGaEdB2rgQC4r8+bY/YhoM4l1TTotRoSZhJCCFRLJXw2N4fbqeMINZsI1OvYGJ8AxWJgNzsf6Jihq0LNshCWmve7XChgPn8HjdETsAYG0HzyBAK6Dq3Z9D0esuMqEWxmr3zMjNTJk/iiuoP+xh5ubf2Bb9bWcD2XAydT4EdVKUsN9GcVo2Akhp/wxiidSCB97k1vfVIpTC0u4dOf5/DdS69ARqJg9SgqdYdOKZARQnFlBaVKBbu1GmIhA6PjWRimiczTE/igWMCNpUWUzkxCU+0T4miELpmUuJF7Bh/O/wK7eA+2YUBulnH+2gI+vvA+yDDwVDaL0avf4q7joN3pIxLyvpM044NYfuttSCGgEcGSEt9/Po33ymWkR0YQDocRsqyumXUfCwA2EZJrqxhZWsRaKo3NRBID5Xs4DYYZj3tuU7l/H9uRCISrUuYjErovBgJApYKp1RV89Nyz+C2fx/pPszCjUbz+7jsIR6NeUPM3b2E5MwLNtT3VXamH95AI5NiQykEmm0UmlzvwyI+zs5jZ3cXemUkIpXyVVR5KZllQ8SHc1IP4+vJlZE6dwmB/v+c4W5UKZq8v4EoohJUXXoQmpWd9fkCJjeLhgRF5ljWwuoxjhSIie7ue5e3EYrg9Ng4nlfaE5GPobYpGJW/vPN+ZcJ9UaRJKkGd1TIBghnSUd/h6ZN1tzf6HsPuJzwxhtfZnjNuT7WblfvYD8gVuS9gl9LbolmW7DO6Fy9/+B0BETCDpErsT1ONrIkKtlgoG9KYICkEsZc+uiYpZBeJxGbRaM2NkL4uo0M72KV4nzeuSP237hNuGIJEw6/XpaDp58Wo63fgbJxOYa63CNrMAAAAASUVORK5CYII=',
    '6': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADdklEQVR4nLWW0WscVRTGf/fOzO7OTrrbZNOkSmyS1m20T4pCH1MUK/pkMU9WEGxBKirEBwOtGApFaB9E0Bf/BVEffNIiYizYQpEIbSUba1JsNnbTTTab7iab2Zl7ZWZNDUh2Z3X7Pc3M5Z7vfOec+80Vk5Na3vqB2GqVdw2YEJDSdA4alBRIrbksDMbF6Kg2M1VOWwZn636wHkJ0kDOAlhLhK8oyU+FRIZjwfLxGQh0nCyCUQktIB1J3m5KkbmiTPDgIHSoVoapOtq0ZxJaitsooJYhtO4Ln7e/NYNIGtoJWKx7CqCKMWpir9m0sswvDEJ0jDGrhueCqAgMjqxx+1mdwv4kCZq+X+P6LDPi9LWtlRlXmexpfLPLKO2WOn9iPIHF//egLitlrOeZ/6SFuS7TqgMKau8KxkyVePXEoHOZ8fonLl5ZACQ6MpJDynwSawYyizt1UdPcvcfzkMFpLZmf+5P1TRarLe7HiAttReJs9WLHm6iKfu7pf4bkxjeM4KO3x8bnb/HEzSSrjcW9NUcx3g3YiTarZfFkjhMBXVbKP2+GX32bzJHeVOf3RQwxmFQtzHpcu/s70VD/pdDeqhcJIPfRVjcGh3vC5K2nzwYWnSae6w/cnnoRnXlzjw4kFrl5MkN5t4/s7O2Skkmp84vFGbgP7+riz6PHJhav89OM8rlsnaacYey2DiN/pTA8DBKUNsLJS4uz4HJ9/OsTk2yvM3CgS+PDDj1gcOOSysa6bGkAkQiliLBXKYeD8Qgm30sPw8B7KhT4KC0GfwTQFsRgopZsac2tCDaZ0yP26GgbOHuwns7dKLneXfY8tMzRihIOyVlbcLYjwaDRjbEHY+JVYRppvvvRw3RqJhMNbZ3oZfekWb7znkD24JzTza9P3WJxLkbAbKneM+PJT+rBpcqXu4SF2ntqNWpGxNwu8fmrkX8N943qec+MV1otZLEuGpf/fXmrHM3z1mc98boajx2z6+hzqns/Ut6tMfZ1gvTRMIvDRFn/WSIRBECEFMbOfn79LMT1VBrEJwkC5A1hGCjspWh76tsw7IA165SRtlLbvD4ZoGFAksu2EOiqp3n5DCb+1d+cyt7a3teu/bgEtNZTrPht/G8mDvEzp4Oojl7u4CZw3jfbK2y6ZFAgFZXnkCGqXw/mazxmgEmTRYVItAjLNFWnw/F/MnksQRss1wwAAAABJRU5ErkJggg==',
    '7': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAACq0lEQVR4nLWWy2oiQRSGT1V3R1tjRBeGkDtZZZOlbnThk7gcMtthniIPMPMOeQmRpMl1k02QEAIJiCCK4N3YVcN/mA5hGNvqGT3QNLbt+er/z6nyCCKii4uLU9/3z7TWSaWUFkIIWkJorbWUEukGlmV9LxaLP4TneV9s2/7Z7/dJCKGJaCmwP7hifX2dptPpqahWq30hRFwpJVcACwJKlVJqYsNGrSFspSGUUhYRJQA0rlnYwkxSaK21bQLDK1LC8fBQSi1alLBNYOPxmFqtFvm+/1clgKytrVEulyPbtkOh0mTVDw8PDEskEhSLxT6ueDzO91QqRd1ul+r1OjsRBpyrED+yLIsTAVSpVEIX1mg06Pz8nCaTCTmOMxc6Fwjr8CPXddlSz/NYCRQH3yWTSdrb22PA29sbzWYzXhyg81ojtIZBbY6Ojuju7o4TIhGUN5tNKhQK/N1oNKKbmxva3t4OdWEhMIBms1nKZDL8GTXq9Xqsolwu8wLu7+/Zhf39fYaHdfTiXv/U7rhD3fPzM52cnNDGxgYDrq6u6Pj4GEcXLdo+RsBAKZKhiQaDAZVKJX6ODobt6XQ6tDv/CYhtgNbP5/PcHNgq19fXXDvTPxhpCoSVqB0aB/Yhnp6e2GbUF/elAaEOG/z19ZXV4ERBPD4+8nNsD6hdGhB2ISFqt7Ozw2qHwyF1Oh3uYFOYMTCwE7YdHh6y4na7zRfUvr+/L7eGUkpWhKS7u7t8hzrsxeD0MQ3b5CUkRK2g9Pb2li18eXnhYw17L8oIZJu8BABmEth3eXnJAHTmwcHBaoAI1G1zc5O2trY+PkdpliAijRiw9jMk6jSpTUeMz/E/I6sQQqBLh1LK6N5EHxN9ZjmO8811Xev3wbuKeZGrBgZY7E+tVvuqlDrD3LjqUf8X7Xp+ZZZZdtoAAAAASUVORK5CYII=',
    '8': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADZElEQVR4nL2WXWgcVRiGnzMz2+yu6TaF7bpJ03SRGq1Goa0BS4VWvGiCYMESUxG8aSCKgjaN5MreiSJetGChN/bnQhQMtfhT7VVLoZBCFVqwWH9QsonRTZtks7Pdnd2ZOeVMZ3EomJ1kt743y5xz5jzn+86733wCQD7CAC4fIehSj4CgOZLeXpJJNA6KG4wLuYm9aHzhQ5oJq6m2p8TlJSG7mQQ6/clmw4JQpSkFlPcpsnvlMbT/CUYtrVpomBCgqeUBqWc1Hl7CCH82SfW2xDSgqgl0KXmg6hJtAXThzYdRKKCUglxFMN+7A6dvkEg6jbNYgAvf0Hr+LO1OCUMPWGMJ1UyzxApBriyZO/ABG98aIxaYcoDs998iRl+hy8rfdUQdLb1E07BLkn+e6Wfjm+94sOkfrnB5/15+OTOOjiTT9zyFfa9hWv49rxToha3pmEVo3bWbqIBC2SJ37H0e+vQ01pF3+XvqL6Rdpe3Zfop+nuRKgTUpP9i3i0jlHNtGzs0Sc4GFm0jXQRgRrHwedYVh9J+m8ZLj2LQmBPZnn2DuGyKRSpEcHuVaSwdrdz1Ne1cXxYJJ5eRh1vhE0bBpNMHiLcmPW7fRfWycjkyGCrAKmM3luDY6xJPffc26pA6uslFDKRWeFW+lk3S+PkZ7JoNlVTD/+J3iQp51qRSPHjjEzce6sS2nCaaJGMznJPbwQTbtGaC0WOCn98b4s6+X62+/ytz0NOu3PEXiwxPMSL0x0wh12orNwoYUbduf8yrJ3MQF4kcOszVWpvPMV8ycOoqUkuTmHszHt4ElEfeWv7BALz2OhHgUEY17G+ttSey2VVizJUoGRNrV9xocx4FItE5s9VLquhCLEP95EvPqhHfytVt6YeQQN3p2Yg4N8+CLL3uZMGemiE1cRP1ZvfdW7FKh4VYlv27YTOvHn7O+5wlvWBUVVbOV8vkC2TcGePjSOVpa6hfxELUUKkXIptOU9uxnTf8LxFYnqFhl5i9dxPjyOB3Xr7I6XutQaBCopGvIssuiC2ZEp4rAEBCv2iRcMOIa1Enl8oAEmgM3sFwFpYWH1UpbuBZD+puqa/KHvJeWASPQYoSLMgASDTRR2cDA/ZL0f7MaLiP+w7IjXQbsbkJcRjTxG+MIBr12vPnQf1t9waBi3QEGgEumGazWJQAAAABJRU5ErkJggg==',
    '9': 'iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADl0lEQVR4nL2WXWhcRRTHfzP37lc2ZnHTBqSiUIPSQqnaQiIGRAvRPvTBYqxFYqH4QRFBqWiCL/ZBa6xaHyJ+IQgqFKSCL0qpQioktoYUsZGg0Wizti7ppnGzyTb7cefI3I0Qxey91qR/uJedvTPzn3POf845qucq2pThdQXtHhgFmhWCAkSYBV6KFTl8AMqqp4E/HEXKA1mcs5IQ+4qBKimej83xgupNIgZErTyZDwGjwQAVFLfq1SSzsCGybFFFwvVI6dUk+wekwn8RiFJorf3TKamd0o7t/2F3AHDDTlUiFIuCREBcBZ6gLxkSccusEPH1EYhwhKLJV4Vr7upg484HSF+7jvyFHGeOHmFqYICkGJQSewUCoXqSNekuB60U0wvCtkOvcO+T+/92wirw8WsvM9j7LE2uQqyv/wUC1bjCLXm0142hdhwK88KG7gfpWiQ7l8lw9L13+f7b0/74/qeeYd2OHZQqNpwq0MK6hI7WFByHjq7diDEUikWO9O7n00ce46N9D3Mhl8NRwp2PPs58RULJXS/3QWlNuVihufU6Uutv8MfnJn7m16FBrndhbvwHRk9+7cftxk2bUM0pP4MQYGVdC+1ar1IGYwUhNK1ZQzydZroilEVoSKV8N7rJRlq23EK1JIFuXZbQutCNuxQms2THRv2NWta2sPPFQ7Ts6mL7wVfZenuHP9dxIyjlhFKpW++jESHleRzv7+emO7axtjnNbZ33+I/FzMWLXJ1OY4yHMdVQOUvXJfQ8YknFzMBXvP3QLkZOnOD871kmxn/kg76DDB0/5s+rFufJnRklEq155rIttBAjNCYh99kXfHh6mPT6VgrZHFMzUzz95SAihvO/TFDNTqMagzNOcKYR8CJR3GaXhWyeyeyIX2tu3tvNxs2bUUozcuxzEvbiE4y6hPYqVIqGpvY22vY9weSpIfITGVq3d9LZvcdP3pmzZxnuP0zCCVe/3UAD7T6JBJ33dYF9luC3TIa39uwmOjtHJKJ8kf0vQhsPN2ov+RifvPkGrVu2kmxIUijMMj78DSPvv0PpuzESiXBkoZK3hRVeyfYKEQdRGmWrQ9kjaiAa15gAZcqS5B2qPNk622AXerbV8mr10a5UwWSXVw//ar/8cr9k7CfP0BD70rL44wpARayFtiu5Am0iZeESDnktQt5dbJJXg88aEgVXFH3ROX7SONxt4KS1dIXdW/OaUFgQnovN0XcAzJ+S9nJQFahsRQAAAABJRU5ErkJggg==',
}

def main(page: ft.Page):
    page.title = "PK10 Betting"
    page.theme_mode = ft.ThemeMode.DARK

    # Store ALL widgets as page attributes to prevent garbage collection
    page.ball_images = {}
    page.selected_nums = {}
    page.current_period_val = ft.Text("--", size=13, color="#E6EDF3")
    page.open_code_val = ft.Text("--", size=13, color="#E6EDF3")
    page.balance_val = ft.Text("--", size=14, color="#E6EDF3")
    page.selected_display = ft.Text("--", size=12, color="#E6EDF3")
    page.log_val = ft.Text("--", size=11, font_family="monospace", color="#8B949E")

    # Build ball images
    for n in range(1, 11):
        key = str(n)
        if key in _EMBEDDED_BALLS:
            page.ball_images[key] = ft.Image(
                src_base64=_EMBEDDED_BALLS[key],
                width=28, height=28
            )
        else:
            page.ball_images[key] = ft.Text(str(n), size=14, color="#E6EDF3")

    # Bet amount field (stored on page too)
    page.bet_amount = ft.TextField(
        value="10", width=80, text_size=14,
        on_change=lambda e: _update_selected(page)
    )

    # ---- Callbacks (defined before use) ----

    def toggle_ball(e):
        n = int(e.control.data)
        key = str(n)
        if key in page.selected_nums:
            del page.selected_nums[key]
        else:
            page.selected_nums[key] = page.bet_amount.value or "10"
        _update_selected(page)

    def _update_selected(e=None):
        if page.selected_nums:
            nums = sorted(page.selected_nums.keys(), key=lambda x: int(x))
            parts = [f"#{n}({page.selected_nums[n]})" for n in nums]
            page.selected_display.value = ", ".join(parts)
        else:
            page.selected_display.value = "--"
        page.update()

    def on_login(e):
        page.log_val.value = page.log_val.value + "[LOGIN] clicked\n"
        page.update()

    def on_bet(e):
        if not page.selected_nums:
            page.log_val.value = page.log_val.value + "[BET] No numbers selected!\n"
        else:
            keys = str(list(page.selected_nums.keys()))
            page.log_val.value = page.log_val.value + f"[BET] selected: {keys}\n"
        page.update()

    # ---- Build ball row ----
    ball_row = ft.Row(
        controls=[page.ball_images[str(n)] for n in range(1, 11)],
        spacing=4
    )

    # ---- Build ball buttons ----
    ball_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                text=str(n), data=n,
                on_click=toggle_ball,
                width=36, height=36, padding=0
            )
            for n in range(1, 11)
        ],
        spacing=4
    )

    # ---- Main column ----
    main_col = ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Column([
                    ft.Text("PK10 Betting", size=16, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
                    ft.Row([
                        ft.Text("Period: ", size=12, color="#8B949E"),
                        page.current_period_val,
                        ft.Text("  Code: ", size=12, color="#8B949E"),
                        page.open_code_val,
                    ]),
                ]),
                bgcolor="#161B22", padding=10, border_radius=6
            ),
            # Balls
            ft.Container(
                content=ft.Column([
                    ft.Text("Balls 1-10:", size=13, color="#E6EDF3"),
                    ball_row,
                    ball_buttons,
                    ft.Row([
                        ft.Text("Amount:", size=12, color="#8B949E"),
                        page.bet_amount,
                        ft.Text(" Selected:", size=12, color="#8B949E"),
                        page.selected_display,
                    ]),
                ]),
                bgcolor="#161B22", padding=10, border_radius=6
            ),
            # Account
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Account", size=14, color="#E6EDF3"),
                        ft.Container(expand=True),
                        page.balance_val,
                        ft.Text(" Balance", size=12, color="#8B949E"),
                    ]),
                    ft.Text("Username", size=11, color="#8B949E"),
                    ft.TextField(width=200, text_size=13),
                    ft.Text("Password", size=11, color="#8B949E"),
                    ft.TextField(width=200, text_size=13, password=True),
                    ft.Text("Verify", size=11, color="#8B949E"),
                    ft.TextField(width=100, text_size=13),
                    ft.Row([
                        ft.ElevatedButton("Login", on_click=on_login, width=90),
                        ft.ElevatedButton("Bet", on_click=on_bet, width=90),
                    ]),
                ]),
                bgcolor="#161B22", padding=10, border_radius=6
            ),
            # Log
            ft.Container(
                content=ft.Column([
                    ft.Text("Log:", size=13, color="#E6EDF3"),
                    page.log_val,
                ]),
                bgcolor="#161B22", padding=10, border_radius=6
            ),
        ],
        spacing=8
    )

    # ---- Add to page ----
    page.add(main_col)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
