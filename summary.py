import json
import click
import collections
import datetime
import matplotlib.pyplot as plt

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


def monthToInt(date):
    return int(datetime.datetime.fromisoformat(date + "-01").strftime('%s'))

def printData(data):
    print("## Documentation and Platform Contributors Stats")
    print()
    print("The Mattermost repositories included in this summary are: mattermost-server, mattermost-webapp, mattermost-redux, mattermost-mobile, desktop, mattermost-utilities, mmctl, mattermost-load-test, mattermost-android-classic, mattermost-ios-classic, mattermost-push-proxy, docs, mattermost-api-reference, mattermost-developer-documentation.")
    print()

    print("#### Contributions Per Month")
    for month, number in data['contributions_per_month'].items():
        print("- {}: {} community contributions".format(month, number))
    print()

    print("#### Contributions Per Month (Accumulative)")
    for month, number in data['accumulative_contributions_per_month'].items():
        print("- {}: {} community contributions".format(month, number))
    print()

    print("#### Active contributions Per Month (Active in last 3 months)")
    for month, users in data['active_contributors'].items():
        print("- {}: {} community contributions".format(month, len(users)))
    print()

    print("#### Contributors Per Month")
    for month, users in data['contributors_per_month'].items():
        print("- {}: {} community contributors".format(month, len(users)))
    print()

    print("#### First time contributors Per Month")
    for month, users in data['new_contributors_per_month'].items():
        print("- {}: {} first time contributors".format(month, len(users)))
    print()

    print("#### First time contributors Per Month (Accumulative)")
    for month, users in data['accumulative_new_contributors_per_month'].items():
        print("- {}: {} first time contributors".format(month, users))
    print()

    print("#### Old Contributors Per Month")
    for month in data['contributors_per_month'].keys():
        total = len(data['contributors_per_month'][month]) - len(data['new_contributors_per_month'][month])
        print("- {}: {} community contributors".format(month, total))
    print()

    print("#### Contributions Per User")
    contributions_per_user = collections.OrderedDict(sorted(data['contributions_per_user'].items(), key=lambda x: x[0]))
    for user, number in contributions_per_user.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### Top community contributors (all time)")
    top25 = collections.OrderedDict(sorted(data['contributions_per_user'].items(), key=lambda x: -x[1])[0:25])
    for user, number in top25.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### Top community contributors (2019)")
    top25 = collections.OrderedDict(sorted(data['contributions_per_user_last_year'].items(), key=lambda x: -x[1])[0:25])
    for user, number in top25.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### First contribution Per User")
    for contrib in data['first_contributions']:
        print("- {}: {} (repo: {})".format(contrib['date'], contrib['user'], contrib['repo']))
    print()

    month, users = list(data['contributors_per_month'].items())[-1]
    print("#### This month contributors (month: {})".format(month))
    for user in sorted(users, key=str.casefold):
        print("- {}".format(user))
    print()

    month, users = list(data['contributors_per_month'].items())[-2]
    print("#### Last month contributors (month: {})".format(month))
    for user in sorted(users, key=str.casefold):
        print("- {}".format(user))
    print()

def plotHistogramOfContributions(contributions_per_user, label, color, idx):
    ax = plt.subplot(8, 1, idx)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    values = list(contributions_per_user.values())
    total_one_time_contributors = len(list(filter(lambda x: x == 1, values)))
    total_two_times_contributors = len(list(filter(lambda x: x == 2, values)))
    total_three_times_contributors = len(list(filter(lambda x: x == 3, values)))
    values = list(filter(lambda x: x != 1 and x != 2 and x != 3, values))
    plt.tick_params(axis="both", which="both", length=0, bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
    plt.xticks(range(4, max(values), 5))
    plt.xlim(4, max(values))
    plt.hist(list(values), bins=max(values)-3)
    plt.xlabel(
        "Plus:  {} one time contributors | {} two times contributors | {} three times contributors".format(
            total_one_time_contributors,
            total_two_times_contributors,
            total_three_times_contributors,
        ),
        fontsize=14
    )

def plotPerMonthData(months, values, label, color, idx):
    ax = plt.subplot(8, 1, idx)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    y_top = max(values)

    plt.ylim(0, y_top)
    plt.xlim(monthToInt(months[0]), monthToInt(months[-1]))

    plt.yticks(range(0, y_top + 1, int(y_top/10)), [str(x) for x in range(0, y_top + 1, int(y_top/10))], fontsize=14)
    xticks = []
    for x, tick in enumerate(months):
        if x % 4 == 0:
            xticks.append("\n" + tick + "\n")
        elif x % 4 == 1:
            xticks.append("\n\n" + tick)
        elif x % 4 == 2:
            xticks.append("\n" + tick + "\n")
        else:
            xticks.append(tick + "\n\n")
    plt.xticks(list(map(monthToInt, months)), xticks, fontsize=9)

    for y in range(0, y_top + 1, int(y_top/10)):
        plt.plot(list(map(monthToInt, months)), [y]*len(months), "--", lw=1, color="black", alpha=0.3, antialiased=True)

    for x in list(map(monthToInt, months)):
        plt.plot([x, x], [0, y_top], "--", lw=1, color="black", alpha=0.3, antialiased=True)

    plt.tick_params(axis="both", which="both", length=0, bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    plt.plot(list(map(monthToInt, months)), list(values), lw=2.5, color=color, antialiased=True)

    label_pos = monthToInt(months[-1]) + 60*60*24*30
    plt.text(label_pos, y_top / 3, label, fontsize=14, color=color)

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

    accumulative_contributions_per_month = collections.OrderedDict()
    last_month = 0
    for month, contributions in contributions_per_month.items():
        accumulative_contributions_per_month[month] = last_month + contributions
        last_month = accumulative_contributions_per_month[month]

    new_contributors_per_month = collections.OrderedDict()
    for contribution in first_contributions:
        if contribution["date"][0:7] in new_contributors_per_month:
            new_contributors_per_month[contribution["date"][0:7]].add(contribution["user"])
        else:
            new_contributors_per_month[contribution["date"][0:7]] = set([contribution["user"]])

    accumulative_new_contributors_per_month = collections.OrderedDict()
    last_month = 0
    for month, contributors in new_contributors_per_month.items():
        accumulative_new_contributors_per_month[month] = last_month + len(contributors)
        last_month = accumulative_new_contributors_per_month[month]

    active_contributors = collections.OrderedDict()
    last_months = []
    for month, contributors in contributors_per_month.items():
        active_contributors[month] = contributors
        for m in last_months:
            active_contributors[month] = active_contributors[month].union(m)
        last_months = [contributors] + last_months
        last_months = last_months[0:4]

    data = {
        'contributions_per_month': contributions_per_month,
        'accumulative_contributions_per_month': accumulative_contributions_per_month,
        'active_contributors': active_contributors,
        'contributors_per_month': contributors_per_month,
        'new_contributors_per_month': new_contributors_per_month,
        'accumulative_new_contributors_per_month': accumulative_new_contributors_per_month,
        'contributions_per_user': contributions_per_user,
        'contributions_per_user': contributions_per_user,
        'contributions_per_user_last_year': contributions_per_user_last_year,
        'first_contributions': first_contributions,
    }

    if plot:
        plt.figure(figsize=(20, 30))

        months = list(contributions_per_month.keys())
        plotPerMonthData(months, list(contributions_per_month.values()), "Contributions\nPer Month", tableau20[0], 1)
        plotPerMonthData(months, list(accumulative_contributions_per_month.values()), "Contributions\nPer Month\n(Accumulative)", tableau20[1], 2)
        plotPerMonthData(months, list(map(len, contributors_per_month.values())), "Contributors\nPer Month", tableau20[2], 3)
        plotPerMonthData(months, list(map(len, new_contributors_per_month.values())), "New Contributors\nPer Month", tableau20[3], 4)
        plotPerMonthData(months, list(accumulative_new_contributors_per_month.values()), "New Contributors\nPer Month\n(Accumulative)", tableau20[4], 5)
        old_contributors_per_month = list(map(lambda month: len(contributors_per_month[month]) - len(new_contributors_per_month[month]), months))
        plotPerMonthData(months, old_contributors_per_month, "Old Contributors\nPer Month", tableau20[5], 6)
        plotHistogramOfContributions(contributions_per_user, "Contributions\nper user", tableau20[6], 7)
        plotPerMonthData(months, list(map(len, active_contributors.values())), "Active Contributions\nPer Month", tableau20[7], 8)

        plt.savefig("plots.png", bbox_inches="tight")
    else:
        printData(data)

if __name__ == "__main__":
    cli()
