#!/bin/sh

python main.py staff --token $GITHUB_TOKEN --org mattermost --include ccbrown --include MusikPolice --include stephenkiers --include rgarmsen2295 --include yuya-oc --json > staff.json
python main.py contributors --token $GITHUB_TOKEN --org mattermost --repo desktop --repo mmctl --repo mattermost-redux --repo mattermost-webapp --repo mattermost-server --repo mattermost-mobile --json > contributions.json
python summary.py --staff-json staff.json --contributions-json contributions.json --plot
python summary.py --staff-json staff.json --contributions-json contributions.json > summary.md

RESULT=$(curl -F 'files=@plots.png' -F 'files=@summary.md' -F "channel_id=$CHANNEL_ID" --header "authorization: Bearer $MATTERMOST_TOKEN" $MATTERMOST_URL/api/v4/files)
echo $RESULT
FILE_IDS=$(echo "
import json
data = json.loads('$RESULT')
print(json.dumps([data['file_infos'][0]['id'], data['file_infos'][1]['id']]))
" | python)
NEW_POST=$(echo "
import json
result = json.dumps({'channel_id': '$CHANNEL_ID', 'message': '#### Contributors stats', 'file_ids': $FILE_IDS})
print(result)
" | python)
curl -X POST --header "authorization: Bearer $MATTERMOST_TOKEN" $MATTERMOST_URL/api/v4/posts -d "$NEW_POST"
