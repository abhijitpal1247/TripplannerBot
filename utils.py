from typing import Dict, Any

import folium


def get_route_leafmap(route: Dict[str, Any]):
    m = folium.Map(location=route[0], zoom_start=13, tiles='cartodbpositron')
    folium.PolyLine(locations=route).add_to(m)
    bounds = m.get_bounds()

    # Zoom to fit the markers
    m.fit_bounds(bounds)
    return m
