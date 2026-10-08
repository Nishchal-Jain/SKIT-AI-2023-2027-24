import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

export default function MapView() {
  const position = [12.9716, 77.5946];

  return (
    <div className="h-[500px] w-full rounded-xl overflow-hidden shadow-sm border border-slate-200">
      <MapContainer center={position} zoom={12} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>Bengaluru Center</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}