from fx import *
SP=dict(wav="/home/claude/asr/run/wav/vo2.wav",chip="قولها بالإنجليزي",total=25.3,emoji="🍽️",cta=20.0,
hook=[("متقولش",110,CORAL,True),("I want",120,CREAM,False)],
segments=[
 (0.22,2.89,"متقولش I want في المطعم أو المحل",True),
 (3.31,4.92,"مش غلط بس فيه أشيك",True),
 (7.22,7.93,"ممكن قهوة؟",True),
 (11.13,12.19,"عايز ترابيزة لاتنين",True),
 (14.65,15.41,"ممكن المنيو",True),
 (16.04,19.53,"التلاتة أدب وبيخلو اللي قدامك يبتسم وهو بياخد طلبك",True),
 (20.16,22.6,"تابع Speaklo عشان كل يوم جملة جديدة",True),
 (22.93,24.88,"واكتب في الكومنتات جملة بتحب تقولها بأدب",True)],
cards=[dict(en="Can I get a coffee?",ar="ممكن قهوة",ent=(5.58,6.76),tag="في الكافيه"),
       dict(en="I'd like a table for two.",ar="عايز ترابيزة لاتنين",ent=(8.75,10.49),tag="في المطعم"),
       dict(en="Could I have the menu?",ar="ممكن المنيو",ent=(13.03,14.21),tag="بأدب")])
