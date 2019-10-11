import json
import click
import collections
import datetime

@click.command()
@click.option('--staff-json', '-s', required=True, help='The json file with the staff data')
@click.option('--contributions-json', '-c', required=True, help='The json file with the contributions data', multiple=True, type=click.Path())
def cli(staff_json, contributions_json):
    staff = json.load(open(staff_json, "r"))
    community = []
    for contrib_json in contributions_json:
        community = community + json.load(open(contrib_json, "r"))

    contributions = filter(lambda x: x["user"] not in staff, community)
    contributions = sorted(contributions, key=lambda x: x["date"])

    first_contributions = []
    contributors = []
    contributions_per_month = collections.OrderedDict()
    contributions_per_user = {}
    contributions_per_user_last_year = {}
    for contribution in contributions:
        if contribution["user"] not in contributors:
            contributors.append(contribution["user"])
            first_contributions.append(contribution)

        if contribution["date"][0:7] in contributions_per_month:
            contributions_per_month[contribution["date"][0:7]] += 1
        else:
            contributions_per_month[contribution["date"][0:7]] = 1

        if contribution["user"] in contributions_per_user:
            contributions_per_user[contribution["user"]] += 1
        else:
            contributions_per_user[contribution["user"]] = 1

        if datetime.datetime.fromisoformat(contribution["date"][0:10]) > (datetime.datetime.now() - datetime.timedelta(days=365)):
            if contribution["user"] in contributions_per_user_last_year:
                contributions_per_user_last_year[contribution["user"]] += 1
            else:
                contributions_per_user_last_year[contribution["user"]] = 1

    print("#### Contributions Per Month")
    for month, number in contributions_per_month.items():
        print("- {}: {} community contributions".format(month, number))
    print()

    # print("#### Contributions Per User")
    # print("----------------------")
    # for user, number in contributions_per_user.items():
    #     print("- {}: {} contributions".format(user, number))
    # print()

    print("#### Top community contributors")
    top25 = collections.OrderedDict(sorted(contributions_per_user.items(), key=lambda x: -x[1])[0:25])
    for user, number in top25.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### Top community contributors (Last year)")
    top25 = collections.OrderedDict(sorted(contributions_per_user_last_year.items(), key=lambda x: -x[1])[0:25])
    for user, number in top25.items():
        print("- {}: {} contributions".format(user, number))
    print()

    print("#### First contribution Per User (Last year)")
    for contrib in first_contributions:
        if datetime.datetime.fromisoformat(contrib["date"][0:10]) > (datetime.datetime.now() - datetime.timedelta(days=365)):
            print("- {}: {}".format(contrib['date'], contrib['user']))
    print()

if __name__ == "__main__":
    cli()
