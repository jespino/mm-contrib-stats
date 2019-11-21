#!/bin/sh

python main.py staff --token $GITHUB_TOKEN --org mattermost --include ccbrown --include MusikPolice --include stephenkiers --include rgarmsen2295 --include yuya-oc --include DavidLu1997 --include thekiiingbob --include atti1a --include JeffSchering --include comharris --include james-mm --include doosp --include willstacey --include yangchen1 --include cvitter --include Matterchen --include rqtaylor --include greensteve --include JustinReynolds-MM --json > staff.json
python main.py contributors --token $GITHUB_TOKEN --org mattermost --repo desktop --repo mattermost-utilities --repo mmctl --repo mattermost-redux --repo mattermost-webapp --repo mattermost-server --repo mattermost-mobile --repo mattermost-load-test --repo mattermost-android-classic  --repo mattermost-ios-classic --repo mattermost-push-proxy --repo docs --repo mattermost-api-reference --repo mattermost-developer-documentation  --json > contributions.json
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
result = json.dumps({'channel_id': '$CHANNEL_ID', 'message': '#### Documentation and Platform Contributors stats\n\nThe repositories included in this summary are: [desktop](https://github.com/mattermost/desktop) [mattermost-utilities](https://github.com/mattermost/mattermost-utilities) [mmctl](https://github.com/mattermost/mmctl) [mattermost-redux](https://github.com/mattermost/mattermost-redux) [mattermost-webapp](https://github.com/mattermost/mattermost-webapp) [mattermost-server](https://github.com/mattermost/mattermost-server) [mattermost-mobile](https://github.com/mattermost/mattermost-mobile) [mattermost-load-test](https://github.com/mattermost/mattermost-load-test) [mattermost-android-classic](https://github.com/mattermost/mattermost-android-classic)  [mattermost-ios-classic](https://github.com/mattermost/mattermost-ios-classic) [mattermost-push-proxy](https://github.com/mattermost/mattermost-push-proxy) [docs](https://github.com/mattermost/docs) [mattermost-api-reference](https://github.com/mattermost/mattermost-api-reference) [mattermost-developer-documentation](https://github.com/mattermost/mattermost-developer-documentation).', 'file_ids': $FILE_IDS})
print(result)
" | python)
curl -X POST --header "authorization: Bearer $MATTERMOST_TOKEN" $MATTERMOST_URL/api/v4/posts -d "$NEW_POST"
