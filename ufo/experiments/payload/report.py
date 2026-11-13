"""从可审核 JSON 结果生成零外部依赖的离线 HTML；不推断缺失实验。"""
import argparse
import csv
import html
import json
from pathlib import Path
from statistics import mean


def aggregate(path):
    d=json.loads(path.read_text());rows=d['rows']
    p=d['physics']['payload']
    return dict(task=d['task'],title=d['title'],condition=d['condition'],mass_kg=p['mass_kg'],offset_m=p['offset_m'],
                horizon_s=d['protocol']['horizon_s'],seeds=[r['seed'] for r in rows],n=len(rows),
                successes=sum(r['success'] for r in rows),worst_drift_m=max(r['max_drift_m'] for r in rows),
                failed_seeds=[dict(seed=r['seed'],hold_fraction=r['hold_fraction'],max_drift_m=r['max_drift_m']) for r in rows if not r['success']],
                **{k:mean(r[k] for r in rows) for k in ('hold_fraction','survival_s','joint_mae_rad','height_error_m','key_body_error_m','max_drift_m','speed_mps','tilt_deg','slip_mps','torque_saturation_fraction')},
                source='raw/eval/'+path.name)


def build(root,output):
    root,output=Path(root),Path(output);output.mkdir(parents=True,exist_ok=True)
    records=[aggregate(p) for p in sorted((root/'eval').glob('*.json'))]
    final=[r for r in records if r['horizon_s']>=29]
    screening=[aggregate(p) for p in sorted((root/'screening').glob('*.json'))] if (root/'screening').exists() else [r for r in records if r['horizon_s']<29]
    search={p.stem:json.loads(p.read_text()) for p in (root/'search').glob('*.json')}
    tasks=json.loads((root/'tasks.json').read_text())
    payload=dict(results=final,screening=screening,search=search,tasks=tasks)
    (output/'data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    if final:
        with (output/'summary.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(final[0]),lineterminator='\n');writer.writeheader();writer.writerows(final)
    # Inspector tables and charts read exactly the same embedded rows; works under file://.
    template=r'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UFO 固定姿态负载与 CEM 实验</title>
<style>
:root{color-scheme:light;--ink:#1b2d35;--muted:#536772;--line:#d9e3e7;--blue:#2e6988;--green:#24876d;--orange:#ca7933}*{box-sizing:border-box}body{font-family:system-ui,"Noto Sans CJK SC",sans-serif;margin:0;background:#f5f7f8;color:var(--ink);line-height:1.7}main{max-width:1190px;margin:auto;padding:42px 26px 80px}h1{font-size:32px;margin:0 0 8px}h2{font-size:23px;margin:40px 0 15px}h3{font-size:18px;margin:14px 0}p{margin:10px 0}.meta,.muted{color:var(--muted);font-size:14px}.lead{font-size:18px;max-width:970px}.panel{background:white;border:1px solid var(--line);border-radius:10px;padding:20px;margin:14px 0}.notice{border-left:4px solid var(--orange);padding-left:17px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.kpi{font-size:28px;font-weight:650}.controls{display:flex;gap:15px;flex-wrap:wrap;align-items:center}select{font:inherit;background:white;border:1px solid #b9ccd5;padding:6px 10px;border-radius:6px}table{width:100%;border-collapse:collapse;font-size:14px;white-space:nowrap}th,td{padding:10px 12px;text-align:right;border-bottom:1px solid var(--line)}th:first-child,td:first-child{text-align:left}th{color:var(--muted);font-weight:600}a{color:var(--blue)}.scroll{overflow:auto}svg{width:100%;display:block;max-height:320px}video{width:100%;background:#ddd;border-radius:8px}code{font-size:13px;overflow-wrap:anywhere}details{margin:15px 0}summary{cursor:pointer;font-weight:600}.pill{display:inline-block;background:#e4efed;color:#226451;padding:2px 8px;border-radius:6px;font-size:12px}.bad{color:#a54f2b}.good{color:#21755d}.videos{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:800px){.grid,.videos{grid-template-columns:1fr}main{padding:25px 15px}h1{font-size:27px}}
</style><main><div class="meta">2026-11-13 · Astro P2 · 冻结 UFO 小网络 · 离线实验报告</div><h1>固定姿态负载适应：只调整 z，能否恢复稳定？</h1>
<div id="verdict" class="lead"></div><p class="meta">模型：0cui9p7l / 191,995,904 steps。所有数值来自实际闭环仿真；没有更新 Actor、Backward 或归一化器。</p>
<h2>主实验按四组比较</h2><p>① 无负载 + 原始 z₀ → ② 负载 + 原始 z₀ → ③ 同一负载 + CEM z* → ④ 无负载 + z*。先用预筛种子确定负载，正式验证使用未参与搜索的五组初始扰动。</p>
<div class="panel controls"><label>姿态 <select id="task"></select></label><label>负载条件 <select id="load"></select></label></div>
<div class="grid" id="cards"></div><div class="panel"><h3>保持目标姿态的时间比例</h3><div id="bars"></div><p class="meta">越高越好。横轴 0–100%；分母是完整评估时长扣除最初 2 秒。失败后的帧计为未保持，不会因自动重置获得额外分数。</p></div>
<div class="panel scroll"><table id="comparison"></table></div><p class="meta">表中姿态误差只统计存活帧；必须同时看完整时长的保持比例和位移，不能只用较低 MAE 判断成功。成功率为五次实验的计数，不能外推总体可靠性。</p>
<h2>CEM 是否真正改善了搜索目标？</h2><div class="panel"><div id="curve"></div><p class="meta">分数越高越好。曲线为截至该代实际试过的最佳候选；原始 z₀ 分数远低于曲线范围，数值另行标注。候选优劣由两个共同初始条件的平均分确定，正式验证不复用这两个种子。</p></div>
<h2>可视化对照</h2><p>同一姿态、同一负载、同一初始扰动，左侧原始 z₀，右侧 CEM z*；固定世界相机保留位移证据。影片按真实仿真时间播放，不能替代五组种子的数值结果。此处“失稳”主要指无法维持原地目标，不代表原始策略每次都跌倒。</p><div class="videos" id="movies"></div>
<h2>怎样理解结果</h2><div id="interpretation"></div><div class="notice"><p>本轮支持的是“在已选固定姿态与所测负载下，搜索固定 z 的可行性”。不能据此声称支持未知负载自动估计、在线自适应、所有姿态泛化或真机负重；CEM 使用已知仿真负载，且每个目标各搜索一个 z。</p></div>
<h2>方法与边界</h2><details open><summary>负载、目标与成功判据</summary><p>负载是刚性固定的长方体，安装在 waist_roll_link。质量、质心及完整惯量用平行轴定理合成，保持关节数、被跟踪 body 和观察维度不变。橙色几何只用于显示，不与机器人或地面额外碰撞。本轮不是手部抓取或可滑动负载。</p><p>三个主目标为显式固定姿态，FK 对齐脚底后通过原模型 Backward 生成 z₀。它们不等同于用户原先 20 个 Goal；原有 20 个 Goal 和 Motion 均保留。中蹲和两个单腿在无负载预检不满足稳定标准，因此不纳入主负载适应结论。</p><p>从相同的 YAML 中立站姿进入，初始高度 0.645 m、速度为零，Actor history 和 last_action 清空；未把机器人直接放到目标姿态。初始关节扰动标准差 0.015 rad。关闭域随机化、推力和观察噪声。部署手柄连续切换时不会清空历史，因此不能与此处独立复位结果等同。</p><p>保持帧必须同时满足：平均关节误差 &lt;0.18 rad、root 高度误差 &lt;0.07 m、局部关键 body 误差 &lt;0.10 m、从起点的平面位移 &lt;0.15 m、倾角 &lt;20°、双脚接触且无非脚接触。单次成功要求完整 30 秒存活且扣除前 2 秒后超过 90% 的帧满足上述条件。失败条件为非有限状态、root&lt;0.28 m、倾角&gt;60°或仿真终止。</p></details>
<details><summary>搜索预算与防止换任务</summary><p>z∈R²⁵⁶，范数保持 16。局部球面 CEM：128 候选、16 精英、20 代，两个共同初始条件（0/11），每次 10 秒；相对 z₀ 的夹角限制 0.55 rad。代价同时包含关节/高度/局部 body 的姿态误差、位移、速度、脚滑、倾角、力矩饱和、非脚接触及动作变化；终止后的每一步持续计失败代价 100。每代强制评估 z₀、历史最优和当前均值。最终导出的是实测过的最佳候选。</p><p>每个任务目前只有一次固定随机种子的 CEM 搜索。多次初始化的验证不等于多次独立优化；不能把一次 CEM 的收益当作统计稳定的算法优势。</p></details>
<details><summary>负载预筛与全部数值</summary><p>预筛只用种子 0/11、15 秒；其作用是确认“无负载稳定、加载后退化”，不是正式成功率。没有根据正式验证结果改选目标或替换原始 z。</p><div class="scroll"><table id="screen"></table></div></details>
<details><summary>数据、代码与复现</summary><p><a href="data.json">结构化数据与 CEM 历史</a> · <a href="summary.csv">正式结果 CSV</a> · <a href="raw/tasks.json">固定目标与原始 z 哈希</a> · <a href="reproduce.md">代码版本、运行命令及部署说明</a></p><p>raw/eval 保存每个种子的结果与完整协议，raw/protocol 保存负载及 XML/模型哈希，raw/checks 保存模型前后指纹，raw/original 和 raw/optimized 保存原始与优化 z。报告所有图表直接使用内嵌的同一份结果，不需要网络、服务端或 CDN。</p></details><footer class="meta">生成器：ufo.experiments.payload.report · 请连同 videos/ 和 raw/ 一起保存本目录。</footer></main>
<script>const DATA=__DATA__;
const names={original:'原始 z₀',cem:'CEM z*'};const $=s=>document.querySelector(s);const fmt=(v,n=3)=>Number(v).toFixed(n);const tasks=DATA.tasks.filter(t=>['stand','arms_forward','shallow_squat'].includes(t.name));
const cond=r=>r.mass_kg+' kg / x='+r.offset_m[0]+' m';const conditions=[...new Set(DATA.results.filter(r=>r.mass_kg>0).map(cond))];
$('#task').innerHTML=tasks.map(t=>`<option value="${t.name}">${t.title}</option>`).join('');$('#load').innerHTML=conditions.map(t=>`<option>${t}</option>`).join('');
function table(target,rows,screen=false){$(target).innerHTML='<thead><tr><th>姿态 / 条件</th><th>成功</th><th>保持</th><th>关节误差 rad</th><th>高度误差 m</th><th>最大位移均值 m</th><th>最差一次 m</th><th>脚滑 m/s</th><th>饱和比例</th></tr></thead><tbody>'+rows.map(r=>`<tr><td>${screen?r.title+' · ':''}${cond(r)} · ${names[r.condition]}</td><td>${r.successes}/${r.n}</td><td>${fmt(100*r.hold_fraction,1)}%</td><td>${fmt(r.joint_mae_rad)}</td><td>${fmt(r.height_error_m)}</td><td>${fmt(r.max_drift_m)}</td><td>${fmt(r.worst_drift_m)}</td><td>${fmt(r.slip_mps)}</td><td>${fmt(r.torque_saturation_fraction*100,2)}%</td></tr>`).join('')+'</tbody>'}
function render(){let task=$('#task').value;const rank=r=>r.mass_kg===0?(r.condition==='original'?0:3):(r.condition==='original'?1:2);const rows=DATA.results.filter(r=>r.task===task&&(r.mass_kg===0||cond(r)===$('#load').value)).sort((a,b)=>rank(a)-rank(b));table('#comparison',rows);const a=rows.find(r=>r.mass_kg===0&&r.condition==='original'),b=rows.find(r=>r.mass_kg>0&&r.condition==='original'),c=rows.find(r=>r.mass_kg>0&&r.condition==='cem');$('#cards').innerHTML=[['无负载原始保持',a],['负载原始保持',b],['负载 CEM 保持',c]].map(([label,r])=>`<div class="panel"><div class="muted">${label}</div><div class="kpi">${r?fmt(r.hold_fraction*100,1)+'%':'未测'}</div><div class="meta">${r?r.successes+'/'+r.n+' 次达到严格成功标准':''}</div></div>`).join('');
const colors=['#7f97a3','#c77d41','#27856e','#4a789c'];$('#bars').innerHTML=`<svg viewBox="0 0 950 ${rows.length*52+40}" role="img" aria-label="完整时长姿态保持比例">`+[0,25,50,75,100].map(x=>`<line x1="${260+x*5.5}" y1="10" x2="${260+x*5.5}" y2="${rows.length*52}" stroke="#dce5e8"/><text x="${260+x*5.5}" y="${rows.length*52+26}" text-anchor="middle" font-size="13">${x}%</text>`).join('')+rows.map((r,i)=>`<text x="245" y="${i*52+31}" text-anchor="end" font-size="14">${cond(r)} · ${names[r.condition]}</text><rect x="260" y="${i*52+13}" width="${r.hold_fraction*550}" height="28" fill="${colors[i%4]}" rx="3"/><text x="${270+r.hold_fraction*550}" y="${i*52+32}" font-size="14">${fmt(r.hold_fraction*100,1)}%</text>`).join('')+'</svg>';
const s=DATA.search[task];if(s){const h=s.history;let min=Math.min(...h.map(x=>x.best_score)),max=Math.max(...h.map(x=>x.best_score));max+=.05*(max-min);const X=i=>70+i*820/Math.max(1,h.length-1),Y=y=>245-(y-min)*195/Math.max(.001,max-min);const line=k=>h.map((x,i)=>(i?'L':'M')+X(i)+','+Y(x[k])).join(' ');$('#curve').innerHTML=`<h3>${tasks.find(t=>t.name===task).title} · ${s.history.length} 代</h3><svg viewBox="0 0 950 285" aria-label="CEM 目标分数曲线"><line x1="70" y1="245" x2="900" y2="245" stroke="#aebdc4"/><path d="${line('best_score')}" fill="none" stroke="#27856e" stroke-width="3"/><text x="70" y="30" font-size="13">最佳 ${fmt(h.at(-1).best_score)} / 原始 ${fmt(h.at(-1).anchor_score)}（图外）</text><text x="70" y="270" font-size="13">第 1 代</text><text x="850" y="270" font-size="13">第 ${h.length} 代</text><text x="15" y="${Y(min)}" font-size="12">${fmt(min,1)}</text><text x="15" y="${Y(max)}" font-size="12">${fmt(max,1)}</text></svg>`}else $('#curve').textContent='未完成搜索';
const token=task+'_'+$('#load').value.replaceAll(' kg / x=','_x').replaceAll(' m','');$('#movies').innerHTML=`<div><h3>${tasks.find(t=>t.name===task).title} · 主负载</h3><video controls preload="metadata" src="videos/${task}.mp4"></video><p class="meta">左原始 / 右 CEM，seed101，30秒</p></div><div><h3>目标固定姿态</h3><img style="width:100%;border-radius:8px" src="videos/${task}_target.jpg" alt="${tasks.find(t=>t.name===task).title}目标姿态"><p class="meta">橙色块标明刚性负载位置；目标图没有经过 CEM 变更。</p></div>`}
if(conditions.includes('8 kg / x=0.3 m'))$('#load').value='8 kg / x=0.3 m';$('#task').onchange=render;$('#load').onchange=render;table('#screen',DATA.screening,true);
const loadResults=DATA.results.filter(r=>r.mass_kg>0);const total=loadResults.filter(r=>r.condition==='cem').reduce((n,r)=>n+r.n,0),success=loadResults.filter(r=>r.condition==='cem').reduce((n,r)=>n+r.successes,0);const main=loadResults.filter(r=>r.mass_kg===8&&r.offset_m[0]===.3),ms=main.filter(r=>r.condition==='cem').reduce((n,r)=>n+r.successes,0),mb=main.filter(r=>r.condition==='original').reduce((n,r)=>n+r.successes,0),mn=main.filter(r=>r.condition==='cem').reduce((n,r)=>n+r.n,0);const taskCounts=main.filter(r=>r.condition==='cem').map(r=>r.title+' '+r.successes+'/'+r.n).join('；');const failures=main.filter(r=>r.condition==='cem').flatMap(r=>r.failed_seeds.map(f=>r.title+' seed'+f.seed+'，最大位移 '+fmt(f.max_drift_m*100,1)+' cm'));$('#verdict').innerHTML=`<p>主负载下，只改变固定 z，严格成功数从 <b>${mb}/${mn}</b> 提高到 <b>${ms}/${mn}</b>。${taskCounts}。</p>`+(failures.length?`<p class="notice">未通过样本：${failures.join('；')}。本轮尚不足以支持直接真机负重。</p>`:'');
$('#interpretation').innerHTML=tasks.map(t=>{let rs=DATA.results.filter(r=>r.task===t.name);return `<p><b>${t.title}：</b>`+rs.filter(r=>r.mass_kg>0&&r.condition==='cem').map(c=>{let b=rs.find(b=>b.condition==='original'&&cond(b)===cond(c));return `${cond(c)}：原始 ${b?fmt(b.hold_fraction*100,1):'未测'}% → CEM ${fmt(c.hold_fraction*100,1)}% 保持，严格成功 ${c.successes}/${c.n}。`}).join(' ')+'</p>'}).join('');render();
</script></html>'''
    (output/'index.html').write_text(template.replace('__DATA__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')))
    return payload

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('output');a=p.parse_args();build(a.root,a.output)
