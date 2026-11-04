import { NavLink } from 'react-router-dom'

// bold + underlined for the page you're on, underline on hover for the others
const linkStyle = ({ isActive }) => (isActive ? 'font-semibold underline' : 'hover:underline')

function Navbar() {
  return (
    <nav className="flex items-center gap-6 bg-green-800 px-6 py-3 text-white">
      <span className="text-lg font-bold">UK Tick Tracker</span>
      <NavLink to="/" end className={linkStyle}>Map</NavLink>
      <NavLink to="/report" className={linkStyle}>Report a sighting</NavLink>
      <NavLink to="/learn" className={linkStyle}>Learn</NavLink>
    </nav>
  )
}

export default Navbar
