import { useEffect, useState } from 'react'


function checkForm(date, location, species) {
  const errors = {}

  if (!date) {
    errors.date = 'Please choose the date you saw the tick'
  } else if (new Date(date) > new Date()) {
    errors.date = "The date can't be in the future"
  }

  if (!location) errors.location = 'Please choose a city'
  if (!species) errors.species = 'Please choose a species, or "Not sure"'

  return errors
}

// warnings appear before user submits - user can double check
function getWarnings(date, species) {
  const warnings = []

  const oneYearAgo = new Date()
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1)
  if (date && new Date(date) < oneYearAgo) {
    warnings.push('This sighting is over a year old - please double-check the date.')
  }

  if (species === 'Not sure') {
    warnings.push('Tip: the Learn page has a guide to help you identify ticks.')
  }

  return warnings
}

function ReportPage() {
  const [cityList, setCityList] = useState([])
  const [speciesList, setSpeciesList] = useState([])
  const [serverError, setServerError] = useState(null)

  const [date, setDate] = useState('')
  const [location, setLocation] = useState('')
  const [species, setSpecies] = useState('')

  const [errors, setErrors] = useState({})
  const [success, setSuccess] = useState(false)  // true once a report has been saved


  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/options`)
      .then((response) => {
        if (!response.ok) throw new Error()
        return response.json()
      })
      .then((data) => {
        setCityList(Object.keys(data.cities))
        setSpeciesList(data.species)
      })
      .catch(() => setServerError("Can't reach the server"))
  }, [])

  function handleSubmit(event) {
    event.preventDefault()  // stop the browser reloading page
    setSuccess(false)
    setServerError(null)

    const formErrors = checkForm(date, location, species)
    setErrors(formErrors)
    if (Object.keys(formErrors).length > 0) return

    fetch(`${import.meta.env.VITE_API_URL}/api/sightings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, location, species }),
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
      .then((result) => {
        if (!result.ok) {
          setErrors(result.data.errors || {})
          return
        }
        // clear form if data sent back all good
        setDate('')
        setLocation('')
        setSpecies('')
        setSuccess(true)
      })
      .catch(() => setServerError("Can't reach the server"))
  }

  const warnings = getWarnings(date, species)

  return (
    <div className="page">
      <h1 className="page-title">Report a sighting</h1>
      {serverError && <p className="server-error">{serverError}</p>}

      {success && <p className="form-success" role="status">Report sent - thank you!</p>}

      <form className="report-form" onSubmit={handleSubmit}>
        <label>
          Date of sighting
          <input type="date" value={date} onChange={(event) => setDate(event.target.value)} />
          {errors.date && <span className="field-error">{errors.date}</span>}
        </label>

        <label>
          City
          <select value={location} onChange={(event) => setLocation(event.target.value)}>
            <option value="">Choose a city</option>
            {cityList.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
          {errors.location && <span className="field-error">{errors.location}</span>}
        </label>

        <label>
          Species
          <select value={species} onChange={(event) => setSpecies(event.target.value)}>
            <option value="">Choose a species</option>
            {speciesList.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
          {errors.species && <span className="field-error">{errors.species}</span>}
        </label>

        {warnings.map((warning) => (
          <p key={warning} className="form-warning">{warning}</p>
        ))}

        <button type="submit" className="primary-button">Submit report</button>
      </form>
    </div>
  )
}

export default ReportPage
