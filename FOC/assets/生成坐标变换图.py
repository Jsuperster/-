from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parent
ROOT.mkdir(exist_ok=True)
FONT='C:/Windows/Fonts/msyh.ttc'
def font(n): return ImageFont.truetype(FONT,n)
BG='#f3f6fb'; INK='#172b4d'; MUT='#52647a'; A='#e45555'; B='#259968'; C='#8961cf'; BLUE='#2276cc'; ORANGE='#e08c22'
def text(d,xy,s,n=20,c=INK): d.text(xy,s,font=font(n),fill=c)
def arrow(d,o,v,c,w=4):
    x,y=o; xx,yy=v; d.line((x,y,xx,yy),fill=c,width=w)
    ang=math.atan2(yy-y,xx-x)
    pts=[(xx,yy),(xx-12*math.cos(ang-.45),yy-12*math.sin(ang-.45)),(xx-12*math.cos(ang+.45),yy-12*math.sin(ang+.45))]
    d.polygon(pts,fill=c)
def pt(o,x,y,s=115): return (o[0]+s*x,o[1]-s*y)
def base(title,sub):
    im=Image.new('RGB',(1280,820),BG); d=ImageDraw.Draw(im)
    text(d,(35,20),title,32); text(d,(35,67),sub,19,MUT)
    d.rounded_rectangle((25,110,630,685),18,fill='white')
    d.rounded_rectangle((650,110,1255,685),18,fill='white')
    return im,d

def clarke(t):
    ia=2*math.cos(t); ib=2*math.cos(t-2*math.pi/3); ic=2*math.cos(t+2*math.pi/3)
    al=2*math.cos(t); be=2*math.sin(t)
    im,d=base('Clarke 变换：三相量 → 静止 αβ 坐标','幅值不变 · 零序为 0 · 相电流峰值 2 A · φ 是电流矢量角，不一定等于转子电角度')
    text(d,(50,130),'① 三相电流瞬时值（A）',25)
    for i,(name,val,col) in enumerate([('ia',ia,A),('ib',ib,B),('ic',ic,C)]):
        y=220+i*120; text(d,(55,y-38),f'{name} = {val:+.3f} A',23,col)
        d.line((95,y,565,y),fill='#dbe2ec',width=2); d.line((330,y-22,330,y+22),fill=MUT,width=2)
        end=330+val*105; d.rectangle((min(330,end),y-13,max(330,end),y+13),fill=col)
    text(d,(70,565),'−2 A                 0                 +2 A',19,MUT)
    text(d,(60,620),f'ia + ib + ic = {ia+ib+ic:.3f} A',22)
    o=(950,390)
    for angle,name,col in [(0,'a / α',A),(2*math.pi/3,'b',B),(4*math.pi/3,'c',C)]:
        end=pt(o,2.08*math.cos(angle),2.08*math.sin(angle)); arrow(d,o,end,col,2); text(d,(end[0]-10,end[1]-26),name,20,col)
    arrow(d,pt(o,0,-2.1),pt(o,0,2.1),MUT,2); text(d,(960,140),'β',22,MUT)
    d.ellipse((720,160,1180,620),outline='#e4eaf2',width=2)
    v=pt(o,al,be); d.line((v[0],o[1],v[0],v[1]),fill=BLUE,width=2); d.line((o[0],v[1],v[0],v[1]),fill=BLUE,width=2); arrow(d,o,v,BLUE,5)
    text(d,(680,630),f'φ = {math.degrees(t)%360:5.1f}°   iα = {al:+.3f}   iβ = {be:+.3f} A',22,BLUE)
    text(d,(40,710),'iα = (2/3)(ia − ib/2 − ic/2) = ia',25)
    text(d,(40,755),'iβ = (2/3)(√3/2)(ib − ic) = (ia + 2ib)/√3',25)
    return im

def park(t):
    id_=1.; iq=1.5; co=math.cos(t); si=math.sin(t); al=id_*co-iq*si; be=id_*si+iq*co
    im,d=base('Park 变换：静止 αβ → 随转子旋转的 dq','同一电流矢量，换一组坐标轴 · 示例 id = 1 A、iq = 1.5 A 恒定（不是 id = 0 控制工况）')
    o=(330,390); s=110
    for v,name in [((2.3,0),'α'),((0,2.3),'β')]:
        end=pt(o,*v,s); arrow(d,pt(o,-v[0],-v[1],s),end,MUT,2); text(d,(end[0]-5,end[1]-30),name,22,MUT)
    for x,y,name,col in [(co,si,'d',ORANGE),(-si,co,'q',B)]:
        end=pt(o,2.05*x,2.05*y,s); arrow(d,pt(o,-2.05*x,-2.05*y,s),end,col,3); text(d,(end[0]+5,end[1]-10),name,23,col)
    v=pt(o,al,be,s); pd=pt(o,id_*co,id_*si,s); pq=pt(o,-iq*si,iq*co,s)
    d.line((*pd,*v),fill=ORANGE,width=2); d.line((*pq,*v),fill=B,width=2); arrow(d,o,v,BLUE,5)
    text(d,(55,625),f'θe = {math.degrees(t)%360:5.1f}°   iα={al:+.3f}   iβ={be:+.3f} A',21,BLUE)
    text(d,(690,135),'在随转子旋转的观察坐标中',25)
    oo=(895,480); arrow(d,(710,480),(1195,480),ORANGE,3); text(d,(1200,475),'d',22,ORANGE)
    arrow(d,(895,590),(895,220),B,3); text(d,(900,195),'q',22,B)
    vv=pt(oo,id_,iq,s); d.line((vv[0],480,*vv),fill=ORANGE,width=2); d.line((895,vv[1],*vv),fill=B,width=2); arrow(d,oo,vv,BLUE,5)
    text(d,(960,505),'id = 1.000 A',22,ORANGE); text(d,(685,285),'iq = 1.500 A',22,B)
    text(d,(690,625),'矢量和坐标轴同步转动 → dq 分量不变',22)
    text(d,(40,710),'id = iα cosθe + iβ sinθe',25); text(d,(650,710),'iq = −iα sinθe + iβ cosθe',25)
    text(d,(40,755),'逆变换：iα = id cosθe − iq sinθe； iβ = id sinθe + iq cosθe',25)
    return im

if __name__=='__main__':
    for name,renderer in [('Clarke',clarke),('Park',park)]:
        renderer(math.pi/6).save(ROOT/f'{name}_坐标变换.png')
        frames=[renderer(2*math.pi*k/72).quantize(colors=128) for k in range(72)]
        frames[0].save(ROOT/f'{name}_坐标变换.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,disposal=2,optimize=False)
    # Verify amplitude-invariant Clarke, Park and inverses over one electrical cycle.
    for k in range(361):
        t=math.radians(k); a=2*math.cos(t); b=2*math.cos(t-2*math.pi/3); c=2*math.cos(t+2*math.pi/3)
        x=2/3*(a-b/2-c/2); y=2/3*(math.sqrt(3)/2*(b-c))
        assert abs(x-a)<1e-12 and abs(y-(a+2*b)/math.sqrt(3))<1e-12
        dd=x*math.cos(t)+y*math.sin(t); qq=-x*math.sin(t)+y*math.cos(t)
        assert abs(dd-2)<1e-12 and abs(qq)<1e-12
        assert abs(-x/2+math.sqrt(3)*y/2-b)<1e-12
        assert abs(-x/2-math.sqrt(3)*y/2-c)<1e-12
    for p in ROOT.glob('*'):
        if p.suffix in ('.png','.gif'):
            with Image.open(p) as im: print(p.name,im.size,'frames=',getattr(im,'n_frames',1))
    print('PASS: 361-angle transform checks')
