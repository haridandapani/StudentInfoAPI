import json

def opener():
    rent = open("data/integration.json", "r")
    reinteg = open("data/reinteg.json", "w")
    jsoner = json.loads(rent.read())

    for i in range(len(jsoner)):
        times = jsoner[i]['meeting_times']
        newval = times.split('; ')
        jsoner[i]['meeting_times'] = newval
        reinteg.write(json.dumps(jsoner[i])+",\n")
    print(json.dumps(jsoner))

def separator():
    reinteg = open("data/reinteg.json", "r")
    info = open("data/studentinfo.json", "w")
    match = open("data/studentmatch.json", "w")
    jsoner = json.loads(reinteg.read())

    for i in range(len(jsoner)):
        elem = jsoner[i]
        infodict = {"id": elem["id"], "name": elem["name"], "meeting": elem["meeting"], "grade": elem["grade"], "years_of_experience": elem["years_of_experience"]}
        matchdict = {"id": elem["id"], "name": elem["name"], "horoscope": elem["horoscope"], "meeting_times": elem["meeting_times"],
                     "preferred_language": elem["preferred_language"], "marginalized_groups": elem["marginalized_groups"], "prefer_group": elem["prefer_group"]}
        print(infodict)
        print(matchdict)

        info.write(json.dumps(infodict)+",\n")
        match.write(json.dumps(matchdict)+",\n")

separator()
    
