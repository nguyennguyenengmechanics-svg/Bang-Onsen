"""Run only after the required speech hostname is allowed by environment settings.
Sends the newly written narration (not the original YouTube audio) for speech synthesis.
The result must be timed and measured before calling it a finished video.
"""
import asyncio, os, json
from pathlib import Path
import edge_tts
ROOT = Path(__file__).parent
async def main():
    proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY')
    text = (ROOT/'narration.txt').read_text()
    output = ROOT/'assets/narration-vi.mp3'
    timings = []
    # This is a standard Vietnamese voice; no imitation or cloning of the channel's presenter.
    speaker = edge_tts.Communicate(text, 'vi-VN-NamMinhNeural', rate='+0%', proxy=proxy)
    with output.open('wb') as f:
        async for event in speaker.stream():
            if event['type'] == 'audio': f.write(event['data'])
            elif event['type'] in ('WordBoundary','SentenceBoundary'): timings.append(event)
    (ROOT/'assets/narration-timings.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2))
    print('Created narration and timing metadata; retime scenes, create real captions, and measure final audio before delivery.')
if __name__ == '__main__': asyncio.run(main())
