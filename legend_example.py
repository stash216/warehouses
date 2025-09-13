import folium
from branca.element import Template, MacroElement

# Create a simple map
m = folium.Map(location=[40, -100], zoom_start=4)

# Legend HTML for top right
legend_html = '''
<div style="position: fixed; top: 20px; right: 20px; width: 260px; height: auto; z-index:9999; font-size:14px; background-color:white; border:2px solid grey; border-radius:8px; box-shadow: 2px 2px 8px #888; padding: 14px;">
<b style="font-size:16px;">Legend</b><br><br>
<u>Facility Types</u><br>
<span style="color:blue; font-size:18px;">&#9679;</span> Traditional Sortable<br>
<span style="color:green; font-size:18px;">&#9679;</span> Traditional Non-Sort<br>
<span style="color:purple; font-size:18px;">&#9679;</span> IXD<br>
<span style="color:orange; font-size:18px;">&#9679;</span> Delivery Station<br>
<span style="color:darkred; font-size:18px;">&#9679;</span> Sort Center<br>
<span style="color:darkblue; font-size:18px;">&#9679;</span> Air Gateway<br>
<span style="color:darkgreen; font-size:18px;">&#9679;</span> Specialty<br>
<span style="color:darkviolet; font-size:18px;">&#9679;</span> QUICK COMMERCE<br>
<span style="color:black; font-size:18px;">&#9679;</span> MbA<br>
<span style="color:cadetblue; font-size:18px;">&#9679;</span> Make on Demand<br><br>
<u>Status</u><br>
<span style="color:green; font-size:18px;">&#10004;</span> Active<br>
<span style="color:orange; font-size:18px;">&#9888;</span> Idle<br>
</div>
'''

legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

m.save('legend_example_map.html')
print("Map with legend saved as legend_example_map.html")
