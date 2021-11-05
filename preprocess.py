import os
import json
import glob
from operator import itemgetter
from dateutil import parser
from pathlib import Path

files = glob.glob("<Path to raw_json_results_from_speech_batch_api/*.json")

for file in files:
    with open(file, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    name = Path(file).stem
    print(name)

    phrases = data['recognizedPhrases']
    final_data = []
    for p in phrases:
        channel = p['channel']
        if channel == 0:
            channel = "Agent"
        else:
            channel = "Caller"
        offset = p['offsetInTicks'] / 10 / 1000 / 1000 # seconds
        text = p['nBest'][0]['display']
        final_data.append({
            "timestamp": offset,
            "speaker": channel,
            "text": text
        })
    sorted_data = sorted(final_data, key=itemgetter('timestamp'))    

    with open(os.path.join("<path to processed files>", name + ".json") , "w", encoding='utf-8') as outfile:
        json.dump({
            'transcription_id': '1234',
            'date': 'replace me please',
            'transcript': sorted_data}, outfile, ensure_ascii=False, indent=4)
            