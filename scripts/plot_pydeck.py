# scripts/plot_pydeck.py
import pydeck as pdk

def plot_aircraft_pydeck(current_df, full_df, up_to_time):
    # Filter past data for trails
    trail_df = full_df[full_df["Time"] <= up_to_time]

    # Group trail points by flight
    paths = []
    for flight in trail_df["Flight"].unique():
        flight_points = trail_df[trail_df["Flight"] == flight]
        path = flight_points[["Lon", "Lat"]].values.tolist()
        if len(path) > 1:
            paths.append({
                "Flight": flight,
                "path": path
            })

    # Path layer for trails
    path_layer = pdk.Layer(
        "PathLayer",
        data=paths,
        get_path="path",
        get_width=3,
        get_color=[200, 30, 0],
        pickable=True,
        width_min_pixels=2
    )

    # Dot layer for current aircraft position
    dot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=current_df,
        get_position="[Lon, Lat]",
        get_fill_color="[0, 100, 255, 160]",
        get_radius=30,
        pickable=True,
        auto_highlight=True,
    )

    tooltip = {
        "html": "<b>{Flight}</b><br>Status: {Status}<br>Gate: {Gate}",
        "style": {"color": "white"}
    }

    # Map view - Ottawa airport
    view_state = pdk.ViewState(
        latitude=45.3192,
        longitude=-75.6675,
        zoom=14,
        pitch=0,
    )

    # Composite layer rendering
    return pdk.Deck(
        layers=[path_layer, dot_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9",
    )
