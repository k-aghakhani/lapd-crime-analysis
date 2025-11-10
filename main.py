# LAPD Crime Analysis Dashboard
# Author: Kiarash Aghakhani
# Project: Analyzing crime patterns in Los Angeles using LAPD open data
# GitHub: https://github.com/k-aghakhani/lapd-crime-analysis.git

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create output directory for saving plots
output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

# Load the dataset from the 'data' folder
# TIME OCC is read as string to preserve leading zeros (e.g., 0015)
print("Loading dataset...")
crimes = pd.read_csv("data/crimes.csv", dtype={"TIME OCC": str}, parse_dates=["Date Rptd", "DATE OCC"])

print(f"Dataset loaded successfully: {crimes.shape[0]:,} crimes, {crimes.shape[1]} columns")
print(f"Date range: {crimes['DATE OCC'].min().date()} to {crimes['DATE OCC'].max().date()}")

# ================================
# Task 1: Peak Crime Hour
# ================================

# Extract hour from TIME OCC (military time as string)
crimes['HOUR OCC'] = crimes['TIME OCC'].str.zfill(4).str[:2].astype(int)

# Count crimes by hour
hour_counts = crimes['HOUR OCC'].value_counts().sort_index()

# Find peak hour
peak_crime_hour = hour_counts.idxmax()

# Plot: Crime Frequency by Hour
plt.figure(figsize=(12, 6))
bars = plt.bar(hour_counts.index, hour_counts.values, color='skyblue', edgecolor='navy', alpha=0.8)
plt.title('Crime Frequency by Hour of Day (24-Hour Format)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Crimes', fontsize=12)
plt.xticks(range(0, 24))
plt.grid(axis='y', alpha=0.3)

# Highlight peak hour
peak_bar = bars[peak_crime_hour]
peak_bar.set_facecolor('red')
peak_bar.set_edgecolor('darkred')

plt.annotate(f'PEAK: {hour_counts[peak_crime_hour]:,} crimes',
             xy=(peak_crime_hour, hour_counts[peak_crime_hour]),
             xytext=(peak_crime_hour, hour_counts[peak_crime_hour] + hour_counts.max()*0.05),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
             fontsize=12, ha='center', color='darkred', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / "peak_crime_hour.png", dpi=300, bbox_inches='tight')
plt.show()

print(f"Peak crime hour: {peak_crime_hour}:00 ({hour_counts[peak_crime_hour]:,} crimes)")

# ================================
# Task 2: Peak Night Crime Location
# ================================

# Define night hours: 10 PM (22) to 3:59 AM (3)
night_hours = [22, 23, 0, 1, 2, 3]
night_crimes = crimes[crimes['HOUR OCC'].isin(night_hours)].copy()

# Count night crimes by area
night_crime_by_area = night_crimes['AREA NAME'].value_counts()

# Find peak night crime location
peak_night_crime_location = night_crime_by_area.idxmax()

# Plot: Top 10 Areas with Most Night Crimes
plt.figure(figsize=(10, 8))
top_night_areas = night_crime_by_area.head(10)
colors = ['salmon' if area != peak_night_crime_location else 'red' for area in top_night_areas.index]

bars = plt.barh(range(len(top_night_areas)), top_night_areas.values, color=colors, edgecolor='black')
plt.title('Top 10 Areas with Most Night Crimes (10 PM - 3:59 AM)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Night Crimes', fontsize=12)
plt.yticks(range(len(top_night_areas)), top_night_areas.index)
plt.gca().invert_yaxis()

# Add value labels
for i, (area, count) in enumerate(top_night_areas.items()):
    plt.text(count + 5, i, f'{count:,}', va='center', fontsize=10, fontweight='bold')

# Highlight peak area
peak_idx = list(top_night_areas.index).index(peak_night_crime_location)
plt.text(top_night_areas[peak_night_crime_location] + 5, peak_idx, 'MOST DANGEROUS AT NIGHT',
         va='center', fontsize=9, color='red', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / "peak_night_crime_location.png", dpi=300, bbox_inches='tight')
plt.show()

print(f"Peak night crime location: {peak_night_crime_location} ({night_crime_by_area[peak_night_crime_location]:,} night crimes)")

# ================================
# Task 3: Victim Age Groups
# ================================

# Define age bins and labels
age_bins = [0, 17, 25, 34, 44, 54, 64, np.inf]
age_labels = ['0-17', '18-25', '26-34', '35-44', '45-54', '55-64', '65+']

# Directly compute age groups (handles invalid ages as NaN, which are excluded in value_counts)
age_groups = pd.cut(crimes['Vict Age'], bins=age_bins, labels=age_labels, right=True)

# Count crimes per age group
victim_ages = age_groups.value_counts().reindex(age_labels, fill_value=0)

# Plot: Victim Age Distribution
plt.figure(figsize=(10, 6))
bars = plt.bar(victim_ages.index, victim_ages.values, color='lightgreen', edgecolor='darkgreen', linewidth=1.2)
plt.title('Number of Crimes by Victim Age Group', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Number of Crimes', fontsize=12)
plt.grid(axis='y', alpha=0.3)

# Add value on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + height*0.01,
             f'{int(height):,}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / "victim_age_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

print("Victim age distribution:")
for age_group, count in victim_ages.items():
    print(f"  {age_group}: {count:,} crimes")

# ================================
# Final Results Summary
# ================================

print("\n" + "="*60)
print("LAPD CRIME ANALYSIS - FINAL RESULTS")
print("="*60)
print(f"1. Peak Crime Hour: {peak_crime_hour}:00 (24-hour format)")
print(f"   → {hour_counts[peak_crime_hour]:,} crimes occurred during this hour")
print(f"2. Most Dangerous Area at Night (10 PM - 3:59 AM): {peak_night_crime_location}")
print(f"   → {night_crime_by_area[peak_night_crime_location]:,} night crimes")
print(f"3. Victim Age Groups:")
for age_group, count in victim_ages.items():
    percentage = (count / victim_ages.sum()) * 100 if victim_ages.sum() > 0 else 0
    print(f"   • {age_group}: {count:,} crimes ({percentage:.1f}%)")
print("="*60)

# Save results to CSV
results_summary = pd.DataFrame({
    "Metric": ["Peak Crime Hour", "Peak Night Crime Location", "Total Crimes Analyzed"],
    "Value": [peak_crime_hour, peak_night_crime_location, len(crimes)]
})
results_summary.to_csv(output_dir / "final_results_summary.csv", index=False)

print(f"All plots and results saved to '{output_dir}' folder.")
print("Project ready for GitHub deployment!")