import React from "react";
import {
  MapContainer,
  Marker,
  Polyline,
  Tooltip,
  TileLayer,
} from "react-leaflet";

const limeOptions = { color: "tomato", opacity: 0.5 };

const Map = ({ flightPlan }) => {
  const multiPolyline = [
    [
      [flightPlan[0].latitude || "", flightPlan[0].longitude || ""],
      [flightPlan[1].latitude || "", flightPlan[1].longitude || ""],
    ],
  ];

  return (
    <MapContainer
      center={[-11.169684, -50.233758]}
      zoom={4}
      scrollWheelZoom={false}
      className="leaflet-map"
    >
      <TileLayer
        attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
      />
      <Marker
        position={[flightPlan[0].latitude || "", flightPlan[0].longitude || ""]}
        opacity="1"
      >
        <Tooltip direction="top" offset={[-15, 5]} opacity={1} permanent>
          {flightPlan[0].icao}
        </Tooltip>
      </Marker>

      <Marker
        position={[flightPlan[1].latitude || "", flightPlan[1].longitude || ""]}
        opacity="1"
      >
        <Tooltip direction="top" offset={[-15, 5]} opacity={1} permanent>
          {flightPlan[1].icao}
        </Tooltip>
      </Marker>

      <Polyline pathOptions={limeOptions} positions={multiPolyline} />
    </MapContainer>
  );
};

export default Map;
