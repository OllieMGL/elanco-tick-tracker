// the panel beside the map - city is the name of the clicked city, or null if none is picked
function CitySidebar({ city, onClose }) {
  if (!city) {
    return (
      <aside className="city-sidebar">
        <p>Click a city on the map to see its sightings.</p>
      </aside>
    )
  }

  return (
    <aside className="city-sidebar">
      <button className="close-button" onClick={onClose}>Close</button>
      <h2 className="sidebar-title">{city}</h2>
    </aside>
  )
}

export default CitySidebar
