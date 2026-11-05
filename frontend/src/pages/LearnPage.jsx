import { useEffect, useState } from 'react'
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const SPECIES_GUIDE = [
  {
    name: 'Fox/badger tick',
    latinName: 'Ixodes canisuga',
    foundOn: 'Foxes, badgers and dogs',
    habitat: 'Lives in fox dens and badger setts, so dogs often pick it up near burrows.',
  },
  {
    name: 'Marsh tick',
    latinName: 'Ixodes apronophorus',
    foundOn: 'Small mammals such as voles',
    habitat: 'Wet places - marshes, riverbanks and damp grassland.',
  },
  {
    name: 'Passerine tick',
    latinName: 'Dermacentor frontalis',
    foundOn: 'Perching birds such as robins and blackbirds',
    habitat: 'Leaf litter, hedges and gardens where birds feed on the ground.',
  },
  {
    name: 'Southern rodent tick',
    latinName: 'Ixodes acuminatus',
    foundOn: 'Mice, voles and shrews',
    habitat: 'Inside rodent burrows, mostly in southern England.',
  },
  {
    name: 'Tree-hole tick',
    latinName: 'Ixodes arboricola',
    foundOn: 'Birds that nest in holes, such as blue tits',
    habitat: 'Tree holes and nest boxes.',
  },
]

const PEOPLE_TIPS = [
  'Stick to paths and avoid long grass and bracken where you can.',
  'Wear long trousers tucked into your socks - light colours make ticks easier to spot.',
  'Use an insect repellent on your skin and clothes.',
  'Check yourself after being outdoors, especially armpits, behind the knees, the waistband and the hairline.',
  'Remove a tick with fine-tipped tweezers or a tick tool: grip it close to the skin and pull up slowly without squeezing it.',
  'Wash the bite and see a GP if you get a spreading rash or flu-like symptoms afterwards.',
]


const PET_TIPS = [
  'Check your pet after walks, especially the head, ears, neck and between the toes.',
  'Ask your vet about tick prevention treatments.',
  "Remove ticks the same way as on people - don't burn them or cover them in creams.",
]

function LearnPage() {
  const [cityList, setCityList] = useState([])
  const [city, setCity] = useState('')
  const [months, setMonths] = useState([])
  const [error, setError] = useState(null)


  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/options`)
      .then((response) => {
        if (!response.ok) throw new Error()
        return response.json()
      })
      .then((data) => setCityList(Object.keys(data.cities)))
      .catch(() => setError("Can't reach the server"))
  }, [])

  // reload the chart whenever different city is picked
  useEffect(() => {
    setError(null)

    const filters = new URLSearchParams()
    if (city) filters.append('location', city)

    fetch(`${import.meta.env.VITE_API_URL}/api/stats/seasonal?${filters}`)
      .then((response) => {
        if (!response.ok) throw new Error()
        return response.json()
      })
      .then((data) => setMonths(data))
      .catch(() => setError("Couldn't load the seasonal chart"))
  }, [city])

  

  return (
    <div className="page">
      <h1 className="page-title">Learn about ticks</h1>

      <section className="learn-section">
        <h2 className="section-title">When are ticks about?</h2>
        <div className="seasonal-layout">
          <div className="seasonal-chart">
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={months}>
                <XAxis dataKey="month" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" name="Sightings" fill="#166534" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="seasonal-info">
            <p>
              In the UK, ticks are usually most active from March to June and again from August to October.
              The chart shows every sighting in our data counted by calendar month - this sample data is
              spread fairly evenly across the year, so it doesn't show the real seasonal peaks.
            </p>

            <label className="chart-filter">
              City
              <select value={city} onChange={(event) => setCity(event.target.value)}>
                <option value="">Whole UK</option>
                {cityList.map((name) => (
                  <option key={name} value={name}>{name}</option>
                ))}
              </select>
            </label>

            {error && <p className="server-error" role="alert">{error}</p>}
          </div>
        </div>
      </section>

      <section className="learn-section">
        <h2 className="section-title">Species guide</h2>
        <p>
          Ticks are tiny and look alike, so where you found one is often the best clue to its species.
          If you can't tell, choose "Not sure" when you report it - that's still useful.
        </p>

        <div className="species-list">
          {SPECIES_GUIDE.map((tick) => (
            <article key={tick.name} className="species-card">
              <h3 className="species-name">{tick.name}</h3>
              <p className="latin-name">{tick.latinName}</p>
              <p><strong>Found on:</strong> {tick.foundOn}</p>
              <p><strong>Where:</strong> {tick.habitat}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="learn-section">
        <h2 className="section-title">Prevention tips</h2>

        {/* "for you" and "for your pets" side by side */}
        <div className="tip-columns">
          <div>
            <h3 className="species-name">For you</h3>
            <ul className="tip-list">
              {PEOPLE_TIPS.map((tip) => (
                <li key={tip}>{tip}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="species-name">For your pets</h3>
            <ul className="tip-list">
              {PET_TIPS.map((tip) => (
                <li key={tip}>{tip}</li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </div>
  )
}

export default LearnPage
