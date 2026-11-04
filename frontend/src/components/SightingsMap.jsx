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

const BIGGEST_RADIUS = 25  // size of radius for the busiest city

// circle size for a city - the square root makes the circle's AREA match the count,
function markerRadius(count, maxCount) {
  return Math.max(4, BIGGEST_RADIUS * Math.sqrt(count / maxCount))  // never smaller than 4
}

const LEVELS = {
  high: { label: 'High activity', colour: '#dc2626' },
  medium: { label: 'Medium activity', colour: '#f59e0b' },
  low: { label: 'Low activity', colour: '#16a34a' }, 
  none: { label: 'No sightings', colour: '#9ca3af' },
}

// how busy city is compared with busiest city ==> top third = high && middle third = medium
function activityLevel(count, maxCount) {
  if (count === 0) return 'none'
  if (count >= maxCount * 2 / 3) return 'high'
  if (count >= maxCount / 3) return 'medium'
  return 'low'
}

function SightingsMap({ cities, counts }) {
  const maxCount = Math.max(1, ...Object.values(counts))  // the busiest city's count --> fallback 1 

  return (
    <div>
      <MapContainer
        bounds={UK_BOUNDS}          // start zoomed to fit the whole UK
        maxBounds={UK_BOUNDS}       // can't drag the map away from the UK
        maxBoundsViscosity={1.0}    // 1.0 = a hard edge
        zoomSnap={0.25}
        className="sightings-map"
      >
        <LimitZoomToUK />
        {/* the map images themselves ==> OpenStreetMap*/}
        <TileLayer
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {Object.entries(cities).map(([name, { lat, lng }]) => {
          const count = counts[name] || 0  // a city with no sightings not in counts
          const level = LEVELS[activityLevel(count, maxCount)]

          return (
            <CircleMarker
              key={name}
              center={[lat, lng]}
              radius={markerRadius(count, maxCount)}
              pathOptions={{ color: level.colour, fillColor: level.colour, fillOpacity: 0.6 }}
            >
              <Tooltip>{name}: {count} sightings ({level.label})</Tooltip>
            </CircleMarker>
          )
        })}
      </MapContainer>

      {/* key explaining the colours */}
      <div className="map-key">
        {Object.values(LEVELS).map((level) => (
          <span key={level.label} className="map-key-item">
            <span className="map-key-dot" style={{ backgroundColor: level.colour }} />
            {level.label}
          </span>
        ))}
      </div>
    </div>
  )
}

export default SightingsMap
