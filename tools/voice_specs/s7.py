from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo7.wav",chip="انطقها صح",total=29.4,emoji="🔢",cta=26.8,
hook=[("13 or 30?",120,YEL,False),("بتفرّق بينهم؟",84,CREAM,True)],
segments=[
 (0.19,1.67,"13 ولا 30",True),
 (2.32,3.95,"غلطة ممكن تبوّظ معاد",True),
 (4.51,5.66,"الفرق كله في التشديد",True),
 (7.46,8.43,"شدتها في الآخر",True),
 (11.28,12.13,"شدتها في الأول",True),
 (13.68,14.69,"ونفس القصة مع",True),
 (20.13,20.79,"كرر ورايا",True),
 (26.89,29.06,"تابع Speaklo وقولي في الكومنتات غلطت في الأرقام دي قبل كده",True)],
cards=[dict(en="thir-TEEN",ar="الشدة في الآخر",ent=(6.49,7.16),t=6.3,tag="13",scene=0),
       dict(en="THIR-ty",ar="الشدة في الأول",ent=(10.51,10.83),t=10.4,tag="30",scene=0),
       dict(en="fif-TEEN",ar="الشدة في الآخر",ent=(14.84,15.5),t=14.7,tag="15",scene=1),
       dict(en="FIF-ty",ar="الشدة في الأول",ent=(16.47,16.86),t=16.1,tag="50",scene=1)])
