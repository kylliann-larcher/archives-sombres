"""Rend les plans par lots dans un budget de temps. Usage: python3 run_shots.py 025 [reset]"""
import sys,os,time,json
from pathlib import Path
N=sys.argv[1]; D=Path(__file__).resolve().parent/N
os.chdir(D); sys.path.insert(0,str(D))
import engine
from multiprocessing import Pool
mark=D/'shots'/'v3.done'
if len(sys.argv)>2 and sys.argv[2]=='reset' or not mark.exists():mark.write_text('[]')
done=set(json.loads(mark.read_text()))
n=len(engine.all_shots()); todo=[i for i in range(n) if i not in done]
t0=time.time()
if __name__=='__main__':
    os.makedirs(D/'shots',exist_ok=True)
    with Pool(2) as p:
        k=0
        while k<len(todo) and time.time()-t0<95:
            batch=todo[k:k+2];k+=2
            for i in p.map(engine.render_shot,[(i,f'{D}/shots/shot_{i:02d}.mp4') for i in batch]):
                done.add(i);mark.write_text(json.dumps(sorted(done)))
    print('DONE',len(done),'/',n,'elapsed',round(time.time()-t0),flush=True)
