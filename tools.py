from datetime import datetime


def dayOfYear():
    date = str(datetime.date(datetime.now()))
    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d = list(map(int, date.split("-")))
    if d[0] % 400 == 0:
        days[2] += 1
    elif d[0] % 4 == 0 and d[0] % 100 != 0:
        days[2] += 1
    for i in range(1, len(days)):
        days[i] += days[i-1]
    return days[d[1]-1]+d[2]


def get_templates(word):

    VOWLS = ["ما"[1], "ي", "و"]
    #    # first , size , vowls, bl, last
    opts = [



        # [True, True, True, True, True],  #im exact
        [True, False, True, True, True],  # exact no sise
        # [True, False, False, True, True],  # exact no size no vowls
        # [True, True, False, True, True],  # exact no vowls

        # [False, True, True, True, True],  #im no f
        # [False, False, True, True, True],  # no f  no sise
        # [False, False, False, True, True],  # no f no size no vowls
        # [False, True, False, True, True],  # no f no vowls

        # [True, True, True, False, True],  #im no bl
        # [True, False, True, False, True],  # no bl no sise
        # [True, False, False, False, True],  #im no bl no size no vowls
        # [True, True, False, False, True],  # no bl no vowls

        # [False, False, False, True, True], #r no f no size no vowls
        # [True, False, False, True, True],  #r  exact no size no vowls
        [False, False, False, True, True],#r
        [False, False, True, False, True],  # r

        [False, False, False, False, True]

    ]
    templates=[]

    for o in opts:
        isfirst=o[0]
        issize=o[1]
        isvowel=o[2]
        isb_last=o[3]
        islast=o[4]

        _template = ""

        if issize:
            print("issize: true")

            _template = "_" * len(word)
            _template = list(_template)
            if isfirst:
                _template[0] = word[0]
            if islast:
                _template[-1] = word[-1]
            if isb_last:
                _template[-2] = word[-2]
            if isvowel:
                for i in range(len(word)):
                    if word[i] in VOWLS:
                        _template[i] = word[i]
            _template = "".join(_template)

        else:
            print("issize: false")

            # just the outs
            outs = []
            if isfirst:
                outs.append(0)
            if islast:
                outs.append(len(word)-1)
            if isb_last:
                outs.append(len(word)-2)

            _template = "%"
            if isfirst:
                _template = word[0]
                _template += "%"
            if isvowel:
                for i in range(len(word)):
                    if word[i] in VOWLS:
                        if i not in outs:
                            _template += word[i]
                            _template += "%"
            if isb_last:
                _template += word[-2]
            if islast:
                _template += word[-1]
        if _template not in templates:
            templates.append(_template)
    return templates
