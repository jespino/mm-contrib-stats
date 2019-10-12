import json
import click
import collections
import datetime
import matplotlib.pyplot as plt

def monthToInt(date):
    return int(datetime.datetime.fromisoformat(date + "-01").strftime('%s'))

def printData(data):
    print("#### Contributions Per Month")
    for month, number in data['contributions_per_month'].items():
        print("- {}: {} community contributions".format(month, number))
    print()

    print("#### Contributors Per Month")
    for month, users in data['contributors_per_month'].items():
        print("- {}: {} community contributors".format(month, len(users)))
    print()

    print("#### First time contributors Per Month")
    for month, users in data['new_contributors_per_month'].items():
        print("- {}: {} first time contributors".format(month, len(number)))
    print()

    print("#### Contributions Per User")
    contributions_per_user = collections.OrderedDict(sorted(data['contributions_per_user'].items(), key=lambda x: x[0]))
    for user, number in contributions_per_user.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### Top community contributors")
    top25 = collections.OrderedDict(sorted(data['contributions_per_user'].items(), key=lambda x: -x[1])[0:25])
    for user, number in top25.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### Top community contributors (Last year)")
    top25 = collections.OrderedDict(sorted(data['contributions_per_user_last_year'].items(), key=lambda x: -x[1])[0:25])
    for user, number in top25.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### First contribution Per User")
    for contrib in data['first_contributions']:
        print("- {}: {}".format(contrib['date'], contrib['user']))
    print()

def plotData(data):
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)

    plt.figure(figsize=(24, 18))

    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    y_top = max(data['contributions_per_month'].values())

    plt.ylim(0, y_top)
    plt.xlim(monthToInt(list(data['contributions_per_month'].keys())[0]), monthToInt(list(data['contributions_per_month'].keys())[-1]))

    plt.yticks(range(0, y_top + 1, int(y_top/20)), [str(x) for x in range(0, y_top + 1, int(y_top/20))], fontsize=14)
    xticks = []
    for x, tick in enumerate(data['contributions_per_month'].keys()):
        if x % 4 == 0:
            xticks.append("\n" + tick + "\n")
        elif x % 4 == 1:
            xticks.append("\n\n" + tick)
        elif x % 4 == 2:
            xticks.append("\n" + tick + "\n")
        else:
            xticks.append(tick + "\n\n")
    plt.xticks(list(map(monthToInt, data['contributions_per_month'].keys())), xticks, fontsize=10)

    for y in range(0, y_top + 1, int(y_top/20)):
        plt.plot(list(map(monthToInt, data['contributions_per_month'].keys())), [y]*len(data['contributions_per_month'].keys()), "--", lw=1, color="black", alpha=0.3, antialiased=True)

    for x in list(map(monthToInt, data['contributions_per_month'].keys())):
        plt.plot([x, x], [0, y_top], "--", lw=1, color="black", alpha=0.3, antialiased=True)

    plt.tick_params(axis="both", which="both", length=0, bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    plt.plot(list(map(monthToInt, data['contributions_per_month'].keys())), list(data['contributions_per_month'].values()), lw=2.5, color=tableau20[0], antialiased=True)
    plt.plot(list(map(monthToInt, data['contributors_per_month'].keys())), list(map(len, data['contributors_per_month'].values())), lw=2.5, color=tableau20[1], antialiased=True)
    plt.plot(list(map(monthToInt, data['new_contributors_per_month'].keys())), list(map(len, data['new_contributors_per_month'].values())), lw=2.5, color=tableau20[2], antialiased=True)

    label_pos = monthToInt(list(data['contributions_per_month'].keys())[-1]) + 60*60*24*30
    plt.text(label_pos, list(data['contributions_per_month'].values())[-1] - 0.5, 'Contributions Per Month', fontsize=14, color=tableau20[0])
    plt.text(label_pos, len(list(data['contributors_per_month'].values())[-1]) - 0.5, 'Contributors Per Month', fontsize=14, color=tableau20[1])
    plt.text(label_pos, len(list(data['new_contributors_per_month'].values())[-1]) - 0.5, 'New Contributors Per Month', fontsize=14, color=tableau20[2])

    plt.savefig("evolution.png", bbox_inches="tight")

@click.command()
@click.option('--staff-json', '-s', required=True, help='The json file with the staff data')
@click.option('--contributions-json', '-c', required=True, help='The json file with the contributions data', multiple=True, type=click.Path())
@click.option('--plot', '-p', is_flag=True)
def cli(staff_json, contributions_json, plot):
    staff = json.load(open(staff_json, "r"))
    community = []
    for contrib_json in contributions_json:
        community = community + json.load(open(contrib_json, "r"))

    contributions = filter(lambda x: x["user"] not in staff, community)
    contributions = sorted(contributions, key=lambda x: x["date"])

    first_contributions = []
    contributors = []
    contributions_per_month = collections.OrderedDict()
    contributors_per_month = collections.OrderedDict()
    contributions_per_user = collections.OrderedDict()
    contributions_per_user_last_year = {}
    for contribution in contributions:
        if contribution["user"] not in contributors:
            contributors.append(contribution["user"])
            first_contributions.append(contribution)

        if contribution["date"][0:7] in contributions_per_month:
            contributions_per_month[contribution["date"][0:7]] += 1
        else:
            contributions_per_month[contribution["date"][0:7]] = 1

        if contribution["date"][0:7] in contributors_per_month:
            contributors_per_month[contribution["date"][0:7]].add(contribution["user"])
        else:
            contributors_per_month[contribution["date"][0:7]] = set([contribution["user"]])

        if contribution["user"] in contributions_per_user:
            contributions_per_user[contribution["user"]] += 1
        else:
            contributions_per_user[contribution["user"]] = 1

        if datetime.datetime.fromisoformat(contribution["date"][0:10]) > (datetime.datetime.now() - datetime.timedelta(days=365)):
            if contribution["user"] in contributions_per_user_last_year:
                contributions_per_user_last_year[contribution["user"]] += 1
            else:
                contributions_per_user_last_year[contribution["user"]] = 1

    new_contributors_per_month = collections.OrderedDict()
    for contribution in first_contributions:
        if contribution["date"][0:7] in new_contributors_per_month:
            new_contributors_per_month[contribution["date"][0:7]].add(contribution["user"])
        else:
            new_contributors_per_month[contribution["date"][0:7]] = set([contribution["user"]])

    data = {
        'contributions_per_month': contributions_per_month,
        'contributors_per_month': contributors_per_month,
        'new_contributors_per_month': new_contributors_per_month,
        'contributions_per_user': contributions_per_user,
        'contributions_per_user': contributions_per_user,
        'contributions_per_user_last_year': contributions_per_user_last_year,
        'first_contributions': first_contributions,
    }

    if plot:
        plotData(data)
    else:
        printData(data)

if __name__ == "__main__":
    cli()
