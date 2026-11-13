# Speaklo Reel quality standard (user rule 2026-11-13: every Reel must be better than the previous one, and more professional)

## Minimum bar for EVERY Reel (word, dialogue, story, lesson)
1. Hook visible in the very first frame (Arabic, 2 lines max) - no empty/black first frame.
2. Safe zones: nothing important below y=1580 or right of x=1000 (Facebook Reels UI covers them). Use tools/fx.py (SAFE_BOTTOM).
3. Animated brand background (fx.make_bg/bg_frame), progress bar (fx.progress), element entrances with easing (fx.ease_out_back), never static slides.
4. Sound: voice + light SFX (pop/whoosh) + soft pad, loudness-normalised to about -16 LUFS (fx.encode does it). Check with ffmpeg ebur128 (peak <= -1.4 dBFS).
5. Karaoke-style highlight of the spoken English words when a sentence is shown (lesson2.py pattern).
6. 24 fps, 1080x1920, h264+aac, new filename for every re-encode. View at least 4 frames (hook, entrance, mid-scene, end) before scheduling.
7. CTA is light (like / send to a friend / write a sentence), never quiz answers. No emoji inside Arabic text drawn with PIL (paste emoji image instead).
8. Facts verified (MW / english-grammar.app) and recorded in ledger `source`.

## Improvement log (each new Reel must add at least one improvement and log it here)
- v1 (Oct-Nov 2026): flat navy slides, voice only, cards for word/dialogue/story.
- v2 lesson (2026-11-13, reels/sample_lesson_modals_v2.mp4): animated bg, slide/pop-in, karaoke highlight, narrator + Sara/Adam, SFX + pad, loudnorm -16.5 LUFS, safe zones, progress bar, Arabic hook + light CTA.

## Backlog (apply in this order, one or two per batch)
1. Port fx kit (bg, SFX, progress, loudnorm, safe zones) to word reels (reel2/voice), dialogues (dialogue.py), stories (story.py).
2. Dialogue v2: typing/pop SFX on each bubble, karaoke on the spoken bubble, character idle animation.
3. Story v2: Ken Burns / parallax on scene cards, simple illustrated scenes instead of one emoji.
4. Hook A/B: store `hook` text in ledger, compare impressions per hook style after 2 weeks.
5. Arabic captions burned in as karaoke (Arabic meaning timed with the English).
6. User voice recording (Egyptian Arabic intro 3-5 s) if the user provides it.
