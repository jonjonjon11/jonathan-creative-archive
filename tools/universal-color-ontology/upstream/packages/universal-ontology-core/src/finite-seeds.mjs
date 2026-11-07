// Finite bounded seed vocabularies for Universal Ontology Core v1.
// Open/infinite domains use generators/import adapters rather than fake finite enumerations.

export const ELEMENTS = [
  ['H','Hydrogen'],['He','Helium'],['Li','Lithium'],['Be','Beryllium'],['B','Boron'],['C','Carbon'],
  ['N','Nitrogen'],['O','Oxygen'],['F','Fluorine'],['Ne','Neon'],['Na','Sodium'],['Mg','Magnesium'],
  ['Al','Aluminum'],['Si','Silicon'],['P','Phosphorus'],['S','Sulfur'],['Cl','Chlorine'],['Ar','Argon'],
  ['K','Potassium'],['Ca','Calcium'],['Sc','Scandium'],['Ti','Titanium'],['V','Vanadium'],['Cr','Chromium'],
  ['Mn','Manganese'],['Fe','Iron'],['Co','Cobalt'],['Ni','Nickel'],['Cu','Copper'],['Zn','Zinc'],
  ['Ga','Gallium'],['Ge','Germanium'],['As','Arsenic'],['Se','Selenium'],['Br','Bromine'],['Kr','Krypton'],
  ['Rb','Rubidium'],['Sr','Strontium'],['Y','Yttrium'],['Zr','Zirconium'],['Nb','Niobium'],['Mo','Molybdenum'],
  ['Tc','Technetium'],['Ru','Ruthenium'],['Rh','Rhodium'],['Pd','Palladium'],['Ag','Silver'],['Cd','Cadmium'],
  ['In','Indium'],['Sn','Tin'],['Sb','Antimony'],['Te','Tellurium'],['I','Iodine'],['Xe','Xenon'],
  ['Cs','Cesium'],['Ba','Barium'],['La','Lanthanum'],['Ce','Cerium'],['Pr','Praseodymium'],['Nd','Neodymium'],
  ['Pm','Promethium'],['Sm','Samarium'],['Eu','Europium'],['Gd','Gadolinium'],['Tb','Terbium'],['Dy','Dysprosium'],
  ['Ho','Holmium'],['Er','Erbium'],['Tm','Thulium'],['Yb','Ytterbium'],['Lu','Lutetium'],['Hf','Hafnium'],
  ['Ta','Tantalum'],['W','Tungsten'],['Re','Rhenium'],['Os','Osmium'],['Ir','Iridium'],['Pt','Platinum'],
  ['Au','Gold'],['Hg','Mercury'],['Tl','Thallium'],['Pb','Lead'],['Bi','Bismuth'],['Po','Polonium'],
  ['At','Astatine'],['Rn','Radon'],['Fr','Francium'],['Ra','Radium'],['Ac','Actinium'],['Th','Thorium'],
  ['Pa','Protactinium'],['U','Uranium'],['Np','Neptunium'],['Pu','Plutonium'],['Am','Americium'],['Cm','Curium'],
  ['Bk','Berkelium'],['Cf','Californium'],['Es','Einsteinium'],['Fm','Fermium'],['Md','Mendelevium'],['No','Nobelium'],
  ['Lr','Lawrencium'],['Rf','Rutherfordium'],['Db','Dubnium'],['Sg','Seaborgium'],['Bh','Bohrium'],['Hs','Hassium'],
  ['Mt','Meitnerium'],['Ds','Darmstadtium'],['Rg','Roentgenium'],['Cn','Copernicium'],['Nh','Nihonium'],['Fl','Flerovium'],
  ['Mc','Moscovium'],['Lv','Livermorium'],['Ts','Tennessine'],['Og','Oganesson']
];

export const FUNDAMENTAL_PARTICLES = [
  ['up','quark'],['down','quark'],['charm','quark'],['strange','quark'],['top','quark'],['bottom','quark'],
  ['anti-up','antiquark'],['anti-down','antiquark'],['anti-charm','antiquark'],['anti-strange','antiquark'],['anti-top','antiquark'],['anti-bottom','antiquark'],
  ['electron','charged-lepton'],['positron','charged-antilepton'],['muon','charged-lepton'],['anti-muon','charged-antilepton'],['tau','charged-lepton'],['anti-tau','charged-antilepton'],
  ['electron-neutrino','neutrino'],['electron-antineutrino','antineutrino'],['muon-neutrino','neutrino'],['muon-antineutrino','antineutrino'],['tau-neutrino','neutrino'],['tau-antineutrino','antineutrino'],
  ['photon','gauge-boson'],['gluon','gauge-boson'],['W+','gauge-boson'],['W-','gauge-boson'],['Z0','gauge-boson'],['Higgs','scalar-boson']
];

export const SI_BASE = [
  ['length','metre','m'],['mass','kilogram','kg'],['time','second','s'],
  ['electric-current','ampere','A'],['thermodynamic-temperature','kelvin','K'],
  ['amount-of-substance','mole','mol'],['luminous-intensity','candela','cd']
];

export const SI_DERIVED = [
  ['frequency','hertz','Hz'],['force','newton','N'],['pressure','pascal','Pa'],['energy','joule','J'],
  ['power','watt','W'],['electric-charge','coulomb','C'],['electric-potential','volt','V'],
  ['capacitance','farad','F'],['resistance','ohm','Ω'],['conductance','siemens','S'],
  ['magnetic-flux','weber','Wb'],['magnetic-flux-density','tesla','T'],['inductance','henry','H'],
  ['luminous-flux','lumen','lm'],['illuminance','lux','lx'],['radioactivity','becquerel','Bq'],
  ['absorbed-dose','gray','Gy'],['dose-equivalent','sievert','Sv'],['catalytic-activity','katal','kat']
];

export const GEOMETRY_CONCEPTS = [
  'point','vertex','origin','line','ray','segment','curve','arc','spline','path','loop','spiral','helix',
  'circle','ellipse','triangle','quadrilateral','polygon','regular-polygon','irregular-polygon','star-polygon',
  'annulus','sector','plane','surface-patch','tessellation','sphere','ellipsoid','cube','cuboid','tetrahedron',
  'polyhedron','prism','pyramid','cylinder','cone','torus','tube','shell','mesh','lattice','voxel-volume',
  'implicit-surface','fractal-volume','n-simplex','hypercube','hypersphere','polytope','n-manifold',
  'product-space','configuration-space','phase-space'
];

export const MATHEMATICS_CONCEPTS = [
  'zero','natural-number','integer','rational-number','irrational-number','real-number','imaginary-number','complex-number',
  'algebraic-number','transcendental-number','cardinal','ordinal','interval','range','scalar','vector','pseudovector',
  'matrix','tensor','quaternion','multivector','sequence','series','set','multiset','tuple','distribution','field','function','operator',
  'identity','negation','addition','subtraction','multiplication','division','exponentiation','root','logarithm','modulo','factorial',
  'permutation','combination','composition','transformation','differentiation','integration','summation','product','limit','optimization',
  'convolution','correlation','fourier-transform','laplace-transform','projection','interpolation','approximation',
  'equal','unequal','greater-than','less-than','approximately-equal','equivalent','congruent','similar','parallel','perpendicular',
  'orthogonal','contains','subset','intersects','disjoint','connected','adjacent','ordered','correlated','independent',
  'group','ring','algebraic-field','vector-space','metric-space','topological-space','manifold','algebra','category','probability-space',
  'state-space','phase-space','true','false','unknown','proposition','predicate','and','or','not','xor','implication','equivalence',
  'quantification','proof','counterexample','constraint'
];

export const MUSIC_CONCEPTS = [
  'silence','impulse','oscillation','noise','tone','frequency','period','phase','amplitude','intensity','envelope','spectrum','timbre',
  'duration','direction','spatial-position','pitch','note','microtone','interval','octave','register','tuning','temperament','beat','pulse',
  'tempo','meter','rhythm','subdivision','syncopation','polyrhythm','tuplet','groove','dyad','chord','triad','seventh-chord','extended-chord',
  'inversion','progression','tonality','modality','consonance','dissonance','motif','phrase','theme','sequence','counterpoint','voice','melody',
  'measure','section','movement','song','composition','string','membrane','tube','resonator','percussion','voice-source','oscillator','sample',
  'additive-synthesis','subtractive-synthesis','frequency-modulation','amplitude-modulation','granular-synthesis','physical-modeling'
];

export const COLOR_CONCEPTS = [
  'red-channel','green-channel','blue-channel','alpha','linear-red','linear-green','linear-blue','luminance','relative-luminance',
  'absolute-luminance','chromaticity-x','chromaticity-y','CIE-X','CIE-Y','CIE-Z','CIELAB-L','CIELAB-a','CIELAB-b',
  'OKLab-L','OKLab-a','OKLab-b','OKLCh-L','OKLCh-C','OKLCh-h','hue','saturation','chroma','lightness','brightness','value',
  'sRGB','linear-sRGB','Display-P3','Rec-709','Rec-2020','CIE-XYZ','CIE-xyY','CIELAB','LCh','OKLab','OKLCh','HSV','HSL','CMYK',
  'spectral-power-distribution','dominant-wavelength','spectral-purity','white-point','black-point','color-temperature','gamut',
  'transfer-function','gamma','tone-mapping','HDR-peak','dynamic-range','DeltaE','metamerism','false-color','semantic-color','artistic-color'
];

export const VISUAL_CHANNELS = [
  'size','brightness','emission','sharpness','blur','roughness','metallicity','transmission','refraction','texture-frequency',
  'symmetry','curvature','complexity','position','velocity','acceleration','rotation','angular-rate','vibration-frequency',
  'vibration-amplitude','pulse-frequency','pulse-amplitude','flicker-frequency','flicker-amplitude','jitter','turbulence',
  'field-radius','field-strength','field-falloff','trail-length','persistence','connector-color','connector-width','connector-opacity',
  'connector-flow','confidence','probability','uncertainty'
];

export const RELATION_TYPES = [
  'IS_A','INSTANCE_OF','PART_OF','HAS_PART','HAS_PROPERTY','HAS_STATE','HAS_VALUE','HAS_UNIT','LOCATED_AT','OCCURS_AT',
  'BEFORE','AFTER','DURING','CAUSES','ENABLES','INHIBITS','TRANSFORMS_TO','INTERACTS_WITH','REACTS_WITH','BINDS_TO',
  'CONTAINS','CONNECTED_TO','ADJACENT_TO','SIMILAR_TO','DIFFERS_FROM','EQUIVALENT_TO','CORRELATED_WITH','INDEPENDENT_OF',
  'MEASURED_BY','EVIDENCED_BY','MODELED_BY','VALID_WITHIN','REPRESENTED_BY','MAPS_TO','SONIFIED_AS','COLORED_AS','SHAPED_AS',
  'ANIMATED_AS','PREREQUISITE_OF','EXPLAINS','EXAMPLE_OF','COUNTEREXAMPLE_OF','USED_BY','PRODUCES','CONSUMES','CONTROLS',
  'OBSERVES','DERIVED_FROM','COMPOSED_OF','MEMBER_OF','OPPOSES','COMPLEMENTS'
];

export const EPISTEMIC_STATUSES = [
  'OBSERVED','MEASURED','EVALUATED_DATA','DERIVED','SIMULATED','INFERRED','ESTIMATED','HYPOTHETICAL','SPECULATIVE',
  'FICTIONAL','CONVENTIONAL','SEMANTIC','PEDAGOGICAL','ARTISTIC_MAPPING'
];

function node(id, domain, subdomain, type, label, properties = {}, epistemicStatus = 'CONVENTIONAL') {
  return { id, domain, subdomain, type, label, properties, state: {}, epistemicStatus };
}

export function buildCoreFiniteNodes() {
  const out = [];

  ELEMENTS.forEach(([symbol, name], index) => {
    out.push(node(
      `urn:universe:chemistry:element:${symbol}`,
      'chemistry','periodic-table','element',name,
      { symbol, atomicNumber: index + 1 },
      'EVALUATED_DATA'
    ));
  });

  FUNDAMENTAL_PARTICLES.forEach(([name, category]) => {
    out.push(node(
      `urn:universe:physics:particle:${name}`,
      'physics','standard-model','particle',name,
      { category },
      'EVALUATED_DATA'
    ));
  });

  SI_BASE.forEach(([dimension, unit, symbol]) => {
    out.push(node(
      `urn:universe:measurement:dimension:${dimension}`,
      'measurement','si','physical-dimension',dimension,
      { baseUnit: unit, symbol }
    ));
    out.push(node(
      `urn:universe:measurement:unit:${unit}`,
      'measurement','si','unit',unit,
      { symbol, dimension }
    ));
  });

  SI_DERIVED.forEach(([quantity, unit, symbol]) => {
    out.push(node(
      `urn:universe:measurement:quantity:${quantity}`,
      'measurement','si-derived','quantity',quantity,
      { unit, symbol }
    ));
    out.push(node(
      `urn:universe:measurement:unit:${unit}`,
      'measurement','si-derived','unit',unit,
      { symbol, quantity }
    ));
  });

  for (const x of GEOMETRY_CONCEPTS) out.push(node(`urn:universe:geometry:type:${x}`,'geometry','primitive-or-structure','geometry-type',x));
  for (const x of MATHEMATICS_CONCEPTS) out.push(node(`urn:universe:mathematics:concept:${x}`,'mathematics','core','math-concept',x));
  for (const x of MUSIC_CONCEPTS) out.push(node(`urn:universe:music:concept:${x}`,'music','theory','music-concept',x));
  for (const x of COLOR_CONCEPTS) out.push(node(`urn:universe:color:concept:${x}`,'color','color-science','color-concept',x));
  for (const x of VISUAL_CHANNELS) out.push(node(`urn:universe:representation:visual-channel:${x}`,'representation','visual','visual-channel',x));
  for (const x of RELATION_TYPES) out.push(node(`urn:universe:graph:relation:${x}`,'graph','relation','relation-type',x));
  for (const x of EPISTEMIC_STATUSES) out.push(node(`urn:universe:evidence:status:${x}`,'evidence','epistemic','epistemic-status',x));

  return out;
}

export const CORE_COUNTS = Object.freeze({
  elements: ELEMENTS.length,
  standardModelParticleSpeciesEntries: FUNDAMENTAL_PARTICLES.length,
  siBaseDimensions: SI_BASE.length,
  siBaseUnits: SI_BASE.length,
  siDerivedQuantityEntries: SI_DERIVED.length,
  siDerivedUnitEntries: SI_DERIVED.length,
  geometryConcepts: GEOMETRY_CONCEPTS.length,
  mathConcepts: MATHEMATICS_CONCEPTS.length,
  musicConcepts: MUSIC_CONCEPTS.length,
  colorConcepts: COLOR_CONCEPTS.length,
  visualChannels: VISUAL_CHANNELS.length,
  relationTypes: RELATION_TYPES.length,
  epistemicStatuses: EPISTEMIC_STATUSES.length
});
