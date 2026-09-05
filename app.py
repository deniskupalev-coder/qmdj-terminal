# --- APP ---
import streamlit as st
import datetime, math

STEMS=['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
BRANCHES=['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
FIVE_RATS={0:0,5:0,1:12,6:12,2:24,7:24,3:36,8:36,4:48,9:48}
HIDDEN={0:'戊',10:'己',20:'庚',30:'辛',40:'壬',50:'癸'}
TERMS=[('Дун Чжи',270),('Сяо Хань',285),('Да Хань',300),('Ли Чунь',315),('Юй Шуй',330),('Цзин Чжэ',345),('Чунь Фэнь',0),('Цин Мин',15),('Гу Юй',30),('Ли Ся',45),('Сяо Мань',60),('Ман Чжун',75),('Ся Чжи',90),('Сяо Шу',105),('Да Шу',120),('Ли Цю',135),('Чу Шу',150),('Бай Лу',165),('Цю Фэнь',180),('Хань Лу',195),('Шуан Цзян',210),('Ли Дун',225),('Сяо Сюэ',240),('Да Сюэ',255)]
JU={'Дун Чжи':(1,7,4),'Сяо Хань':(2,8,5),'Да Хань':(3,9,6),'Ли Чунь':(8,5,2),'Юй Шуй':(9,6,3),'Цзин Чжэ':(1,7,4),'Чунь Фэнь':(3,9,6),'Цин Мин':(4,1,7),'Гу Юй':(5,2,8),'Ли Ся':(4,1,7),'Сяо Мань':(5,2,8),'Ман Чжун':(6,3,9),'Ся Чжи':(9,3,6),'Сяо Шу':(8,2,5),'Да Шу':(7,1,4),'Ли Цю':(2,5,8),'Чу Шу':(1,4,7),'Бай Лу':(9,3,6),'Цю Фэнь':(7,1,4),'Хань Лу':(6,9,3),'Шуан Цзян':(5,8,2),'Ли Дун':(6,9,3),'Сяо Сюэ':(5,8,2),'Да Сюэ':(4,7,1)}
YANG=set(['Дун Чжи','Сяо Хань','Да Хань','Ли Чунь','Юй Шуй','Цзин Чжэ','Чунь Фэнь','Цин Мин','Гу Юй','Ли Ся','Сяо Мань','Ман Чжун'])
FLIP={'Верхний':'Нижний','Нижний':'Верхний','Средний':'Средний'}
ORDER=['戊','己','庚','辛','壬','癸','丁','丙','乙']
STAR_CN={1:'天蓬',2:'天芮',3:'天冲',4:'天辅',5:'天禽',6:'天心',7:'天柱',8:'天任',9:'天英'}
STAR_RU={1:'Тянь Пэн',2:'Тянь Жуй',3:'Тянь Чун',4:'Тянь Фу',5:'Тянь Цинь',6:'Тянь Синь',7:'Тянь Чжу',8:'Тянь Жэнь',9:'Тянь Ин'}
RING=[1,8,3,4,9,2,7,6]
PAL_WX={1:'Вода',2:'Земля',3:'Дерево',4:'Дерево',5:'Земля',6:'Металл',7:'Металл',8:'Земля',9:'Огонь'}
GEN={'Дерево':'Огонь','Огонь':'Земля','Земля':'Металл','Металл':'Вода','Вода':'Дерево'}
OVE={'Дерево':'Земля','Земля':'Вода','Вода':'Огонь','Огонь':'Металл','Металл':'Дерево'}

def name(n): return STEMS[n%10]+BRANCHES[n%12]
def day_gz(d): return (54+(d-datetime.date(2000,1,1)).days)%60
def sh_br(h): return ((h+1)//2)%12
def sh_start(b): return (1380+b*120)%1440
def ft_info(n):
    ft=n-n%10; b=ft%12
    y='Верхний' if b in (0,3,6,9) else ('Средний' if b in (2,5,8,11) else 'Нижний')
    return ft,HIDDEN[ft],y
def jday(dt):
    y,m=dt.year,dt.month
    dd=dt.day+(dt.hour+dt.minute/60)/24
    a=(14-m)//12; yy=y+4800-a; mm=m+12*a-3
    return dd+((153*mm+2)//5)+365*yy+yy//4-yy//100+yy//400-32045-0.5
def sun_lon(dt):
    t=(jday(dt)-2451545)/36525
    l0=280.46646+36000.76983*t+0.0003032*t*t
    mr=math.radians(357.52911+35999.05029*t-0.0001537*t*t)
    c=(1.914602-0.004817*t)*math.sin(mr)+0.019993*math.sin(2*mr)+0.000289*math.sin(3*mr)
    return (l0+c)%360
def term_of(dt):
    lon=sun_lon(dt); best=None; bd=361
    for nm,L in TERMS:
        dl=(lon-L)%360
        if dl<bd: bd,bb=dl,nm
    return best
def dun_ju(tm,y): return ('Ян' if tm in YANG else 'Инь'), JU[tm][{'Верхний':0,'Средний':1,'Нижний':2}[y]]
def eplate(ju,dun):
    pl={}; p=ju
    for s in ORDER:
        pl[p]=s
        p+=1 if dun=='Ян' else -1
        if p==0:p=9
        if p==10:p=1
    return pl
def pal_of(pl,s):
    for k,v in pl.items():
        if v==s: return 2 if k==5 else k
def dwalk(stt,n,dun):
    seq=list(range(1,10)) if dun=='Ян' else list(range(9,0,-1))
    return seq[(seq.index(stt)+n)%9]
def build(mode,date,hh,mm,off,yr):
    tot=(hh*60+mm+off)%1440; h=tot//60; hb=sh_br(h)
    ke=((tot-sh_start(hb))%1440)//2
    dp=day_gz(date); hp=(FIVE_RATS[dp%10]+hb)%60
    kp=ke%60 if mode=='ke' else hp
    ftk,hid,yk=ft_info(kp); _,_,yd=ft_info(dp)
    yuan=FLIP[yk] if yr=='auto' else (yd if yr=='day' else yk)
    tm=term_of(datetime.datetime(date.year,date.month,date.day,hh,mm))
    dun,ju=dun_ju(tm,yuan)
    pl=eplate(ju,dun)
    home=pal_of(pl,hid); target=pal_of(pl,STEMS[kp%10])
    steps=(RING.index(target)-RING.index(home))%8
    stars={RING[(RING.index(p)+steps)%8]:p for p in RING}
    door=dwalk(home,(kp-ftk)%9,dun)
    return dict(dp=dp,hp=hp,kp=kp,term=tm,dun=dun,ju=ju,stars=stars,zf=target,zs=door,fy=steps==0)
def verdict(p,s,fy):
    pe,se=PAL_WX[p],PAL_WX[s]
    if fy or GEN[se]==pe: return 2
    return 0 if OVE[se]==pe else 1
def nums(p,lim):
    out=[p+10*k for k in range(5) if p+10*k<=lim]
    if p==5: out+=[x for x in (10,20,30,40) if x<=lim]
    return ' '.join(f'{n:02d}' for n in out)

CSS='<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@600;900&display=swap" rel="stylesheet"><style>.hz{font-family:"Noto Serif SC",serif;font-size:22px;font-weight:900}.pal{border:2px solid #444;border-radius:12px;padding:10px;text-align:center;margin:4px}.v2{background:#d4edda}.v1{background:#fff3cd}.v0{background:#f8d7da}</style>'
st.set_page_config(page_title='Ци Мэнь Терминал',layout='wide')
st.markdown(CSS,unsafe_allow_html=True)
st.title('🧭 Ци Мэнь Дунь Цзя — Терминал')
with st.sidebar:
    mode=st.radio('Режим',['2 мин → 4 из 20','Час → 6 из 45'])
    d=st.date_input('Дата',datetime.date(2026,9,5))
    t=st.time_input('Время',datetime.time(19,52))
    off=st.number_input('Поправка солнечного времени (мин)',value=-30,step=5)
    yr=st.selectbox('Юань',['auto','day','standard'])
m='ke' if mode.startswith('2') else 'hour'
lim=20 if m=='ke' else 45
c=build(m,d,t.hour,t.minute,int(off),yr)
st.subheader(f"{c['term']} | {c['dun']} Дунь {c['ju']} | Кэ {name(c['kp'])} | Час {name(c['hp'])} | День {name(c['dp'])}")
st.markdown(f"**Чжи Фу => {c['zf']} | Чжи Ши => {c['zs']}**" + (" | 💎 **ФУ ИНЬ!**" if c['fy'] else ""))
for row in [[4,9,2],[3,5,7],[8,1,6]]:
    line=st.columns(3)
    for i,p in enumerate(row):
        s=c['stars'].get(p)
        v=verdict(p,s,c['fy']) if s else 1
        mk=(' [ЧФ]' if p==c['zf'] else '')+(' [ЧШ]' if p==c['zs'] else '')
        body=f"<div class='pal v{v}'><b>Дворец {p}</b><br><span class='hz'>{STAR_CN[s] if s else ''}</span><br>{STAR_RU[s] if s else '—'}<br>{'✅ 2' if v==2 else ('⚪ 1' if v==1 else '❌ 0')}{mk}<br><small>{nums(p,lim) if (s and v>0) else 'БРАК'}</small></div>"
        line[i].markdown(body,unsafe_allow_html=True)
pri,neu=[],[]
for p in range(1,10):
    s=c['stars'].get(p)
    if not s: continue
    v=verdict(p,s,c['fy'])
    if v==2: pri.append(nums(p,lim))
    if v==1: neu.append(nums(p,lim))
st.markdown('---')
st.markdown(f"🟢 **ПУЛ ПРИОРИТЕТ:** {' '.join(pri) if pri else '-'}")
st.markdown(f"⚪ **ПУЛ НЕЙТРАЛЬНО:** {' '.join(neu) if neu else '-'}")
st.markdown(f"🎯 **СНАЙПЕР:** {'ДА! (2-3 приоритетных)' if 2<=len(pri)<=3 else 'нет ('+str(len(pri))+')'}")
