import sys;sys.path.insert(0,'/home/claude/gen')
import os
from fx import *
import speaklo_ar2 as S, story2, lesson2, dialogue2, yt_version as Y
R='/home/claude/speaklo-media/'
for d in ('images/2026-11-25','images/2026-11-26'):os.makedirs(R+d,exist_ok=True)
R='/home/claude/speaklo-media/'
CTA=("اعمل لايك","وابعتها لصاحبك","واكتب جملتك في الكومنتات")
items=[("must be","متأكد إنه صح","This must be her house. I can see her car in the garage.","ده أكيد بيتها. شايف عربيتها في الجراج.","🏠",MINT,True),
("might be","ممكن بس مش متأكد","She's not here yet. She might be stuck in traffic.","لسه مجتش. ممكن تكون عالقة في الزحمة.","🚗",YEL,True),
("could be","ممكن برضو","He's not answering. He could be in class.","مش بيرد. ممكن يكون في المحاضرة.","📚",CORAL,False),
("can't be","متأكد إنه مستحيل","It can't be far now. We've been driving for hours.","أكيد مش بعيد. بقالنا ساعات بنسوق.","🛣️",(70,110,170),False)]
lesson2.make(("متأكد ولا","بتخمّن؟"),"must, might or can't?","Are you sure, or just guessing? Let's learn how to guess in English!","التخمين في الإنجليزي","modals of deduction",items,CTA,"Like, and send it to a friend!",R+'reels/raw_lesson_deduction.mp4',tmp="/tmp/l_ded")

for raw,n in (("raw_lesson_deduction","2026-11-26_lesson_deduction"),):
    Y.make(R+'reels/'+raw+".mp4",R+'reels/'+n+"_fb.mp4",tmp="/tmp/ytv_"+n,mode="fb")
    Y.make(R+'reels/'+raw+".mp4",R+'reels/yt/'+n+"_yt.mp4",tmp="/tmp/ytv_"+n,mode="yt")
