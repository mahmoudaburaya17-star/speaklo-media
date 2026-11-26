from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo4.wav",chip="انطقها صح",total=30.0,emoji="🥦",cta=26.0,
hook=[("vegetable",110,YEL,False),("بتنطقها غلط؟",86,CREAM,True)],
segments=[
 (0.16,2.59,"لو بتقول فيجيتابل الفيديو ده ليك",True),
 (2.91,5.18,"٣ كلمات بنقولهم غلط كل يوم",True),
 (7.16,7.99,"مش فيجيتابل",True),
 (9.71,11.27,"بنرمي حرف من النص خالص",True),
 (13.08,14.15,"مش تشوكولات",True),
 (15.96,16.96,"وكمان library",True),
 (17.36,18.6,"مش library",True),
 (20.68,21.34,"كرروهم ورايا",True),
 (26.18,28.0,"تابع Speaklo وقولي في الكومنتات",True),
 (28.0,29.71,"كلمة بتتلخبط في نطقها",True)],
cards=[dict(en="vegetable",ar="/ˈvɛdʒtəbəl/",ent=(6.04,6.7),t=5.6,tag="٣ مقاطع بس"),
       dict(en="chocolate",ar="/ˈtʃɑːk(ə)lət/",ent=(12.05,12.63),t=11.6,tag="الحرف الأوسط خفيف"),
       dict(en="library",ar="/ˈlaɪbrɛri/",ent=(16.45,16.96),t=15.7,tag="متنساش R الأولى")])
