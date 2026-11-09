"""Regenerate publication figures from saved study summaries; no model execution."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,
 'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,
 'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8})
BLUE='#2166a6'; ORANGE='#cc6b20'; GRAY='#a8b1bb'; GREEN='#238572'

# Explanatory figure, not an additional empirical observation.
fig,axs=plt.subplots(1,2,figsize=(7.0,2.25),sharex=True,sharey=True)
for ax,filing,title in zip(axs,[40,68],['Early public filing: day 40','Late public filing: day 68']):
 for y,first,color in [(2,filing,BLUE),(1,max(filing,60),ORANGE),(0,60,GRAY)]:
  ax.plot([0,first],[y,y],color='#d7dde2',lw=3)
  ax.plot([first,75],[y,y],color=color,lw=6,solid_capstyle='butt')
  ax.scatter([first],[y],color=color,s=28,zorder=3)
 ax.axvline(filing,color=BLUE,ls=':',lw=1)
 ax.axvline(60,color=ORANGE,ls='--',lw=1)
 ax.set_title(title,fontsize=10,weight='bold',pad=9)
 ax.set_xlim(0,76);ax.set_ylim(-.5,2.5)
 ax.set_xticks([0,20,40,60,75]);ax.set_xlabel('Calendar days after report date')
 ax.set_yticks([0,1,2],['Fixed day 60','Max(filing, day 60)','Filing date'])
 ax.grid(axis='x',alpha=.15)
axs[0].annotate('Available, but withheld',xy=(50,1),xytext=(30,-.48),fontsize=8,
 arrowprops={'arrowstyle':'->','color':ORANGE},color=ORANGE)
axs[1].annotate('Premature use',xy=(64,0),xytext=(23,.45),fontsize=8,
 arrowprops={'arrowstyle':'->','color':'#555'},color='#555')
fig.tight_layout(w_pad=1.5);fig.savefig(ROOT/'figures/timing.pdf',bbox_inches='tight');plt.close(fig)

s=json.loads((ROOT/'evidence/A04_SUMMARY.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(7.0,2.7),sharey=True)
for ax,vendor,label in zip(axs,['GPT','CLAUDE'],['GPT: High (3/5)','Claude: Opus 5.5 Extra']):
 cells=[c for c in s['cells'] if c['vendor']==vendor]
 for x,c in enumerate(cells):
  p=c['all_seed_policy_counts']; standard=sum(p[k] for k in ['floor60_inclusive','floor60_strict'])
  exact=p['filing_inclusive'];strict=p['filing_strict'];other=3-standard-exact-strict
  bottom=0
  for n,color,hatch in [(exact,BLUE,None),(strict,GRAY,None),(standard,ORANGE,None),(other,'#f8ddc2','////')]:
   if n:
    ax.bar(x,n,bottom=bottom,width=.68,color=color,edgecolor='#555' if hatch else 'white',hatch=hatch,lw=.5)
    ax.text(x,bottom+n/2,str(n),ha='center',va='center',color='white' if color in [BLUE,ORANGE] else '#222',fontsize=9,weight='bold')
   bottom+=n
 ax.axvline(2.5,color='#bbb',lw=.7);ax.set_ylim(0,3.2);ax.set_yticks([0,1,2,3])
 ax.set_xticks(range(6),['N-PORT\n'+c['condition'] if c['form']=='NPORT' else '13F\n'+c['condition'] for c in cells])
 ax.set_title(label,fontsize=10,weight='bold');ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
axs[0].set_ylabel('First-answer programs')
handles=[Patch(facecolor=BLUE,label='Filing day included'),Patch(facecolor=GRAY,label='Filing day excluded'),Patch(facecolor=ORANGE,label='60-day floor (frozen)'),Patch(facecolor='#f8ddc2',edgecolor='#555',hatch='////',label='Calendar floor (post hoc)')]
fig.legend(handles=handles,loc='lower center',ncol=2,fontsize=8,frameon=False,bbox_to_anchor=(.5,-.08))
fig.tight_layout(rect=(0,.14,1,1));fig.savefig(ROOT/'figures/policies.pdf',bbox_inches='tight');plt.close(fig)

s=json.loads((ROOT/'evidence/metadata_recheck.json').read_text())['full_cohort']
labels=list(s['bins']);vals=[100*s['bins'][x]/s['n'] for x in labels]
fig,ax=plt.subplots(figsize=(3.45,2.65));bars=ax.bar(labels,vals,color=[GRAY]+[BLUE]*5,width=.68)
for b,v in zip(bars,vals):ax.text(b.get_x()+b.get_width()/2,v+.6,f'{v:.1f}',ha='center',fontsize=8)
ax.set_ylim(0,33);ax.set_ylabel('Accessions (%)');ax.set_xlabel('Additional calendar days')
ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
ax.text(.98,.97,'Mean: 4.13 days\nMedian: 3 days',transform=ax.transAxes,ha='right',va='top',fontsize=8)
fig.tight_layout();fig.savefig(ROOT/'figures/metadata.pdf',bbox_inches='tight');plt.close(fig)
import runpy
runpy.run_path(str(ROOT/'make_rule_timeline.py'), run_name='__main__')
print('Generated four vector PDF figures: three evidence illustrations and the rule chronology.')
