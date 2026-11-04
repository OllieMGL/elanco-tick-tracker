import { BrowserRouter, Route, Routes } from 'react-router-dom'

import Navbar from './components/Navbar'
import LearnPage from './pages/LearnPage'
import MapPage from './pages/MapPage'
import ReportPage from './pages/ReportPage'

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<MapPage />} />
          <Route path="/report" element={<ReportPage />} />
          <Route path="/learn" element={<LearnPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
