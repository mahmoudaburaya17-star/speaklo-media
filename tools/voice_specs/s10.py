from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo10.wav",chip="انطقها صح",total=33.9,emoji="🗣️",cta=30.6,
hook=[("-ed",150,YEL,False),("بتتنطق ٣ طرق",92,CREAM,True)],
segments=[
 (0.32,2.2,"ليه wanted بتتنطق إد؟",True),
 (2.52,4.13,"worked بتتنطق ت",True),
 (5.05,8.35,"الأفعال اللي آخرها ED ليها ٣ نطقات بس",True),
 (16.0,18.24,"لو الفعل آخره T أو D",True),
 (18.58,19.68,"بتتنطق إد",True),
 (22.36,22.92,"وغير كده",True),
 (26.46,27.21,"احفظ الثلاثة دول",True),
 (30.76,33.61,"تابع Speaklo واكتب في الكومنتات فعل عايز تعرف نطقه",True)],
cards=[dict(en="worked, stopped",ar="/t/",ent=(13.84,15.38),t=8.8,tag="صوت خفيف في الآخر"),
       dict(en="wanted, needed",ar="/ɪd/",ent=(20.2,21.71),t=15.95,tag="T أو D"),
       dict(en="played, cleaned",ar="/d/",ent=(24.28,25.79),t=22.3,tag="وغير كده")])
