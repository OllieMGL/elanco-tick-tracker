// the 5 species in the Elanco data - latin names match the data
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
  return (
    <div className="page">
      <h1 className="page-title">Learn about ticks</h1>

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

      <h2 className="section-title">Prevention tips</h2>

      <h3 className="species-name">For you</h3>
      <ul className="tip-list">
        {PEOPLE_TIPS.map((tip) => (
          <li key={tip}>{tip}</li>
        ))}
      </ul>

      <h3 className="species-name">For your pets</h3>
      <ul className="tip-list">
        {PET_TIPS.map((tip) => (
          <li key={tip}>{tip}</li>
        ))}
      </ul>
    </div>
  )
}

export default LearnPage
