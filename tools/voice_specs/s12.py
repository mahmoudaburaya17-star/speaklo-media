from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo12.wav",chip="غلطة شائعة",total=25.3,emoji="👶",cta=20.7,
hook=[("I born in Egypt",84,CORAL,False),("صح ولا غلط؟",90,CREAM,True)],
segments=[
 (0.25,3.01,"لو بتقول I born in Egypt وقّف",True),
 (3.63,4.11,"الصح",True),
 (6.5,8.67,"الولادة حاجة حصلت وخلصت يعني ماضي",True),
 (11.17,12.06,"أنا اتولدت في القاهرة",True),
 (14.97,16.23,"هي اتولدت سنة 1990",True),
 (16.86,20.08,"متقولش I born قول I was born",True),
 (20.74,22.44,"تابع Speaklo واكتب في الكومنتات",True),
 (22.86,23.91,"I was born in",True),
 (24.39,24.83,"كملها إنت",True)],
cards=[dict(en="I born in Egypt.",ar="غلط",color=CORAL,ent=(1.0,2.4),t=1.6,tag="الغلطة",scene=0),
       dict(en="I was born in Egypt.",ar="الصح",color=MINT,ent=(4.47,5.96),t=4.3,tag="الصح",scene=0),
       dict(en="I was born in Cairo.",ar="أنا اتولدت في القاهرة",color=YEL,ent=(9.32,10.79),t=9.2,tag="ماضي",scene=1),
       dict(en="She was born in 1990.",ar="هي اتولدت سنة 1990",color=MINT,ent=(12.63,14.59),t=12.5,tag="ماضي",scene=1)])
