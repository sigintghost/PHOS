import json, itertools

def simulate(V0, C, L0, Lp, m0, B):
    dt, tEnd = 1e-9, 4e-6
    q=C*V0; i=0.0; x=1e-4; v=0.0; t=0.0
    peakI=0.0; lastV=0.0; lastX=x
    while t < tEnd:
        Ltot=L0+Lp*x
        di=(q/C - Lp*v*i)/Ltot*dt
        q-=i*dt
        M=m0*x+1e-9
        v+=(0.5*Lp*i*i + B*i*0.02 - v*(m0*v))/M*dt
        i+=di; x+=v*dt; t+=dt
        if abs(i)>peakI: peakI=abs(i)
        lastV, lastX = v, x
    swept=m0*lastX+1e-9
    imp=swept*lastV
    eIn=0.5*C*V0*V0
    eKin=0.5*swept*lastV*lastV
    eff=max(0.0, min(100.0, eKin/eIn*100))
    return {"pkI":peakI/1000,"vEx":lastV/1000,"imp":imp*1e6,"eff":eff}

VARS={"V0":(500,3000,1500,1.0),"C":(0.5,6.0,2.0,1e-6),
      "L0":(10,100,30,1e-9),"Lp":(0.1,1.0,0.40,1e-6),
      "m0":(0.3,3.0,1.0,1e-6),"B":(0.0,2.0,0.0,1.0)}

def base_si():
    return {k:VARS[k][2]*VARS[k][3] for k in VARS}

def run_pair(a,b,n=11):
    la,ha=VARS[a][0],VARS[a][1]
    lb,hb=VARS[b][0],VARS[b][1]
    grid=[]
    for ia in range(n):
        ra=la+(ha-la)*ia/(n-1); row=[]
        for ib in range(n):
            rb=lb+(hb-lb)*ib/(n-1)
            ar=base_si(); ar[a]=ra*VARS[a][3]; ar[b]=rb*VARS[b][3]
            o=simulate(**ar)
            row.append({"a":round(ra,4),"b":round(rb,4),
                "pkI":round(o["pkI"],3),"vEx":round(o["vEx"],4),
                "imp":round(o["imp"],4),"eff":round(o["eff"],4)})
        grid.append(row)
    return grid

def curvature(grid,key):
    n=len(grid); worst=0.0; where=None
    for r in range(1,n-1):
        for c in range(1,n-1):
            v=grid[r][c][key]
            lap=(grid[r-1][c][key]+grid[r+1][c][key]
                 +grid[r][c-1][key]+grid[r][c+1][key]-4*v)
            if abs(lap)>worst:
                worst=abs(lap)
                where={"a":grid[r][c]["a"],"b":grid[r][c]["b"],key:v}
    return {"bend":round(worst,4),"at":where}

def main():
    pairs=list(itertools.combinations(VARS.keys(),2))
    rep={"model":"snowplow_slug_v1","outputs":["pkI","vEx","imp","eff"],
         "vars":{k:{"min":VARS[k][0],"max":VARS[k][1],"base":VARS[k][2]} for k in VARS},
         "pairs":[]}
    for a,b in pairs:
        g=run_pair(a,b)
        e={"pair":[a,b],"grid":g,"bends":{}}
        for key in ("eff","imp","vEx"):
            e["bends"][key]=curvature(g,key)
        rep["pairs"].append(e)
    ranked=sorted(rep["pairs"],key=lambda p:p["bends"]["eff"]["bend"],reverse=True)
    rep["orchestrator_hint"]=[{"pair":p["pair"],
        "eff_bend":p["bends"]["eff"]["bend"],
        "imp_bend":p["bends"]["imp"]["bend"],
        "hottest_at":p["bends"]["eff"]["at"]} for p in ranked[:5]]
    with open("agents/map_report.json","w") as f:
        json.dump(rep,f,indent=1)
    print("mapped",len(pairs),"pairs -> agents/map_report.json")
    for h in rep["orchestrator_hint"]:
        p=h["pair"]
        print(f"  {p[0]:>3}x{p[1]:<3} eff_bend={h['eff_bend']:.3f} imp_bend={h['imp_bend']:.3f}")

if __name__ == "__main__":
    main()
