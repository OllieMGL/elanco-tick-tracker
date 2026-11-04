import { useEffect, useState } from 'react'

import SightingsMap from '../components/SightingsMap'

function MapPage() {
  const [counts, setCounts] = useState({})  // sightings per city
  const [cities, setCities] = useState({})  // each city's coordinates
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
    <div className="page">
      <h1 className="page-title">Tick sightings map</h1>
      {serverError && <p className="server-error">{serverError}</p>}
      <p>{totalSightings} sightings across {Object.keys(counts).length} cities</p>
      <SightingsMap cities={cities} counts={counts} />
    </div>
  )
}

export default MapPage
