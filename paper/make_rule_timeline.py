"""Draw the SEC document chronology; explanatory, not an empirical result."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
BLUE = '#2166a6'
GRAY = '#596470'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'pdf.fonttype': 42})
fig, ax = plt.subplots(figsize=(7.0, 1.75))
ax.set_xlim(2014.8, 2027.5)
ax.set_ylim(-1.0, 1.0)
ax.axis('off')
ax.plot([2016, 2026], [0, 0], color='#b3bbc3', lw=1.4, zorder=1)
items = [
    (2016, 1, 'Adopted', 'Quarter end + 60 days',
     'Third fiscal month; superseded', GRAY),
    (2019, -1, 'Interim final', 'Public upon filing',
     'Third fiscal month; task rule', BLUE),
    (2024, 1, 'Adopted', 'Month end + 60 days',
     'Every month; implementation delayed', GRAY),
    (2026, -1, 'Proposed', 'Quarter end + 60 days',
     'Third fiscal month; not operative', GRAY),
]
for year, side, status, schedule, scope, color in items:
    ax.scatter([year], [0], color=color, s=38, zorder=3)
    # Actual calendar-year spacing is retained; alternating labels avoid overlap.
    ax.text(year, -side * .12, str(year), ha='center', va='center',
            color=color, weight='bold', fontsize=10)
    ax.plot([year, year], [side * .05, side * .21], color=color, lw=.8)
    ax.text(year, side * .35, status, ha='center', va='center',
            color=color, weight='bold', fontsize=9)
    ax.text(year, side * .57, schedule, ha='center', va='center',
            color=color, weight='bold', fontsize=9)
    ax.text(year, side * .78, scope, ha='center', va='center',
            color=color, fontsize=7.8)
fig.subplots_adjust(left=.01, right=.99, top=.99, bottom=.01)
fig.savefig(ROOT / 'figures/rule_versions.pdf', bbox_inches='tight', pad_inches=.03)
plt.close(fig)
print('Generated the four-text SEC rule chronology.')
