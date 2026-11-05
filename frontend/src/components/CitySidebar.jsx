import { useEffect, useState } from 'react'


function CitySidebar({ city, species, start, end, onClose }) {
  const [sightings, setSightings] = useState([])
  const [error, setError] = useState(null)

  // load the city's sightings whenever a different city is clicked or a filter changes
  useEffect(() => {
    if (!city) return  // nothing to load until a city is clicked

    const filters = new URLSearchParams()
    filters.append('location', city)
    if (species) filters.append('species', species)
    if (start) filters.append('start', start)
    if (end) filters.append('end', end)

    fetch(`${import.meta.env.VITE_API_URL}/api/sightings?${filters}`)
      .then((response) => response.json())
      .then((data) => setSightings(data))
      .catch(() => setError("Couldn't load this city's sightings"))
  }, [city, species, start, end])

  if (!city) {
    return (
      <aside className="city-sidebar">
        <p>Click a city on the map to see its sightings.</p>
      </aside>
    )
  }

  // {"Marsh tick": 12, "Tree-hole tick": 9}
  const speciesCounts = {}
  for (const sighting of sightings) {
    speciesCounts[sighting.species] = (speciesCounts[sighting.species] || 0) + 1
  }

  const recentSightings = sightings.slice(0, 5)  // the list is newest first

  return (
    <aside className="city-sidebar">
      <button className="close-button" onClick={onClose}>Close</button>
      <h2 className="sidebar-title">{city}</h2>
      {error && <p className="server-error">{error}</p>}
      <p>{sightings.length} sightings</p>

      <h3 className="sidebar-heading">By species</h3>
      <ul>
        {Object.entries(speciesCounts).map(([name, count]) => (
          <li key={name}>{name}: {count}</li>
        ))}
      </ul>

      <h3 className="sidebar-heading">Most recent</h3>
      <ul>
        {recentSightings.map((sighting) => (
          <li key={sighting.id}>
            {new Date(sighting.date).toLocaleDateString('en-GB')} - {sighting.species}
          </li>
        ))}
      </ul>
    </aside>
  )
}

export default CitySidebar
