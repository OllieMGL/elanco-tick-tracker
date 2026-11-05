import { useEffect, useState } from 'react'

import CitySidebar from '../components/CitySidebar'
import SightingsMap from '../components/SightingsMap'

function MapPage() {
  const [counts, setCounts] = useState({})
  const [cities, setCities] = useState({})
  const [speciesList, setSpeciesList] = useState([])
  const [serverError, setServerError] = useState(null)

  const [species, setSpecies] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')

  const [selectedCity, setSelectedCity] = useState(null)  // the city clicked on the map, or null

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/options`)
      .then((response) => response.json())
      .then((data) => {
        setCities(data.cities)
        setSpeciesList(data.species)
      })
      .catch(() => setServerError("Can't reach the server"))
  }, [])

  // load the counts again every time a filter changes
  useEffect(() => {
    // only add the filters that have been picked, e.g. "species=Marsh+tick&start=2024-01-01"
    const filters = new URLSearchParams()
    if (species) filters.append('species', species)
    if (start) filters.append('start', start)
    if (end) filters.append('end', end)

    fetch(`${import.meta.env.VITE_API_URL}/api/stats/regions?${filters}`)
      .then((response) => response.json())
      .then((data) => setCounts(data))
      .catch(() => setServerError("Can't reach the server"))
  }, [species, start, end])

  // add up every city's count to get the total
  const totalSightings = Object.values(counts).reduce((total, count) => total + count, 0)

  return (
    <div className="page">
      <h1 className="page-title">Tick sightings map</h1>
      {serverError && <p className="server-error">{serverError}</p>}

      <div className="map-filters">
        <label>
          Species
          <select value={species} onChange={(event) => setSpecies(event.target.value)}>
            <option value="">All species</option>
            {speciesList.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
        </label>

        <label>
          From
          <input type="date" value={start} onChange={(event) => setStart(event.target.value)} />
        </label>

        <label>
          To
          <input type="date" value={end} onChange={(event) => setEnd(event.target.value)} />
        </label>
      </div>

      <p>{totalSightings} sightings across {Object.keys(counts).length} cities</p>
      {/* the map and the sidebar side by side */}
      <div className="map-layout">
        <div className="map-column">
          <SightingsMap cities={cities} counts={counts} onSelectCity={setSelectedCity} />
        </div>
        <CitySidebar
          city={selectedCity}
          species={species}
          start={start}
          end={end}
          onClose={() => setSelectedCity(null)}
        />
      </div>
    </div>
  )
}

export default MapPage
