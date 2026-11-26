from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo13.wav",chip="قولها بالإنجليزي",total=22.6,emoji="🍔",cta=19.2,
hook=[("أول مرة تطلب أكل",96,YEL,True),("بالإنجليزي؟",90,CREAM,True)],
segments=[
 (0.29,1.91,"أول مرة تطلب أكل بالإنجليزي؟",True),
 (2.52,3.87,"٥ جمل وخلاص",True),
 (5.95,6.72,"ممكن المنيو؟",True),
 (8.65,9.24,"هاخد الفراخ",True),
 (11.33,12.01,"مياه لو سمحت",True),
 (14.25,15.19,"كده كفاية شكرا",True),
 (15.71,16.21,"وفي الآخر",True),
 (17.9,18.64,"الحساب لو سمحت",True),
 (19.35,22.25,"تابع Speaklo واكتب في الكومنتات أكلة بتحبها بالإنجليزي",True)],
cards=[dict(en="Can I see the menu?",ar="ممكن المنيو؟",ent=(4.47,5.39),t=4.3,tag="المنيو",scene=0),
       dict(en="I'll have the chicken.",ar="هاخد الفراخ",ent=(7.35,8.12),t=7.2,tag="الطلب",scene=0),
       dict(en="Water, please.",ar="مياه لو سمحت",ent=(9.93,10.75),t=9.8,tag="الشرب",scene=0),
       dict(en="That's all, thanks.",ar="كده كفاية شكرا",ent=(12.58,13.79),t=12.45,tag="لما تخلص",scene=1),
       dict(en="The check, please.",ar="الحساب لو سمحت",ent=(16.64,17.45),t=16.5,tag="الحساب",scene=1)])
