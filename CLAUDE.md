# Speaklo page: how to run it (read before touching Buffer)

Page: Facebook "Speaklo" (Buffer channel 6ac94a6a6a5c39ccb666bab4), English learning. STRATEGY (from 2026-10-14): ARABIC-FIRST for Arab learners (Egyptian dialect, simple), English examples inside; English-only foreign content paused until engagement grows. Reason: English-only posts reached 1-3 impressions each, 0 reactions.
Brand: navy #1B2A4E, yellow #FFC93C, coral #FF6B4A, mint #2EC4B6, cream #FFF8EE. Fonts Poppins/Nunito. Tagline "Speak it. Own it."
Daily slots (Cairo time, +03:00 until Egypt DST ends 2026-10-29, then +02:00): 09:00 Word of the Day (كلمة اليوم), 15:00 Common Mistake (غلطة شائعة), 21:00 Quiz (كويز). User asked (2026-10-17) for 6 posts/day: slots 08:00, 11:00, 14:00, 17:00, 20:00, 23:00 Cairo. Free plan cap of 10 scheduled posts covers under 2 days at this rate. Quiz captions say 'الكويز اللي فات' (not 'yesterday') because quizzes can be hours apart. Ledger key = UTC time + slot + #ar. NEVER write quiz answers or promise to reveal them (user rule 2026-10-18): quiz caption = question + options + 'اكتب إجابتك في الكومنتات' + hashtags only. Long-post exercises also have no answers. Arabic cards: speaklo_ar2.py in session gen dir uses Tajawal (sparse-clone github.com/google/fonts ofl/tajawal works through the proxy). Arabic text ending in Latin/punctuation needs care (bidi).
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


## Update 2026-10-22
User approved reducing to 3 posts/day: slots 09:00 (word), 15:00 (mistake), 21:00 (quiz) Cairo. Long posts (4) were published Oct 19-20. Reels: silent animated 9:16 videos made with Pillow+ffmpeg are possible (no voice); user test pending. edit_post needs full payload (text+assets+metadata).

USER RULE (2026-10-22): write one LONG valuable post (Arabic, title card, no quiz answers, source cited) EVERY DAY. If today has none, write it and schedule it at ~20:00 Cairo, replacing/removing another queued post if the 10-post cap is full (log the removed one in ledger to reschedule). Long post 5 (make vs do) scheduled 2026-10-22 20:00. 'available' word post was removed from the queue to make room.

## PLAN v3 (user, 2026-10-22): 4 posts/day, 1 long post on some days and 2 on others (alternate), daily Reel at my discretion, best times.
Slots (Cairo): 09:00 Reel (word of the day, silent animated 9:16, tools/reel2.py), 13:00 mistake image OR long post on 2-long days, 20:00 long post (title card), 22:00 quiz. Best-time rationale is my inference (Egypt: morning commute, lunch, evening peak), not measured; re-check with Insights. Buffer accepts Reels via create_post metadata.facebook.type='reel' + video asset URL (GitHub raw mp4 worked). Cap 10 scheduled: ~2.5 days queued. Removed from queue for later: appreciate, bored, in May, familiar. Long posts must cite a source page (english-grammar.app lessons used so far). Reel zoompan: feed ONE still frame per input (no -loop) or frames multiply.
