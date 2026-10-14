# Speaklo page: how to run it (read before touching Buffer)

Page: Facebook "Speaklo" (Buffer channel 6ac94a6a6a5c39ccb666bab4), English learning. STRATEGY (from 2026-10-14): ARABIC-FIRST for Arab learners (Egyptian dialect, simple), English examples inside; English-only foreign content paused until engagement grows. Reason: English-only posts reached 1-3 impressions each, 0 reactions.
Brand: navy #1B2A4E, yellow #FFC93C, coral #FF6B4A, mint #2EC4B6, cream #FFF8EE. Fonts Poppins/Nunito. Tagline "Speak it. Own it."
Daily slots (Cairo time, +03:00 until Egypt DST ends 2026-10-29, then +02:00): 09:00 Word of the Day (كلمة اليوم), 15:00 Common Mistake (غلطة شائعة), 21:00 Quiz (كويز). 3 posts/day only (6/day with no audience hurt reach). Ledger key = UTC time + slot + #ar. Quiz answer is revealed in the NEXT day's quiz caption. Arabic cards: /home/claude/gen/speaklo_ar.py (DejaVu Sans Bold for Arabic; Tajawal/Cairo not downloadable here).
`ledger.json` is the source of truth for every post (key = UTC time + slot). Images are served from raw.githubusercontent.com/mahmoudaburaya17-star/speaklo-media/main/<image>.

## Never post twice (do ALL checks, in order)
1. Call Buffer list_posts for the org and read every post on the Speaklo channel (scheduled, sent, error).
2. Skip an item if ANY of these is true: its ledger entry already has a bufferId; Buffer already has a post with the same dueAt; Buffer already has a post with the same first line / topic. Never "retry" by creating again: edit or delete the existing post instead.
3. Never use shareNow / publish now. Always customScheduled with a future dueAt (account timezone Africa/Cairo, +03:00).
4. After create_post, call get_post and confirm: status = scheduled, error = null, image 1080x1080, source URL is the GitHub raw URL. Only then write bufferId into ledger.json and commit.
5. Buffer free plan: max 10 scheduled posts at once. Count scheduled posts first; only fill the free slots. No first comment on free plan (put the quiz answer in the next day's post or tell the user).

## Facts must be verified
Every word, IPA, definition, idiom and grammar rule must be checked against a dictionary/grammar source before it goes in an image or caption. Record the source in the item's `source` field. If unsure, do not post it.

## Routine when the user says "continue"
Sync with Buffer, mark sent/error posts in the ledger, fix any error post, build the next images (Pillow script style: Poppins, sizes 1080x1080), view them, push to this repo, then schedule into free slots following the checks above. Report only what changed.
