import 'leaflet/dist/leaflet.css'
import { useEffect } from 'react'
import { CircleMarker, MapContainer, TileLayer, Tooltip, useMap } from 'react-leaflet'

const UK_BOUNDS = [[49.8, -8.2], [60.9, 1.8]]

// stops the user zooming out any further than the zoom that just fits the whole UK
function LimitZoomToUK() {
  const map = useMap()

  useEffect(() => {
    map.setMinZoom(map.getBoundsZoom(UK_BOUNDS))
  }, [map])

  return null 
}

// cities is e.g. {"London": {"lat": 51.5, "lng": -0.13}, ...} from /api/options
function SightingsMap({ cities }) {
  return (
    <MapContainer
      bounds={UK_BOUNDS}          // start zoomed to fit the whole UK
      maxBounds={UK_BOUNDS}       // can't drag the map away from the UK
      maxBoundsViscosity={1.0}    // 1.0 = a hard edge
      zoomSnap={0.25}             
      className="h-[70vh] w-full"
    >
      <LimitZoomToUK />
      {/* the map images themselves ==> OpenStreetMap*/}
      <TileLayer
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {Object.entries(cities).map(([name, { lat, lng }]) => (
        <CircleMarker key={name} center={[lat, lng]} radius={8}>
          <Tooltip>{name}</Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  )
}

export default SightingsMap
