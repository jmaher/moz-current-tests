import requests
import os
import json

def get_allrevs(pushrev):
    fname = '.cache/%s' % pushrev
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            data = json.load(f)
    else:
        # https://hg.mozilla.org/integration/autoland/json-automationrelevance/<pushrev>
        url = "https://hg.mozilla.org/integration/autoland/json-automationrelevance/%s" % pushrev
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
        data = response.json()
        with open(fname, 'w') as f:
            json.dump(data, f)

    if 'changesets' not in data:
        return [], None

    revs = []
    if 'pushdate' in data['changesets'][0]:
        pushdate = data['changesets'][0]['pushdate'][0]

    for item in data['changesets']:
        revs.append(item['node'])

    return revs, pushdate


with open("ML_data_raw.csv", 'r') as f:
    data = f.read()

revisions = {}
tests = []
for line in data.split('\n'):
    parts = line.split(',')
    rev = parts[0]
    if rev.strip() == "":
        continue
    test = "%s/%s" % (parts[1], parts[2])
    if test not in tests:
        tests.append(test)
    if rev not in revisions.keys():
        revisions[rev] = []
    revisions[rev].append(test)


dates = []
datemap = {}
for rev in revisions:
    revs, pushdate = get_allrevs(rev)
    if revs == []:
        # not on autoland
        continue
    dates.append(pushdate)
    datemap[pushdate] = [revs, None, tests, revisions[rev], []]
#    print(output)

dates.sort()
for date in dates:
    print(json.dumps(datemap[date]))
#print("min push: %s" % min_rev)
#print("max push: %s" % max_rev)
