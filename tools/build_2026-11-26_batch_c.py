import sys;sys.path.insert(0,'/home/claude/gen')
import os
from fx import *
import speaklo_ar2 as S, story2, lesson2, dialogue2, yt_version as Y
R='/home/claude/speaklo-media/'
for d in ('images/2026-11-25','images/2026-11-26'):os.makedirs(R+d,exist_ok=True)
S.mistake_ar("He must to be at home.","He must be at home.","بعد must بنستخدم الفعل من غير to",R+'images/2026-11-26/1300_mistake_must_to_be.png')
S.title_ar("درس اليوم","بقالي ساعات بذاكر","present perfect continuous",R+'images/2026-11-25/2000_long39_present_perfect_continuous.png')
CTA=("اعمل لايك","وابعتها لصاحبك","واكتب جملتك في الكومنتات")
items=[("must be","متأكد إنه صح","This must be her house. I can see her car in the garage.","ده أكيد بيتها. شايف عربيتها في الجراج.","🏠",MINT,True),
("might be","ممكن بس مش متأكد","She's not here yet. She might be stuck in traffic.","لسه مجتش. ممكن تكون عالقة في الزحمة.","🚗",YEL,True),
("could be","ممكن برضو","He's not answering. He could be in class.","مش بيرد. ممكن يكون في المحاضرة.","📚",CORAL,False),
("can't be","متأكد إنه مستحيل","It can't be far now. We've been driving for hours.","مش ممكن يكون بعيد دلوقتي. بقالنا ساعات بنسوق.","🛣️",(70,110,170),False)]
lesson2.make(("متأكد ولا","بتخمّن؟"),"must, might or can't?","Are you sure, or just guessing? Let's learn how to guess in English!","التخمين في الإنجليزي","modals of deduction",items,CTA,"Like, and send it to a friend!",R+'reels/raw_lesson_deduction.mp4',tmp="/tmp/l_ded")
lines=[(0,"Hi! I would like to join the gym.","أهلاً! عايزة أشترك في الجيم."),(1,"Sure! Do you want a monthly membership?","أكيد! عايزة اشتراك شهري؟"),(0,"Yes, please. How much is it?","أيوه لو سمحت. بكام؟"),(1,"It's three hundred pounds a month.","تلتميت جنيه في الشهر."),(0,"Can I try one class first?","ينفع أجرب حصة واحدة الأول؟"),(1,"Of course. Your first class is free!","طبعًا. أول حصة ببلاش!")]
dialogue2.make("محادثة في الجيم","At the gym",("هتشترك","في الجيم؟"),"Do you want to join a gym? Listen to this conversation!",lines,CTA,"Like, and send it to a friend!",R+'reels/raw_dialogue_gym.mp4',tmp="/tmp/d_gym")
sc=[('N',"Today is Sara's birthday.","النهارده عيد ميلاد سارة.","🎂",(70,110,170),False),
(1,"Sara does not know about the party. It is a surprise!","سارة مش عارفة عن الحفلة. دي مفاجأة!","🎉",YEL,True),
(1,"I bought a gift. I will hide it in the kitchen.","اشتريت هدية. هخبيها في المطبخ.","🎁",MINT,True),
('N',"Sara opened the door.","سارة فتحت الباب.","🚪",(70,110,170),False),
(0,"Why is it so quiet?","ليه الدنيا هادية كده؟","🤔",CORAL,False),
('N',"Everyone was hiding behind the sofa.","كل الناس كانوا مستخبيين ورا الكنبة.","🛋️",(70,110,170),False),
(1,"Surprise! Happy birthday, Sara!","مفاجأة! كل سنة وإنتي طيبة يا سارة!","🥳",YEL,True),
(0,"Oh my! Thank you, everyone!","يا سلام! شكرًا لكم كلكم!","😍",CORAL,False)]
words=[("surprise","مفاجأة"),("hide","يخبّي"),("gift","هدية")]
story2.make("قصة: حفلة المفاجأة","The Surprise Party",("قصة قصيرة","وتتعلم منها 3 كلمات"),"Let's learn three new words with a short story!",sc,words,("اعمل لايك","وابعتها لصاحبك","عملت حفلة مفاجأة قبل كده؟"),"Like, and send it to a friend. Did you ever plan a surprise party?",R+'reels/raw_story_party.mp4',tmp="/tmp/s_party")
for raw,n in (("raw_lesson_deduction","2026-11-26_lesson_deduction"),("raw_dialogue_gym","2026-11-26_dialogue_gym"),("raw_story_party","2026-11-27_story_surprise_party")):
    Y.make(R+'reels/'+raw+".mp4",R+'reels/'+n+"_fb.mp4",tmp="/tmp/ytv_"+n,mode="fb")
    Y.make(R+'reels/'+raw+".mp4",R+'reels/yt/'+n+"_yt.mp4",tmp="/tmp/ytv_"+n,mode="yt")
