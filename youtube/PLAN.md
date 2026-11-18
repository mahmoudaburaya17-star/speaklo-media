# YouTube plan (Speaklo)
Plan doc (Claude Docs): https://claude.ai/artifact/NZ1DTjFYMtQCNGaQJJa5js
- 14 Shorts/week, 12:00 and 19:00 Cairo (estimate). Series: word, dialogue, mistake, lesson, story, phrasal verbs, pronunciation, weekly review. No quiz/slang unless user asks.
- Buffer YouTube: Shorts only, <=3 min, 9:16, title <=100 chars, description <=5000, no custom thumbnail, channel must be connected by the Google account that owns it. Check metadata.youtube fields via introspect_schema before the first create_post. Check the per-channel scheduled cap after linking.
- Ledger: youtube/ledger_youtube.json (14 ready items reused from FB reels; mistakes/phrasal/pronunciation/review still to build).
- Open: logo file + tagline (page uses blue S + 'Speak Naturally. Understand More.'), channel name, Kokoro commercial license check, YPP availability in Egypt.
- Policy risk: templated+TTS content can be classed as repetitive; vary scenarios, add original Egyptian-Arabic explanation.
- Do NOT schedule until user says the channel is connected.
