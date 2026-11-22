import sys;sys.path.insert(0,'/home/claude/gen')
import os
from fx import *
import speaklo_ar2 as S, word2, yt_version
R='/home/claude/speaklo-media/'
os.makedirs(R+'images/2026-11-23',exist_ok=True);os.makedirs(R+'images/2026-11-24',exist_ok=True)
S.mistake_ar("My birthday is in 19 October.","My birthday is on 19 October.","مع التاريخ بنستخدم on ومع الشهر لوحده بنستخدم in",R+'images/2026-11-23/1300_mistake_birthday_in_on.png')
S.mistake_ar("She will marry with him.","She will marry him.","الفعل marry بييجي بعده الشخص مباشرة من غير with",R+'images/2026-11-24/1300_mistake_marry_with.png')
S.title_ar("درس اليوم","إزاي تتكلم عن المستقبل","will vs going to",R+'images/2026-11-23/2000_long38_will_going_to.png')
CTA=("اعمل لايك","وابعتها لصاحبك","واكتب جملتك في الكومنتات")
word2.make("كلمة اليوم",("بتقولها كل يوم","وفاهمها صح؟"),"Do you know what this word means?","accept","/əkˈsɛpt/","يقبل","I accept your invitation.","أنا بقبل دعوتك.","🤝",MINT,True,CTA,"Like, and send it to a friend!",R+'reels/raw_word_accept.mp4',tmp="/tmp/w_accept")
word2.make("كلمة اليوم",("بتقولها كل يوم","وفاهمها صح؟"),"Do you know what this word means?","remind","/rɪˈmaɪnd/","يفكّر حد بحاجة","Please remind me to call my mom.","من فضلك فكّرني أكلم ماما.","⏰",CORAL,False,CTA,"Like, and send it to a friend!",R+'reels/raw_word_remind.mp4',tmp="/tmp/w_remind")
