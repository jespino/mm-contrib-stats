#!/usr/bin/env python

import requests
import json as jsonlib
import click
import csv as csvlib
import sys
from jinja2 import Template

ORGANIZATION = "mattermost"

def graphql_query(query, github_token):
    headers = {"Authorization": "Bearer {}".format(github_token)}
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    raise Exception("Query failed to run by returning code of {}.".format(request.status_code))

def gen_query(org, repo, cursor = ""):
    return Template("""
    {
      repository(name: "{{repo}}", owner: "{{org}}") {
        name
        pullRequests(first: 100, states: [MERGED] {%if cursor %}, after: "{{cursor}}"{% endif %}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            number
            mergedAt
            author {
              login
            }
          }
        }
      }
    }
    """).render(repo=repo, cursor=cursor, org=org)

def gen_staff_query(org, cursor = ""):
    return Template("""
    {
      organization(login: "{{org}}") {
        membersWithRole(first: 100 {%if cursor %}, after: "{{cursor}}"{% endif %}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            login
          }
        }
      }
    }
    """).render(org=org, cursor=cursor)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--token', '-t', prompt='Your Github access token', help='The token used to authenticate the user against Github.')
@click.option('--org', '-o', prompt='Organization', help='The organization containing the repo. E.g. mattermost')
@click.option('--repo', '-r', prompt='Repository', help='The repository which contains the issues. E.g. mattermost-server', multiple=True)
@click.option('--json', '-j', help='The output is going to be a JSON', is_flag=True)
@click.option('--csv', '-c', help='The output is going to be a CSV', is_flag=True)
def contributors(token, org, repo, json, csv):
    data = []

    if json and csv:
        print("Error: you can't use --csv and --json flags at the same time")
        return

    writer = csvlib.writer(sys.stdout)
    if csv:
        writer.writerow(["PR", "Merged At", "Author"])

    for one_repo in repo:
        has_next = True
        cursor = ""
        while has_next:
            query = gen_query(org, one_repo, cursor)
            try:
                result = graphql_query(query, token) # Execute the query
            except Exception as e:
                print(e)
                return

            pull_requests = result["data"]["repository"]["pullRequests"]
            has_next = pull_requests["pageInfo"]["hasNextPage"]
            cursor = pull_requests["pageInfo"]["endCursor"]

            for node in pull_requests["nodes"]:
                if node and node["author"]:
                    if json:
                        data.append({
                            "date": node["mergedAt"],
                            "user": node["author"]["login"],
                            "pr": node["number"],
                            "repo": one_repo,
                        })
                    elif csv:
                        writer.writerow([node["number"], node["mergedAt"], node["author"]["login"]])
                    else:
                        print("PR {} (Merged: {}): {}".format(node["number"], node["mergedAt"], node["author"]["login"]))

    if json:
        print(jsonlib.dumps(data))

@cli.command()
@click.option('--token', '-t', prompt='Your Github access token', help='The token used to authenticate the user against Github.')
@click.option('--org', '-o', prompt='Organization', help='The organization containing the staff members')
@click.option('--json', '-j', help='The output is going to be a JSON', is_flag=True)
@click.option('--csv', '-c', help='The output is going to be a CSV', is_flag=True)
@click.option('--exclude', help='Exclude a user by username', multiple=True)
@click.option('--include', help='Include a user by username', multiple=True)
def staff(token, org, json, csv, exclude, include):
    data = []

    if json and csv:
        print("Error: you can't use --csv and --json flags at the same time")
        return

    writer = csvlib.writer(sys.stdout)
    if csv:
        writer.writerow(["Username"])

    has_next = True
    cursor = ""
    while has_next:
        query = gen_staff_query(org, cursor)
        try:
            result = graphql_query(query, token) # Execute the query
        except Exception as e:
            print(e)
            return
        members = result["data"]["organization"]["membersWithRole"]
        has_next = members["pageInfo"]["hasNextPage"]
        cursor = members["pageInfo"]["endCursor"]

        for node in members["nodes"]:
            if node and node["login"]:
                if node["login"] in exclude:
                    continue

                if json:
                    data.append(node["login"])
                elif csv:
                    writer.writerow([node["login"]])
                else:
                    print("Username: {}".format(node["login"]))

        for user in include:
            if json:
                data.append(user)
            elif csv:
                writer.writerow([user])
            else:
                print("Username: {}".format(user))

    if json:
        print(jsonlib.dumps(data))

if __name__ == "__main__":
    cli()
