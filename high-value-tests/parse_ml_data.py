import requests
import os
import json

def get_allrevs(pushrev):
    fname = '.cache/%s' % pushrev
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            retVal = json.load(f)
        return retVal
    
    # https://hg.mozilla.org/integration/autoland/json-automationrelevance/<pushrev>
    url = "https://hg.mozilla.org/integration/autoland/json-automationrelevance/%s" % pushrev
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    data = response.json()
    revs = []
    if 'changesets' not in data:
        return []

    for item in data['changesets']:
        revs.append(item['node'])

    # TODO: write fname
    with open(fname, 'w') as f:
        json.dump(revs, f)

    return revs


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


for rev in revisions:
    revs = get_allrevs(rev)
    if revs == []:
        # not on autoland
        continue
    output = [revs, None, tests, revisions[rev], []]
    print(output)
