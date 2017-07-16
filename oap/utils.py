import json


def oap_make_json(data, tests):
    labels = []
    for item in data:
        if item[0]=="date_reported":
            for i in range(1,6):
                if item[i] and item[i] != "None":
                    labels.append(item[i].strftime("%d, %b %Y"))
                else:
                    labels.append('-')
    datasets = []
    color = ("violet", "blue", "green", "red", "grey", "cyan", "black", "yellow", "magenta", "pink" , "darkOrange", "indigo")
    dark_color = ("darkViolet", "darkBlue", "darkGreen", "darkRed", "darkGrey", "darkCyan" , "black", "darkYellow", "darkMagenta", "darkPink", "darkOrange", "darkIndigo", )
    for x, test in enumerate(tests):
        label = None
        data = []
        if test[0]:
            label = test[0].test_name
            data.append(int(test[0].result))
            for t, i in enumerate(test):
                if t >= 1:
                    try:
                        data.append(int(i.result))
                    except:
                        data.append(-1)
        datasets.append(
            {
                'label': label,
                'data': data,
                'fillColor': 'rgba(0,0,0,0)',
                'strokeColor': color[x],
                'pointColor': dark_color[x],

            }
        )

    return json.dumps({'labels': labels, 'datasets': datasets })

