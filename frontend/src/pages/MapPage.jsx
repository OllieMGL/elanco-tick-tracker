import { useEffect, useState } from 'react'

import SightingsMap from '../components/SightingsMap'

function MapPage() {
  const [counts, setCounts] = useState({})  // sightings per city
  const [cities, setCities] = useState({})  // each city's coordinates, e.g. {"London": {lat, lng}}
  const [serverError, setServerError] = useState(null)

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/options`)
      .then((response) => response.json())
      .then((data) => setCities(data.cities))
      .catch(() => setServerError("Can't reach the server"))

    fetch(`${import.meta.env.VITE_API_URL}/api/stats/regions`)
      .then((response) => response.json())
      .then((data) => setCounts(data))
      .catch(() => setServerError("Can't reach the server"))
  }, [])

  // add up every city's count to get the total
  const totalSightings = Object.values(counts).reduce((total, count) => total + count, 0)

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Tick sightings map</h1>
      {serverError && <p className="text-red-600">{serverError}</p>}
      <p>{totalSightings} sightings across {Object.keys(counts).length} cities</p>
      <SightingsMap cities={cities} />
    </div>
  )
}

export default MapPage
