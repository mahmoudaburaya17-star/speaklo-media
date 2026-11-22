import sys;sys.path.insert(0,'/home/claude/gen')
from fx import *
import story2, lesson2
R='/home/claude/speaklo-media/'
sc=[('N',"It was a rainy morning.","كان صباح ممطر.","🌧️",(70,110,170),False),
(0,"Oh no! I forgot my umbrella.","يا نهار! نسيت الشمسية.","☂️",CORAL,False),
(1,"Don't worry, Sara. Take my umbrella.","متقلقيش يا سارة. خدي الشمسية بتاعتي.","🤝",MINT,True),
(0,"Thank you! But then you will be wet.","شكرًا! بس كده إنت هتتبل.","😮",YEL,True),
(1,"I can hurry. The office is close.","أقدر أجري بسرعة. المكتب قريب.","🏃",MINT,True),
('N',"Adam hurried to the office in the rain.","آدم أسرع للمكتب تحت المطر.","🌦️",(70,110,170),False),
('N',"He was soaked, but he was smiling.","كان مبلول خالص، بس كان بيبتسم.","😄",YEL,True),
(0,"You are a good friend, Adam!","إنت صاحب جدع يا آدم!","💛",CORAL,False),
(1,"You're welcome, Sara.","العفو يا سارة.","😊",MINT,True)]
words=[("umbrella","شمسية"),("hurry","يستعجل"),("soaked","مبلول خالص")]
story2.make("قصة: الصبح الممطر","A Rainy Morning",("قصة قصيرة","وتتعلم منها 3 كلمات"),"Let's learn three new words with a short story!",sc,words,("اعمل لايك","وابعتها لصاحبك","نسيت الشمسية قبل كده؟"),"Like, and send it to a friend. Did you ever forget your umbrella?",R+'reels/raw_story_rainy.mp4',tmp="/tmp/s_rain")
items=[("so + adjective","بتقوّي الصفة","It's so hot today!","الجو حر أوي النهارده!","🔥",CORAL,False),
("such a + noun","بتقوّي الاسم","It's such a hot day today!","النهارده يوم حر أوي!","☀️",YEL,True),
("so many","للعدد الكتير","There are so many people here!","فيه ناس كتير أوي هنا!","👥",MINT,True),
("so ... that","بتديك النتيجة","It was so cold that the water in the lake froze.","كان برد لدرجة إن مية البحيرة اتجمدت.","🥶",(70,110,170),False)]
lesson2.make(("بتقول so","ولا such؟"),"so or such?","So, or such? Do you know the difference?","الفرق بين الاتنين","so vs such",items,("اعمل لايك","وابعتها لصاحبك","واكتب جملتك في الكومنتات"),"Like, and send it to a friend!",R+'reels/raw_lesson_so_such.mp4',tmp="/tmp/l_sosuch")
