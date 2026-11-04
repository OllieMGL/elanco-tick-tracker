import { NavLink } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <span className="navbar-title">UK Tick Tracker</span>
      <NavLink to="/" end className="nav-link">Map</NavLink>
      <NavLink to="/report" className="nav-link">Report a sighting</NavLink>
      <NavLink to="/learn" className="nav-link">Learn</NavLink>
    </nav>
  )
}

export default Navbar
