from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo3.wav",chip="غلطة شائعة",total=27.0,emoji="⚠️",cta=23.1,
hook=[("أشهر غلطة",110,CORAL,True),("بنقولها كلنا",84,CREAM,True)],
segments=[
 (0.29,1.76,"أشهر غلطة بنقولها كلنا",True),
 (3.83,4.35,"غلط",True),
 (4.94,7.51,"agree فعل لوحده مش محتاج am",True),
 (8.13,8.56,"الصح",True),
 (10.18,11.23,"يعني أنا موافق",True),
 (11.84,14.55,"زي ما بتقول I like قول I agree",True),
 (15.09,17.71,"مفيش I am like ولا I am agree",True),
 (18.35,18.91,"جرب معايا",True),
 (20.63,21.28,"ولو مش موافق",True),
 (23.27,26.65,"تابع Speaklo وقولي في الكومنتات إيه غلطة بتسمعها كتير؟",True)],
cards=[dict(en="I am agree",ar="غلط",color=CORAL,ent=(2.38,3.23),t=2.1,tag="الغلطة"),
       dict(en="I agree",ar="أنا موافق",color=MINT,ent=(9.03,9.64),t=8.0,tag="الصح"),
       dict(en="I disagree",ar="أنا مش موافق",color=YEL,ent=(21.78,22.52),t=19.3,tag="ولو مش موافق")])
