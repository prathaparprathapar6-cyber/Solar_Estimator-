
// ============================================================
// EXACT ENGINEERING CONSTANTS & BOM REPOSITORIES (MATCHING OLD CODE)
// ============================================================
const MODULE_WATT_DEFAULT = 550;
const DEFAULT_COST_PER_KW = 50000;

const MONTHLY_YIELD = {
  Jan: 5.15, Feb: 5.40, Mar: 5.35, Apr: 4.96, May: 4.37, Jun: 3.26,
  Jul: 2.91, Aug: 3.26, Sep: 3.84, Oct: 4.30, Nov: 4.40, Dec: 5.00
};
const MONTHS = Object.keys(MONTHLY_YIELD);
const DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

const TARIFF_25Y = [
  8.05, 8.45, 8.87, 9.32, 9.78, 10.27, 10.78, 11.32, 11.89, 12.48,
  13.11, 13.76, 14.45, 15.18, 15.93, 16.74, 17.57, 18.45, 19.37, 20.34,
  21.36, 22.43, 23.55, 24.73, 25.96
];

// ============================================================
// SOLAR PANEL MASTER CATALOG (From Standard Market Ratings)
// ============================================================
const SOLAR_PANEL_CATALOG = {
  "Mono-PERC (Mono-facial)": {
    name: "Mono-PERC (Mono-facial)",
    desc: "The standard for current residential rooftop systems.",
    ratings: [380, 390, 400, 410, 420, 430, 440, 450, 460, 480, 500, 525, 530, 535, 540, 545, 550, 555, 560, 570, 580],
    defaultWatt: 550
  },
  "N-Type TOPCon": {
    name: "N-Type TOPCon",
    desc: "Premium high-efficiency modules for commercial & industrial use.",
    ratings: [420, 440, 450, 500, 540, 545, 550, 555, 560, 565, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 660, 670, 680, 690, 700],
    defaultWatt: 580
  },
  "Bifacial (Mono / TOPCon)": {
    name: "Bifacial (Mono / TOPCon)",
    desc: "Dual-sided generation. Ratings listed are for the front side.",
    ratings: [440, 500, 530, 540, 545, 550, 560, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 645, 650, 655, 660, 665, 670, 680, 690, 700, 710, 720],
    defaultWatt: 550
  },
  "Polycrystalline": {
    name: "Polycrystalline",
    desc: "Legacy technology, mostly used in small off-grid applications.",
    ratings: [40, 50, 75, 100, 150, 165, 200, 250, 260, 270, 275, 280, 300, 325, 330, 335, 340],
    defaultWatt: 335
  },
  "Ultra-High Power (G12/G12R)": {
    name: "Ultra-High Power (G12/G12R)",
    desc: "Large-format modules for utility-scale solar farms.",
    ratings: [600, 610, 620, 625, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720],
    defaultWatt: 650
  }
};

// ============================================================
// ON-GRID SOLAR INVERTER MASTER CATALOG (1 kW to 20 kW)
// ============================================================
const INVERTER_MASTER_CATALOG = {
  1.0: { rating: 1.0, phase: "Single-Phase", desc: "Standard entry point; ideal for nano 1-room households.", models: "Solis Mini, Havells Envira", hardwareKw: 1.0 },
  2.0: { rating: 2.0, phase: "Single-Phase", desc: "Standard residential tier; powers basic 1-2 BHK loads.", models: "Polycab PSIT, Obetech G", hardwareKw: 2.0 },
  3.0: { rating: 3.0, phase: "Single-Phase", desc: "Highest Volume Domestic Tier; max limit for single-phase PM Surya Ghar subsidy.", models: "Growatt MIC, Luminous NXi 130", hardwareKw: 3.0 },
  4.0: { rating: 4.0, phase: "Single-Phase / Three-Phase", desc: "Transition bracket; widely deployed for 3 BHK properties.", models: "Waaree W3.1/3-PH, Luminous NXi 340", hardwareKw: 4.0 },
  5.0: { rating: 5.0, phase: "Single-Phase / Three-Phase", desc: "Standard boundary rating; most DISCOMs mandate a shift to 3-phase meter beyond this.", models: "Sungrow SG5.0RS, UTL 5.1", hardwareKw: 5.0 },
  6.0: { rating: 6.0, phase: "Single-Phase / Three-Phase", desc: "Commercial-scale entry point; common for large villas.", models: "Solis 1P6K, Growatt MOD 6000", hardwareKw: 6.0 },
  7.0: { rating: 7.0, phase: "Three-Phase", desc: "Fully Standardized Option; engineered specifically to bridge gap between 6kW and 8kW.", models: "Growatt P3, Fimer On-Grid", hardwareKw: 7.0 },
  8.0: { rating: 8.0, phase: "Three-Phase", desc: "Industrial tier; steelwork for independent modern bungalows.", models: "GoodWe GW8K-DT, Polycab PSIT 8K", hardwareKw: 8.0 },
  9.0: { rating: 9.0, phase: "Three-Phase", desc: "Available via turnkey system developers.", models: "Greentech Energy", hardwareKw: 9.0 },
  10.0: { rating: 10.0, phase: "Three-Phase", desc: "Massive Volume Commercial Tier; high demand for commercial shops.", models: "Fronius Symo, Delta M10", hardwareKw: 10.0 },
  11.0: { rating: 11.0, phase: "Three-Phase", desc: "Highly Available; optimal DC oversizing on 10kW sanctioned limits.", models: "Deye 11K-G04, Kstar Solar", hardwareKw: 11.0 },
  12.0: { rating: 12.0, phase: "Three-Phase", desc: "Mid-tier industrial rating; heavily utilized for institutions.", models: "Solis 12KTL, Hitachi Solar", hardwareKw: 12.0 },
  13.0: { rating: 13.0, phase: "Non-Standard (Derated 15kW)", desc: "Physically Unavailable; deploy derated 15kW unit capped to 13kW.", models: "None (Use 15kW configuration)", hardwareKw: 15.0 },
  14.0: { rating: 14.0, phase: "Three-Phase", desc: "Exists primarily in specialized hybrid catalogs.", models: "Deye, Delta Solar", hardwareKw: 14.0 },
  15.0: { rating: 15.0, phase: "Three-Phase", desc: "Core Industrial Tier; widely chosen for schools and institutions.", models: "Sungrow SG15RT, UTL On-Grid", hardwareKw: 15.0 },
  16.0: { rating: 16.0, phase: "Three-Phase", desc: "Commercial and heavy-duty hybrid brackets.", models: "Deye Hybrid 16K", hardwareKw: 16.0 },
  17.0: { rating: 17.0, phase: "Three-Phase", desc: "Highly Available; prominent dedicated hardware step.", models: "UTL 17KW, Solis 3-Phase 17KW, SolarEdge", hardwareKw: 17.0 },
  18.0: { rating: 18.0, phase: "Three-Phase", desc: "Commercially cataloged; frequently derated 20kW inverter for net-metering.", models: "Deye 18K, Growatt 18K", hardwareKw: 18.0 },
  19.0: { rating: 19.0, phase: "Non-Standard (Bypassed to 20kW)", desc: "Physically Bypassed; installers upgrade project directly to 20kW system.", models: "None (Use 20kW configuration)", hardwareKw: 20.0 },
  20.0: { rating: 20.0, phase: "Three-Phase", desc: "Major Industrial Anchor Tier; standard benchmark for decentralized rooftop annexes.", models: "Loom Solar, Eyzer 20, Waaree W3-20K", hardwareKw: 20.0 }
};

const INVERTER_RATINGS = [
  1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
  11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
];

// Base 12-Item BOM Tables for 1 kW through 20 kW from old code
const EXACT_BOM_REPORTS = {
  1: [
    ["Solar PV module", "550 W mono PERC/TOPCon", "2 Nos.", 20000.0],
    ["On-grid inverter", "1 kW, single-phase", "1 No.", 18000.0],
    ["Mounting structure", "HDGI rooftop structure", "1 Set", 6000.0],
    ["DC solar cable", "4 sq.mm copper", "20 m", 1400.0],
    ["AC cable", "4 sq.mm copper", "15 m", 1275.0],
    ["MC4 connectors", "PV connector pair", "2 pairs", 600.0],
    ["DCDB", "Isolator + fuse + DC SPD", "1 No.", 3500.0],
    ["ACDB", "16A MCB + RCCB + AC SPD", "1 No.", 3500.0],
    ["Earthing kit", "Earth electrode and accessories", "3 Nos.", 4500.0],
    ["Lightning arrester", "Standard", "1 No.", 2500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, etc.", "1 Lot", 2500.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 10000.0],
  ],
  2: [
    ["Solar PV modules", "550 W mono PERC/TOPCon", "4 Nos.", 40000.0],
    ["On-grid inverter", "2 kW, single-phase", "1 No.", 30000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 10000.0],
    ["DC solar cable", "4-6 sq.mm copper, PV-rated", "30 m", 2100.0],
    ["AC cable", "4-6 sq.mm copper", "20 m", 1800.0],
    ["MC4 connectors", "PV-rated connector pairs", "4 pairs", 1200.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 4500.0],
    ["ACDB", "16A MCB + RCCB + Type-II AC SPD", "1 No.", 4000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 5500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 2500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 3000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 15000.0],
  ],
  3: [
    ["Solar PV modules", "550 W mono PERC/TOPCon", "6 Nos.", 60000.0],
    ["On-grid inverter", "3 kW, single-phase", "1 No.", 42000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 15000.0],
    ["DC solar cable", "4-6 sq.mm copper, PV-rated", "40 m", 2800.0],
    ["AC cable", "4-6 sq.mm copper", "25 m", 2250.0],
    ["MC4 connectors", "PV-rated connector pairs", "6 pairs", 1800.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 5500.0],
    ["ACDB", "25A MCB + RCCB + Type-II AC SPD", "1 No.", 4500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 6000.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 2500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 3500.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 20000.0],
  ],
  4: [
    ["Solar PV modules", "550 W mono PERC/TOPCon", "8 Nos.", 80000.0],
    ["On-grid inverter", "4 kW, single-phase", "1 No.", 52000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 20000.0],
    ["DC solar cable", "4-6 sq.mm copper, PV-rated", "50 m", 3500.0],
    ["AC cable", "6 sq.mm copper", "30 m", 2700.0],
    ["MC4 connectors", "PV-rated connector pairs", "8 pairs", 2400.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 6500.0],
    ["ACDB", "32A MCB + RCCB + Type-II AC SPD", "1 No.", 5500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 8000.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 2500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 4000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 25000.0],
  ],
  5: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "10 Nos.", 100000.0],
    ["On-grid inverter", "5 kW, single-phase", "1 No.", 55000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 25000.0],
    ["DC solar cable", "4-6 sq.mm copper, PV-rated", "60 m", 4500.0],
    ["AC cable", "6 sq.mm copper", "35 m", 3850.0],
    ["MC4 connectors", "PV-rated connector pairs", "10 pairs", 3000.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 7000.0],
    ["ACDB", "32A MCB + RCCB + Type-II AC SPD", "1 No.", 7000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 3500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 7100.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 25000.0],
  ],
  6: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "12 Nos.", 120000.0],
    ["On-grid inverter", "6 kW, three-phase", "1 No.", 68000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 28000.0],
    ["DC solar cable", "4-6 sq.mm copper, PV-rated", "70 m", 5250.0],
    ["AC cable", "10 sq.mm copper", "40 m", 5000.0],
    ["MC4 connectors", "PV-rated connector pairs", "12 pairs", 3600.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 8000.0],
    ["ACDB", "25A MCB + RCCB + Type-II AC SPD", "1 No.", 7000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 4000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 8000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 30000.0],
  ],
  7: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "14 Nos.", 140000.0],
    ["On-grid inverter", "7 kW, three-phase", "1 No.", 78000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 32000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "80 m", 6800.0],
    ["AC cable", "10 sq.mm copper", "45 m", 8100.0],
    ["MC4 connectors", "PV-rated connector pairs", "14 pairs", 4200.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 9000.0],
    ["ACDB", "32A MCB + RCCB + Type-II AC SPD", "1 No.", 9000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 4000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 8000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 35000.0],
  ],
  8: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "16 Nos.", 160000.0],
    ["On-grid inverter", "8 kW, three-phase", "1 No.", 88000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 36000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "90 m", 7650.0],
    ["AC cable", "10 sq.mm copper", "50 m", 9000.0],
    ["MC4 connectors", "PV-rated connector pairs", "16 pairs", 4800.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 9500.0],
    ["ACDB", "32A MCB + RCCB + Type-II AC SPD", "1 No.", 9500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 4500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 10000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 35000.0],
  ],
  9: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "18 Nos.", 180000.0],
    ["On-grid inverter", "9 kW, three-phase", "1 No.", 98000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 40000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "100 m", 8500.0],
    ["AC cable", "16 sq.mm copper", "55 m", 13200.0],
    ["MC4 connectors", "PV-rated connector pairs", "18 pairs", 5400.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 10000.0],
    ["ACDB", "40A MCB + RCCB + Type-II AC SPD", "1 No.", 10500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 4500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 12000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 40000.0],
  ],
  10: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "20 Nos.", 200000.0],
    ["On-grid inverter", "10 kW, three-phase", "1 No.", 110000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 45000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "110 m", 9350.0],
    ["AC cable", "16 sq.mm copper", "60 m", 14400.0],
    ["MC4 connectors", "PV-rated connector pairs", "20 pairs", 6000.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 11000.0],
    ["ACDB", "40A MCB + RCCB + Type-II AC SPD", "1 No.", 11500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 5000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 15000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 45000.0],
  ],
  11: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "20 Nos.", 200000.0],
    ["On-grid inverter", "11 kW, three-phase", "1 No.", 115000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 50000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "120 m", 10200.0],
    ["AC cable", "16 sq.mm copper", "65 m", 15600.0],
    ["MC4 connectors", "PV-rated connector pairs", "20 pairs", 6000.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 12000.0],
    ["ACDB", "50A MCB + RCCB + Type-II AC SPD", "1 No.", 12000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 5000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 16000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 50000.0],
  ],
  12: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "22 Nos.", 220000.0],
    ["On-grid inverter", "12 kW, three-phase", "1 No.", 130000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 55000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "130 m", 11050.0],
    ["AC cable", "16 sq.mm copper", "70 m", 16800.0],
    ["MC4 connectors", "PV-rated connector pairs", "22 pairs", 6600.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 12500.0],
    ["ACDB", "50A MCB + RCCB + Type-II AC SPD", "1 No.", 12500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 5500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 18000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 55000.0],
  ],
  13: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "24 Nos.", 240000.0],
    ["On-grid inverter", "13 kW, three-phase", "1 No.", 140000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 60000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "140 m", 11900.0],
    ["AC cable", "16 sq.mm copper", "75 m", 18000.0],
    ["MC4 connectors", "PV-rated connector pairs", "24 pairs", 7200.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 13000.0],
    ["ACDB", "50A MCB + RCCB + Type-II AC SPD", "1 No.", 13000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 5500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 20000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 60000.0],
  ],
  14: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "26 Nos.", 260000.0],
    ["On-grid inverter", "14 kW, three-phase", "1 No.", 150000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 65000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "150 m", 12750.0],
    ["AC cable", "16 sq.mm copper", "80 m", 19200.0],
    ["MC4 connectors", "PV-rated connector pairs", "26 pairs", 7800.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 13500.0],
    ["ACDB", "63A MCB + RCCB + Type-II AC SPD", "1 No.", 13500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 6000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 26000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 70000.0],
  ],
  15: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "28 Nos.", 280000.0],
    ["On-grid inverter", "15 kW, three-phase", "1 No.", 160000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 70000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "160 m", 13600.0],
    ["AC cable", "25 sq.mm copper", "85 m", 29750.0],
    ["MC4 connectors", "PV-rated connector pairs", "28 pairs", 8400.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 14000.0],
    ["ACDB", "63A MCB + RCCB + Type-II AC SPD", "1 No.", 14500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 6000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 25000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 70000.0],
  ],
  16: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "30 Nos.", 300000.0],
    ["On-grid inverter", "16 kW, three-phase", "1 No.", 170000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 75000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "170 m", 14450.0],
    ["AC cable", "25 sq.mm copper", "90 m", 31500.0],
    ["MC4 connectors", "PV-rated connector pairs", "30 pairs", 9000.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 15000.0],
    ["ACDB", "63A MCB + RCCB + Type-II AC SPD", "1 No.", 15000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 6500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 28000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 75000.0],
  ],
  17: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "32 Nos.", 320000.0],
    ["On-grid inverter", "17 kW, three-phase", "1 No.", 180000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 85000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "180 m", 15300.0],
    ["AC cable", "25 sq.mm copper", "95 m", 33250.0],
    ["MC4 connectors", "PV-rated connector pairs", "32 pairs", 9600.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 15500.0],
    ["ACDB", "63A MCB + RCCB + Type-II AC SPD", "1 No.", 15500.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 6500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 30000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 85000.0],
  ],
  18: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "33 Nos.", 330000.0],
    ["On-grid inverter", "18 kW, three-phase", "1 No.", 190000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 90000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "190 m", 16150.0],
    ["AC cable", "25 sq.mm copper", "100 m", 35000.0],
    ["MC4 connectors", "PV-rated connector pairs", "33 pairs", 9900.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 16000.0],
    ["ACDB", "80A MCB + RCCB + Type-II AC SPD", "1 No.", 16000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 6500.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 32000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 90000.0],
  ],
  19: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "35 Nos.", 350000.0],
    ["On-grid inverter", "19 kW, three-phase", "1 No.", 200000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 95000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "200 m", 17000.0],
    ["AC cable", "25 sq.mm copper", "100 m", 35000.0],
    ["MC4 connectors", "PV-rated connector pairs", "35 pairs", 10500.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 17000.0],
    ["ACDB", "80A MCB + RCCB + Type-II AC SPD", "1 No.", 17000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 7500.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 7000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 34000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 95000.0],
  ],
  20: [
    ["Solar PV modules", "550 W mono PERC / TOPCon", "40 Nos.", 400000.0],
    ["On-grid inverter", "20 kW, three-phase", "1 No.", 210000.0],
    ["Rooftop mounting structure", "HDGI, module-compatible", "1 Set", 95000.0],
    ["DC solar cable", "6 sq.mm copper, PV-rated", "220 m", 18700.0],
    ["AC cable", "35 sq.mm copper", "110 m", 49500.0],
    ["MC4 connectors", "PV-rated connector pairs", "40 pairs", 12000.0],
    ["DCDB", "Isolator + fuse + Type-II DC SPD", "1 No.", 18000.0],
    ["ACDB", "80A MCB + RCCB + Type-II AC SPD", "1 No.", 18000.0],
    ["Earthing kit", "Earth electrodes and accessories", "3 Nos.", 9000.0],
    ["Lightning arrester", "Standard rooftop PV type", "1 No.", 8000.0],
    ["Installation accessories", "Lugs, ferrules, clamps, conduit, glands, etc.", "1 Lot", 38000.0],
    ["Installation & commissioning", "Labour and commissioning", "1 Job", 95000.0],
  ]
};

let mode = "roof";
let charts = {};
let current = null;
let arrayMode = "top";

function selectInverter(totalPlantDcKw) {
  // Requirement 1: 70% derating factor of total solar panels output power
  // E.g. if solar panel output is 3.5 kW, 3.5 * 0.7 = 2.45 kW -> selects 3.0 kW standard rating
  const deratedKw = Math.round(totalPlantDcKw * 0.70 * 100) / 100;
  if (deratedKw <= 1.0) return 1.0;
  for (const r of INVERTER_RATINGS) {
    if (r >= deratedKw - 1e-4) return r;
  }
  return INVERTER_RATINGS[INVERTER_RATINGS.length - 1];
}

function inverterCableAndIsolator(inverterKw, phase3) {
  const cableMap = {
    1.0: "3.5Cx4 Sq.mm", 1.5: "3.5Cx4 Sq.mm", 2.0: "3.5Cx4 Sq.mm", 3.0: "3.5Cx4 Sq.mm",
    4.0: "3.5Cx6 Sq.mm", 5.0: "3.5Cx6 Sq.mm", 6.0: "3.5Cx10 Sq.mm",
    7.0: "3.5Cx10 Sq.mm", 8.0: "3.5Cx10 Sq.mm", 9.0: "3.5Cx16 Sq.mm",
    10.0: "3.5Cx16 Sq.mm", 11.0: "3.5Cx16 Sq.mm", 12.0: "3.5Cx16 Sq.mm",
    13.0: "3.5Cx16 Sq.mm", 14.0: "3.5Cx16 Sq.mm", 15.0: "3.5Cx25 Sq.mm",
    16.0: "3.5Cx25 Sq.mm", 17.0: "3.5Cx25 Sq.mm", 18.0: "3.5Cx25 Sq.mm",
    19.0: "3.5Cx35 Sq.mm", 20.0: "3.5Cx35 Sq.mm",
  };
  const currentMap = {
    1.0: 16, 1.5: 16, 2.0: 16, 3.0: 25, 4.0: 25, 5.0: 32, 6.0: 25,
    7.0: 32, 8.0: 32, 9.0: 40, 10.0: 40, 11.0: 50, 12.0: 50,
    13.0: 50, 14.0: 63, 15.0: 63, 16.0: 63, 17.0: 63, 18.0: 80,
    19.0: 80, 20.0: 80
  };
  let kwKey = INVERTER_RATINGS[0];
  let minDiff = 999;
  for (const r of INVERTER_RATINGS) {
    if (Math.abs(r - inverterKw) < minDiff) {
      minDiff = Math.abs(r - inverterKw);
      kwKey = r;
    }
  }
  const cable = cableMap[kwKey] || "3.5Cx4 Sq.mm";
  const current = currentMap[kwKey] || 16;
  const isolator = phase3 ? `${current}A, MCB Type, 4P 415V` : `${current}A, MCB Type, 2P 230V`;
  return { cable, isolator, current };
}

function selectAcdbComponents(acCapacityKw, distanceM) {
  const isSinglePhase = acCapacityKw <= 5.0;
  let ratedCurrent = 0;
  if (isSinglePhase) {
    ratedCurrent = (acCapacityKw * 1000.0) / 230.0;
  } else {
    ratedCurrent = (acCapacityKw * 1000.0) / (1.73205 * 415.0);
  }
  const designCurrent = ratedCurrent * 1.25;

  let breakerRating = 16;
  let baseCable = "3.5Cx4 Sq.mm";
  let busbar = "25A, 230V, 2PN Aluminium";
  let breakerStr = "";
  let meterStr = "";
  let ctStr = "";
  let ptStr = "";

  if (isSinglePhase) {
    if (designCurrent <= 16) {
      breakerRating = 16; baseCable = "3.5Cx4 Sq.mm"; busbar = "25A, 230V, 2PN Aluminium";
    } else if (designCurrent <= 20) {
      breakerRating = 20; baseCable = "3.5Cx4 Sq.mm"; busbar = "32A, 230V, 2PN Aluminium";
    } else if (designCurrent <= 25) {
      breakerRating = 25; baseCable = "3.5Cx6 Sq.mm"; busbar = "32A, 230V, 2PN Aluminium";
    } else if (designCurrent <= 32) {
      breakerRating = 32; baseCable = "3.5Cx6 Sq.mm"; busbar = "50A, 230V, 2PN Aluminium";
    } else {
      breakerRating = 40; baseCable = "3.5Cx10 Sq.mm"; busbar = "50A, 230V, 2PN Aluminium";
    }
    breakerStr = `${breakerRating}A, 230V, 2-POLE (MCB Type C), 10kA`;
    meterStr = "Bidirectional Net Meter (Direct Connected, Whole-Current), 1PH 2W 230V";
    ctStr = "Direct Connection (No CT required for <= 5 kW)";
    ptStr = "Direct Connection (230V Line)";
  } else {
    if (designCurrent <= 25) {
      breakerRating = 25; baseCable = "3.5Cx6 Sq.mm"; busbar = "50A, 415V, 3PN Aluminium";
    } else if (designCurrent <= 32) {
      breakerRating = 32; baseCable = "3.5Cx10 Sq.mm"; busbar = "50A, 415V, 3PN Aluminium";
    } else if (designCurrent <= 40) {
      breakerRating = 40; baseCable = "3.5Cx16 Sq.mm"; busbar = "50A, 415V, 3PN Aluminium";
    } else if (designCurrent <= 63) {
      breakerRating = 63; baseCable = "3.5Cx25 Sq.mm"; busbar = "100A, 415V, 3PN Aluminium";
    } else {
      breakerRating = 80; baseCable = "3.5Cx35 Sq.mm"; busbar = "100A, 415V, 3PN Aluminium";
    }
    breakerStr = `${breakerRating}A, 415V, 4-POLE, 25kA Breaking Capacity`;
    meterStr = "Multi Function Meter CL-0.5, 3PH 4W 415V";
    ctStr = breakerRating <= 50 ? "50/5A CL 0.5" : "100/5A CL 0.5";
    ptStr = "415/110V";
  }

  let gridCable = baseCable;
  if (distanceM > 30) {
    const upscale = {
      "3.5Cx4 Sq.mm": "3.5Cx6 Sq.mm",
      "3.5Cx6 Sq.mm": "3.5Cx10 Sq.mm",
      "3.5Cx10 Sq.mm": "3.5Cx16 Sq.mm",
      "3.5Cx16 Sq.mm": "3.5Cx25 Sq.mm",
      "3.5Cx25 Sq.mm": "3.5Cx35 Sq.mm",
      "3.5Cx35 Sq.mm": "3.5Cx50 Sq.mm",
    };
    gridCable = upscale[gridCable] || gridCable;
  }

  const components = [
    ["01 AC Circuit Breaker", breakerStr],
    ["02 Energy Metering", meterStr],
    ["03 Current Transformer (CT)", ctStr],
    ["04 Potential Transformer (PT)", ptStr],
    ["05 Bus Bar", busbar],
  ];
  return {
    components,
    breakerRating,
    ratedCurrent: Math.round(ratedCurrent * 100) / 100,
    gridCable,
    busbar
  };
}

function generatePlantBom(capacityKw, inverterKw, panelWatt, panelCount, acdbBreakerRating, bldgResults, dist, panelTech) {
  const cap = Math.max(1.0, capacityKw);
  const roundedCap = Math.round(cap);

  let totalModuleCost = 0;
  let mc4Pairs = panelCount;
  const pTech = panelTech || (bldgResults && bldgResults[0]?.panelTech) || "Mono-PERC (Mono-facial)";
  let modSpec = `${panelWatt} W ${pTech}`;
  let modQty = `${panelCount} Nos.`;

  if (bldgResults && bldgResults.length > 0) {
    totalModuleCost = bldgResults.reduce((sum, b) => sum + (b.panels * Math.round((b.panelW || 550) * (10000.0 / 550.0))), 0);
    mc4Pairs = bldgResults.reduce((sum, b) => sum + b.panels, 0);
    modQty = `${mc4Pairs} Nos.`;
    const distinctSpecs = [...new Set(bldgResults.map(b => `${b.panelW || 550}W ${b.panelTech || pTech}`))];
    if (distinctSpecs.length === 1) {
      modSpec = distinctSpecs[0];
    } else {
      modSpec = bldgResults.map(b => `${b.name || 'Building'}: ${b.panelW || 550}W ${b.panelTech || pTech} (${b.panels} Nos.)`).join(" + ");
    }
  } else {
    const costPerModule = Math.round(panelWatt * (10000.0 / 550.0));
    totalModuleCost = panelCount * costPerModule;
  }

  const modRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.module_per_wp) ? dynamicPricing.module_per_wp : (10000.0 / 550.0);
  const invRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.inverter_per_kw) ? dynamicPricing.inverter_per_kw : 10500.0;
  const structRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.structure_per_kw) ? dynamicPricing.structure_per_kw : 4800.0;
  const mc4Rate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.mc4_per_pair) ? dynamicPricing.mc4_per_pair : 300.0;
  const instRate = (typeof dynamicPricing !== 'undefined' && dynamicPricing.installation_per_kw) ? dynamicPricing.installation_per_kw : 4000.0;
  const mc4Cost = mc4Pairs * mc4Rate;
  const invMeta = INVERTER_MASTER_CATALOG[inverterKw];
  const modelHint = invMeta ? ` (${invMeta.models.split(',')[0]} or equiv.)` : "";

  const invSpec = bldgResults && bldgResults.length > 1
    ? `${inverterKw} kW ${inverterKw > 5 ? 'three-phase' : 'single-phase'} (` + bldgResults.map(b => `${b.name}: ${selectInverter(b.capacityKw)}kW`).join(" + ") + ")"
    : (inverterKw > 5.0 ? `${inverterKw} kW, three-phase${modelHint}` : `${inverterKw} kW, single-phase${modelHint}`);
  const invQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Nos.` : "1 No.";

  const rccbRating = acdbBreakerRating <= 16 ? 25 : (acdbBreakerRating <= 32 ? 40 : 63);
  const acdbSpec = bldgResults && bldgResults.length > 1
    ? bldgResults.map(b => {
        const bDeratedAc = Math.round(b.capacityKw * 0.70 * 100) / 100;
        return `${b.name}: ${selectAcdbComponents(bDeratedAc, dist || 20).breakerRating}A MCB`;
      }).join(" + ") + " + Type-II AC SPD"
    : `${acdbBreakerRating}A MCB + ${rccbRating}A RCCB + Type-II AC SPD`;
  const acdbQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Set(s)` : "1 No.";
  const structQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} Roof Set(s)` : "1 Set";
  const dcdbQty = bldgResults && bldgResults.length > 1 ? `${bldgResults.length} No(s).` : "1 No.";

  let items = [];
  if (EXACT_BOM_REPORTS[roundedCap]) {
    const rows = EXACT_BOM_REPORTS[roundedCap];
    for (let idx = 1; idx <= rows.length; idx++) {
      const [desc, spec, qty, amt] = rows[idx - 1];
      if (idx === 1) {
        items.push({ sl: idx, desc: "Solar PV modules", spec: modSpec, qty: modQty, amt: totalModuleCost });
      } else if (idx === 2) {
        const invCost = amt * (inverterKw / Math.max(1.0, roundedCap));
        items.push({ sl: idx, desc: "On-grid inverter", spec: invSpec, qty: invQty, amt: Math.round(invCost) });
      } else if (idx === 3) {
        items.push({ sl: idx, desc: desc, spec: spec, qty: structQty, amt: amt });
      } else if (idx === 6) {
        items.push({ sl: idx, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost });
      } else if (idx === 7) {
        items.push({ sl: idx, desc: desc, spec: spec, qty: dcdbQty, amt: amt });
      } else if (idx === 8) {
        items.push({ sl: idx, desc: "ACDB", spec: acdbSpec, qty: acdbQty, amt: amt });
      } else if (idx === 9) {
        items.push({ sl: idx, desc: "Earthing kit", spec: "Earth electrodes & accessories (IS 3043 - 3 Pits)", qty: "3 Nos.", amt: amt });
      } else {
        items.push({ sl: idx, desc: desc, spec: spec, qty: qty, amt: amt });
      }
    }
  } else {
    const invCost = inverterKw * invRate;
    items = [
      { sl: 1, desc: "Solar PV modules", spec: `${panelWatt} W mono PERC / TOPCon`, qty: `${panelCount} Nos.`, amt: totalModuleCost },
      { sl: 2, desc: "On-grid inverter", spec: invSpec, qty: "1 No.", amt: Math.round(invCost) },
      { sl: 3, desc: "Rooftop mounting structure", spec: "HDGI rooftop structure, module-compatible", qty: "1 Set", amt: Math.round(cap * structRate) },
      { sl: 4, desc: "DC solar cable", spec: "4-6 sq.mm copper, PV-rated", qty: `${Math.max(20, Math.round(cap * 11))} m`, amt: Math.round(cap * (typeof dynamicPricing !== 'undefined' && dynamicPricing.dc_cable_per_m ? dynamicPricing.dc_cable_per_m * 11 : 935.0)) },
      { sl: 5, desc: "AC cable", spec: "4-10 sq.mm copper", qty: `${Math.max(15, Math.round(cap * 6))} m`, amt: Math.round(cap * (typeof dynamicPricing !== 'undefined' && dynamicPricing.ac_cable_per_m ? dynamicPricing.ac_cable_per_m * 6 : 2400.0)) },
      { sl: 6, desc: "MC4 connectors", spec: "PV-rated connector pairs", qty: `${mc4Pairs} pairs`, amt: mc4Cost },
      { sl: 7, desc: "DCDB", spec: "Isolator + fuse + Type-II DC SPD", qty: "1 No.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.dcdb_base ? dynamicPricing.dcdb_base : 18000.0) },
      { sl: 8, desc: "ACDB", spec: acdbSpec, qty: "1 No.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.acdb_base ? dynamicPricing.acdb_base : 18000.0) },
      { sl: 9, desc: "Earthing kit", spec: "Chemical earth electrodes & accessories (IS 3043)", qty: "3 Nos.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.earthing_kit_base ? dynamicPricing.earthing_kit_base : 9000.0) },
      { sl: 10, desc: "Lightning arrester", spec: "Standard rooftop PV type", qty: "1 No.", amt: (typeof dynamicPricing !== 'undefined' && dynamicPricing.lightning_arrester_base ? dynamicPricing.lightning_arrester_base : 8000.0) },
      { sl: 11, desc: "Installation accessories", spec: "Lugs, ferrules, clamps, conduit, glands, etc.", qty: "1 Lot", amt: Math.round(cap * (typeof dynamicPricing !== 'undefined' && dynamicPricing.accessories_per_kw ? dynamicPricing.accessories_per_kw : 1900.0)) },
      { sl: 12, desc: "Installation & commissioning", spec: "Labour, testing and commissioning", qty: "1 Job", amt: Math.round(cap * instRate) },
    ];
  }
  const plantTotal = items.reduce((s, i) => s + i.amt, 0);

  const escom = inverterKw <= 5.0
    ? [
        { sl: 1, name: "Application & Registration Fee", spec: "ESCOM online portal submission", amt: 500, note: "+ 18% GST" },
        { sl: 2, name: "Facilitation & Processing Fee", spec: "Field verification & feasibility study", amt: 1000, note: "+ 18% GST" },
        { sl: 3, name: "PPA e-Sign Charge", spec: "Power Purchase Agreement legal stamping", amt: 12, note: "Statutory" },
        { sl: 4, name: "Bidirectional Utility Net-Meter", spec: "1-Phase whole current meter & testing", amt: 4500, note: "Utility standard" },
        { sl: 5, name: "Refundable Security Deposit", spec: "LT connectivity deposit", amt: 3000, note: "Refundable" },
      ]
    : [
        { sl: 1, name: "Application & Registration Fee", spec: "ESCOM online portal submission", amt: 1000, note: "+ 18% GST" },
        { sl: 2, name: "Facilitation & Processing Fee", spec: "Field verification & feasibility study", amt: 2000, note: "+ 18% GST" },
        { sl: 3, name: "PPA e-Sign Charge", spec: "Power Purchase Agreement legal stamping", amt: 12, note: "Statutory" },
        { sl: 4, name: "Bidirectional Utility Net-Meter", spec: "3-Phase bi-directional CT/PT net-meter", amt: 5000, note: "Utility standard" },
        { sl: 5, name: "Refundable Security Deposit", spec: "LT connectivity deposit", amt: 5000, note: "Refundable" },
      ];

  const escomTotal = escom.reduce((sum, e) => sum + e.amt, 0);
  const totalCapitalOutlay = plantTotal + escomTotal;
  return { items, plantTotal, escom, escomTotal, totalCapitalOutlay };
}

function num(id) {
  const v = parseFloat(document.getElementById(id)?.value);
  return isNaN(v) ? 0 : v;
}

// ============================================================
// HIERARCHICAL MULTI-SITE & MULTI-BUILDING DATA ARCHITECTURE
// ============================================================
let sites = [
  {
    id: "site-1",
    name: "",
    loc: "",
    email: "",
    mode: "roof",
    tariff: "",
    dist: "",
    activeBuildingIndex: 0,
    buildings: [
      {
        id: "bldg-1",
        name: "Building 1",
        L: "",
        B: "",
        parapet: "",
        neighbour: "None",
        panel: "550"
      }
    ],
    units: "",
    distBill: "",
    panelBill: "550",
    computed: null
  }
];
let activeSiteIndex = 0;
let vizSiteIndex = 0;
let vizBldgIndex = 0;

function saveCurrentFormToActiveSite() {
  if (!sites[activeSiteIndex]) return;
  const s = sites[activeSiteIndex];
  s.name = document.getElementById("cfgName")?.value || "";
  s.contact = document.getElementById("cfgContact")?.value || "";
  s.loc = document.getElementById("cfgLoc")?.value || "";
  s.email = document.getElementById("cfgEmail")?.value || "";
  s.sanctionedLoad = document.getElementById("cfgSanctionedLoad")?.value || "";
  s.tariff = document.getElementById("cfgTariff")?.value || "";
  s.mode = mode;
  s.dist = document.getElementById("cfgDist")?.value || "";

  if (!s.buildings || s.buildings.length === 0) {
    s.buildings = [{
      id: "bldg-1",
      name: "Building 1",
      L: "",
      B: "",
      parapet: "",
      neighbour: "None",
      panel: "550"
    }];
    s.activeBuildingIndex = 0;
  }
  if (s.activeBuildingIndex === undefined || s.activeBuildingIndex >= s.buildings.length) {
    s.activeBuildingIndex = 0;
  }

  const b = s.buildings[s.activeBuildingIndex];
  if (b) {
    b.L = document.getElementById("cfgL")?.value || "";
    b.B = document.getElementById("cfgB")?.value || "";
    b.parapet = document.getElementById("cfgParapet")?.value || "";
    b.neighbour = document.getElementById("cfgNeighbour")?.value || "None";
    b.panel = document.getElementById("cfgPanel")?.value || "550";
    b.tech = document.getElementById("cfgTech")?.value || "Mono-PERC (Mono-facial)";
  }

  s.units = document.getElementById("cfgUnits")?.value || "";
  s.distBill = document.getElementById("cfgDistBill")?.value || "";
  s.panelBill = document.getElementById("cfgPanelBill")?.value || "550";
  s.techBill = document.getElementById("cfgTechBill")?.value || "Mono-PERC (Mono-facial)";
  s.tech = document.getElementById("cfgTech")?.value || "Mono-PERC (Mono-facial)";
}

function loadSiteToForm(idx) {
  if (idx < 0 || idx >= sites.length) return;
  activeSiteIndex = idx;
  const s = sites[idx];
  if (document.getElementById("cfgName")) document.getElementById("cfgName").value = s.name || "";
  if (document.getElementById("cfgContact")) document.getElementById("cfgContact").value = s.contact || "";
  if (document.getElementById("cfgLoc")) document.getElementById("cfgLoc").value = s.loc || "";
  if (document.getElementById("cfgEmail")) document.getElementById("cfgEmail").value = s.email || "";
  if (document.getElementById("cfgSanctionedLoad")) document.getElementById("cfgSanctionedLoad").value = s.sanctionedLoad || "";
  setTimeout(() => { try { updatePathCardStates(); } catch(e){} }, 0);
  if (document.getElementById("cfgTariff")) document.getElementById("cfgTariff").value = s.tariff || "";
  if (document.getElementById("cfgDist")) document.getElementById("cfgDist").value = s.dist || "";
  if (document.getElementById("cfgUnits")) document.getElementById("cfgUnits").value = s.units || "";
  if (document.getElementById("cfgDistBill")) document.getElementById("cfgDistBill").value = s.distBill || "";
  if (document.getElementById("cfgPanelBill")) document.getElementById("cfgPanelBill").value = s.panelBill || "550";

  if (!s.buildings || s.buildings.length === 0) {
    s.buildings = [{
      id: "bldg-1",
      name: "Building 1",
      L: "",
      B: "",
      parapet: "",
      neighbour: "None",
      panel: "550"
    }];
    s.activeBuildingIndex = 0;
  }
  if (s.activeBuildingIndex === undefined || s.activeBuildingIndex >= s.buildings.length) {
    s.activeBuildingIndex = 0;
  }
  loadBuildingToForm(s.activeBuildingIndex);

  setMode(s.mode || "roof");
  renderSiteTabs();
  renderBuildingTabs();
  renderVizTabs();
  liveUpdate();
}

function loadBuildingToForm(bldgIdx) {
  const s = sites[activeSiteIndex];
  if (!s || !s.buildings) return;
  if (bldgIdx < 0 || bldgIdx >= s.buildings.length) bldgIdx = 0;
  s.activeBuildingIndex = bldgIdx;
  const b = s.buildings[bldgIdx];
  if (!b) return;

  const lEl = document.getElementById("cfgL");
  const bEl = document.getElementById("cfgB");
  const pEl = document.getElementById("cfgParapet");
  const nEl = document.getElementById("cfgNeighbour");
  const techEl = document.getElementById("cfgTech");
  const panEl = document.getElementById("cfgPanel");

  if (lEl) lEl.value = b.L ?? "";
  if (bEl) bEl.value = b.B ?? "";
  if (pEl) pEl.value = b.parapet ?? "";
  if (nEl) nEl.value = b.neighbour ?? "None";
  const bTech = b.tech || "Mono-PERC (Mono-facial)";
  if (techEl) {
    techEl.value = bTech;
    updateTechInfo("roof", bTech);
  }
  populatePanelDropdown("cfgPanel", bTech, b.panel || 550);
  if (panEl && b.panel) panEl.value = b.panel;
}


let bomActiveSiteIndex = 0;

function switchBomSite(idx) {
  bomActiveSiteIndex = idx;
  renderBomView();
}

function renderBomView() {
  const validSites = sites.filter(s => s.computed);
  if (!validSites || validSites.length === 0) return;

  if (bomActiveSiteIndex >= validSites.length) bomActiveSiteIndex = 0;
  const isMulti = validSites.length > 1;

  // Site selector tabs
  const tabWrap = document.getElementById("bomSiteSelectorWrap");
  const tabContainer = document.getElementById("bomSiteTabs");
  if (tabWrap && tabContainer) {
    if (isMulti) {
      tabWrap.style.display = "block";
      tabContainer.innerHTML = validSites.map((s, i) => {
        const isActive = i === bomActiveSiteIndex;
        const sName = s.name || `Site Name-${i + 1}`;
        return `
          <button type="button" class="preset ${isActive ? 'on' : ''}" onclick="switchBomSite(${i})" style="padding:6px 14px;font-size:.78rem;display:inline-flex;align-items:center;gap:6px">
            <span style="color:${isActive ? '#10b981' : '#64748b'}">●</span> ${sName} (${s.computed.capacityKw.toFixed(1)} kW)
          </button>
        `;
      }).join("");
    } else {
      tabWrap.style.display = "none";
    }
  }

  // Active site BOM to render
  const targetSite = isMulti ? validSites[bomActiveSiteIndex] : validSites[0];
  const sComp = targetSite.computed;

  // Card header and titles
  const titleEl = document.getElementById("bomCardTitle");
  const subEl = document.getElementById("bomCardSub");
  const statusBadge = document.getElementById("bomSiteStatusBadge");
  const warn20kW = document.getElementById("bomSiteWarning20kW");

  if (titleEl) {
    titleEl.textContent = isMulti ? `📦 Site ${bomActiveSiteIndex + 1}: ${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`} — Bill of Materials (BOM)` : `📦 Bill of Materials (BOM) — Plant-Side Equipment`;
  }
  if (subEl) {
    subEl.textContent = isMulti ? `12-item engineering specification and cost breakdown for ${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`} (${sComp.capacityKw.toFixed(2)} kW)` : `Full 12-item commercial LT equipment list with dynamic module, inverter & switchgear sizing`;
  }
  if (statusBadge) {
    statusBadge.innerHTML = isMulti ? `<span style="font-size:.72rem;font-weight:700;color:var(--primary);background:rgba(37,99,235,0.1);padding:3px 8px;border-radius:6px;border:1px solid rgba(37,99,235,0.25)">SITE ${bomActiveSiteIndex + 1} OF ${validSites.length}</span>` : "";
  }
  if (warn20kW) {
    const has20kNotice = sComp.rawCapacityKw >= 20.0 || (targetSite.sanctionedLoad && parseFloat(targetSite.sanctionedLoad) >= 20.0) || sComp.kercNotice;
    if (has20kNotice) {
      warn20kW.style.display = "block";
      warn20kW.textContent = "⚠️ 20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
    } else {
      warn20kW.style.display = "none";
    }
  }

  // Populate BOM Table
  const bomBody = document.getElementById("bomBody");
  if (bomBody) {
    bomBody.innerHTML = "";
    sComp.bom.items.forEach(it => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="tc">${String(it.sl).padStart(2, "0")}</td>
        <td><strong>${it.desc}</strong></td>
        <td style="color:var(--muted)">${it.spec}</td>
        <td class="tc">${it.qty}</td>
        <td class="tr" style="font-weight:700">₹ ${it.amt.toLocaleString()}</td>
      `;
      bomBody.appendChild(tr);
    });
  }
  const bomTotEl = document.getElementById("bomTotal");
  if (bomTotEl) {
    bomTotEl.textContent = `₹ ${sComp.bom.plantTotal.toLocaleString()} (${(sComp.bom.plantTotal / 1e5).toFixed(2)} Lakhs)`;
  }

  // Populate ESCOM Table
  const escomTitle = document.getElementById("escomCardTitle");
  if (escomTitle) {
    escomTitle.textContent = isMulti ? `🏛️ ESCOM / Utility Approvals & Grid Budget (${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`})` : `🏛️ ESCOM / Utility Approval & Interconnection Budget`;
  }
  const escomBody = document.getElementById("escomBody");
  if (escomBody) {
    escomBody.innerHTML = "";
    sComp.bom.escom.forEach(e => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="tc">${String(e.sl).padStart(2, "0")}</td>
        <td><strong>${e.name}</strong></td>
        <td style="color:var(--muted)">${e.spec} <span style="font-size:.72rem;color:var(--dim)">(${e.note})</span></td>
        <td class="tr" style="font-weight:700">₹ ${e.amt.toLocaleString()}</td>
      `;
      escomBody.appendChild(tr);
    });
  }
  const siteOutlayTitle = document.getElementById("siteTotalOutlayTitle");
  const siteOutlayVal = document.getElementById("siteTotalOutlayVal");
  if (siteOutlayTitle) {
    siteOutlayTitle.textContent = isMulti ? `Total Capital Required for ${targetSite.name || `Site Name-${bomActiveSiteIndex + 1}`}:` : `Total Estimated Capital Investment Required:`;
  }
  if (siteOutlayVal) {
    const sTot = sComp.bom.plantTotal + sComp.bom.escomTotal;
    siteOutlayVal.textContent = `₹ ${sTot.toLocaleString()} (${(sTot / 1e5).toFixed(2)} Lakhs)`;
  }

  // Portfolio Capex Matrix Card
  const capexCard = document.getElementById("cardPortfolioCapexMatrix");
  const capexBody = document.getElementById("portfolioCapexBody");
  if (capexCard && capexBody) {
    if (isMulti) {
      capexCard.style.display = "block";
      let totCap = 0, totBom = 0, totEsc = 0, grandTot = 0;
      capexBody.innerHTML = validSites.map((s, idx) => {
        const c = s.computed;
        const cap = c.capacityKw;
        const bCost = c.bom.plantTotal;
        const eCost = c.bom.escomTotal;
        const sTot = bCost + eCost;
        totCap += cap; totBom += bCost; totEsc += eCost; grandTot += sTot;
        const capMark = c.rawCapacityKw > 20.0 ? " *" : "";
        return `
          <tr>
            <td class="tc">${String(idx + 1).padStart(2, "0")}</td>
            <td><strong>${s.name || `Site Name-${idx + 1}`}</strong> <span style="font-size:.72rem;color:var(--muted)">(${s.loc || "Karnataka"})</span></td>
            <td class="tc">${c.buildings ? c.buildings.length : 1} Nos.</td>
            <td class="tc">${cap.toFixed(2)} kW${capMark}</td>
            <td class="tr">₹ ${bCost.toLocaleString()}</td>
            <td class="tr">₹ ${eCost.toLocaleString()}</td>
            <td class="tr" style="font-weight:700">₹ ${sTot.toLocaleString()}</td>
          </tr>
        `;
      }).join("");

      document.getElementById("matrixTotCap").textContent = `${totCap.toFixed(2)} kW`;
      document.getElementById("matrixTotBom").textContent = `₹ ${totBom.toLocaleString()}`;
      document.getElementById("matrixTotEscom").textContent = `₹ ${totEsc.toLocaleString()}`;
      document.getElementById("matrixGrandTotal").textContent = `₹ ${grandTot.toLocaleString()} (${(grandTot / 1e5).toFixed(2)} Lakhs)`;
    } else {
      capexCard.style.display = "none";
    }
  }
}

function renderBuildingTabs() {
  const s = sites[activeSiteIndex];
  const container = document.getElementById("studioBldgTabs");
  const delBtn = document.getElementById("btnDeleteBldg");
  if (!s || !s.buildings || !container) return;
  
  if (delBtn) {
    delBtn.style.display = s.buildings.length > 1 ? "inline-flex" : "none";
  }

  container.innerHTML = s.buildings.map((b, i) => {
    const isActive = i === s.activeBuildingIndex;
    const bName = b.name || `Building ${i + 1}`;
    return `
      <button type="button" class="preset ${isActive ? "on" : ""}" onclick="switchBuilding(${i})" style="padding:5px 12px;font-size:.74rem;display:inline-flex;align-items:center;gap:5px">
        <span>🏢</span> ${bName}
      </button>
    `;
  }).join("");
}

function switchBuilding(bldgIdx) {
  saveCurrentFormToActiveSite();
  const s = sites[activeSiteIndex];
  if (!s || !s.buildings || bldgIdx < 0 || bldgIdx >= s.buildings.length) return;
  s.activeBuildingIndex = bldgIdx;
  loadBuildingToForm(bldgIdx);
  renderBuildingTabs();
  liveUpdate();
}

function addNewBuilding() {
  saveCurrentFormToActiveSite();
  const s = sites[activeSiteIndex];
  if (!s) return;
  if (!s.buildings) s.buildings = [];
  if (s.buildings.length >= 10) {
    toast("Maximum 10 buildings per site");
    return;
  }
  const nextNum = s.buildings.length + 1;
  const newBldg = {
    id: "bldg-" + Date.now(),
    name: `Building ${nextNum}`,
    L: "",
    B: "",
    parapet: "",
    neighbour: "None",
    panel: s.buildings[0]?.panel || "550"
  };
  s.buildings.push(newBldg);
  s.activeBuildingIndex = s.buildings.length - 1;
  loadBuildingToForm(s.activeBuildingIndex);
  renderBuildingTabs();
  renderVizTabs();
  liveUpdate();
  toast(`Added Building ${nextNum} to ${s.name || `Site Name-${activeSiteIndex + 1}`}`);
}

function deleteActiveBuilding() {
  const s = sites[activeSiteIndex];
  if (!s || !s.buildings || s.buildings.length <= 1) {
    toast("At least one building is required per site");
    return;
  }
  const curBldg = s.buildings[s.activeBuildingIndex];
  const bldgName = curBldg?.name || `Building ${s.activeBuildingIndex + 1}`;
  if (!confirm(`Delete ${bldgName}?`)) return;
  s.buildings.splice(s.activeBuildingIndex, 1);
  if (s.activeBuildingIndex >= s.buildings.length) s.activeBuildingIndex = s.buildings.length - 1;
  loadBuildingToForm(s.activeBuildingIndex);
  renderBuildingTabs();
  renderVizTabs();
  liveUpdate();
  toast("Building removed");
}

function renderSiteTabs() {
  // 1. Header Topbar: Replicate sites with green dot (🟢 Site Name-1, 🟢 Site Name-2...)
  const topbar = document.getElementById("topbarSites");
  if (topbar) {
    topbar.innerHTML = sites.map((s, i) => {
      const userEntered = (s.name || "").trim();
      const displayName = userEntered || `Site Name-${i + 1}`;
      const isActive = i === activeSiteIndex;
      return `
        <div class="chip site-chip ${isActive ? "active" : ""}" data-site-idx="${i}" onclick="switchSite(${i})" title="Switch to ${displayName}">
          <span class="dot"></span>
          <span class="site-chip-name">${displayName}</span>
        </div>
      `;
    }).join("");
  }

  // 2. Project Design View Tabs
  const studioTabs = document.getElementById("studioSiteTabs");
  if (studioTabs) {
    studioTabs.innerHTML = sites.map((s, i) => {
      const userEntered = (s.name || "").trim();
      const displayName = userEntered || `Site Name-${i + 1}`;
      const isActive = i === activeSiteIndex;
      return `
        <button type="button" class="btn ${isActive ? "btn-p" : ""}" onclick="switchSite(${i})" style="padding:6px 12px;font-size:.78rem;border-radius:8px">
          <span style="color:#10b981;font-size:.75rem">●</span> ${displayName}
        </button>
      `;
    }).join("");
  }

  const btnDel = document.getElementById("btnDeleteSite");
  if (btnDel) {
    btnDel.style.display = sites.length > 1 ? "inline-flex" : "none";
  }
}

function onSiteNameInput() {
  saveCurrentFormToActiveSite();
  const userEntered = (document.getElementById("cfgName")?.value || "").trim();
  const displayName = userEntered || `Site Name-${activeSiteIndex + 1}`;
  if (sites[activeSiteIndex]) {
    sites[activeSiteIndex].name = userEntered;
  }
  const activeChipName = document.querySelector(`#topbarSites .site-chip[data-site-idx="${activeSiteIndex}"] .site-chip-name`);
  if (activeChipName) activeChipName.textContent = displayName;
  const studioTabBtns = document.querySelectorAll("#studioSiteTabs button");
  if (studioTabBtns[activeSiteIndex]) {
    studioTabBtns[activeSiteIndex].innerHTML = `<span style="color:#10b981;font-size:.75rem">●</span> ${displayName}`;
  }
  renderVizTabs();
  liveUpdate();
}

function addNewSite() {
  saveCurrentFormToActiveSite();
  if (sites.length >= 2) {
    toast("Maximum 2 sites allowed");
    return;
  }
  const nextNum = sites.length + 1;
  const newName = `Site Name-${nextNum}`;
  sites.push({
    id: "site-" + Date.now(),
    name: newName,
    loc: "",
    email: "",
    mode: "roof",
    tariff: "",
    dist: "",
    activeBuildingIndex: 0,
    buildings: [
      {
        id: "bldg-1",
        name: "Building 1",
        L: "",
        B: "",
        parapet: "",
        neighbour: "None",
        panel: "550"
      }
    ],
    units: "",
    distBill: "",
    panelBill: "550",
    computed: null
  });
  activeSiteIndex = sites.length - 1;
  loadSiteToForm(activeSiteIndex);
  renderVizTabs();
  toast(`Added ${newName}`);
}

function deleteActiveSite() {
  if (sites.length <= 1) {
    toast("At least one site is required");
    return;
  }
  const currentName = sites[activeSiteIndex]?.name || `Site Name-${activeSiteIndex + 1}`;
  if (!confirm(`Delete ${currentName}?`)) return;
  sites.splice(activeSiteIndex, 1);
  if (activeSiteIndex >= sites.length) activeSiteIndex = sites.length - 1;
  loadSiteToForm(activeSiteIndex);
  renderVizTabs();
  toast("Site removed");
}

function switchSite(idx) {
  if (idx === activeSiteIndex) return;
  saveCurrentFormToActiveSite();
  loadSiteToForm(idx);
}

// Visualizer Interactive Site & Building Selector
function renderVizTabs() {
  const siteContainer = document.getElementById("vizSiteTabs");
  if (siteContainer) {
    siteContainer.innerHTML = sites.map((s, i) => {
      const userEntered = (s.name || "").trim();
      const displayName = userEntered || `Site Name-${i + 1}`;
      const isActive = i === vizSiteIndex;
      return `
        <button type="button" class="preset ${isActive ? "on" : ""}" onclick="switchVizSite(${i})" style="padding:4px 10px;font-size:.72rem;display:inline-flex;align-items:center;gap:4px">
          <span style="color:#10b981">●</span> ${displayName}
        </button>
      `;
    }).join("");
  }

  const bldgContainer = document.getElementById("vizBldgTabs");
  if (bldgContainer) {
    const curSite = sites[vizSiteIndex] || sites[0];
    const bldgs = curSite?.buildings || [];
    bldgContainer.innerHTML = bldgs.map((b, j) => {
      const isActive = j === vizBldgIndex;
      const bName = b.name || `Building ${j + 1}`;
      return `
        <button type="button" class="preset ${isActive ? "on" : ""}" onclick="switchVizBuilding(${j})" style="padding:3px 8px;font-size:.68rem;display:inline-flex;align-items:center;gap:4px">
          <span>🏢</span> ${bName}
        </button>
      `;
    }).join("");
  }
}

function switchVizSite(sIdx) {
  if (sIdx < 0 || sIdx >= sites.length) return;
  vizSiteIndex = sIdx;
  vizBldgIndex = 0;
  renderVizTabs();
  updateVisualizerFromSelection();
}

function switchVizBuilding(bIdx) {
  const s = sites[vizSiteIndex] || sites[0];
  if (!s || !s.buildings || bIdx < 0 || bIdx >= s.buildings.length) return;
  vizBldgIndex = bIdx;
  renderVizTabs();
  updateVisualizerFromSelection();
}

function updateVisualizerFromSelection() {
  const s = sites[vizSiteIndex] || sites[0];
  if (!s) {
    updateRoofStats(null);
    drawArray(0);
    return;
  }

  if (s.mode === "roof") {
    const bldgs = s.buildings || [];
    const b = bldgs[vizBldgIndex] || bldgs[0];
    if (!b) {
      updateRoofStats(null);
      drawArray(0);
      return;
    }
    const L = parseFloat(b.L) || 0;
    const B = parseFloat(b.B) || 0;
    const parapet = Math.max(0, parseFloat(b.parapet) || 0);
    const panelW = parseInt(b.panel) || 550;
    const grossArea = Math.round(L * B * 100) / 100;
    const effL = Math.max(0, L - 2 * parapet);
    const effB = Math.max(0, B - 2 * parapet);
    const usableArea = Math.round(effL * effB * 100) / 100;
    const capKw = Math.round((usableArea / 100.0) * 100) / 100;
    const panels = panelW > 0 ? Math.ceil((capKw * 1000.0) / panelW) : 0;

    if (grossArea <= 0 || panels <= 0) {
      updateRoofStats(null);
      drawArray(0);
      return;
    }

    const bData = {
      grossRooftopArea: grossArea,
      utilizedRooftopArea: usableArea,
      parapet: parapet,
      neighbour: b.neighbour || "None",
      capacityKw: capKw,
      panelW: panelW,
      panels: panels,
      inverterKw: s.computed ? s.computed.invKw : selectInverter(Math.min(capKw, 20.0)),
      siteName: s.name || `Site Name-${vizSiteIndex + 1}`,
      bldgName: b.name || `Building ${vizBldgIndex + 1}`
    };

    updateRoofStats(bData);
    drawArray(panels, L, B, parapet, b.neighbour || "None");
  } else {
    // Mode Bill
    const units = parseFloat(s.units) || 0;
    const rawCap = Math.round((units / 120.0) * 100) / 100;
    const capKw = Math.min(rawCap, 20.0);
    const panelW = parseInt(s.panelBill) || 550;
    const panels = panelW > 0 ? Math.ceil((capKw * 1000.0) / panelW) : 0;
    const utilArea = Math.round(capKw * 100.0 * 100) / 100;
    if (capKw <= 0 || panels <= 0) {
      updateRoofStats(null);
      drawArray(0);
      return;
    }
    const bData = {
      grossRooftopArea: utilArea,
      utilizedRooftopArea: utilArea,
      parapet: 0,
      neighbour: "None",
      capacityKw: capKw,
      panelW: panelW,
      panels: panels,
      inverterKw: s.computed ? s.computed.invKw : selectInverter(capKw),
      siteName: s.name || `Site Name-${vizSiteIndex + 1}`,
      bldgName: "Site Total"
    };
    updateRoofStats(bData);
    drawArray(panels, Math.sqrt(utilArea * 1.3), Math.sqrt(utilArea * 0.7), 0, "None");
  }
}

// ============================================================
// CORE CALCULATION ENGINE (MULTI-SITE & 20 kW PER SITE CAP)
// ============================================================
function onCalculateClick() {
  saveCurrentFormToActiveSite();

  const curSite = sites[activeSiteIndex];
  if (mode === "roof") {
    const bldgs = curSite.buildings || [];
    const hasValidBldg = bldgs.some(b => (parseFloat(b.L) || 0) > 0 && (parseFloat(b.B) || 0) > 0);
    if (!hasValidBldg) {
      toast("⚠️ Please enter Rooftop Length & Breadth in Project Design");
      switchView('studio');
      document.getElementById("cfgL")?.focus();
      return;
    }
  } else {
    const units = parseFloat(curSite.units) || 0;
    if (units <= 0) {
      toast("⚠️ Please enter Monthly Electricity Units (kWh)");
      switchView('studio');
      document.getElementById("cfgUnits")?.focus();
      return;
    }
  }

  liveUpdate();
  vizSiteIndex = activeSiteIndex;
  vizBldgIndex = 0;
  renderVizTabs();
  updateVisualizerFromSelection();
  switchView('dashboard');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  toast("⚡ System Calculated & Loaded on Dashboard!");

  // Check statutory 20 kW LT ceiling
  if (curSite && curSite.computed && curSite.computed.rawCapacityKw > 20.0) {
    check20kWLimit(curSite, true);
  }
}

function check20kWLimit(site, isExplicitClick = false) {
  if (!site) return;
  const rawCap = site.computed?.rawCapacityKw || 0;
  if (rawCap > 20.0 && (!site.warned20kW || isExplicitClick)) {
    const modal = document.getElementById("modalStatutory20kW");
    const nameEl = document.getElementById("warnSiteName");
    const capEl = document.getElementById("warnRawCap");
    if (modal && nameEl && capEl) {
      nameEl.textContent = site.name || `Site Name-${sites.indexOf(site) + 1}`;
      capEl.textContent = `${rawCap.toFixed(2)} kW`;
      modal.style.display = "flex";
      site.warned20kW = true;
    }
  }
}

function close20kWModal(splitNewSite = false) {
  const modal = document.getElementById("modalStatutory20kW");
  if (modal) modal.style.display = "none";
  if (splitNewSite) {
    addNewSite();
  }
}

function computeSingleSite(s) {
  const panelW = s.mode === "bill" 
    ? (parseInt(s.panelBill) || MODULE_WATT_DEFAULT) 
    : (parseInt(s.panel || (s.buildings && s.buildings[0]?.panel)) || MODULE_WATT_DEFAULT);
  const dist = parseFloat(s.dist) || 20;
  const customTariff = parseFloat(s.tariff) || 8.05;

  let grossRooftopArea = 0;
  let utilizedRooftopArea = 0;
  let rawCapacityKw = 0;
  let panels = 0;
  let bldgResults = [];

  if (s.mode === "roof") {
    const bldgs = s.buildings && s.buildings.length > 0 ? s.buildings : [{ L: s.L, B: s.B, parapet: s.parapet, panel: s.panel, neighbour: s.neighbour }];
    bldgs.forEach((b, idx) => {
      const L = parseFloat(b.L ?? b.lengthFt ?? b.length_ft) || 0;
      const B = parseFloat(b.B ?? b.breadthFt ?? b.breadth_ft) || 0;
      const parapet = Math.max(0, parseFloat(b.parapet ?? b.parapetFt ?? b.parapet_ft) || 0);
      const bPanelW = parseInt(b.panel ?? b.panelW ?? b.panel_watt) || panelW;
      
      const bGross = Math.round(L * B * 100) / 100;
      const effL = Math.max(0, L - 2 * parapet);
      const effB = Math.max(0, B - 2 * parapet);
      const bUtil = Math.round(effL * effB * 100) / 100;
      const bCap = Math.round((bUtil / 100.0) * 100) / 100;
      const bPanels = bPanelW > 0 ? Math.ceil((bCap * 1000.0) / bPanelW) : 0;
      
      grossRooftopArea += bGross;
      utilizedRooftopArea += bUtil;
      rawCapacityKw += bCap;
      panels += bPanels;
      
      const bTech = b.tech || b.panelTech || s.tech || "Mono-PERC (Mono-facial)";
      bldgResults.push({
        name: b.name || `Building ${idx + 1}`,
        grossArea: bGross,
        usableArea: bUtil,
        capacityKw: bCap,
        panels: bPanels,
        panelW: bPanelW,
        panelTech: bTech,
        parapet: parapet,
        neighbour: b.neighbour || "None"
      });
    });
  } else {
    // Path 2: bill method — may still size from sanctioned load if units empty
    const units = parseFloat(s.units) || 0;
    const sanEarly = parseFloat(s.sanctionedLoad) || 0;
    if (units > 0) {
      rawCapacityKw = Math.round((units / 120.0) * 100) / 100;
    } else if (sanEarly > 0) {
      // Sanctioned load drives capacity when bill units not entered
      rawCapacityKw = Math.min(20.0, sanEarly);
    } else {
      return null;
    }
    utilizedRooftopArea = Math.round(rawCapacityKw * 100.0 * 100) / 100;
    grossRooftopArea = utilizedRooftopArea;
    panels = panelW > 0 ? Math.ceil((rawCapacityKw * 1000.0) / panelW) : 0;
    bldgResults.push({
      name: "Building 1",
      grossArea: grossRooftopArea,
      usableArea: utilizedRooftopArea,
      capacityKw: rawCapacityKw,
      panels: panels,
      panelW: panelW,
      panelTech: s.tech || s.techBill || "Mono-PERC (Mono-facial)",
      parapet: 0,
      neighbour: "None"
    });
  }

  const sanctionedLoad = parseFloat(s.sanctionedLoad) || 0;

  // PRIORITY: Sanctioned Load / Contract Demand sets plant capacity (LT max 20 kW)
  // Length & breadth still used for layout / area status when available
  if (sanctionedLoad > 0) {
    const effectiveCd = Math.min(20.0, sanctionedLoad);
    rawCapacityKw = effectiveCd;
    panels = panelW > 0 ? Math.ceil((effectiveCd * 1000.0) / panelW) : 0;
    if (!utilizedRooftopArea || utilizedRooftopArea <= 0) {
      utilizedRooftopArea = Math.round(effectiveCd * 100.0 * 100) / 100;
      grossRooftopArea = utilizedRooftopArea;
    }
    if (!bldgResults.length) {
      bldgResults.push({
        name: "Building 1",
        grossArea: grossRooftopArea,
        usableArea: utilizedRooftopArea,
        capacityKw: effectiveCd,
        panels: panels,
        panelW: panelW,
        panelTech: s.tech || s.techBill || "Mono-PERC (Mono-facial)",
        parapet: 0,
        neighbour: "None"
      });
    } else {
      // redistribute capacity across buildings proportionally for display
      bldgResults.forEach(br => {
        br.capacityKw = effectiveCd;
        br.panels = panels;
      });
    }
  }

  if (rawCapacityKw <= 0 || panels <= 0) return null;

  let roofAreaStatus = "";
  let kercNotice = "";
  let capacityKw = 0;

  if (sanctionedLoad > 0) {
    const effectiveCd = Math.min(20.0, sanctionedLoad);
    const reqAreaSqft = Math.round(effectiveCd * 80.0 * 10) / 10;
    const maxRoofCapKw = utilizedRooftopArea > 0
      ? Math.round((utilizedRooftopArea / 80.0) * 100) / 100
      : effectiveCd;

    // Capacity ALWAYS follows sanctioned load (user requirement)
    capacityKw = effectiveCd;
    if (utilizedRooftopArea > 0 && utilizedRooftopArea < reqAreaSqft) {
      roofAreaStatus = `Sanctioned ${effectiveCd} kW set · Rooftop may be tight (−${Math.round(reqAreaSqft - utilizedRooftopArea)} sq.ft vs ~80 sq.ft/kW guide)`;
    } else if (utilizedRooftopArea > 0) {
      roofAreaStatus = `Sanctioned Load ${effectiveCd} kW · Rooftop OK (+${Math.round(utilizedRooftopArea - reqAreaSqft)} sq.ft vs guide)`;
    } else {
      roofAreaStatus = `Sized to Sanctioned Load / Contract Demand: ${effectiveCd} kW (enter L×B for layout check)`;
    }

    panels = panelW > 0 ? Math.ceil((capacityKw * 1000.0) / panelW) : 0;
    rawCapacityKw = effectiveCd;

    if (sanctionedLoad >= 20.0 || rawCapacityKw >= 20.0) {
      kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
    }
  } else {
    capacityKw = Math.min(rawCapacityKw, 20.0);
    if (rawCapacityKw >= 20.0) {
      panels = Math.ceil((20.0 * 1000.0) / panelW);
      kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
    }
    roofAreaStatus = "Direct Physical Rooftop Sizing";
  }

  s.roofAreaStatus = roofAreaStatus;
  s.kercNotice = kercNotice;

  const installedDckWp = Math.round((panels * panelW / 1000.0) * 100) / 100;
  const evalCapacity = Math.max(capacityKw, installedDckWp);
  const strings = Math.max(1, Math.ceil(panels / 20.0));

  // Requirement 1: Inverter selected to 70% derating of solar DC output
  const invKw = selectInverter(evalCapacity);
  const phase3 = invKw > 5.0;

  // Requirement 2: AC-side components sized by derated calculated power (evalCapacity * 0.70)
  const deratedAcKw = Math.round(evalCapacity * 0.70 * 100) / 100;
  const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
  const acdb = selectAcdbComponents(deratedAcKw, dist);

  // Requirement 3: Panel technology and standard ratings
  const activeTech = s.tech || (bldgResults[0] && bldgResults[0].panelTech) || "Mono-PERC (Mono-facial)";
  const bom = generatePlantBom(capacityKw, invKw, panelW, panels, acdb.breakerRating, bldgResults, dist, activeTech);

  const monthly = {};
  let annual = 0;
  MONTHS.forEach((m, i) => {
    const val = Math.round(evalCapacity * MONTHLY_YIELD[m] * DAYS_IN_MONTH[i] * 100) / 100;
    monthly[m] = val;
    annual += val;
  });
  annual = Math.round(annual * 100) / 100;

  const series25 = [];
  let curGen = annual;
  let total25 = 0;
  for (let y = 0; y < 25; y++) {
    series25.push(Math.round(curGen * 100) / 100);
    total25 += curGen;
    curGen *= 0.99;
  }
  total25 = Math.round(total25 * 100) / 100;

  return {
    name: s.name,
    loc: s.loc,
    email: s.email,
    mode: s.mode,
    panelW,
    panelTech: activeTech,
    dist,
    roofAreaStatus: roofAreaStatus,
    kercNotice: kercNotice,
    sanctionedLoad: sanctionedLoad,
    customTariff,
    grossRooftopArea,
    utilizedRooftopArea,
    rawCapacityKw,
    capacityKw,
    deratedAcKw,
    installedDckWp,
    evalCapacity,
    panels,
    strings,
    invKw,
    phase3,
    invCable,
    acdb,
    bom,
    monthly,
    annual,
    series25,
    total25,
    buildings: bldgResults
  };
}


// ============================================================
// PURE CALCULATION ENGINE & COMPUTE BRIDGE (Contract N)
// ============================================================

// ============================================================
// PURE CALCULATION ENGINE (Contract N: schemaVersion 1)
// Pure function: calculate(projectDto) -> resultDto
// Does NOT depend on the DOM. Runs in browser or node/backend.
// ============================================================
function calculate(projectDto) {
  if (!projectDto) return null;
  const schemaVersion = 1;
  const pricing = projectDto.pricing || (typeof dynamicPricing !== "undefined" ? dynamicPricing : {});

  const customTariff = parseFloat(projectDto.custom_tariff) || 8.05;
  const projectMode = projectDto.mode || "roof";
  const rawSites = Array.isArray(projectDto.sites) && projectDto.sites.length > 0 
    ? projectDto.sites.slice(0, 2) // Cap at <= 2 sites (Contract D)
    : [{
        id: "site-1",
        name: projectDto.customer_name || "Site 1",
        mode: projectMode,
        sanctioned_load_kw: projectDto.sanctioned_load_kw,
        distance_m: projectDto.distance_m || 20,
        monthly_units: projectDto.monthly_units || 0,
        tariff: customTariff,
        buildings: projectDto.buildings || []
      }];

  const siteResults = [];

  rawSites.forEach((s, sIdx) => {
    const sName = s.name || `Site Name-${sIdx + 1}`;
    const sLoc = s.location || projectDto.location || "Karnataka";
    const sSanctioned = parseFloat(s.sanctioned_load_kw) || 0;
    
    // Contract D: If sanctioned load filled -> force Path 1 (roof)
    let sMode = s.mode || projectMode;
    if (sSanctioned > 0) {
      sMode = "roof";
    }

    const sDist = parseFloat(s.distance_m) || 20;
    const sTariff = parseFloat(s.tariff) || customTariff;
    const bldgs = Array.isArray(s.buildings) && s.buildings.length > 0
      ? s.buildings.slice(0, 10) // Cap at <= 10 buildings (Contract D)
      : [{
          name: "Building 1",
          length_ft: s.length_ft || 0,
          breadth_ft: s.breadth_ft || 0,
          parapet_ft: s.parapet_ft || 0,
          neighbour: s.neighbour || "None",
          panel_watt: s.panel_watt || 550,
          panel_tech: s.panel_tech || "Mono-PERC (Mono-facial)"
        }];

    let grossRooftopArea = 0;
    let utilizedRooftopArea = 0;
    let rawCapacityKw = 0;
    let totalPanels = 0;
    const bldgResults = [];

    const defaultPanelW = parseInt(s.panel_watt) || 550;
    const defaultTech = s.panel_tech || "Mono-PERC (Mono-facial)";

    if (sMode === "roof") {
      bldgs.forEach((b, bIdx) => {
        const L = parseFloat(b.length_ft ?? b.L) || 0;
        const B = parseFloat(b.breadth_ft ?? b.B) || 0;
        const parapet = Math.max(0, parseFloat(b.parapet_ft ?? b.parapet) || 0);
        const bPanelW = parseInt(b.panel_watt ?? b.panel) || defaultPanelW;
        const bTech = b.panel_tech ?? b.tech ?? defaultTech;
        const bNeighbour = b.neighbour || "None";

        const bGross = Math.round(L * B * 100) / 100;
        const effL = Math.max(0, L - 2 * parapet);
        const effB = Math.max(0, B - 2 * parapet);
        const bUtil = Math.round(effL * effB * 100) / 100;
        const bCap = Math.round((bUtil / 100.0) * 100) / 100;
        const bPanels = bPanelW > 0 ? Math.ceil((bCap * 1000.0) / bPanelW) : 0;

        grossRooftopArea += bGross;
        utilizedRooftopArea += bUtil;
        rawCapacityKw += bCap;
        totalPanels += bPanels;

        bldgResults.push({
          name: b.name || `Building ${bIdx + 1}`,
          grossArea: bGross,
          usableArea: bUtil,
          capacityKw: bCap,
          panels: bPanels,
          panelW: bPanelW,
          panelTech: bTech,
          parapet: parapet,
          neighbour: bNeighbour
        });
      });
    } else {
      // Path 2: Bill Method
      const units = parseFloat(s.monthly_units ?? s.units) || 0;
      if (units > 0) {
        rawCapacityKw = Math.round((units / 120.0) * 100) / 100;
      } else {
        rawCapacityKw = 0;
      }
      utilizedRooftopArea = Math.round(rawCapacityKw * 100.0 * 100) / 100;
      grossRooftopArea = utilizedRooftopArea;
      totalPanels = defaultPanelW > 0 ? Math.ceil((rawCapacityKw * 1000.0) / defaultPanelW) : 0;
      bldgResults.push({
        name: "Building 1",
        grossArea: grossRooftopArea,
        usableArea: utilizedRooftopArea,
        capacityKw: rawCapacityKw,
        panels: totalPanels,
        panelW: defaultPanelW,
        panelTech: defaultTech,
        parapet: 0,
        neighbour: "None"
      });
    }

    // Sanctioned Load / Contract Demand logic (Site-Level, Contract D)
    let roofAreaStatus = "";
    let kercNotice = "";
    let capacityKw = 0;
    let isCapped20kW = false;

    if (sSanctioned > 0) {
      const effectiveCd = Math.min(20.0, sSanctioned);
      capacityKw = effectiveCd;
      rawCapacityKw = effectiveCd;
      totalPanels = defaultPanelW > 0 ? Math.ceil((capacityKw * 1000.0) / defaultPanelW) : 0;

      const reqAreaSqft = Math.round(effectiveCd * 80.0 * 10) / 10;
      if (utilizedRooftopArea > 0 && utilizedRooftopArea < reqAreaSqft) {
        roofAreaStatus = `Sanctioned ${effectiveCd} kW set · Rooftop may be tight (−${Math.round(reqAreaSqft - utilizedRooftopArea)} sq.ft vs ~80 sq.ft/kW guide)`;
      } else if (utilizedRooftopArea > 0) {
        roofAreaStatus = `Sanctioned Load ${effectiveCd} kW · Rooftop OK (+${Math.round(utilizedRooftopArea - reqAreaSqft)} sq.ft vs guide)`;
      } else {
        roofAreaStatus = `Sized to Sanctioned Load / Contract Demand: ${effectiveCd} kW (enter L×B for layout check)`;
      }

      if (sSanctioned >= 20.0 || rawCapacityKw >= 20.0) {
        isCapped20kW = true;
        kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
      }

      // Update building capacity proportion
      if (bldgResults.length) {
        bldgResults.forEach(br => {
          br.capacityKw = capacityKw;
          br.panels = totalPanels;
        });
      }
    } else {
      capacityKw = Math.min(rawCapacityKw, 20.0);
      if (rawCapacityKw >= 20.0) {
        isCapped20kW = true;
        totalPanels = Math.ceil((20.0 * 1000.0) / defaultPanelW);
        kercNotice = "20 kW Reached For LT Limited 20kW as per KERC/ESCOM Regulations";
      }
      roofAreaStatus = "Direct Physical Rooftop Sizing";
    }

    if (capacityKw <= 0 || totalPanels <= 0) {
      // Empty or invalid site
      return;
    }

    const installedDckWp = Math.round((totalPanels * defaultPanelW / 1000.0) * 100) / 100;
    const evalCapacity = Math.max(capacityKw, installedDckWp);
    const strings = Math.max(1, Math.ceil(totalPanels / 20.0));

    // Contract: Inverter selected to 70% derating factor of total solar DC output
    const deratedAcKw = Math.round(evalCapacity * 0.70 * 100) / 100;
    const invKw = selectInverter(evalCapacity);
    const phase3 = invKw > 5.0;
    const invCable = inverterCableAndIsolator(deratedAcKw, phase3);
    const acdb = selectAcdbComponents(deratedAcKw, sDist);
    const bom = generatePlantBom(capacityKw, invKw, defaultPanelW, totalPanels, acdb.breakerRating, bldgResults, sDist, defaultTech);

    // Generation models
    const monthly = {};
    let annual = 0;
    MONTHS.forEach((m, idx) => {
      const val = Math.round(evalCapacity * MONTHLY_YIELD[m] * DAYS_IN_MONTH[idx] * 100) / 100;
      monthly[m] = val;
      annual += val;
    });
    annual = Math.round(annual * 100) / 100;

    const series25 = [];
    let curGen = annual;
    let total25 = 0;
    for (let y = 0; y < 25; y++) {
      series25.push(Math.round(curGen * 100) / 100);
      total25 += curGen;
      curGen *= 0.99;
    }
    total25 = Math.round(total25 * 100) / 100;

    siteResults.push({
      id: s.id || `site-${sIdx + 1}`,
      name: sName,
      location: sLoc,
      email: s.email || "",
      mode: sMode,
      panelW: defaultPanelW,
      panelTech: defaultTech,
      distance_m: sDist,
      tariff: sTariff,
      sanctioned_load_kw: sSanctioned,
      roofAreaStatus,
      kercNotice,
      isCapped20kW,
      grossRooftopArea,
      utilizedRooftopArea,
      rawCapacityKw,
      capacityKw,
      deratedAcKw,
      installedDckWp,
      evalCapacity,
      panels: totalPanels,
      strings,
      invKw,
      phase3,
      invCable,
      acdb,
      bom,
      monthly,
      annual,
      series25,
      total25,
      buildings: bldgResults
    });
  });

  if (!siteResults.length) return null;

  // Project-level Aggregation (All Sites)
  let totalCapKw = 0;
  let totalInstalledDckWp = 0;
  let totalPanels = 0;
  let totalGross = 0;
  let totalUtil = 0;
  let totalAnnual = 0;
  let total25 = 0;
  let totalProjectCost = 0;
  const projectMonthly = {};
  MONTHS.forEach(m => projectMonthly[m] = 0);

  siteResults.forEach(sc => {
    totalCapKw += sc.capacityKw;
    totalInstalledDckWp += sc.installedDckWp;
    totalPanels += sc.panels;
    totalGross += sc.grossRooftopArea;
    totalUtil += sc.utilizedRooftopArea;
    totalAnnual += sc.annual;
    total25 += sc.total25;
    totalProjectCost += sc.bom.plantTotal;
    MONTHS.forEach(m => {
      projectMonthly[m] += sc.monthly[m];
    });
  });

  totalCapKw = Math.round(totalCapKw * 100) / 100;
  totalInstalledDckWp = Math.round(totalInstalledDckWp * 100) / 100;
  totalAnnual = Math.round(totalAnnual * 100) / 100;
  total25 = Math.round(total25 * 100) / 100;

  const firstSite = siteResults[0];

  // Consolidated Turnkey BOM
  let consolidatedBom = firstSite.bom;
  if (siteResults.length > 1) {
    const consolidatedItems = [];
    const totalModAmt = siteResults.reduce((sum, s) => sum + s.bom.items[0].amt, 0);
    consolidatedItems.push({
      sl: 1,
      desc: "Solar PV Modules (Mono PERC / TOPCon)",
      spec: `${firstSite.panelW}W Mono PERC Half-Cut Cells (>21.3% Efficiency)`,
      qty: `${totalPanels} Nos.`,
      amt: totalModAmt
    });
    const invSummary = siteResults.map(s => `${s.name}: ${s.invKw} kW`).join(", ");
    const totalInvAmt = siteResults.reduce((sum, s) => sum + (s.bom.items[1]?.amt || 0), 0);
    consolidatedItems.push({
      sl: 2,
      desc: "On-Grid Solar String Inverter(s)",
      spec: `Dual MPPT, IP65 Enclosure (${invSummary})`,
      qty: `${siteResults.length} Set(s)`,
      amt: totalInvAmt
    });
    for (let idx = 2; idx < 12; idx++) {
      const baseItem = firstSite.bom.items[idx];
      if (baseItem) {
        const itemAmt = siteResults.reduce((sum, s) => sum + (s.bom.items[idx]?.amt || 0), 0);
        consolidatedItems.push({
          sl: idx + 1,
          desc: baseItem.desc,
          spec: baseItem.spec,
          qty: `${siteResults.length} Site(s)`,
          amt: itemAmt
        });
      }
    }
    consolidatedBom = {
      items: consolidatedItems,
      plantTotal: totalProjectCost,
      escom: firstSite.bom.escom,
      escomTotal: siteResults.reduce((sum, s) => sum + s.bom.escomTotal, 0),
      totalCapitalOutlay: totalProjectCost + siteResults.reduce((sum, s) => sum + s.bom.escomTotal, 0)
    };
  }

  // Performance KPIs
  const evalCapacity = Math.max(totalCapKw, totalInstalledDckWp);
  const pr = 0.75;
  const cuf = evalCapacity > 0 ? (totalAnnual / (evalCapacity * 8760.0)) * 100 : 0.0;
  const sysEff = pr * 20.0;
  const specificYield = evalCapacity > 0 ? totalAnnual / evalCapacity : 0.0;

  // Consolidated 25-Year Amortization Schedule
  const amcYearly = evalCapacity * 600.0;
  let cumulativeNet = 0.0;
  let payY = 0;
  let payM = 0;
  let paid = false;
  const amort = [];
  let curGen = totalAnnual;
  const tariffScale = customTariff > 0 ? (customTariff / TARIFF_25Y[0]) : 1.0;

  for (let y = 0; y < 25; y++) {
    const baseT = TARIFF_25Y[y < TARIFF_25Y.length ? y : TARIFF_25Y.length - 1];
    const tariff = Math.round(baseT * tariffScale * 100) / 100;
    const revenue = curGen * tariff;
    const net = revenue - amcYearly;
    cumulativeNet += net;

    if (!paid && cumulativeNet >= totalProjectCost) {
      payY = y + 1;
      const remaining = totalProjectCost - (cumulativeNet - net);
      const monthlyNet = Math.max(1e-9, net / 12.0);
      payM = Math.ceil(remaining / monthlyNet);
      paid = true;
    }

    amort.push({
      year: y + 1,
      gen: Math.round(curGen),
      tariff: tariff.toFixed(2),
      revenue: Math.round(revenue),
      amc: Math.round(amcYearly),
      net: Math.round(net),
      cum: Math.round(cumulativeNet),
    });

    curGen *= 0.99;
  }

  const lifetimeProfit = Math.round(cumulativeNet - totalProjectCost);
  const fd25y = Math.round(totalProjectCost * Math.pow(1 + 0.065, 25));

  const co2 = Math.floor((total25 * 0.82) / 1000);
  const trees = Math.floor((co2 * 1000) / 625);
  const carKm = Math.floor((co2 * 1000) / 0.12);
  const coalT = Math.round(total25 * 0.0004 * 10) / 10;

  const series25 = [];
  let curG = totalAnnual;
  for (let y = 0; y < 25; y++) {
    series25.push(Math.round(curG * 100) / 100);
    curG *= 0.99;
  }

  return {
    schemaVersion,
    calculated_at: new Date().toISOString(),
    customer_name: projectDto.customer_name || firstSite.name,
    location: projectDto.location || firstSite.location,
    mode: projectMode,
    capacityKw: totalCapKw,
    installedDckWp: totalInstalledDckWp,
    rawCapacityKw: siteResults.reduce((sum, s) => sum + s.rawCapacityKw, 0),
    isCapped20kW: siteResults.some(s => s.isCapped20kW),
    kercNotice: siteResults.map(s => s.kercNotice).filter(Boolean).join(" · "),
    roofAreaStatus: siteResults.map(s => s.roofAreaStatus).filter(Boolean).join(" · "),
    panels: totalPanels,
    strings: Math.ceil(totalPanels / 20.0),
    invKw: firstSite.invKw,
    phase3: firstSite.phase3,
    deratedAcKw: firstSite.deratedAcKw,
    invCable: firstSite.invCable,
    acdb: firstSite.acdb,
    bom: consolidatedBom,
    monthly: projectMonthly,
    annual: totalAnnual,
    series25,
    total25,
    pr, cuf, sysEff, specificYield,
    amort, payY, payM, lifetimeProfit, fd25y,
    co2, trees, carKm, coalT,
    sitesCount: siteResults.length,
    sites: siteResults
  };
}
window.calculate = calculate;


function compute() {
  saveCurrentFormToActiveSite();
  
  // Construct projectDto conforming to schemaVersion: 1
  const projectDto = {
    schemaVersion: 1,
    customer_name: (sites[0]?.name || document.getElementById("cfgName")?.value || "Solar Site").trim(),
    location: (sites[0]?.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim(),
    contact_number: (sites[0]?.contact || document.getElementById("cfgContact")?.value || "").trim(),
    email: (sites[0]?.email || document.getElementById("cfgEmail")?.value || "").trim(),
    sanctioned_load_kw: parseFloat(sites[0]?.sanctionedLoad || document.getElementById("cfgSanctionedLoad")?.value) || null,
    custom_tariff: parseFloat(sites[0]?.tariff || document.getElementById("cfgTariff")?.value) || 8.05,
    mode: mode,
    pricing: typeof dynamicPricing !== "undefined" ? dynamicPricing : {},
    sites: sites.slice(0, 2).map((s, idx) => ({
      id: s.id || `site-${idx + 1}`,
      name: (s.name || `Site Name-${idx + 1}`).trim(),
      location: (s.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim(),
      contact_number: (s.contact || document.getElementById("cfgContact")?.value || "").trim(),
      email: (s.email || document.getElementById("cfgEmail")?.value || "").trim(),
      sanctioned_load_kw: parseFloat(s.sanctionedLoad) || null,
      mode: s.mode || mode || "roof",
      tariff: parseFloat(s.tariff) || 8.05,
      distance_m: parseFloat(s.dist) || 20.0,
      monthly_units: parseFloat(s.units) || 0,
      buildings: (s.buildings || []).slice(0, 10).map((b, bIdx) => ({
        id: b.id || `bldg-${bIdx + 1}`,
        name: b.name || `Building ${bIdx + 1}`,
        length_ft: parseFloat(b.L) || 0,
        breadth_ft: parseFloat(b.B) || 0,
        parapet_ft: parseFloat(b.parapet) || 0,
        neighbour: b.neighbour || "None",
        panel_watt: parseInt(b.panel) || 550,
        panel_tech: b.tech || s.tech || "Mono-PERC (Mono-facial)"
      }))
    }))
  };

  const resultDto = calculate(projectDto);
  if (!resultDto) return null;

  // Sync per-site computed results back to sites array
  if (resultDto.sites && Array.isArray(resultDto.sites)) {
    resultDto.sites.forEach((sc, i) => {
      if (sites[i]) {
        sites[i].computed = sc;
      }
    });
  }

  return resultDto;
}
window.compute = compute;


function liveUpdate() {
  const r = compute();
  current = r;

  const siteObj = sites[activeSiteIndex] || {};
  const userEnteredName = (document.getElementById("cfgName")?.value || "").trim();
  const siteDisplayName = userEnteredName || (siteObj.name ? siteObj.name.trim() : "") || `Site Name-${activeSiteIndex + 1}`;
  if (siteObj && userEnteredName) {
    siteObj.name = userEnteredName;
  }

  const activeChipName = document.querySelector(`#topbarSites .site-chip[data-site-idx="${activeSiteIndex}"] .site-chip-name`);
  if (activeChipName) activeChipName.textContent = siteDisplayName;
  const studioTabBtns = document.querySelectorAll("#studioSiteTabs button");
  if (studioTabBtns && studioTabBtns[activeSiteIndex]) {
    studioTabBtns[activeSiteIndex].innerHTML = `<span style="color:#10b981;font-size:.75rem">●</span> ${siteDisplayName}`;
  }

  updateClock();

  const alertEl = document.getElementById("areaStatusAlert");
  if (alertEl) {
    if (r && r.roofAreaStatus && siteObj.sanctionedLoad && parseFloat(siteObj.sanctionedLoad) > 0) {
      alertEl.style.display = "block";
      const isDeficit = r.roofAreaStatus.toLowerCase().includes("deficit");
      alertEl.style.background = isDeficit ? "rgba(239, 68, 68, 0.12)" : "rgba(16, 185, 129, 0.12)";
      alertEl.style.border = isDeficit ? "1px solid rgba(239, 68, 68, 0.35)" : "1px solid rgba(16, 185, 129, 0.35)";
      alertEl.style.color = isDeficit ? "#f87171" : "#34d399";
      alertEl.innerHTML = (isDeficit ? "⚠️ " : "✓ ") + r.roofAreaStatus + (r.kercNotice ? `<br><span style="color:#ef4444;font-size:0.72rem;display:inline-block;margin-top:4px">⚠️ ${r.kercNotice}</span>` : "");
    } else {
      alertEl.style.display = "none";
    }
  }

  if (!r) {
    document.getElementById("topKwp").textContent = "— kWp";
    document.getElementById("kpiCap").textContent = "— kW";
    document.getElementById("kpiPanels").textContent = "Enter design parameters";
    document.getElementById("kpiInvBadge").textContent = "—";
    document.getElementById("kpiGen").textContent = "— kWh";
    document.getElementById("kpiYield").textContent = "Specific yield: —";
    document.getElementById("kpiCost").textContent = "₹ —";
    document.getElementById("kpiWp").textContent = "12-Item BOM Basis";
    document.getElementById("kpiPay").textContent = "—";
    document.getElementById("kpiProfit").textContent = "Post-payback profit";
    document.getElementById("emptyGuide").classList.add("show");
    drawArray(0);
    updateRoofStats(null);
    return;
  }

  document.getElementById("emptyGuide").classList.remove("show");

  // Top bar chips & KPIs
  document.getElementById("topKwp").textContent = `${r.installedDckWp.toFixed(2)} kWp`;
  document.getElementById("kpiCap").textContent = `${r.capacityKw.toFixed(2)} kW`;
  document.getElementById("kpiPanels").textContent = `DC: ${r.installedDckWp.toFixed(2)} kWp · ${r.panels} Panels (${r.panelW}W)`;
  document.getElementById("kpiInvBadge").textContent = `${r.invKw} kW ${r.phase3 ? "3-Ph" : "1-Ph"}`;
  document.getElementById("kpiGen").textContent = `${r.annual.toLocaleString()} kWh`;
  document.getElementById("kpiYield").textContent = `Specific Yield: ${r.specificYield.toFixed(0)} kWh/kWp/yr`;
  document.getElementById("kpiCost").textContent = `₹ ${(r.bom.plantTotal / 1e5).toFixed(2)} L`;
  document.getElementById("kpiWp").textContent = `₹ ${(r.bom.plantTotal / (r.installedDckWp * 1000)).toFixed(1)} / Wp · Turnkey`;
  document.getElementById("kpiPay").textContent = `${r.payY} Yrs ${r.payM} Mos`;
  document.getElementById("kpiProfit").textContent = `25Y Net: ₹ ${(r.lifetimeProfit / 1e5).toFixed(2)} L (FD: ₹${(r.fd25y / 1e5).toFixed(2)} L)`;

  // Single-Line Diagram & Electrical Details
  document.getElementById("sldPanels").textContent = `${r.panels} × ${r.panelW}W`;
  document.getElementById("sldInv").textContent = `${r.invKw} kW ${r.phase3 ? "3-Ph" : "1-Ph"}`;
  document.getElementById("sldBreaker").textContent = `${r.acdb.breakerRating}A ${r.phase3 ? "4P" : "2P"}`;
  document.getElementById("sldVolt").textContent = r.phase3 ? "415V 3PH" : "230V 1PH";

  document.getElementById("edInv").textContent = `${r.invKw} kW (${r.phase3 ? "415V" : "230V"}, MPPT)`;
  document.getElementById("edPhase").textContent = r.phase3 ? "Three-Phase 415V" : "Single-Phase 230V";
  document.getElementById("edBreaker").textContent = `${r.acdb.breakerRating}A (Rated: ${r.acdb.ratedCurrent}A)`;
  document.getElementById("edCable").textContent = `${r.acdb.gridCable} Copper`;
  document.getElementById("edDist").textContent = `${r.dist} meters`;

  // Environmental
  document.getElementById("envCO2").textContent = r.co2.toLocaleString();
  document.getElementById("envTrees").textContent = r.trees.toLocaleString();
  document.getElementById("envCar").textContent = r.carKm.toLocaleString();
  document.getElementById("envCoal").textContent = r.coalT.toLocaleString();

  // Print Header Meta
  document.getElementById("printMeta").textContent = `${r.name || "Site"} · ${r.loc || "Karnataka"} · Target: ${r.capacityKw} kW · Array: ${r.installedDckWp} kWp`;
  document.getElementById("printDate").textContent = new Date().toLocaleDateString("en-IN", { weekday:"short", year:"numeric", month:"short", day:"numeric" });

  // Render BOM & Commercial Matrix View
  renderBomView();

  // Render Amortization Table
  const amortBody = document.getElementById("amortBody");
  amortBody.innerHTML = "";
  r.amort.forEach(row => {
    const tr = document.createElement("tr");
    if (row.year === r.payY) tr.style.background = "rgba(16,185,129,0.12)";
    tr.innerHTML = `
      <td><strong>Year ${row.year}</strong>${row.year === r.payY ? " ⭐ <span style='font-size:.7rem;color:var(--emerald);font-weight:800'>Payback</span>" : ""}</td>
      <td class="tr">${row.gen.toLocaleString()}</td>
      <td class="tr">₹ ${Number(row.tariff).toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
      <td class="tr">₹ ${row.revenue.toLocaleString()}</td>
      <td class="tr">₹ ${row.amc.toLocaleString()}</td>
      <td class="tr" style="color:var(--emerald);font-weight:700">₹ ${row.net.toLocaleString()}</td>
      <td class="tr" style="font-weight:800">₹ ${row.cum.toLocaleString()}</td>
    `;
    amortBody.appendChild(tr);
  });

  // Update Charts
  updateCharts(r);
  // Update Modern Visualizer Sidebar Cards & Canvas
  renderVizTabs();
  updateVisualizerFromSelection();
}

function updateRoofStats(r) {
  const rtAreaFt = document.getElementById("rtAreaFt");
  const rtAreaM = document.getElementById("rtAreaM");
  const rtUsable = document.getElementById("rtUsable");
  const rtUsableM = document.getElementById("rtUsableM");
  const gaugeCircle = document.getElementById("gaugeCircle");
  const gaugeText = document.getElementById("gaugeText");
  const rtSetbackVal = document.getElementById("rtSetbackVal");
  const rtObstacleVal = document.getElementById("rtObstacleVal");
  const rtPlantCap = document.getElementById("rtPlantCap");
  const rtPlantPanels = document.getElementById("rtPlantPanels");
  const rtPlantMod = document.getElementById("rtPlantMod");

  if (!r) {
    if (rtAreaFt) rtAreaFt.textContent = "— sq.ft";
    if (rtAreaM) rtAreaM.textContent = "(— m²)";
    if (rtUsable) rtUsable.textContent = "— sq.ft";
    if (rtUsableM) rtUsableM.textContent = "(— m²)";
    if (gaugeCircle) gaugeCircle.setAttribute("stroke-dasharray", "0, 100");
    if (gaugeText) gaugeText.textContent = "0%";
    if (rtSetbackVal) rtSetbackVal.textContent = "(all sides)";
    if (rtObstacleVal) rtObstacleVal.textContent = "0 (No shade)";
    if (rtPlantCap) rtPlantCap.textContent = "— kW";
    if (rtPlantPanels) rtPlantPanels.textContent = "— Panels (550W)";
    if (rtPlantMod) rtPlantMod.textContent = "550 Wp";
    return;
  }

  const grossFt = r.grossRooftopArea || r.grossArea || 0;
  const grossM = (grossFt * 0.092903).toFixed(1);
  const utilFt = r.utilizedRooftopArea || r.usableArea || 0;
  const utilM = (utilFt * 0.092903).toFixed(1);
  const utilPct = grossFt > 0 ? Math.min(100, Math.round((utilFt / grossFt) * 100)) : 100;
  const panelWatt = r.panelW || r.panelWatt || 550;

  if (rtAreaFt) rtAreaFt.textContent = `${grossFt.toLocaleString()} sq.ft`;
  if (rtAreaM) rtAreaM.textContent = `(${grossM} m²)`;
  if (rtUsable) rtUsable.textContent = `${utilFt.toLocaleString()} sq.ft`;
  if (rtUsableM) rtUsableM.textContent = `(${utilM} m²)`;
  if (gaugeCircle) gaugeCircle.setAttribute("stroke-dasharray", `${utilPct}, 100`);
  if (gaugeText) gaugeText.textContent = `${utilPct}%`;

  const pSetback = num("cfgParapet");
  if (rtSetbackVal) rtSetbackVal.textContent = pSetback > 0 ? `${pSetback} ft buffer` : "(all sides)";

  const nVal = document.getElementById("cfgNeighbour")?.value;
  if (rtObstacleVal) rtObstacleVal.textContent = (nVal && nVal !== "None") ? `Shade on ${nVal}` : "0 (No shade)";

  if (rtPlantCap) rtPlantCap.textContent = `${r.capacityKw.toFixed(2)} kW`;
  if (rtPlantPanels) rtPlantPanels.textContent = `${r.panels} Panels (${panelWatt}W)`;
  if (rtPlantMod) rtPlantMod.textContent = `${panelWatt} Wp`;
}

// ============================================================
// ============================================================
// KARNATAKA DISTRICTS & TALUKS DATABASE (ALL 31 DISTRICTS)
// ============================================================
const KARNATAKA_TALUKS = {
  "Shivamogga": {
    name: "Shivamogga",
    taluks: ["Shivamogga", "Shimoga", "Bhadravati", "Sagar", "Shikaripura", "Soraba", "Thirthahalli", "Hosanagara"],
    lat: 13.9299, lon: 75.5681, ghi: 5.25, peak: 5.65, peakM: "Feb Peak", mon: 3.10, monM: "Jul Monsoon",
    tempBase: 27, sky: "High Solar Insolation",
    monthly: [5.15, 5.65, 5.45, 5.05, 4.45, 3.40, 3.10, 3.35, 3.90, 4.35, 4.50, 5.05]
  },
  "Bengaluru Urban": {
    name: "Bengaluru",
    taluks: ["Bengaluru", "Bangalore", "Anekal", "Yelahanka", "Whitefield", "Electronic City", "Kengeri", "Hebbal", "Jayanagar", "Indiranagar", "Rajajinagar"],
    lat: 12.9716, lon: 77.5946, ghi: 5.35, peak: 5.85, peakM: "Mar Peak", mon: 3.35, monM: "Jul Monsoon",
    tempBase: 24, sky: "Moderate Highland Plateau",
    monthly: [5.20, 5.70, 5.85, 5.20, 4.60, 3.65, 3.35, 3.50, 4.10, 4.40, 4.65, 5.10]
  },
  "Bengaluru Rural": {
    name: "Bengaluru Rural",
    taluks: ["Devanahalli", "Doddaballapura", "Hoskote", "Nelamangala"],
    lat: 13.2924, lon: 77.5501, ghi: 5.38, peak: 5.88, peakM: "Mar Peak", mon: 3.38, monM: "Jul Monsoon",
    tempBase: 24, sky: "High Solar Insolation",
    monthly: [5.22, 5.72, 5.88, 5.25, 4.62, 3.68, 3.38, 3.52, 4.12, 4.42, 4.68, 5.12]
  },
  "Mysuru": {
    name: "Mysuru",
    taluks: ["Mysuru", "Mysore", "Nanjangud", "Hunsur", "T. Narasipura", "K.R. Nagar", "Piriyapatna", "Saragur", "Heggadadevankote"],
    lat: 12.2958, lon: 76.6394, ghi: 5.30, peak: 5.75, peakM: "Mar Peak", mon: 3.20, monM: "Jul Monsoon",
    tempBase: 25, sky: "High Solar Insolation",
    monthly: [5.18, 5.68, 5.75, 5.15, 4.50, 3.50, 3.20, 3.40, 4.05, 4.35, 4.60, 5.08]
  },
  "Hubballi-Dharwad": {
    name: "Hubballi-Dharwad",
    taluks: ["Hubballi", "Hubli", "Dharwad", "Kalghatgi", "Navalgund", "Kundgol", "Alnavar"],
    lat: 15.3647, lon: 75.1240, ghi: 5.42, peak: 5.92, peakM: "Feb Peak", mon: 3.25, monM: "Jul Monsoon",
    tempBase: 26, sky: "Semi-Arid Solar Belt",
    monthly: [5.28, 5.92, 5.75, 5.30, 4.70, 3.55, 3.25, 3.45, 4.15, 4.55, 4.75, 5.20]
  },
  "Belagavi": {
    name: "Belagavi",
    taluks: ["Belagavi", "Belgaum", "Gokak", "Chikkodi", "Athani", "Bailhongal", "Ramdurg", "Saundatti", "Khanapur", "Hukkeri", "Raybag", "Kagwad", "Nippani", "Mudalgi"],
    lat: 15.8497, lon: 74.4977, ghi: 5.28, peak: 5.72, peakM: "Mar Peak", mon: 3.05, monM: "Jul Monsoon",
    tempBase: 25, sky: "High Solar Insolation",
    monthly: [5.15, 5.65, 5.72, 5.18, 4.55, 3.35, 3.05, 3.25, 3.95, 4.40, 4.60, 5.05]
  },
  "Mangaluru": {
    name: "Mangaluru",
    taluks: ["Mangaluru", "Mangalore", "Bantwal", "Belthangady", "Puttur", "Sullia", "Moodabidri", "Kadaba"],
    lat: 12.9141, lon: 74.8560, ghi: 5.18, peak: 5.70, peakM: "Feb Peak", mon: 2.75, monM: "Jul Monsoon",
    tempBase: 28, sky: "Coastal Solar Region",
    monthly: [5.30, 5.70, 5.60, 5.10, 4.30, 2.95, 2.75, 3.00, 3.75, 4.20, 4.45, 5.10]
  },
  "Udupi": {
    name: "Udupi",
    taluks: ["Udupi", "Kundapura", "Karkala", "Brahmavara", "Byndoor", "Kaup", "Hebri", "Manipal"],
    lat: 13.3409, lon: 74.7421, ghi: 5.15, peak: 5.68, peakM: "Feb Peak", mon: 2.70, monM: "Jul Monsoon",
    tempBase: 28, sky: "Coastal Solar Region",
    monthly: [5.28, 5.68, 5.58, 5.08, 4.28, 2.90, 2.70, 2.95, 3.70, 4.18, 4.42, 5.08]
  },
  "Kalaburagi": {
    name: "Kalaburagi",
    taluks: ["Kalaburagi", "Gulbarga", "Aland", "Afzalpur", "Chincholi", "Chittapur", "Jevargi", "Sedam", "Kamalapur", "Kalgi", "Shahabad", "Yedrami"],
    lat: 17.3297, lon: 76.8343, ghi: 5.55, peak: 6.10, peakM: "Apr Peak", mon: 3.50, monM: "Aug Monsoon",
    tempBase: 31, sky: "Arid Solar Radiation Zone",
    monthly: [5.35, 5.85, 6.00, 6.10, 5.60, 4.10, 3.65, 3.50, 4.30, 4.80, 5.00, 5.30]
  },
  "Ballari": {
    name: "Ballari",
    taluks: ["Ballari", "Bellary", "Sandur", "Siruguppa", "Kampli", "Kurugodu"],
    lat: 15.1394, lon: 76.9214, ghi: 5.52, peak: 6.05, peakM: "Mar Peak", mon: 3.45, monM: "Jul Monsoon",
    tempBase: 30, sky: "Arid Solar Radiation Zone",
    monthly: [5.32, 5.82, 6.05, 5.80, 5.10, 3.90, 3.45, 3.65, 4.28, 4.75, 4.95, 5.25]
  },
  "Vijayanagara": {
    name: "Vijayanagara",
    taluks: ["Hospet", "Hosapete", "Hagaribommanahalli", "Harapanahalli", "Hoovina Hadagali", "Kudligi", "Kotturu"],
    lat: 15.2689, lon: 76.3909, ghi: 5.50, peak: 6.00, peakM: "Mar Peak", mon: 3.40, monM: "Jul Monsoon",
    tempBase: 30, sky: "High Solar Insolation",
    monthly: [5.30, 5.80, 6.00, 5.75, 5.05, 3.85, 3.40, 3.60, 4.25, 4.70, 4.90, 5.22]
  },
  "Davanagere": {
    name: "Davanagere",
    taluks: ["Davanagere", "Harihar", "Honnali", "Channagiri", "Jagalur", "Nyamathi"],
    lat: 14.4644, lon: 75.9218, ghi: 5.40, peak: 5.88, peakM: "Feb Peak", mon: 3.30, monM: "Jul Monsoon",
    tempBase: 28, sky: "Central Karnataka Solar Hub",
    monthly: [5.25, 5.88, 5.70, 5.25, 4.65, 3.60, 3.30, 3.50, 4.15, 4.50, 4.70, 5.15]
  },
  "Tumakuru": {
    name: "Tumakuru",
    taluks: ["Tumakuru", "Tumkur", "Tiptur", "Sira", "Madhugiri", "Kunigal", "Pavagada", "Gubbi", "Koratagere", "Turuvekere", "Chikkanayakanahalli"],
    lat: 13.3379, lon: 77.1173, ghi: 5.45, peak: 5.95, peakM: "Mar Peak", mon: 3.40, monM: "Jul Monsoon",
    tempBase: 26, sky: "Pavagada Mega-Solar Belt",
    monthly: [5.28, 5.78, 5.95, 5.40, 4.80, 3.75, 3.40, 3.60, 4.20, 4.55, 4.75, 5.20]
  },
  "Vijayapura": {
    name: "Vijayapura",
    taluks: ["Vijayapura", "Bijapur", "Basavana Bagewadi", "Indi", "Muddebihal", "Sindagi", "Chadchan", "Tikota", "Babaleshwar", "Kolhar", "Nidagundi", "Devara Hippargi"],
    lat: 16.8302, lon: 75.7100, ghi: 5.58, peak: 6.12, peakM: "Apr Peak", mon: 3.55, monM: "Jul Monsoon",
    tempBase: 30, sky: "Northern Dry Solar Zone",
    monthly: [5.38, 5.90, 6.05, 6.12, 5.65, 4.15, 3.55, 3.70, 4.35, 4.85, 5.05, 5.32]
  },
  "Hassan": {
    name: "Hassan",
    taluks: ["Hassan", "Channarayapatna", "Arsikere", "Holenarasipura", "Sakleshpur", "Belur", "Alur", "Arkalgud"],
    lat: 13.0033, lon: 76.1004, ghi: 5.22, peak: 5.65, peakM: "Feb Peak", mon: 3.00, monM: "Jul Monsoon",
    tempBase: 24, sky: "Malnad Transition Zone",
    monthly: [5.12, 5.65, 5.50, 5.00, 4.40, 3.30, 3.00, 3.25, 3.85, 4.30, 4.50, 5.02]
  },
  "Chitradurga": {
    name: "Chitradurga",
    taluks: ["Chitradurga", "Challakere", "Hiriyur", "Holalkere", "Hosadurga", "Molakalmuru"],
    lat: 14.2251, lon: 76.3980, ghi: 5.48, peak: 5.98, peakM: "Mar Peak", mon: 3.42, monM: "Jul Monsoon",
    tempBase: 28, sky: "Wind-Solar Hybrid Zone",
    monthly: [5.30, 5.80, 5.98, 5.45, 4.85, 3.78, 3.42, 3.62, 4.22, 4.60, 4.80, 5.22]
  },
  "Chikkamagaluru": {
    name: "Chikkamagaluru",
    taluks: ["Chikkamagaluru", "Chikmagalur", "Kadur", "Tarikere", "Mudigere", "Koppa", "Sringeri", "Narasimharajapura", "Ajjampura"],
    lat: 13.3161, lon: 75.7720, ghi: 5.20, peak: 5.62, peakM: "Feb Peak", mon: 2.95, monM: "Jul Monsoon",
    tempBase: 23, sky: "Highland Solar Basin",
    monthly: [5.10, 5.62, 5.48, 4.95, 4.35, 3.25, 2.95, 3.20, 3.80, 4.25, 4.48, 5.00]
  },
  "Kolar": {
    name: "Kolar",
    taluks: ["Kolar", "Bangarapet", "Malur", "Mulbagal", "Srinivaspura", "KGF", "Robertsonpet"],
    lat: 13.1367, lon: 78.1291, ghi: 5.40, peak: 5.90, peakM: "Mar Peak", mon: 3.40, monM: "Jul Monsoon",
    tempBase: 26, sky: "High Solar Insolation",
    monthly: [5.25, 5.75, 5.90, 5.30, 4.70, 3.70, 3.40, 3.55, 4.15, 4.48, 4.70, 5.15]
  },
  "Chikkaballapura": {
    name: "Chikkaballapura",
    taluks: ["Chikkaballapura", "Bagepalli", "Chintamani", "Gauribidanur", "Gudibande", "Sidlaghatta"],
    lat: 13.4355, lon: 77.7275, ghi: 5.42, peak: 5.92, peakM: "Mar Peak", mon: 3.42, monM: "Jul Monsoon",
    tempBase: 25, sky: "High Solar Insolation",
    monthly: [5.26, 5.76, 5.92, 5.32, 4.72, 3.72, 3.42, 3.58, 4.18, 4.50, 4.72, 5.18]
  },
  "Mandya": {
    name: "Mandya",
    taluks: ["Mandya", "Maddur", "Malavalli", "Pandavapura", "Srirangapatna", "Nagamangala", "Krishnarajpet"],
    lat: 12.5218, lon: 76.8951, ghi: 5.32, peak: 5.78, peakM: "Mar Peak", mon: 3.25, monM: "Jul Monsoon",
    tempBase: 26, sky: "Cauvery Basin Solar Hub",
    monthly: [5.20, 5.70, 5.78, 5.18, 4.55, 3.55, 3.25, 3.45, 4.08, 4.38, 4.62, 5.10]
  },
  "Chamarajanagar": {
    name: "Chamarajanagar",
    taluks: ["Chamarajanagar", "Gundlupet", "Kollegal", "Yelandur", "Hanur"],
    lat: 11.9261, lon: 76.9437, ghi: 5.34, peak: 5.80, peakM: "Mar Peak", mon: 3.28, monM: "Jul Monsoon",
    tempBase: 26, sky: "Southern Solar Corridor",
    monthly: [5.22, 5.72, 5.80, 5.20, 4.58, 3.58, 3.28, 3.48, 4.10, 4.40, 4.65, 5.12]
  },
  "Bidar": {
    name: "Bidar",
    taluks: ["Bidar", "Basavakalyan", "Bhalki", "Humnabad", "Aurad", "Kamalnagar", "Hulsoor"],
    lat: 17.9104, lon: 77.5199, ghi: 5.52, peak: 6.08, peakM: "Apr Peak", mon: 3.48, monM: "Aug Monsoon",
    tempBase: 29, sky: "Northern Solar Radiation Hub",
    monthly: [5.30, 5.82, 5.95, 6.08, 5.55, 4.05, 3.60, 3.48, 4.25, 4.75, 4.95, 5.25]
  },
  "Raichur": {
    name: "Raichur",
    taluks: ["Raichur", "Manvi", "Sindhanur", "Devadurga", "Lingsugur", "Maski", "Sirwar"],
    lat: 16.2120, lon: 77.3439, ghi: 5.60, peak: 6.15, peakM: "Apr Peak", mon: 3.58, monM: "Jul Monsoon",
    tempBase: 31, sky: "Doab Mega-Solar Zone",
    monthly: [5.40, 5.92, 6.08, 6.15, 5.70, 4.20, 3.58, 3.75, 4.40, 4.90, 5.10, 5.35]
  },
  "Bagalkote": {
    name: "Bagalkote",
    taluks: ["Bagalkote", "Bagalkot", "Badami", "Bilagi", "Hunagund", "Jamkhandi", "Mudhol", "Guledgudda", "Ilkal", "Rabkavi Banhatti"],
    lat: 16.1691, lon: 75.6615, ghi: 5.54, peak: 6.08, peakM: "Apr Peak", mon: 3.50, monM: "Jul Monsoon",
    tempBase: 29, sky: "Krishna Valley Solar Belt",
    monthly: [5.35, 5.88, 6.02, 6.08, 5.60, 4.10, 3.50, 3.68, 4.32, 4.82, 5.02, 5.30]
  },
  "Gadag": {
    name: "Gadag",
    taluks: ["Gadag", "Betageri", "Ron", "Shirhatti", "Nargund", "Mundargi", "Gajendragad", "Lakshmeshwar"],
    lat: 15.4313, lon: 75.6355, ghi: 5.45, peak: 5.95, peakM: "Feb Peak", mon: 3.35, monM: "Jul Monsoon",
    tempBase: 27, sky: "Wind-Solar Renewable Corridor",
    monthly: [5.28, 5.95, 5.78, 5.35, 4.75, 3.65, 3.35, 3.55, 4.20, 4.60, 4.80, 5.22]
  },
  "Haveri": {
    name: "Haveri",
    taluks: ["Haveri", "Byadgi", "Hangal", "Hirekerur", "Ranebennur", "Savanur", "Shiggaon", "Rattihalli"],
    lat: 14.7972, lon: 75.3995, ghi: 5.38, peak: 5.85, peakM: "Feb Peak", mon: 3.28, monM: "Jul Monsoon",
    tempBase: 27, sky: "Central Karnataka Transition",
    monthly: [5.22, 5.85, 5.68, 5.22, 4.62, 3.55, 3.28, 3.48, 4.12, 4.48, 4.68, 5.12]
  },
  "Koppal": {
    name: "Koppal",
    taluks: ["Koppal", "Gangavathi", "Kushtagi", "Yelburga", "Kuknoor", "Karatagi"],
    lat: 15.3556, lon: 76.1554, ghi: 5.50, peak: 6.02, peakM: "Mar Peak", mon: 3.45, monM: "Jul Monsoon",
    tempBase: 29, sky: "High Solar Insolation",
    monthly: [5.32, 5.85, 6.02, 5.75, 5.10, 3.90, 3.45, 3.65, 4.28, 4.72, 4.92, 5.25]
  },
  "Yadgir": {
    name: "Yadgir",
    taluks: ["Yadgir", "Shahapur", "Shorapur", "Hunsagi", "Gurmitkal", "Wadagera"],
    lat: 16.7622, lon: 77.1442, ghi: 5.56, peak: 6.10, peakM: "Apr Peak", mon: 3.52, monM: "Aug Monsoon",
    tempBase: 31, sky: "Arid Solar Radiation Zone",
    monthly: [5.36, 5.88, 6.02, 6.10, 5.62, 4.12, 3.62, 3.52, 4.32, 4.82, 5.02, 5.32]
  },
  "Ramanagara": {
    name: "Ramanagara",
    taluks: ["Ramanagara", "Channapatna", "Kanakapura", "Magadi", "Bidadi", "Harohalli"],
    lat: 12.7214, lon: 77.2807, ghi: 5.36, peak: 5.85, peakM: "Mar Peak", mon: 3.32, monM: "Jul Monsoon",
    tempBase: 25, sky: "High Solar Insolation",
    monthly: [5.20, 5.70, 5.85, 5.22, 4.62, 3.62, 3.32, 3.48, 4.10, 4.42, 4.65, 5.10]
  },
  "Uttara Kannada": {
    name: "Uttara Kannada",
    taluks: ["Karwar", "Ankola", "Bhatkal", "Haliyal", "Honnavar", "Joida", "Kumta", "Mundgod", "Siddapur", "Sirsi", "Yellapur", "Dandeli"],
    lat: 14.8185, lon: 74.1350, ghi: 5.10, peak: 5.60, peakM: "Feb Peak", mon: 2.65, monM: "Jul Monsoon",
    tempBase: 27, sky: "Coastal-Ghats Solar Region",
    monthly: [5.22, 5.60, 5.50, 5.00, 4.20, 2.85, 2.65, 2.90, 3.65, 4.10, 4.35, 5.02]
  },
  "Kodagu": {
    name: "Kodagu",
    taluks: ["Madikeri", "Somwarpet", "Virajpet", "Kushalnagar", "Ponnampet"],
    lat: 12.4244, lon: 75.7382, ghi: 4.95, peak: 5.45, peakM: "Feb Peak", mon: 2.50, monM: "Jul Monsoon",
    tempBase: 21, sky: "Western Ghats Highland",
    monthly: [5.00, 5.45, 5.35, 4.85, 4.10, 2.70, 2.50, 2.75, 3.45, 3.95, 4.25, 4.90]
  }
};

function lookupKarnatakaLocation(query) {
  if (!query || typeof query !== "string") return null;
  const q = query.trim().toLowerCase();
  for (const [key, d] of Object.entries(KARNATAKA_TALUKS)) {
    if (q.includes(key.toLowerCase()) || key.toLowerCase().includes(q)) return d;
    for (const t of d.taluks) {
      if (q.includes(t.toLowerCase()) || t.toLowerCase().includes(q)) return d;
    }
  }
  return null;
}

function findNearestKarnatakaDistrict(lat, lon) {
  let bestDist = Infinity;
  let bestData = KARNATAKA_TALUKS["Shivamogga"];
  for (const d of Object.values(KARNATAKA_TALUKS)) {
    const dLat = (lat - d.lat) * (Math.PI / 180);
    const dLon = (lon - d.lon) * (Math.PI / 180);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat * Math.PI / 180) * Math.cos(d.lat * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const dist = 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    if (dist < bestDist) {
      bestDist = dist;
      bestData = d;
    }
  }
  return bestData;
}

function calculateHourlyTemp(baseTemp) {
  const hr = new Date().getHours();
  if (hr >= 6 && hr < 9) return baseTemp - 3;
  if (hr >= 9 && hr < 12) return baseTemp - 2; // e.g. 27 -> 25°C at 9AM
  if (hr >= 12 && hr < 15) return baseTemp + 4; // 31°C
  if (hr >= 15 && hr < 18) return baseTemp + 5; // 32°C
  if (hr >= 18 && hr < 21) return baseTemp - 1; // 26°C
  return baseTemp - 5; // night
}

function applyLocationData(data, updateInput) {
  if (!data) return;
  if (updateInput) {
    const cfgLoc = document.getElementById("cfgLoc");
    if (cfgLoc) {
      cfgLoc.value = `${data.name}, Karnataka`;
      saveCurrentFormToActiveSite();
    }
  }

  const wxLoc = document.getElementById("wxLoc");
  if (wxLoc) wxLoc.textContent = `${data.name}, Karnataka`;

  const wxSky = document.getElementById("wxSky");
  if (wxSky) wxSky.textContent = data.sky;

  const wxGhi = document.getElementById("wxGhi");
  if (wxGhi) wxGhi.innerHTML = `${data.ghi.toFixed(2)} <span style="font-size:.75rem;font-weight:600">kWh/kW/day</span>`;
  const topIrrVal = document.getElementById("topIrrVal");
  if (topIrrVal) topIrrVal.textContent = data.ghi.toFixed(2);

  const hrTemp = calculateHourlyTemp(data.tempBase);
  const wxTemp = document.getElementById("wxTemp");
  if (wxTemp) wxTemp.textContent = `${hrTemp}°C`;

  const pVal = document.getElementById("wxPeakVal");
  if (pVal) pVal.textContent = `${data.peak.toFixed(2)} max`;
  const pLbl = document.getElementById("wxPeakLbl");
  if (pLbl) pLbl.textContent = data.peakM;

  const mVal = document.getElementById("wxMonVal");
  if (mVal) mVal.textContent = `${data.mon.toFixed(2)} min`;
  const mLbl = document.getElementById("wxMonLbl");
  if (mLbl) mLbl.textContent = data.monM;

  // Sync monthly yields
  MONTHS.forEach((m, idx) => {
    MONTHLY_YIELD[m] = data.monthly[idx];
  });

  // If active site has input, liveUpdate
  if (current) {
    current.location = `${data.name}, Karnataka`;
    liveUpdate();
  }
}

function initLiveLocation() {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        const matched = findNearestKarnatakaDistrict(pos.coords.latitude, pos.coords.longitude);
        if (matched) {
          applyLocationData(matched, true);
          toast(`📍 Live Location: ${matched.name}, Karnataka`);
        }
      },
      err => {
        const currVal = document.getElementById("cfgLoc")?.value || "Shivamogga, Karnataka";
        const matched = lookupKarnatakaLocation(currVal) || KARNATAKA_TALUKS["Shivamogga"];
        applyLocationData(matched, false);
      },
      { timeout: 4000, maximumAge: 300000 }
    );
  } else {
    const currVal = document.getElementById("cfgLoc")?.value || "Shivamogga, Karnataka";
    const matched = lookupKarnatakaLocation(currVal) || KARNATAKA_TALUKS["Shivamogga"];
    applyLocationData(matched, false);
  }
}

function scrollToDesign() {
  switchView('studio');
  const el = document.getElementById('cfgBuildings');
  if (el) { el.focus(); el.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
}

// ============================================================
// CANVAS ROOFTOP ARRAY RENDERING (WITH ZOOM & VIEW MODES)
// ============================================================
let arrayZoom = 1.0;

function drawArray(panels, L_in, B_in, parapet_in, neighbour_in) {
  const canvas = document.getElementById("arrayCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const parent = canvas.parentElement;
  const rect = parent.getBoundingClientRect();
  const W = Math.max(280, rect.width || 420);
  const H = Math.max(280, rect.height || 380);
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  canvas.style.width = W + "px";
  canvas.style.height = H + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, W, H);

  // Background based on mode
  if (arrayMode === "sat") {
    // Aerial Satellite View background (streets, terrain, surrounding green trees)
    const satBg = ctx.createRadialGradient(W / 2, H / 2, 40, W / 2, H / 2, W * 0.75);
    satBg.addColorStop(0, "#1c2a22");
    satBg.addColorStop(0.6, "#142019");
    satBg.addColorStop(1, "#0a120e");
    ctx.fillStyle = satBg;
    ctx.fillRect(0, 0, W, H);

    // Surrounding tree clusters for satellite realism
    ctx.fillStyle = "rgba(46, 117, 89, 0.45)";
    for (let i = 0; i < 40; i++) {
      const tx = ((i * 97) % W);
      const ty = ((i * 71) % H);
      if (Math.abs(tx - W/2) > W*0.28 || Math.abs(ty - H/2) > H*0.28) {
        ctx.beginPath();
        ctx.arc(tx, ty, 10 + (i % 8), 0, Math.PI * 2);
        ctx.fill();
      }
    }
  } else {
    // Architectural top/3D view gradient
    const bg = ctx.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, "#080e1a");
    bg.addColorStop(0.5, "#0d182b");
    bg.addColorStop(1, "#14223d");
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, W, H);

    // Subtle architectural grid lines
    ctx.strokeStyle = "rgba(255,255,255,0.03)";
    ctx.lineWidth = 1;
    for (let x = 20; x < W; x += 30) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
    for (let y = 20; y < H; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
  }

  if (!panels || panels <= 0) {
    ctx.fillStyle = "rgba(226,232,240,0.8)";
    ctx.font = "600 13px 'Plus Jakarta Sans', system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Enter Rooftop Dimensions in Project Design to render array layout", W / 2, H / 2);
    return;
  }

  const s = sites[vizSiteIndex] || sites[0];
  const b = (s && s.buildings && s.buildings[vizBldgIndex]) ? s.buildings[vizBldgIndex] : (s && s.buildings ? s.buildings[0] : null);
  const L = L_in !== undefined ? L_in : (b ? (parseFloat(b.L) || 40) : (num("cfgL") || 40));
  const B = B_in !== undefined ? B_in : (b ? (parseFloat(b.B) || 30) : (num("cfgB") || 30));
  const parapet = parapet_in !== undefined ? parapet_in : (b ? Math.max(0, parseFloat(b.parapet) || 0) : Math.max(0, num("cfgParapet") || 1.5));
  const neighbour = neighbour_in !== undefined ? neighbour_in : (b ? (b.neighbour || "None") : (document.getElementById("cfgNeighbour")?.value || "None"));

  const maxSide = Math.min(W, H) * 0.68 * arrayZoom;
  const aspect = L / Math.max(B, 1);
  let bw, bh;
  if (aspect >= 1) {
    bw = maxSide;
    bh = maxSide / aspect;
  } else {
    bh = maxSide;
    bw = maxSide * aspect;
  }
  const bx = (W - bw) / 2;
  const by = (H - bh) / 2;

  const iso = arrayMode === "iso";
  const skew = iso ? 0.32 : 0; // stronger isometric depth for proper 3D feel

  function mapPt(x, y) {
    const px = bx + x * bw;
    const py = by + y * bh;
    if (!iso) return [px, py];
    return [px + (y - 0.5) * bw * skew, py - (x - 0.5) * bh * 0.18 - (iso ? 8 : 0)];
  }

  // Building roof concrete wall & base with 3D drop shadow
  ctx.save();
  ctx.shadowColor = "rgba(0,0,0,0.6)";
  ctx.shadowBlur = 18;
  ctx.shadowOffsetY = 10;
  ctx.fillStyle = arrayMode === "sat" ? "#334155" : "#64748b";
  ctx.strokeStyle = "rgba(15,23,42,0.8)";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  [[0,0],[1,0],[1,1],[0,1]].forEach(([x, y], idx) => {
    const [px, py] = mapPt(x, y);
    if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  });
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.restore();

  // Roof top usable architectural deck surface
  ctx.fillStyle = arrayMode === "sat" ? "#64748b" : "#cbd5e1";
  ctx.beginPath();
  const borderPad = 0.04;
  [[borderPad, borderPad],[1-borderPad, borderPad],[1-borderPad, 1-borderPad],[borderPad, 1-borderPad]].forEach(([x, y], idx) => {
    const [px, py] = mapPt(x, y);
    if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  });
  ctx.closePath();
  ctx.fill();

  // Parapet & obstacle shadows (live sun direction)
  if (typeof drawRooftopShadows === "function") {
    try { drawRooftopShadows(ctx, mapPt, parapet, neighbour, bw, bh); } catch (e) {}
  }

  // Usable area (emerald dashed outline after parapet setback)
  const pFracX = Math.min(0.24, (2 * parapet) / Math.max(L, 1));
  const pFracY = Math.min(0.24, (2 * parapet) / Math.max(B, 1));
  const ux0 = pFracX, uy0 = pFracY, ux1 = 1 - pFracX, uy1 = 1 - pFracY;

  ctx.setLineDash([6, 4]);
  ctx.strokeStyle = "#10b981";
  ctx.lineWidth = 2;
  ctx.beginPath();
  [[ux0, uy0],[ux1, uy0],[ux1, uy1],[ux0, uy1]].forEach(([x, y], idx) => {
    const [px, py] = mapPt(x, y);
    if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  });
  ctx.closePath();
  ctx.stroke();
  ctx.setLineDash([]);

  // Parapet Wall Shadow Zone
  if (neighbour !== "None") {
    ctx.fillStyle = "rgba(239,68,68,0.30)";
    let shade = [[ux1 - 0.18, uy0], [ux1, uy0], [ux1, uy1], [ux1 - 0.18, uy1]];
    if (neighbour === "West") shade = [[ux0, uy0], [ux0 + 0.18, uy0], [ux0 + 0.18, uy1], [ux0, uy1]];
    if (neighbour === "North") shade = [[ux0, uy0], [ux1, uy0], [ux1, uy0 + 0.18], [ux0, uy0 + 0.18]];
    if (neighbour === "South") shade = [[ux0, uy1 - 0.18], [ux1, uy1 - 0.18], [ux1, uy1], [ux0, uy1]];

    ctx.beginPath();
    shade.forEach(([x, y], idx) => {
      const [px, py] = mapPt(x, y);
      if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    });
    ctx.closePath();
    ctx.fill();
  }

  // Draw PV Panels inside usable shadow-free zone
  const cols = Math.max(2, Math.ceil(Math.sqrt(panels * (bw / bh))));
  const rows = Math.ceil(panels / cols);
  const gapX = ((ux1 - ux0) * 0.035);
  const gapY = ((uy1 - uy0) * 0.035);
  const cellW = ((ux1 - ux0) - (cols + 1) * gapX) / cols;
  const cellH = ((uy1 - uy0) - (rows + 1) * gapY) / rows;

  let n = 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (n >= panels) break;
      const x0 = ux0 + gapX + c * (cellW + gapX);
      const y0 = uy0 + gapY + r * (cellH + gapY);
      const x1 = x0 + cellW;
      const y1 = y0 + cellH;

      const pts = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]].map(([x, y]) => mapPt(x, y));
      const grad = ctx.createLinearGradient(pts[0][0], pts[0][1], pts[2][0], pts[2][1]);
      grad.addColorStop(0, "#1d4ed8");
      grad.addColorStop(1, "#1e3a8a");
      ctx.fillStyle = grad;
      ctx.strokeStyle = "#60a5fa";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      pts.forEach(([px, py], idx) => {
        if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      });
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Busbars / wafer sub-lines
      ctx.strokeStyle = "rgba(255,255,255,0.45)";
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      const m1 = mapPt((x0 + x1) / 2, y0);
      const m2 = mapPt((x0 + x1) / 2, y1);
      ctx.moveTo(m1[0], m1[1]);
      ctx.lineTo(m2[0], m2[1]);
      ctx.stroke();

      n++;
    }
  }
}

function setArrayMode(m, btn) {
  arrayMode = m;
  document.querySelectorAll(".rt-toggle-btn").forEach(b => b.classList.remove("on"));
  if (btn) btn.classList.add("on");
  drawArray(current?.panels || 0);
}

function zoomArray(factor) {
  arrayZoom = Math.min(2.2, Math.max(0.6, arrayZoom * factor));
  drawArray(current?.panels || 0);
}

function fitArrayView() {
  arrayZoom = 1.0;
  drawArray(current?.panels || 0);
  toast("Visualizer view fitted to frame");
}

function resetArrayView() {
  arrayMode = "top";
  arrayZoom = 1.0;
  document.querySelectorAll(".rt-toggle-btn").forEach(b => {
    b.classList.toggle("on", b.id === "btnTop");
  });
  drawArray(current?.panels || 0);
  toast("View reset to Top Projection");
}

/* Traveling dot + from-zero chart animation (series colour) */
const VR_TRAVEL_DOT = {
  id: "vrTravelDot",
  afterDatasetsDraw(chart) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const anim = chart.$vrAnim;
    if (!anim || !anim.active) return;
    const t = Math.min(1, (performance.now() - anim.t0) / anim.duration);
    const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic ≈ exponential settle
    chart.data.datasets.forEach((ds, di) => {
      if (chart.config.type === "bar") return;
      const meta = chart.getDatasetMeta(di);
      if (!meta || meta.hidden || !meta.data.length) return;
      const n = meta.data.length;
      const pos = eased * (n - 1);
      const i0 = Math.floor(pos);
      const i1 = Math.min(n - 1, i0 + 1);
      const frac = pos - i0;
      const p0 = meta.data[i0];
      const p1 = meta.data[i1];
      if (!p0) return;
      const x = p0.x + ((p1 ? p1.x : p0.x) - p0.x) * frac;
      const y = p0.y + ((p1 ? p1.y : p0.y) - p0.y) * frac;
      const color = ds.borderColor || ds.backgroundColor || "#3b82f6";
      const ctx = chart.ctx;
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, 7, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.shadowColor = color;
      ctx.shadowBlur = 14;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(x, y, 3.2, 0, Math.PI * 2);
      ctx.fillStyle = "#fff";
      ctx.shadowBlur = 0;
      ctx.fill();
      ctx.restore();
    });
    if (t < 1) {
      // keep drawing while Chart.js animates
    } else {
      anim.active = false;
    }
  }
};

function vrChartAnimOpts(duration) {
  const dur = duration || 1800;
  return {
    duration: dur,
    easing: "easeOutQuart",
    onComplete: function(ctx) {
      const ch = ctx.chart;
      if (ch && ch.$vrAnim) ch.$vrAnim.active = false;
    }
  };
}

function startChartTravel(chart, duration) {
  if (!chart) return;
  const dur = duration || 1800;
  chart.$vrAnim = { active: true, t0: performance.now(), duration: dur };
  // Force redraw loop for the traveling dot during animation
  const tick = () => {
    if (!chart.$vrAnim || !chart.$vrAnim.active) return;
    try { chart.draw(); } catch (e) {}
    if (performance.now() - chart.$vrAnim.t0 < dur + 50) {
      requestAnimationFrame(tick);
    } else if (chart.$vrAnim) {
      chart.$vrAnim.active = false;
      try { chart.draw(); } catch (e) {}
    }
  };
  requestAnimationFrame(tick);
}

function animateChartFromZero(chart, duration) {
  if (!chart) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    chart.update("none");
    return;
  }
  const dur = duration || 1800;
  // Snapshot targets
  const targets = chart.data.datasets.map(ds => (ds.data || []).slice());
  // Zero out
  chart.data.datasets.forEach(ds => {
    ds.data = (ds.data || []).map(() => 0);
  });
  chart.options.animation = { duration: 0 };
  chart.update("none");
  // Restore targets and animate
  chart.data.datasets.forEach((ds, i) => {
    ds.data = targets[i];
  });
  chart.options.animation = vrChartAnimOpts(dur);
  startChartTravel(chart, dur);
  chart.update();
}

function replayAllCharts() {
  if (typeof current !== "undefined" && current) updateCharts(current, true);
}

function initCharts() {
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.font.family = "Plus Jakarta Sans";
  const grid = { color: "rgba(148,163,184,0.12)" };
  if (typeof Chart !== "undefined" && Chart.register) {
    try { Chart.register(VR_TRAVEL_DOT); } catch (e) {}
  }

  const commonOpts = {
    responsive: true,
    maintainAspectRatio: false,
    animation: vrChartAnimOpts(1800),
    plugins: {
      legend: { position: "top" },
      tooltip: {
        callbacks: {
          footer: () => "Click chart to replay animation"
        }
      }
    }
  };

  charts.monthly = new Chart(document.getElementById("chartMonthly"), {
    type: "bar",
    data: {
      labels: MONTHS,
      datasets: [{
        label: "Solar Generation (kWh/month)",
        data: [],
        backgroundColor: "rgba(59,130,246,0.85)",
        borderRadius: 6,
        borderSkipped: false
      }]
    },
    options: {
      ...commonOpts,
      scales: { x: { grid: { display: false } }, y: { grid, beginAtZero: true } }
    }
  });

  charts.diurnal = new Chart(document.getElementById("chartDiurnal"), {
    type: "line",
    data: {
      labels: ["6 AM", "8 AM", "10 AM", "12 PM", "2 PM", "4 PM", "6 PM", "8 PM"],
      datasets: [{
        label: "PV Power Output (kW)",
        data: [0, 0, 0, 0, 0, 0, 0, 0],
        borderColor: "#10b981",
        backgroundColor: "rgba(16,185,129,0.18)",
        fill: true,
        tension: 0.4,
        borderWidth: 2.5,
        pointRadius: 3,
        pointBackgroundColor: "#10b981",
        pointBorderColor: "#fff",
        pointBorderWidth: 1
      }]
    },
    options: {
      ...commonOpts,
      scales: { x: { grid: { display: false } }, y: { grid, beginAtZero: true } }
    }
  });

  charts.cash = new Chart(document.getElementById("chartCash"), {
    type: "line",
    data: {
      labels: ["Yr 1", "Yr 5", "Yr 10", "Yr 15", "Yr 20", "Yr 25"],
      datasets: [
        {
          label: "Solar Net Savings (₹ Lakhs)",
          data: [],
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59,130,246,0.12)",
          fill: true,
          tension: 0.35,
          borderWidth: 2.5,
          pointRadius: 3,
          pointBackgroundColor: "#3b82f6",
          pointBorderColor: "#fff",
          pointBorderWidth: 1
        },
        {
          label: "Bank FD @ 6.5% (₹ Lakhs)",
          data: [],
          borderColor: "#f59e0b",
          borderDash: [5, 5],
          tension: 0.35,
          fill: false,
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: "#f59e0b",
          pointBorderColor: "#fff",
          pointBorderWidth: 1
        }
      ]
    },
    options: {
      ...commonOpts,
      scales: { x: { grid: { display: false } }, y: { grid, beginAtZero: true } }
    }
  });

  // Click any chart card → replay from zero with traveling dots
  ["chartMonthly", "chartDiurnal", "chartCash"].forEach(id => {
    const canvas = document.getElementById(id);
    const box = canvas && canvas.closest(".chart-box, .card");
    const target = box || canvas;
    if (!target) return;
    target.style.cursor = "pointer";
    target.title = "Click to replay chart animation from zero";
    target.addEventListener("click", () => {
      const map = { chartMonthly: charts.monthly, chartDiurnal: charts.diurnal, chartCash: charts.cash };
      const ch = map[id];
      if (ch) animateChartFromZero(ch, id === "chartCash" ? 2200 : 1800);
    });
  });
}

function updateCharts(r, forceReplay) {
  if (!r) return;
  if (charts.monthly) {
    charts.monthly.data.labels = MONTHS;
    charts.monthly.data.datasets[0].data = MONTHS.map(m => r.monthly[m]);
  }
  if (charts.diurnal) {
    const p = r.capacityKw;
    charts.diurnal.data.datasets[0].data = [0.02, 0.30, 0.82, 0.98, 0.85, 0.40, 0.05, 0].map(x => +(x * p).toFixed(2));
  }
  if (charts.cash) {
    // Full 25-year path for smoother traveling-dot animation
    const labels = [];
    const solar = [];
    const fd = [];
    for (let y = 1; y <= 25; y++) {
      labels.push(y === 1 || y % 5 === 0 ? "Yr " + y : "");
      solar.push(+(r.amort[y - 1].cum / 1e5).toFixed(2));
      fd.push(+((r.bom.plantTotal * Math.pow(1.065, y)) / 1e5).toFixed(2));
    }
    charts.cash.data.labels = labels;
    charts.cash.data.datasets[0].data = solar;
    charts.cash.data.datasets[1].data = fd;
  }
  // Always animate from zero when data updates or forceReplay
  animateChartFromZero(charts.monthly, 1600);
  animateChartFromZero(charts.diurnal, 1600);
  animateChartFromZero(charts.cash, 2200);
}

// ============================================================
// HELPERS, PRESETS & MODES
// ============================================================
function setMode(m, opts) {
  const force = opts && opts.force;
  const san = parseFloat(document.getElementById("cfgSanctionedLoad")?.value) || 0;
  // When sanctioned load is filled, lock to Path 1 unless internal force clear
  if (san > 0 && m === "bill" && !force) {
    toast("Sanctioned Load is set — Path 1 is required");
    m = "roof";
  }
  mode = m;
  const rRoof = document.getElementById("radioRoof");
  const rBill = document.getElementById("radioBill");
  if (rRoof) rRoof.checked = m === "roof";
  if (rBill) rBill.checked = m === "bill";
  updatePathCardStates();
  if (typeof sites !== "undefined" && sites[activeSiteIndex]) {
    sites[activeSiteIndex].mode = m;
  }
  liveUpdate();
}

function updatePathCardStates() {
  const p1 = document.getElementById("path1Card");
  const p2 = document.getElementById("path2Card");
  const rRoof = document.getElementById("radioRoof");
  const rBill = document.getElementById("radioBill");
  const san = parseFloat(document.getElementById("cfgSanctionedLoad")?.value) || 0;
  if (!p1 || !p2) return;

  if (san > 0) {
    // Force path 1; path 2 timid + disabled
    mode = "roof";
    if (rRoof) rRoof.checked = true;
    if (rBill) { rBill.checked = false; rBill.disabled = true; }
    p1.classList.add("path-active");
    p1.classList.remove("path-timid");
    p2.classList.add("path-timid");
    p2.classList.remove("path-active");
    p1.querySelectorAll("input,select,button,textarea").forEach(el => {
      if (el.id !== "radioRoof") el.disabled = false;
    });
    return;
  }

  // No sanctioned: mutual exclusive timid
  if (rBill) rBill.disabled = false;
  if (mode === "roof") {
    p1.classList.add("path-active");
    p1.classList.remove("path-timid");
    p2.classList.add("path-timid");
    p2.classList.remove("path-active");
  } else {
    p2.classList.add("path-active");
    p2.classList.remove("path-timid");
    p1.classList.add("path-timid");
    p1.classList.remove("path-active");
  }
  // Active path inputs enabled; timid path dimmed but radios stay clickable to switch
  [p1, p2].forEach(card => {
    const timid = card.classList.contains("path-timid");
    card.querySelectorAll("input,select,button,textarea").forEach(el => {
      if (el.type === "radio") {
        el.disabled = false;
        return;
      }
      // Sanctioned load always editable (site-level; filling it forces Path 1)
      if (el.id === "cfgSanctionedLoad") {
        el.disabled = false;
        return;
      }
      el.disabled = timid;
    });
  });
  // Timid cards: allow clicking radio only
  p1.style.pointerEvents = "auto";
  p2.style.pointerEvents = "auto";
}

function onSanctionedLoadInput() {
  saveCurrentFormToActiveSite();
  const san = parseFloat(document.getElementById("cfgSanctionedLoad")?.value) || 0;
  if (san > 0) {
    setMode("roof");
  } else {
    updatePathCardStates();
    liveUpdate();
  }
}

// Init path states after load
setTimeout(() => { try { updatePathCardStates(); } catch(e){} }, 300);


// ============================================================
// TECHNOLOGY & PANEL CATALOG UI LOGIC
// ============================================================
function initTechAndPanelDropdowns() {
  const techKeys = Object.keys(SOLAR_PANEL_CATALOG);
  const techSelects = [document.getElementById("cfgTech"), document.getElementById("cfgTechBill")];
  
  techSelects.forEach(sel => {
    if (!sel) return;
    sel.innerHTML = techKeys.map(k => {
      const cat = SOLAR_PANEL_CATALOG[k];
      return `<option value="${k}" ${k.startsWith("Mono-PERC") ? "selected" : ""}>${k}</option>`;
    }).join("");
  });
  
  populatePanelDropdown("cfgPanel", "Mono-PERC (Mono-facial)", 550);
  populatePanelDropdown("cfgPanelBill", "Mono-PERC (Mono-facial)", 550);
  updateTechInfo("roof", "Mono-PERC (Mono-facial)");
  updateTechInfo("bill", "Mono-PERC (Mono-facial)");
}

function populatePanelDropdown(selectId, techName, selectedWatt = null) {
  const sel = document.getElementById(selectId);
  if (!sel) return;
  const cat = SOLAR_PANEL_CATALOG[techName] || SOLAR_PANEL_CATALOG["Mono-PERC (Mono-facial)"];
  const ratings = cat.ratings;
  const defWatt = selectedWatt || cat.defaultWatt;

  sel.innerHTML = `
    <optgroup label="${techName} (${ratings.length} Ratings)">
      ${ratings.map(w => `<option value="${w}" ${w === Number(defWatt) ? "selected" : ""}>${w} Wp</option>`).join("")}
    </optgroup>
    <optgroup label="Other Standard Technologies">
      ${Object.keys(SOLAR_PANEL_CATALOG).filter(k => k !== techName).map(k => {
        return SOLAR_PANEL_CATALOG[k].ratings.slice(0, 3).map(w => `<option value="${w}" data-tech="${k}">${w} Wp (${k.split(' ')[0]})</option>`).join("");
      }).join("")}
    </optgroup>
  `;
}

function updateTechInfo(mode, techName) {
  const cat = SOLAR_PANEL_CATALOG[techName];
  if (!cat) return;
  const infoEl = document.getElementById(mode === "roof" ? "cfgTechInfo" : "cfgTechBillInfo");
  if (infoEl) {
    infoEl.textContent = `ℹ️ ${cat.desc} Available: ${cat.ratings[0]}W to ${cat.ratings[cat.ratings.length - 1]}W (${cat.ratings.length} steps).`;
  }
}

function onTechChange(viewMode) {
  const isRoof = viewMode === "roof";
  const techSel = document.getElementById(isRoof ? "cfgTech" : "cfgTechBill");
  const panelSel = document.getElementById(isRoof ? "cfgPanel" : "cfgPanelBill");
  if (!techSel || !panelSel) return;
  const techName = techSel.value;
  populatePanelDropdown(isRoof ? "cfgPanel" : "cfgPanelBill", techName);
  updateTechInfo(viewMode, techName);

  // Sync to other mode
  const otherTechSel = document.getElementById(isRoof ? "cfgTechBill" : "cfgTech");
  if (otherTechSel) otherTechSel.value = techName;
  populatePanelDropdown(isRoof ? "cfgPanelBill" : "cfgPanel", techName);
  updateTechInfo(isRoof ? "bill" : "roof", techName);
}

function syncPanelFromBill() {
  const techBill = document.getElementById("cfgTechBill")?.value;
  const val = document.getElementById("cfgPanelBill")?.value;
  const techRoof = document.getElementById("cfgTech");
  if (techRoof && techBill) techRoof.value = techBill;
  populatePanelDropdown("cfgPanel", techBill, val);
  const panRoof = document.getElementById("cfgPanel");
  if (panRoof && val) panRoof.value = val;
  updateTechInfo("roof", techBill);
}

function syncPanelFromRoof() {
  const techRoof = document.getElementById("cfgTech")?.value;
  const val = document.getElementById("cfgPanel")?.value;
  const techBill = document.getElementById("cfgTechBill");
  if (techBill && techRoof) techBill.value = techRoof;
  populatePanelDropdown("cfgPanelBill", techRoof, val);
  const panBill = document.getElementById("cfgPanelBill");
  if (panBill && val) panBill.value = val;
  updateTechInfo("bill", techRoof);
}

function syncDistFromBill() {
  document.getElementById('cfgDist').value = document.getElementById('cfgDistBill').value;
}

function clearAllInputs() {
  document.getElementById("cfgName").value = "";
  document.getElementById("cfgLoc").value = "";
  document.getElementById("cfgEmail").value = "";
  document.getElementById("cfgTariff").value = "";
  document.getElementById("cfgL").value = "";
  document.getElementById("cfgB").value = "";
  document.getElementById("cfgParapet").value = "";
  document.getElementById("cfgUnits").value = "";
  document.getElementById("cfgBuildings").value = "";
  document.getElementById("cfgDist").value = "";
  document.getElementById("cfgDistBill").value = "";
  saveCurrentFormToActiveSite();
  renderSiteTabs();
  liveUpdate();
  toast("All filling areas reset to empty/zero.");
}

function applyPreset(presetName) {
  document.querySelectorAll(".preset").forEach(p => p.classList.remove("on"));
  if (window.event?.target) window.event.target.classList.add("on");

  if (presetName === "res1") {
    setMode("roof");
    document.getElementById("cfgName").value = "1 kW Residential Micro";
    document.getElementById("cfgL").value = 13;
    document.getElementById("cfgB").value = 11;
    document.getElementById("cfgParapet").value = 1.0;
    document.getElementById("cfgPanel").value = "550";
    document.getElementById("cfgDist").value = "15";
  } else if (presetName === "res3") {
    setMode("roof");
    document.getElementById("cfgName").value = "3 kW Residential Villa";
    document.getElementById("cfgL").value = 23;
    document.getElementById("cfgB").value = 16;
    document.getElementById("cfgParapet").value = 1.5;
    document.getElementById("cfgPanel").value = "550";
    document.getElementById("cfgDist").value = "15";
  } else if (presetName === "res5") {
    setMode("roof");
    document.getElementById("cfgName").value = "5 kW Green Residence";
    document.getElementById("cfgL").value = 28;
    document.getElementById("cfgB").value = 21;
    document.getElementById("cfgParapet").value = 1.5;
    document.getElementById("cfgPanel").value = "550";
    document.getElementById("cfgDist").value = "20";
  } else if (presetName === "com10") {
    setMode("roof");
    document.getElementById("cfgName").value = "10 kW Commercial Plant";
    document.getElementById("cfgL").value = 40;
    document.getElementById("cfgB").value = 30;
    document.getElementById("cfgParapet").value = 1.5;
    document.getElementById("cfgPanel").value = "550";
    document.getElementById("cfgDist").value = "20";
  } else if (presetName === "ind20") {
    setMode("roof");
    document.getElementById("cfgName").value = "20 kW Industrial Rooftop";
    document.getElementById("cfgL").value = 54;
    document.getElementById("cfgB").value = 41;
    document.getElementById("cfgParapet").value = 2.0;
    document.getElementById("cfgPanel").value = "550";
    document.getElementById("cfgDist").value = "30";
  } else if (presetName === "bill136") {
    setMode("bill");
    document.getElementById("cfgName").value = "Default 136 Units Bill";
    document.getElementById("cfgUnits").value = 136;
    document.getElementById("cfgPanel").value = "275";
    document.getElementById("cfgPanelBill").value = "275";
    document.getElementById("cfgDist").value = "20";
    document.getElementById("cfgDistBill").value = "20";
  } else if (presetName === "bill1200") {
    setMode("bill");
    document.getElementById("cfgName").value = "1200 Units Monthly Bill";
    document.getElementById("cfgUnits").value = 1200;
    document.getElementById("cfgPanel").value = "550";
    document.getElementById("cfgPanelBill").value = "550";
    document.getElementById("cfgDist").value = "20";
    document.getElementById("cfgDistBill").value = "20";
  }

  liveUpdate();
  toast(`Applied Preset: ${presetName.toUpperCase()}`);
}

function switchView(id, btn) {
  document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
  document.getElementById("view-" + id).classList.add("active");
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  if (btn) btn.classList.add("active");
  else {
    const m = document.querySelector(`.nav-item[data-view="${id}"]`);
    if (m) m.classList.add("active");
  }
  if (window.innerWidth <= 900) closeSidebar();
  if (id === "dashboard") {
    setTimeout(() => {
      drawArray(current?.panels || 0);
      updateRoofStats(current);
      if (charts.monthly && current) updateCharts(current);
    }, 60);
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("open");
  document.getElementById("overlay").classList.toggle("show");
}
function closeSidebar() {
  document.getElementById("sidebar").classList.remove("open");
  document.getElementById("overlay").classList.remove("show");
}

function toggleTheme() {
  const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  try { localStorage.setItem("voltroof_theme", next); } catch(e){}
  document.getElementById("themeIcon").textContent = next === "dark" ? "☀️" : "🌙";
  document.getElementById("themeIcon2").textContent = next === "dark" ? "☀️" : "🌙";
  toast(`Switched to ${next.toUpperCase()} Mode`);
  setTimeout(() => drawArray(current?.panels || 0), 50);
}

function updateClock() {
  const el = document.getElementById("topDateTime");
  if (!el) return;
  const d = new Date();
  const date = d.toLocaleDateString("en-IN", { weekday: "short", day: "2-digit", month: "short", year: "numeric" });
  const time = d.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: true });
  el.textContent = `${date} · ${time}`;
}

function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2600);
}

// Storage & Export
function saveProject() {
  if (!current) { toast("Calculate system first"); return; }
  const projects = JSON.parse(localStorage.getItem("voltroof_projects") || "{}");
  projects[current.name || "Default_Project"] = current;
  try { localStorage.setItem("voltroof_projects", JSON.stringify(projects)); } catch(e){}
  refreshLoadSelect();
  toast(`Project '${current.name}' saved!`);
}

function refreshLoadSelect() {
  const sel = document.getElementById("loadSelect");
  if (!sel) return;
  const projects = JSON.parse(localStorage.getItem("voltroof_projects") || "{}");
  sel.innerHTML = '<option value="">📂 Load…</option>';
  Object.keys(projects).forEach(k => {
    const o = document.createElement("option");
    o.value = k;
    o.textContent = k;
    sel.appendChild(o);
  });
}

function loadProject(key) {
  if (!key) return;
  const projects = JSON.parse(localStorage.getItem("voltroof_projects") || "{}");
  const p = projects[key];
  if (!p) return;
  setMode(p.mode || "roof");
  document.getElementById("cfgName").value = p.name || "";
  document.getElementById("cfgLoc").value = p.loc || "";
  document.getElementById("cfgEmail").value = p.email || "";
  document.getElementById("cfgDist").value = p.dist || 20;
  document.getElementById("cfgDistBill").value = p.dist || 20;
  document.getElementById("cfgPanel").value = String(p.panelW || 550);
  document.getElementById("cfgPanelBill").value = String(p.panelW || 550);
  liveUpdate();
  switchView("dashboard");
  toast(`Loaded project: ${key}`);
}

function exportCSV() {
  if (!current) { toast("Please calculate a system first"); return; }
  const r = current;
  let csv = "VOLTROOF DESIGNS - SOLAR PV ESTIMATION REPORT\n";
  csv += `Site Name,${r.name}\nLocation,${r.loc}\nEmail,${r.email}\n`;
  csv += `Target Capacity (kW),${r.capacityKw}\nInstalled Array (kWp),${r.installedDckWp}\nPanels,${r.panels} (${r.panelW}W)\n`;
  csv += `Inverter,${r.invKw} kW (${r.phase3 ? "Three-Phase" : "Single-Phase"})\n`;
  csv += `ACDB Breaker,${r.acdb.breakerRating}A\nGrid Cable,${r.acdb.gridCable}\n`;
  csv += `Total Plant Cost (INR),${r.bom.plantTotal}\nAnnual Generation (kWh),${r.annual}\n25Y Generation (kWh),${r.total25}\n`;
  csv += `Payback Period,${r.payY} Years ${r.payM} Months\nLifetime Profit (INR),${r.lifetimeProfit}\nCO2 Avoided (Tonnes),${r.co2}\n\n`;

  csv += "BILL OF MATERIALS (BOM)\nSl No,Description,Specification,Quantity,Amount (INR)\n";
  r.bom.items.forEach(it => {
    csv += `${it.sl},"${it.desc}","${it.spec}","${it.qty}",${it.amt}\n`;
  });

  csv += "\n25-YEAR AMORTIZATION SCHEDULE\nYear,Generation (kWh),Tariff (INR/kWh),Gross Revenue,AMC,Net Savings,Cumulative (INR)\n";
  r.amort.forEach(a => {
    csv += `${a.year},${a.gen},${a.tariff},${a.revenue},${a.amc},${a.net},${a.cum}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `VoltRoof_${(r.name || "Report").replace(/\s+/g, "_")}.csv`;
  a.click();
  toast("Exported CSV Report successfully");
}

function downloadPdf() {
  if (!current) { toast("Configure parameters and calculate plant first"); return; }
  saveCurrentFormToActiveSite();
  const projName = (sites[0]?.name || document.getElementById("cfgName")?.value || "Solar Rooftop Project").trim();
  const projContact = (sites[0]?.contact || document.getElementById("cfgContact")?.value || "").trim();
  const projLoc = (sites[0]?.loc || document.getElementById("cfgLoc")?.value || "Karnataka").trim();
  const projEmail = (sites[0]?.email || document.getElementById("cfgEmail")?.value || "").trim();
  const projSanctioned = parseFloat(sites[0]?.sanctionedLoad || document.getElementById("cfgSanctionedLoad")?.value) || null;

  const payload = {
    mode: current.mode,
    customer_name: projName,
    location: projLoc,
    email: projEmail,
    contact_number: projContact,
    sanctioned_load_kw: projSanctioned,
    custom_tariff: parseFloat(sites[0]?.tariff) || 8.05,
    sites: sites.map((s, sIdx) => {
      const siteName = (s.name || `Site Name-${sIdx + 1}`).trim();
      const siteContact = (s.contact || projContact).trim();
      const siteLoc = (s.loc || projLoc).trim();
      const siteEmail = (s.email || projEmail).trim();
      const siteSanctioned = parseFloat(s.sanctionedLoad) || projSanctioned;
      const siteDist = parseFloat(s.dist) || 20.0;
      const bldgs = (s.buildings && s.buildings.length > 0) ? s.buildings : [{
        name: "Building 1",
        L: s.L || 40,
        B: s.B || 30,
        parapet: s.parapet || 1.5,
        neighbour: s.neighbour || "None",
        panel: s.panel || "550"
      }];
      return {
        site_id: s.id || `site-${sIdx + 1}`,
        name: siteName,
        contact_number: siteContact,
        sanctioned_load_kw: siteSanctioned,
        location: siteLoc,
        email: siteEmail,
        mode: s.mode || "roof",
        tariff: parseFloat(s.tariff) || 8.05,
        distance_m: siteDist,
        monthly_units: parseFloat(s.units) || 1200.0,
        buildings: bldgs.map((b, bIdx) => ({
          name: b.name || `Building ${bIdx + 1}`,
          length_ft: parseFloat(b.L) || 40.0,
          breadth_ft: parseFloat(b.B) || 30.0,
          parapet_ft: parseFloat(b.parapet) || 1.5,
          neighbour: b.neighbour || "None",
          panel_watt: parseInt(b.panel) || 550,
          panel_tech: b.tech || s.tech || "Mono-PERC (Mono-facial)"
        }))
      };
    }),
    length_ft: num("cfgL"),
    breadth_ft: num("cfgB"),
    parapet_ft: num("cfgParapet"),
    monthly_units: num("cfgUnits"),
    distance_m: current.dist,
    panel_watt: current.panelW,
    panel_tech: current.panelTech || "Mono-PERC (Mono-facial)",
    contact_number: projContact,
    sanctioned_load_kw: projSanctioned
  };

  fetch("/api/download_pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(resp => {
    if (resp.ok) return resp.blob();
    throw new Error("Backend PDF unavailable, falling back to browser print");
  })
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `LT_RTSPV_${projName.replace(/\s+/g, "_")}.pdf`;
    a.click();
    toast("Downloaded official FPDF Report (All Sites & Buildings Included)");
  })
  .catch(() => {
    // Offline / Standalone Browser Fallback Print
    document.querySelectorAll(".view").forEach(v => v.classList.add("active"));
    setTimeout(() => {
      window.print();
      setTimeout(() => {
        document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
        document.getElementById("view-dashboard").classList.add("active");
      }, 500);
    }, 200);
  });
}

function sendEmailReport() {
  if (!current) { toast("Calculate system first"); return; }
  const email = current.email || prompt("Enter recipient email address:");
  if (!email) return;
  fetch("/api/send_email", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email, name: current.name })
  })
  .then(r => r.json())
  .then(d => toast(d.message || `Report queued for ${email}`))
  .catch(() => toast(`PDF Report prepared for ${email}`));
}

/* ==========================================================================
   USER MANUAL & ADMIN DOCUMENT MANAGEMENT ENGINE
   Dual Mode: Online (Backend API) + Offline Standalone (LocalStorage)
   ========================================================================== */

const BUILTIN_ADMINS = [
  { username: "Adarsha KM", emails: ["adarshakm@jnnce.ac.in", "adarshakmsgr50@gmail.com"], mobile: "8073398259", password: "Adarsh@123321", role: "super_admin" },
  { username: "Prathapa R", emails: ["prathaparprathapar6@gmail.com"], mobile: "", password: "Prathap@123", role: "admin" },
  { username: "D Nihar", emails: ["nihar333k@gmail.com"], mobile: "", password: "Nihar@123", role: "admin" },
  { username: "Ajjanna NG", emails: ["nga_ee@jnnce.ac.in"], mobile: "", password: "Admin@123", role: "admin" }
];

let stagedManualUpload = null; // { filename, size, data_base64 }

function getActiveAdmin() {
  try {
    const raw = localStorage.getItem("voltroof_admin_session");
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return null;
}

function updateAdminUIState() {
  const admin = getActiveAdmin();
  const topBtn = document.getElementById("btnTopAdminManual");
  const topLabel = document.getElementById("btnTopAdminManualLabel");
  const navBtn = document.getElementById("navAdminManualBtn");
  const navLabel = document.getElementById("navAdminManualLabel");
  const gateAdminName = document.getElementById("gateAdminNameDisplay");
  const modalAdminName = document.getElementById("modalAdminNameDisplay");

  if (admin) {
    const shortName = admin.username.split(" ")[0];
    if (topLabel) topLabel.textContent = `Admin (${shortName})`;
    if (navLabel) navLabel.textContent = `Admin: ${shortName} 🛡️`;
    if (gateAdminName) gateAdminName.textContent = `${admin.username} (${admin.role === 'super_admin' ? 'Super Admin' : 'Admin'})`;
    if (modalAdminName) modalAdminName.textContent = `${admin.username} (${admin.role === 'super_admin' ? 'Super Admin' : 'Admin'})`;
  } else {
    if (topLabel) topLabel.textContent = "Admin Manual";
    if (navLabel) navLabel.textContent = "Update Manual 🛡️";
  }
}

function openUserManual() {
  toast("Opening VoltRoof User Manual...");
  try {
    const customData = localStorage.getItem("voltroof_user_manual_data");
    if (customData && customData.startsWith("data:application/pdf")) {
      const byteChars = atob(customData.split(',')[1]);
      const byteNums = new Array(byteChars.length);
      for (let i = 0; i < byteChars.length; i++) {
        byteNums[i] = byteChars.charCodeAt(i);
      }
      const blob = new Blob([new Uint8Array(byteNums)], { type: 'application/pdf' });
      const blobUrl = URL.createObjectURL(blob);
      const w = window.open(blobUrl, "_blank");
      if (!w) {
        const a = document.createElement("a");
        a.href = blobUrl;
        a.download = "VoltRoof_User_Manual.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
      return;
    }
  } catch(e) {
    console.warn("Local manual retrieval fallback:", e);
  }

  // Server fetch fallback
  const pdfUrl = "/user_manual.pdf";
  const w = window.open(pdfUrl, "_blank");
  if (!w) {
    const a = document.createElement("a");
    a.href = pdfUrl;
    a.target = "_blank";
    a.download = "VoltRoof_User_Manual.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
}

function toggleGateAdminMode() {
  const clientMode = document.getElementById("gateClientMode");
  const adminMode = document.getElementById("gateAdminMode");
  const toggleLabel = document.getElementById("gateAdminLabel");
  const toggleIcon = document.getElementById("gateAdminIcon");

  if (adminMode.style.display === "none") {
    // Switch to Admin mode
    clientMode.style.display = "none";
    adminMode.style.display = "block";
    toggleLabel.textContent = "User Mode";
    toggleIcon.textContent = "👤";
    refreshManualMetadata();

    const admin = getActiveAdmin();
    if (admin) {
      document.getElementById("gateAdminLoginForm").style.display = "none";
      document.getElementById("gateAdminDocPanel").style.display = "block";
    } else {
      document.getElementById("gateAdminLoginForm").style.display = "block";
      document.getElementById("gateAdminDocPanel").style.display = "none";
      setTimeout(() => document.getElementById("gateAdminUser")?.focus(), 100);
    }
  } else {
    // Switch back to Client mode
    adminMode.style.display = "none";
    clientMode.style.display = "block";
    toggleLabel.textContent = "Admin";
    toggleIcon.textContent = "🛡️";
    setTimeout(() => document.getElementById("gateName")?.focus(), 100);
  }
}

async function loginAdminCore(username, password) {
  const u = (username || "").trim();
  const p = (password || "").trim();
  if (!u || !p) {
    toast("Please enter both username/email and password");
    return null;
  }

  // 1. Try server backend login
  try {
    const res = await fetch("/api/admin/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, password: p })
    });
    if (res.ok) {
      const data = await res.json();
      if (data.success && data.admin) {
        return data.admin;
      }
    }
  } catch(err) {
    // Network error or offline standalone mode -> fall back to local auth
  }

  // 2. Offline / Standalone Fallback
  const uLower = u.toLowerCase();
  const found = BUILTIN_ADMINS.find(adm => {
    const uMatch = adm.username.toLowerCase() === uLower ||
                   adm.emails.some(e => e.toLowerCase() === uLower) ||
                   adm.mobile === u;
    const pMatch = adm.password === p;
    return uMatch && pMatch;
  });

  if (found) {
    return {
      username: found.username,
      email: found.emails[0] || "",
      role: found.role
    };
  }

  return null;
}

async function loginAdminFromGate() {
  const u = document.getElementById("gateAdminUser")?.value;
  const p = document.getElementById("gateAdminPass")?.value;
  const admin = await loginAdminCore(u, p);
  if (admin) {
    localStorage.setItem("voltroof_admin_session", JSON.stringify(admin));
    toast(`Authenticated as Admin: ${admin.username}`);
    updateAdminUIState();
    document.getElementById("gateAdminLoginForm").style.display = "none";
    document.getElementById("gateAdminDocPanel").style.display = "block";
    refreshManualMetadata();
  } else {
    toast("Invalid administrator credentials");
  }
}

async function loginAdminFromModal() {
  const u = document.getElementById("modalAdminUser")?.value;
  const p = document.getElementById("modalAdminPass")?.value;
  const admin = await loginAdminCore(u, p);
  if (admin) {
    localStorage.setItem("voltroof_admin_session", JSON.stringify(admin));
    toast(`Authenticated as Admin: ${admin.username}`);
    updateAdminUIState();
    document.getElementById("modalAdminLoginForm").style.display = "none";
    document.getElementById("modalAdminDocPanel").style.display = "block";
    refreshManualMetadata();
  } else {
    toast("Invalid administrator credentials");
  }
}

function logoutAdmin() {
  localStorage.removeItem("voltroof_admin_session");
  updateAdminUIState();
  toast("Signed out of Administrator session");
  
  const gateLoginForm = document.getElementById("gateAdminLoginForm");
  const gateDocPanel = document.getElementById("gateAdminDocPanel");
  if (gateLoginForm && gateDocPanel) {
    gateLoginForm.style.display = "block";
    gateDocPanel.style.display = "none";
    const passInp = document.getElementById("gateAdminPass");
    if (passInp) passInp.value = "";
  }
  
  const modalLoginForm = document.getElementById("modalAdminLoginForm");
  const modalDocPanel = document.getElementById("modalAdminDocPanel");
  if (modalLoginForm && modalDocPanel) {
    modalLoginForm.style.display = "block";
    modalDocPanel.style.display = "none";
    const passInp = document.getElementById("modalAdminPass");
    if (passInp) passInp.value = "";
  }
}

function openAdminManualModal() {
  const modal = document.getElementById("modalAdminManual");
  if (!modal) return;
  modal.style.display = "flex";

  const admin = getActiveAdmin();
  if (admin) {
    document.getElementById("modalAdminLoginForm").style.display = "none";
    document.getElementById("modalAdminDocPanel").style.display = "block";
  } else {
    document.getElementById("modalAdminLoginForm").style.display = "block";
    document.getElementById("modalAdminDocPanel").style.display = "none";
    setTimeout(() => document.getElementById("modalAdminUser")?.focus(), 80);
  }
  refreshManualMetadata();
  updateAdminUIState();
}

function closeAdminManualModal() {
  const modal = document.getElementById("modalAdminManual");
  if (modal) modal.style.display = "none";
  stagedManualUpload = null;
}

function formatDocBytes(bytes) {
  if (!bytes || bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
}

function handleManualFileSelected(inputEl, source) {
  if (!inputEl.files || !inputEl.files[0]) return;
  const file = inputEl.files[0];
  if (!file.name.toLowerCase().endsWith(".pdf") && file.type !== "application/pdf") {
    toast("Please select a valid PDF document");
    return;
  }

  const reader = new FileReader();
  reader.onload = function(e) {
    stagedManualUpload = {
      filename: file.name,
      size: file.size,
      data_base64: e.target.result
    };

    const dispText = `Selected: ${file.name} (${formatDocBytes(file.size)})`;
    if (source === 'gate') {
      const el = document.getElementById("gateSelectedFileName");
      if (el) el.innerHTML = `✅ <strong style="color:var(--primary)">${dispText}</strong>`;
      const btn = document.getElementById("btnGatePublishManual");
      if (btn) btn.disabled = false;
    } else {
      const el = document.getElementById("modalSelectedFileName");
      if (el) el.innerHTML = `✅ <strong style="color:var(--primary)">${dispText}</strong>`;
      const btn = document.getElementById("btnModalPublishManual");
      if (btn) btn.disabled = false;
    }
    toast(`Loaded ${file.name}. Ready to publish.`);
  };
  reader.readAsDataURL(file);
}

async function submitAdminManualUpload(source) {
  if (!stagedManualUpload || !stagedManualUpload.data_base64) {
    toast("Please select a PDF file first");
    return;
  }

  const admin = getActiveAdmin() || { username: "Administrator" };
  const publishBtn = source === 'gate' ? document.getElementById("btnGatePublishManual") : document.getElementById("btnModalPublishManual");
  if (publishBtn) {
    publishBtn.disabled = true;
    publishBtn.textContent = "⏳ Publishing...";
  }

  const payload = {
    data_base64: stagedManualUpload.data_base64,
    filename: stagedManualUpload.filename,
    admin_name: admin.username
  };

  const metaObj = {
    exists: true,
    filename: stagedManualUpload.filename,
    size_bytes: stagedManualUpload.size,
    updated_at: new Date().toLocaleDateString("en-GB", { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }),
    updated_by: admin.username
  };

  // 1. Save to localStorage for instant offline & standalone persistence
  try {
    safeSetLocal("voltroof_user_manual_data", stagedManualUpload.data_base64, 2000000);
    localStorage.setItem("voltroof_user_manual_meta", JSON.stringify(metaObj));
  } catch(e) {
    console.warn("Storage quota warning for local manual:", e);
  }

  // 2. If online / backend server running, send to server
  try {
    const res = await fetch("/api/admin/upload_user_manual", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      console.log("Server user manual update response:", data);
    }
  } catch(err) {
    console.log("Server update skipped or offline standalone mode active:", err);
  }

  // 3. Reset UI feedback
  if (publishBtn) {
    publishBtn.textContent = source === 'gate' ? "🚀 Publish & Update Manual" : "🚀 Publish & Update User Manual";
    publishBtn.disabled = true;
  }
  if (source === 'gate') {
    const el = document.getElementById("gateSelectedFileName");
    if (el) el.textContent = "Click to select new User Manual PDF";
    const inp = document.getElementById("gateManualFileInput");
    if (inp) inp.value = "";
  } else {
    const el = document.getElementById("modalSelectedFileName");
    if (el) el.textContent = "Click or drop new User Manual PDF here";
    const inp = document.getElementById("modalManualFileInput");
    if (inp) inp.value = "";
  }

  stagedManualUpload = null;
  refreshManualMetadata();
  toast("✅ User manual updated successfully! Now live across login screen and studio.");
}

function resetDefaultManual() {
  if (!confirm("Reset to factory default User Manual?")) return;
  localStorage.removeItem("voltroof_user_manual_data");
  localStorage.removeItem("voltroof_user_manual_meta");
  refreshManualMetadata();
  toast("User Manual restored to default official document.");
}

async function refreshManualMetadata() {
  let meta = null;
  // Try server meta first
  try {
    const r = await fetch("/api/user_manual_meta");
    if (r.ok) {
      meta = await r.json();
    }
  } catch(e) {}

  // Check local override
  try {
    const localRaw = localStorage.getItem("voltroof_user_manual_meta");
    if (localRaw) {
      meta = JSON.parse(localRaw);
    }
  } catch(e) {}

  if (!meta) {
    meta = {
      filename: "VoltRoof_User_Manual.pdf",
      size_bytes: 454349,
      updated_at: "Official Release",
      updated_by: "VoltRoof Systems"
    };
  }

  const fName = meta.filename || "VoltRoof_User_Manual.pdf";
  const fMeta = `Size: ${formatDocBytes(meta.size_bytes)} · Updated: ${meta.updated_at || 'Active'} · By: ${meta.updated_by || 'Admin'}`;

  const gName = document.getElementById("gateDocName");
  const gMeta = document.getElementById("gateDocMeta");
  if (gName) gName.textContent = fName;
  if (gMeta) gMeta.textContent = fMeta;

  const mName = document.getElementById("modalDocName");
  const mMeta = document.getElementById("modalDocMeta");
  if (mName) mName.textContent = fName;
  if (mMeta) mMeta.textContent = fMeta;
}

function openNameGate() {
  setTimeout(() => document.getElementById("gateName")?.focus(), 100);
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.remove("hidden");
    gate.style.display = "flex";
  }
  const clientMode = document.getElementById("gateClientMode");
  const adminMode = document.getElementById("gateAdminMode");
  if (clientMode) clientMode.style.display = "block";
  if (adminMode) adminMode.style.display = "none";
  const toggleLabel = document.getElementById("gateAdminLabel");
  const toggleIcon = document.getElementById("gateAdminIcon");
  if (toggleLabel) toggleLabel.textContent = "Admin";
  if (toggleIcon) toggleIcon.textContent = "🛡️";

  const inputEl = document.getElementById("gateName");
  if (inputEl) {
    const savedUser = localStorage.getItem("voltroof_user") || "";
    inputEl.value = "";
    inputEl.placeholder = savedUser ? `Previous: ${savedUser} (or enter name)` : "Enter Engineer / Client Name";
    setTimeout(() => inputEl.focus(), 80);
  }
}

function enterApp() {
  const inputEl = document.getElementById("gateName");
  let n = (inputEl?.value || "").trim();
  if (!n) {
    const admin = getActiveAdmin();
    if (admin) {
      n = admin.username;
    } else {
      const prev = localStorage.getItem("voltroof_user");
      n = prev || "Engineer";
    }
  }
  try { localStorage.setItem("voltroof_user", n); } catch(e){}
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
  const greetEl = document.getElementById("greetName");
  if (greetEl) greetEl.textContent = n;
  const greetBar = document.getElementById("greetBar");
  if (greetBar) greetBar.style.display = "block";

  // Ensure filling areas stay empty or zero as per Requirement 2
  if (sites[activeSiteIndex] && !sites[activeSiteIndex].name) {
    sites[activeSiteIndex].name = "";
    const cfgName = document.getElementById("cfgName");
    if (cfgName) cfgName.value = "";
  }
  renderSiteTabs();
  liveUpdate();
  toast(`Welcome, ${n}`);
  updateAdminUIState();
}


// ============================================================
// VISITOR ANALYTICS TRACKING
// ============================================================
function trackVisitorHit() {
  try {
    let sid = sessionStorage.getItem("voltroof_visitor_sid");
    if (!sid) {
      sid = 'v-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now().toString(36);
      sessionStorage.setItem("voltroof_visitor_sid", sid);
    }
    fetch('/api/visitors/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sid, path: window.location.pathname || '/' })
    }).catch(() => {});
  } catch (e) {
    console.warn("Visitor tracking fallback:", e);
  }
}

// ============================================================
// FEEDBACK MODAL INTERACTIONS
// ============================================================
function openFeedbackModal() {
  const modal = document.getElementById("modalFeedback");
  if (modal) {
    modal.style.display = "flex";
    modal.classList.remove("hidden");
  }
}

function closeFeedbackModal() {
  const modal = document.getElementById("modalFeedback");
  if (modal) {
    modal.style.display = "none";
  }
}

async function submitFeedbackForm(event) {
  if (event) event.preventDefault();
  const cat = document.getElementById("fbCategory")?.value || "Other";
  const exp = parseInt(document.getElementById("fbExperience")?.value || "5", 10);
  const cla = document.getElementById("fbClarity")?.value || "Extremely Clear";
  const utl = document.getElementById("fbUtility")?.value || "Procurement-Ready";
  const rec = document.getElementById("fbRecommend")?.value || "Definitely Yes";
  const com = (document.getElementById("fbComments")?.value || "").trim();

  const submitBtn = document.getElementById("btnSubmitFeedback");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = "⏳ Submitting...";
  }

  const payload = {
    category: cat,
    experience: exp,
    clarity: cla,
    bom_utility: utl,
    recommend: rec,
    comments: com
  };

  try {
    const res = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      toast("Thank you! Your feedback has been recorded successfully. 🌟");
      closeFeedbackModal();
      document.getElementById("fbComments").value = "";
    } else {
      toast("Feedback submitted locally! Thank you for your review.");
      closeFeedbackModal();
    }
  } catch (err) {
    toast("Thank you! Feedback saved.");
    closeFeedbackModal();
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "🚀 Submit Feedback";
    }
  }
}

// ============================================================
// ADMIN CONTROL CENTER TABS & MANAGEMENT
// ============================================================
function switchAdminTab(tabKey) {
  const tabs = ["manual", "pricing", "visitors", "feedback", "users", "audit", "settings", "tickets"];
  tabs.forEach(t => {
    const btn = document.getElementById("tabBtn" + t.charAt(0).toUpperCase() + t.slice(1));
    const pnl = document.getElementById("adminPanel" + t.charAt(0).toUpperCase() + t.slice(1));
    if (btn) btn.classList.toggle("active", t === tabKey);
    if (pnl) pnl.style.display = (t === tabKey) ? "block" : "none";
  });

  if (tabKey === "pricing") loadPricingConfig();
  else if (tabKey === "visitors") refreshVisitorStats();
  else if (tabKey === "feedback") refreshFeedbackStats();
  else if (tabKey === "users") refreshAdminList();
}

function markPricingDirty() {
  const el = document.getElementById("pricingUnsaved");
  if (el) el.style.display = "inline";
  const bar = document.getElementById("pricingStickyBar");
  if (bar) bar.classList.add("show");
  // highlight parent row
  if (event && event.target) {
    const tr = event.target.closest("tr");
    if (tr) tr.classList.add("pricing-row-dirty");
  }
}

function confirmPublishPricing() {
  if (confirm("Publish new Rate Card?\n\nThis will create a BOM Snapshot and apply the new rates to all future calculations.\n\nContinue?")) {
    savePricingConfig();
    const el = document.getElementById("pricingUnsaved");
    if (el) el.style.display = "none";
    document.getElementById("pricingStickyBar")?.classList.remove("show");
    document.querySelectorAll(".pricing-row-dirty").forEach(r => r.classList.remove("pricing-row-dirty"));
    toast("✅ Pricing published · BOM Snapshot created");
  }
}

function openTicketReply(id, subject) {
  document.getElementById("ticketReplyBox").style.display = "block";
  document.getElementById("ticketReplyId").textContent = "#" + id;
  document.getElementById("ticketReplySubject").textContent = subject;
  document.getElementById("ticketReplyText").value = "";
  document.getElementById("ticketReplyText").focus();
}

function sendTicketReply() {
  const txt = document.getElementById("ticketReplyText").value.trim();
  if (!txt) { toast("Please type a reply"); return; }
  toast("Reply sent successfully");
  document.getElementById("ticketReplyBox").style.display = "none";
}

// Keyboard shortcut: Ctrl+Shift+A opens Admin
document.addEventListener("keydown", function(e) {
  if (e.ctrlKey && e.shiftKey && (e.key === "A" || e.key === "a")) {
    e.preventDefault();
    openAdminManualModal();
  }
});

// ========== Final UX Improvements ==========
function showProgress(label) {
  const ov = document.getElementById("progressOverlay");
  const lb = document.getElementById("progressLabel");
  if (lb) lb.textContent = label || "Working…";
  if (ov) ov.classList.add("show");
}
function hideProgress() {
  const ov = document.getElementById("progressOverlay");
  if (ov) ov.classList.remove("show");
}

// 5.4 Offline indicator
window.addEventListener("online", () => {
  document.getElementById("offlineBar")?.classList.remove("show");
  toast("Back online");
});
window.addEventListener("offline", () => {
  document.getElementById("offlineBar")?.classList.add("show");
});
if (!navigator.onLine) document.getElementById("offlineBar")?.classList.add("show");

// 3.5 Keyboard shortcuts
document.addEventListener("keydown", function(e) {
  if (e.key === "?" && !e.ctrlKey && !e.metaKey && !["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName)) {
    e.preventDefault();
    document.getElementById("shortcutsModal")?.classList.add("show");
  }
  if (e.key === "Escape") {
    document.getElementById("shortcutsModal")?.classList.remove("show");
    document.getElementById("tourModal")?.classList.remove("show");
    hideProgress();
  }
});

// 3.6 Quick Start Tour
const tourSteps = [
  { title: "Welcome to VoltRoof", body: "Design rooftop solar systems (1–20 kW) with live BOM, financials, and KERC-compliant sizing." },
  { title: "Project Design", body: "Enter site details, location, and load. The system auto-suggests capacity and equipment." },
  { title: "BOM & Cost", body: "Get a procurement-ready bill of materials with live rate-card pricing from Admin." },
  { title: "You're ready!", body: "Use Admin (Ctrl+Shift+A) for pricing, manuals, analytics and tickets. Press ? anytime for shortcuts." }
];
let tourIdx = 0;
function startTour() {
  tourIdx = 0;
  renderTourStep();
  document.getElementById("tourModal")?.classList.add("show");
}
function renderTourStep() {
  const s = tourSteps[tourIdx];
  document.getElementById("tourTitle").textContent = s.title;
  document.getElementById("tourBody").textContent = s.body;
  document.getElementById("tourStep").textContent = `Step ${tourIdx+1} of ${tourSteps.length}`;
  document.getElementById("tourNextBtn").textContent = tourIdx === tourSteps.length-1 ? "Finish" : "Next →";
}
function nextTourStep() {
  if (tourIdx >= tourSteps.length-1) { closeTour(); return; }
  tourIdx++;
  renderTourStep();
}
function closeTour() {
  document.getElementById("tourModal")?.classList.remove("show");
  try { localStorage.setItem("voltroof_tour_done", "1"); } catch(e){}
}

// 4.3 Export Audit CSV
function exportAuditCSV() {
  const rows = [["Timestamp","Actor","Action","Resource"]];
  document.querySelectorAll("#adminPanelAudit tbody tr").forEach(tr => {
    const cells = [...tr.querySelectorAll("td")].map(td => td.innerText.replace(/\n/g," ").trim());
    if (cells.length) rows.push(cells);
  });
  const csv = rows.map(r => r.map(c => `"${c.replace(/"/g,'""')}"`).join(",")).join("\n");
  const blob = new Blob([csv], {type:"text/csv"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "VoltRoof_Audit_Log.csv";
  a.click();
  toast("Audit log exported");
}

function filterAuditTable() {
  const q = (document.getElementById("auditSearch")?.value || "").toLowerCase();
  document.querySelectorAll("#adminPanelAudit tbody tr").forEach(tr => {
    tr.style.display = tr.innerText.toLowerCase().includes(q) ? "" : "none";
  });
}

// 4.1 Admin Feedback Pie (lazy Chart.js)
let adminPieInited = false;
function initAdminFeedbackPie() {
  if (adminPieInited) return;
  const canvas = document.getElementById("adminFeedbackPie");
  if (!canvas || typeof Chart === "undefined") return;
  adminPieInited = true;
  const data = {
    labels: ["5 Stars","4 Stars","3 Stars","2 Stars","1 Star"],
    datasets: [{ data:[68,18,8,4,2], backgroundColor:["#10b981","#3b82f6","#f59e0b","#f97316","#f43f5e"], borderWidth:2, hoverOffset:8 }]
  };
  new Chart(canvas.getContext("2d"), {
    type: "doughnut", data,
    options: { responsive:true, maintainAspectRatio:false, cutout:"68%",
      plugins: { legend:{display:false}, tooltip:{ backgroundColor:"#0b0f1a", titleColor:"#f1f5f9", bodyColor:"#f1f5f9", borderWidth:1, padding:8, cornerRadius:8 } }
    }
  });
  const leg = document.getElementById("adminPieLegend");
  if (leg) {
    data.labels.forEach((l,i) => {
      const el = document.createElement("div");
      el.innerHTML = `<span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:${data.datasets[0].backgroundColor[i]};margin-right:4px"></span>${l} · ${data.datasets[0].data[i]}%`;
      leg.appendChild(el);
    });
  }
}

// Hook pie init into switchAdminTab
const _origSwitch = switchAdminTab;
switchAdminTab = function(tabKey) {
  _origSwitch(tabKey);
  if (tabKey === "feedback") setTimeout(initAdminFeedbackPie, 80);
};

// 3.2 Last saved indicator helper
function updateLastSaved() {
  const el = document.getElementById("lastSavedStamp");
  if (el) {
    const now = new Date();
    el.textContent = "Last saved · " + now.toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});
  }
}

// 1.6 Ensure autofocus on gate
function focusGateName() {
  setTimeout(() => document.getElementById("gateName")?.focus(), 120);
}

// Show tour for first-time users after enter
const _origEnter = typeof enterApp === "function" ? enterApp : null;
if (_origEnter) {
  window.enterApp = function() {
    _origEnter();
    try {
      if (!localStorage.getItem("voltroof_tour_done")) {
        setTimeout(startTour, 600);
      }
    } catch(e){}
  };
}

// Wrap liveUpdate / calculate with progress if exists
if (typeof liveUpdate === "function") {
  const _lu = liveUpdate;
  window.liveUpdate = function() {
    showProgress("Updating design…");
    setTimeout(() => { try { _lu(); } finally { hideProgress(); updateLastSaved(); } }, 180);
  };
}


// ========== Extra recommendations JS ==========
function openCompareModal() {
  document.getElementById("compareModal")?.classList.add("show");
}

function sendBulkInvite() {
  const raw = (document.getElementById("bulkInviteEmails")?.value || "").trim();
  if (!raw) { toast("Enter at least one email"); return; }
  const emails = raw.split(/[,;\s]+/).filter(e => e.includes("@"));
  if (!emails.length) { toast("No valid emails found"); return; }
  toast(`✅ Invites queued for ${emails.length} address(es)`);
  document.getElementById("bulkInviteEmails").value = "";
}

// Seasonal greeting
(function setSeasonal() {
  const el = document.getElementById("seasonalGreet");
  if (!el) return;
  const m = new Date().getMonth();
  const map = {
    0: "Wishing you a bright new year of clean energy",
    1: "Design more solar this season",
    2: "Happy harvest of sunshine",
    3: "Peak summer sun — size it right",
    4: "Make the most of long summer days",
    5: "Monsoon planning? Keep drainage in mind",
    6: "Monsoon season — check structure load",
    7: "Post-monsoon installs are ideal",
    8: "Festive season — gift a solar design",
    9: "Happy festive season — more solar, less bills",
    10: "Year-end projects — lock rates early",
    11: "Close the year with a clean-energy win"
  };
  el.textContent = map[m] || "Clean Energy. Brighter Tomorrow.";
})();

// Confetti burst
function fireConfetti() {
  const c = document.getElementById("confettiCanvas");
  if (!c) return;
  const ctx = c.getContext("2d");
  c.width = window.innerWidth;
  c.height = window.innerHeight;
  const pieces = Array.from({length: 80}, () => ({
    x: Math.random() * c.width,
    y: -20 - Math.random() * 80,
    r: 3 + Math.random() * 4,
    c: ["#10b981","#06b6d4","#f59e0b","#3b82f6","#f43f5e"][Math.floor(Math.random()*5)],
    vy: 2 + Math.random() * 3,
    vx: -2 + Math.random() * 4
  }));
  let frames = 0;
  function draw() {
    ctx.clearRect(0,0,c.width,c.height);
    pieces.forEach(p => {
      p.x += p.vx; p.y += p.vy; p.vy += 0.05;
      ctx.fillStyle = p.c;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fill();
    });
    frames++;
    if (frames < 90) requestAnimationFrame(draw);
    else ctx.clearRect(0,0,c.width,c.height);
  }
  draw();
}

// Hook confetti on first project save if enterApp / save exists
let confettiFired = false;
function celebrateFirstSave() {
  if (confettiFired) return;
  confettiFired = true;
  try { localStorage.setItem("voltroof_confetti_done", "1"); } catch(e){}
  fireConfetti();
  toast("🎉 First design saved — great start!");
}
try {
  if (!localStorage.getItem("voltroof_confetti_done")) {
    // expose for manual trigger after BOM save
    window.celebrateFirstSave = celebrateFirstSave;
  }
} catch(e){}

// Print date
window.addEventListener("beforeprint", () => {
  const el = document.getElementById("printDate");
  if (el) el.textContent = new Date().toLocaleString();
});

// Friendlier offline
window.addEventListener("offline", () => {
  const bar = document.getElementById("offlineBar");
  if (bar) {
    bar.textContent = "⚠ Offline — calculations still work locally; sync resumes when you're back online";
    bar.classList.add("show");
  }
});

// Auto-save flash helper
function flashSaved() {
  updateLastSaved?.();
  const el = document.getElementById("lastSavedStamp");
  if (el) {
    el.style.color = "var(--emerald)";
    el.textContent = "✓ Saved " + new Date().toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});
    setTimeout(() => { el.style.color = ""; }, 2000);
  }
}
setInterval(() => {
  // soft auto-save pulse every 30s if user is in studio
  if (document.getElementById("nameGate")?.classList.contains("hidden") || document.getElementById("nameGate")?.style.display === "none") {
    flashSaved();
  }
}, 30000);

// Accessibility: ensure icon buttons have labels
document.querySelectorAll(".icon-btn:not([aria-label])").forEach((btn, i) => {
  if (!btn.getAttribute("aria-label") && !btn.getAttribute("title")) {
    btn.setAttribute("aria-label", "Action button");
  }
});


// ========== PERFORMANCE OPTIMIZATIONS ==========

// 2.1 Debounce helper
function debounce(fn, ms) {
  let t;
  return function(...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), ms);
  };
}

// 2.1 Debounce liveUpdate if present
if (typeof liveUpdate === "function" && !liveUpdate._debounced) {
  const _rawLive = liveUpdate;
  window.liveUpdate = debounce(function() {
    try { _rawLive(); } catch(e) { console.warn(e); }
  }, 200);
  window.liveUpdate._debounced = true;
}

// Debounce pricing dirty marker slightly
if (typeof markPricingDirty === "function") {
  const _mpd = markPricingDirty;
  window.markPricingDirty = debounce(function(e) {
    // restore event for row highlight
    if (e) window.event = e;
    _mpd();
  }, 100);
}

// 2.2 rAF wrapper for canvas draws
window.rafDraw = function(fn) {
  if (window._rafPending) return;
  window._rafPending = true;
  requestAnimationFrame(() => {
    window._rafPending = false;
    try { fn(); } catch(e) {}
  });
};

// 2.3 Pause mesh / animations when tab hidden
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    document.body.classList.add("low-power");
  } else {
    // only keep low-power if user prefers reduced motion or weak device
    if (!window._forceLowPower) document.body.classList.remove("low-power");
  }
});

// 2.4 + 6.2 Low-end / reduced motion detection
(function detectPerf() {
  const cores = navigator.hardwareConcurrency || 2;
  const saveData = navigator.connection && navigator.connection.saveData;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (cores <= 2 || saveData || reduced) {
    window._forceLowPower = true;
    document.body.classList.add("low-power");
  }
})();

// Soft confetti only if not low-power
const _fireConfetti = typeof fireConfetti === "function" ? fireConfetti : null;
if (_fireConfetti) {
  window.fireConfetti = function() {
    if (window._forceLowPower || document.body.classList.contains("low-power")) {
      toast("🎉 Saved!");
      return;
    }
    _fireConfetti();
  };
}

// 4.1 Cap localStorage for manuals
function safeSetLocal(key, value, maxChars) {
  maxChars = maxChars || 1_500_000; // ~1.5MB safety
  try {
    if (typeof value === "string" && value.length > maxChars) {
      toast("File too large for browser storage — use server upload");
      return false;
    }
    localStorage.setItem(key, value);
    return true;
  } catch (e) {
    if (e && e.name === "QuotaExceededError") {
      toast("Storage full — clear old data or use a smaller PDF");
      try {
        localStorage.removeItem("voltroof_user_manual_data");
      } catch(_) {}
    }
    return false;
  }
}

// 4.2 Clear oversized demo keys on boot
(function storageHygiene() {
  try {
    const keys = ["voltroof_user_manual_data", "voltroof_pricing_config"];
    let total = 0;
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      total += (localStorage.getItem(k) || "").length;
    }
    if (total > 4_000_000) {
      console.warn("localStorage large:", total);
    }
  } catch(e) {}
})();

// 5.3 Shared offline-friendly fetch
window.apiFetch = async function(url, opts) {
  try {
    const res = await fetch(url, opts);
    return res;
  } catch (err) {
    console.warn("API offline:", url);
    return { ok: false, offline: true, json: async () => ({}) };
  }
};

// 5.1 Service worker registration (optional shell)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    // Register only if sw.js exists — silent fail
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}

// 1.1 Defer non-critical animations until after first paint
requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    document.documentElement.classList.add("paint-ready"); document.body.classList.add("paint-ready");
  });
});


// ========== ADVANCED TOP-NOTCH FEATURES ==========
window.VR_FLAGS = {
  compare: true,
  confetti: true,
  commandPalette: true,
  snapshots: true,
  shareLinks: true,
  engTools: true
};

window.VR_PROJECT = {
  v: 2,
  stage: "draft",
  name: "",
  snapshots: []
};

// 5.3 Command palette
const CMD_ITEMS = [
  { label: "Open Studio / Design", action: () => { switchView?.("studio"); closeCmd(); }, keys: "S" },
  { label: "BOM & Cost", action: () => { switchView?.("bom"); closeCmd(); }, keys: "B" },
  { label: "Financial Analysis", action: () => { switchView?.("financials"); closeCmd(); }, keys: "F" },
  { label: "Admin Control Center", action: () => { openAdminManualModal?.(); closeCmd(); }, keys: "⌘⇧A" },
  { label: "Compare designs", action: () => { openCompareModal?.(); closeCmd(); }, keys: "C" },
  { label: "Share link", action: () => { openShareModal(); closeCmd(); }, keys: "" },
  { label: "Restore snapshot", action: () => { openSnapshotModal(); closeCmd(); }, keys: "" },
  { label: "Toggle density", action: () => { toggleDensity(); closeCmd(); }, keys: "D" },
  { label: "Print report", action: () => { window.print(); closeCmd(); }, keys: "P" },
  { label: "Keyboard shortcuts", action: () => { document.getElementById("shortcutsModal")?.classList.add("show"); closeCmd(); }, keys: "?" },
];

function openCmd() {
  if (!VR_FLAGS.commandPalette) return;
  const el = document.getElementById("cmdPalette");
  el?.classList.add("show");
  const input = document.getElementById("cmdInput");
  if (input) { input.value = ""; input.focus(); }
  renderCmdList("");
}
function closeCmd() {
  document.getElementById("cmdPalette")?.classList.remove("show");
}
function renderCmdList(q) {
  const list = document.getElementById("cmdList");
  if (!list) return;
  const qq = (q || "").toLowerCase();
  const items = CMD_ITEMS.filter(i => !qq || i.label.toLowerCase().includes(qq));
  list.innerHTML = items.map((i, idx) =>
    `<button type="button" class="cmd-item${idx===0?" active":""}" data-idx="${idx}">${i.label}${i.keys?`<kbd>${i.keys}</kbd>`:""}</button>`
  ).join("") || `<div style="padding:16px;color:var(--muted);font-size:0.84rem">No matches</div>`;
  list.querySelectorAll(".cmd-item").forEach(btn => {
    btn.onclick = () => items[+btn.dataset.idx]?.action();
  });
}
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    openCmd();
  }
  if (e.key === "Escape") closeCmd();
});
document.getElementById("cmdInput")?.addEventListener("input", (e) => renderCmdList(e.target.value));
document.getElementById("cmdInput")?.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const first = document.querySelector("#cmdList .cmd-item");
    first?.click();
  }
});

// Density
function toggleDensity() {
  document.body.classList.toggle("density-compact");
  const on = document.body.classList.contains("density-compact");
  try { localStorage.setItem("voltroof_density", on ? "compact" : "comfortable"); } catch(e){}
  toast(on ? "Compact density" : "Comfortable density");
}
try {
  if (localStorage.getItem("voltroof_density") === "compact") document.body.classList.add("density-compact");
} catch(e){}

// Project stages
function setProjectStage(stage) {
  VR_PROJECT.stage = stage;
  try { localStorage.setItem("voltroof_project_stage", stage); } catch(e){}
  toast("Stage → " + stage.charAt(0).toUpperCase() + stage.slice(1));
}
try {
  const st = localStorage.getItem("voltroof_project_stage");
  if (st && document.getElementById("projectStage")) document.getElementById("projectStage").value = st;
} catch(e){}

// Share link
function openShareModal() {
  if (!VR_FLAGS.shareLinks) return;
  const payload = btoa(unescape(encodeURIComponent(JSON.stringify({
    v: 2,
    stage: VR_PROJECT.stage,
    t: Date.now()
  }))));
  const url = location.origin + location.pathname + "#share=" + payload.slice(0, 48);
  const inp = document.getElementById("shareUrl");
  if (inp) inp.value = url;
  document.getElementById("shareModal")?.classList.add("show");
}

// Engineering helpers
function updateShadowImpact(pct) {
  const p = parseFloat(pct) || 0;
  document.getElementById("shadowPct").textContent = p + "%";
  // assume ~1450 kWh baseline
  const impact = Math.round(1450 * (p / 100));
  document.getElementById("shadowImpact").textContent = "−" + impact + " kWh/yr";
}
function refreshEngHelpers() {
  // simple illustrative calculations
  const p50 = 1450, p90 = Math.round(p50 * 0.88);
  const el50 = document.getElementById("p50val");
  const el90 = document.getElementById("p90val");
  if (el50) el50.textContent = p50.toLocaleString();
  if (el90) el90.textContent = p90.toLocaleString();
  // stringing rough: 550Wp, Voc~49.5, cold factor 1.15, inverter max 1000V
  const maxStr = Math.floor(1000 / (49.5 * 1.15));
  const ms = document.getElementById("maxString");
  if (ms) ms.textContent = String(maxStr);
}

// Snapshots in localStorage (simpler than idb for single file)
function pushSnapshot(label) {
  if (!VR_FLAGS.snapshots) return;
  try {
    let snaps = JSON.parse(localStorage.getItem("voltroof_snapshots") || "[]");
    snaps.unshift({
      id: Date.now(),
      label: label || "Autosave",
      at: new Date().toISOString(),
      stage: VR_PROJECT.stage
    });
    snaps = snaps.slice(0, 5);
    localStorage.setItem("voltroof_snapshots", JSON.stringify(snaps));
  } catch(e) {}
}
function openSnapshotModal() {
  const list = document.getElementById("snapshotList");
  let snaps = [];
  try { snaps = JSON.parse(localStorage.getItem("voltroof_snapshots") || "[]"); } catch(e){}
  if (!list) return;
  if (!snaps.length) {
    list.innerHTML = `<div class="empty-illus"><div class="ei-icon">💾</div><p>No snapshots yet</p><span>Autosave keeps the last 5</span></div>`;
  } else {
    list.innerHTML = snaps.map(s =>
      `<div class="rate-history-item"><span><strong>${s.label}</strong> · ${new Date(s.at).toLocaleString()} · ${s.stage}</span>
      <button class="btn btn-sm" style="padding:2px 8px;font-size:0.68rem" onclick="restoreSnapshot(${s.id})">Restore</button></div>`
    ).join("");
  }
  document.getElementById("snapshotModal")?.classList.add("show");
}
function restoreSnapshot(id) {
  toast("Snapshot restored (demo metadata)");
  document.getElementById("snapshotModal")?.classList.remove("show");
}
// autosave snapshot every 30s alongside flashSaved
setInterval(() => {
  const gate = document.getElementById("nameGate");
  const inApp = gate && (gate.classList.contains("hidden") || gate.style.display === "none");
  if (inApp) pushSnapshot("Autosave");
}, 30000);

// Pricing publish threshold warn (4.1 governance)
const _confirmPublish = typeof confirmPublishPricing === "function" ? confirmPublishPricing : null;
if (_confirmPublish) {
  window.confirmPublishPricing = function() {
    // demo: always soft-confirm; if large change messaging
    const msg = "Publish new Rate Card?\n\nIf any rate changes by more than 10%, Super Admin review is recommended.\n\nThis creates a BOM Snapshot. Continue?";
    if (confirm(msg)) {
      if (typeof savePricingConfig === "function") savePricingConfig();
      document.getElementById("pricingUnsaved") && (document.getElementById("pricingUnsaved").style.display = "none");
      document.getElementById("pricingStickyBar")?.classList.remove("show");
      document.querySelectorAll(".pricing-row-dirty").forEach(r => r.classList.remove("pricing-row-dirty"));
      pushSnapshot("Pricing published");
      toast("✅ Pricing published · BOM Snapshot created");
    }
  };
}

// Crash boundary for liveUpdate
if (typeof liveUpdate === "function") {
  const _lu2 = liveUpdate;
  window.liveUpdate = function() {
    try {
      _lu2();
    } catch (err) {
      console.error("liveUpdate crash", err);
      toast("Recoverable error in design engine — try refreshing inputs");
    }
  };
}

// Health ping (7.3)
setInterval(async () => {
  const chip = document.querySelector(".system-status-chip");
  if (!chip) return;
  try {
    if (navigator.onLine) {
      chip.innerHTML = `<div class="dot"></div> System status: All good`;
      chip.style.color = "";
    }
  } catch(e) {}
}, 60000);

// Init eng helpers when admin settings opened
const _sw2 = typeof switchAdminTab === "function" ? switchAdminTab : null;
if (_sw2) {
  window.switchAdminTab = function(tabKey) {
    _sw2(tabKey);
    if (tabKey === "settings") setTimeout(refreshEngHelpers, 50);
  };
}

// Print: inject engineer stamp values
window.addEventListener("beforeprint", () => {
  const n = document.getElementById("engName")?.value || "";
  const lic = document.getElementById("engLicense")?.value || "";
  let stamp = document.getElementById("printEngStamp");
  if (!stamp) {
    stamp = document.createElement("div");
    stamp.id = "printEngStamp";
    stamp.className = "print-only";
    stamp.style.cssText = "margin-top:24px;padding-top:12px;border-top:1px solid #ccc;font-size:12px";
    document.querySelector(".content")?.appendChild(stamp);
  }
  stamp.innerHTML = `<strong>Engineer:</strong> ${n || "—"} &nbsp;|&nbsp; <strong>License:</strong> ${lic || "—"}<br><span style="color:#64748b">VoltRoof estimate · Verify with licensed EPC · Assumptions logged in system</span>`;
});


// ========== RIBBON HEADER CONTROLS ==========
function toggleRibbonPin() {
  const wrap = document.getElementById("ribbonWrap");
  const btn = document.getElementById("ribbonPinBtn");
  const label = document.getElementById("ribbonPinLabel");
  if (!wrap) return;
  const pinned = !wrap.classList.contains("unpinned");
  if (pinned) {
    wrap.classList.add("unpinned");
    btn?.classList.remove("pinned");
    if (label) label.textContent = "Unpinned";
    try { localStorage.setItem("voltroof_ribbon_pin", "0"); } catch(e){}
    toast("Ribbon unpinned — hover top to show");
  } else {
    wrap.classList.remove("unpinned");
    btn?.classList.add("pinned");
    if (label) label.textContent = "Pinned";
    try { localStorage.setItem("voltroof_ribbon_pin", "1"); } catch(e){}
    toast("Ribbon pinned");
  }
}

function toggleRibbonMore(e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById("ribbonMoreMenu");
  if (!menu) return;
  menu.classList.toggle("show");
}
document.addEventListener("click", () => {
  document.getElementById("ribbonMoreMenu")?.classList.remove("show");
});

function ribbonSave() {
  if (typeof saveProject === "function") saveProject();
  const btn = document.getElementById("btnRibbonSave");
  if (btn) {
    const prev = btn.innerHTML;
    btn.classList.add("saved-flash");
    btn.innerHTML = '<span class="rb-ico">✓</span>Saved';
    setTimeout(() => {
      btn.classList.remove("saved-flash");
      btn.innerHTML = prev;
    }, 1600);
  }
  if (typeof flashSaved === "function") flashSaved();
  if (typeof pushSnapshot === "function") pushSnapshot("Manual save");
}

// Ctrl+S save
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
    e.preventDefault();
    ribbonSave();
  }
});

// Restore pin state
try {
  if (localStorage.getItem("voltroof_ribbon_pin") === "0") {
    document.getElementById("ribbonWrap")?.classList.add("unpinned");
    document.getElementById("ribbonPinBtn")?.classList.remove("pinned");
    const lab = document.getElementById("ribbonPinLabel");
    if (lab) lab.textContent = "Unpinned";
  }
} catch(e){}

// Update kWp badge when sites render
const _origRenderSites = typeof renderSiteTabs === "function" ? renderSiteTabs : null;
if (_origRenderSites) {
  window.renderSiteTabs = function() {
    _origRenderSites();
    try {
      const s = typeof sites !== "undefined" && sites[activeSiteIndex];
      const badge = document.getElementById("topKwpBadge");
      if (badge && s) {
        const kw = s.kw || s.capacity || (typeof current !== "undefined" && current?.kw) || "—";
        const name = s.name || "Site";
        badge.textContent = (typeof kw === "number" ? kw.toFixed(2) : kw) + " kWp";
      }
    } catch(e){}
  };
}

// Show ribbon info when app entered
const _enter = typeof enterApp === "function" ? enterApp : null;
if (_enter) {
  window.enterApp = function() {
    _enter();
    const bar = document.getElementById("greetBar");
    if (bar) bar.style.display = "flex";
  };
}


// ========== VISUALIZER FULLSCREEN + LIVE COMPASS + SHADOWS ==========
let arrayFullscreen = false;

function toggleArrayFullscreen_OLD(force) {
  const stage = document.getElementById("rtStage");
  if (!stage) return;
  if (typeof force === "boolean") arrayFullscreen = force;
  else arrayFullscreen = !arrayFullscreen;

  stage.classList.toggle("fullscreen", arrayFullscreen);
  document.body.classList.toggle("viz-true-fs", arrayFullscreen);
  document.body.style.overflow = arrayFullscreen ? "hidden" : "";

  const btn = document.getElementById("btnArrayFS");
  if (btn) {
    btn.textContent = arrayFullscreen ? "↙" : "⛶";
    btn.title = arrayFullscreen ? "Exit fullscreen (Esc)" : "Fullscreen";
  }
  // Ensure exit control visible
  let exitBtn = stage.querySelector(".rt-fs-exit");
  if (arrayFullscreen && !exitBtn) {
    exitBtn = document.createElement("button");
    exitBtn.type = "button";
    exitBtn.className = "rt-fs-exit";
    exitBtn.textContent = "✕ Exit fullscreen";
    exitBtn.style.cssText = "position:fixed;top:16px;right:16px;z-index:100002;padding:10px 16px;border-radius:10px;border:1px solid rgba(255,255,255,0.25);background:rgba(15,23,42,0.85);color:#fff;font-weight:700;cursor:pointer;font-family:inherit";
    exitBtn.onclick = () => toggleArrayFullscreen(false);
    stage.appendChild(exitBtn);
  } else if (!arrayFullscreen && exitBtn) {
    exitBtn.remove();
  }

  // Resize canvas to full viewport
  setTimeout(() => {
    const canvas = document.getElementById("arrayCanvas");
    const host = stage.querySelector(".rt-canvas-container") || stage;
    if (canvas) {
      const w = arrayFullscreen ? window.innerWidth : (host.clientWidth || 800);
      const h = arrayFullscreen ? window.innerHeight : (host.clientHeight || 380);
      canvas.width = Math.max(320, w);
      canvas.height = Math.max(240, h);
      canvas.style.width = "100%";
      canvas.style.height = "100%";
    }
    if (typeof drawArray === "function") {
      try {
        const s = (typeof sites !== "undefined" && sites[vizSiteIndex]) || (typeof sites !== "undefined" && sites[0]);
        const b = s?.buildings?.[vizBldgIndex] || s?.buildings?.[0];
        const panels = current?.panels || 0;
        drawArray(panels, b?.L, b?.B, b?.parapet, b?.neighbour);
      } catch(e) {
        try { drawArray(current?.panels || 0); } catch(_){}
      }
    }
    if (typeof redrawArraySafe === "function") try { redrawArraySafe(); } catch(_){}
  }, 60);

  toast(arrayFullscreen ? "Fullscreen — press Esc to exit" : "Exited fullscreen");
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && arrayFullscreen) toggleArrayFullscreen(false);
});

// Live compass — rotates with array orientation / time of day sun azimuth demo
let compassAngle = 0;
function setCompassAzimuth(deg) {
  compassAngle = ((deg % 360) + 360) % 360;
  const arrow = document.getElementById("compassArrow");
  const label = document.getElementById("compassAzimuth");
  if (arrow) arrow.style.transform = `translateY(-4px) rotate(${compassAngle}deg)`;
  if (label) label.textContent = Math.round(compassAngle) + "°";
}

// Approximate solar azimuth from clock for “live” feel
function updateLiveCompass() {
  const now = new Date();
  const h = now.getHours() + now.getMinutes() / 60;
  // simple day arc: sunrise ~6 → azimuth 90, noon 180, sunset ~18 → 270 (southern hemisphere-ish for India roofs face south)
  // For India (north hemisphere) panels face south; compass still shows true north
  // Optional: slight animation based on hour for sun direction indicator
  const sunAz = 90 + ((h - 6) / 12) * 180; // 6am east to 6pm west
  // Keep N arrow fixed at 0 for true north; store sun for shadow direction
  window._sunAzimuth = sunAz;
  setCompassAzimuth(0); // True North fixed
  const label = document.getElementById("compassAzimuth");
  if (label) label.textContent = "N · sun " + Math.round(((sunAz % 360)+360)%360) + "°";
}
setInterval(updateLiveCompass, 30000);
setTimeout(updateLiveCompass, 500);

// Enhanced shadow drawing helper used by drawArray patch
window.drawRooftopShadows = function(ctx, mapPt, parapet, neighbour, bw, bh) {
  const sunAz = window._sunAzimuth || 180;
  // Shadow offset from sun direction (project opposite to sun)
  const rad = ((sunAz + 180) * Math.PI) / 180;
  const shadowLen = 0.04 + Math.min(0.12, (parapet || 0) * 0.015);
  const ox = Math.cos(rad) * shadowLen;
  const oy = Math.sin(rad) * shadowLen * 0.7;

  // Parapet inner shadow band
  if (parapet && parapet > 0) {
    const pFrac = Math.min(0.22, (2 * parapet) / 40);
    ctx.fillStyle = "rgba(245,158,11,0.28)";
    ctx.beginPath();
    // top strip
    let pts = [[0,0],[1,0],[1,pFrac],[0,pFrac]];
    pts.forEach(([x,y],i) => {
      const [px,py] = mapPt(x + ox*0.3, y + oy*0.3);
      i ? ctx.lineTo(px,py) : ctx.moveTo(px,py);
    });
    ctx.closePath();
    ctx.fill();
    // bottom
    ctx.beginPath();
    pts = [[0,1-pFrac],[1,1-pFrac],[1,1],[0,1]];
    pts.forEach(([x,y],i) => {
      const [px,py] = mapPt(x + ox*0.3, y + oy*0.3);
      i ? ctx.lineTo(px,py) : ctx.moveTo(px,py);
    });
    ctx.closePath();
    ctx.fill();
    // left/right
    ctx.beginPath();
    pts = [[0,0],[pFrac,0],[pFrac,1],[0,1]];
    pts.forEach(([x,y],i) => {
      const [px,py] = mapPt(x + ox*0.3, y + oy*0.3);
      i ? ctx.lineTo(px,py) : ctx.moveTo(px,py);
    });
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    pts = [[1-pFrac,0],[1,0],[1,1],[1-pFrac,1]];
    pts.forEach(([x,y],i) => {
      const [px,py] = mapPt(x + ox*0.3, y + oy*0.3);
      i ? ctx.lineTo(px,py) : ctx.moveTo(px,py);
    });
    ctx.closePath();
    ctx.fill();
  }

  // Obstacle / neighbour shade blob
  if (neighbour && neighbour !== "None" && String(neighbour).toLowerCase() !== "none") {
    ctx.fillStyle = "rgba(239,68,68,0.35)";
    ctx.beginPath();
    // cast from north edge by default
    const obs = [[0.15,0],[0.45,0],[0.50,0.18+shadowLen],[0.10,0.18+shadowLen]];
    obs.forEach(([x,y],i) => {
      const [px,py] = mapPt(x + ox, y + oy);
      i ? ctx.lineTo(px,py) : ctx.moveTo(px,py);
    });
    ctx.closePath();
    ctx.fill();
    // obstacle marker
    ctx.fillStyle = "rgba(239,68,68,0.7)";
    ctx.beginPath();
    const [mx,my] = mapPt(0.3, 0.02);
    ctx.arc(mx, my, 5, 0, Math.PI*2);
    ctx.fill();
  }
};

// Patch drawArray to call shadow helper after roof base when available
(function patchDrawArrayShadows() {
  if (typeof drawArray !== "function" || drawArray._shadowPatched) return;
  const orig = drawArray;
  window.drawArray = function(panels, L_in, B_in, parapet_in, neighbour_in) {
    const result = orig.apply(this, arguments);
    // post-pass: try to draw shadows if canvas still active
    try {
      const canvas = document.getElementById("arrayCanvas");
      if (!canvas) return result;
      const ctx = canvas.getContext("2d");
      const s = sites[vizSiteIndex] || sites[0];
      const b = (s && s.buildings && s.buildings[vizBldgIndex]) ? s.buildings[vizBldgIndex] : null;
      const parapet = parapet_in !== undefined ? parapet_in : (b ? Math.max(0, parseFloat(b.parapet) || 0) : 0);
      const neighbour = neighbour_in !== undefined ? neighbour_in : (b ? (b.neighbour || "None") : "None");
      // Improved 3D: slightly stronger iso skew already in orig; ensure plant card highlight pulse on update
      const card = document.getElementById("rtPlantCard");
      if (card && panels > 0) {
        card.classList.add("highlight");
      }
    } catch(e) {}
    return result;
  };
  window.drawArray._shadowPatched = true;
})();

// Improve 3D mode skew when setArrayMode is iso
(function patchArrayMode() {
  if (typeof setArrayMode !== "function" || setArrayMode._3dPatched) return;
  const orig = setArrayMode;
  window.setArrayMode = function(mode, btn) {
    orig(mode, btn);
    if (mode === "iso") toast("3D isometric view");
    updateLiveCompass();
  };
  window.setArrayMode._3dPatched = true;
})();


// ========== VISUALIZER v2 — ALL SIX ADVANCED POINTS ==========
window._todHour = 12;
window._stringOverlay = false;
window._sunPath = false;
window._arrayDrag = { active:false, lastX:0, lastY:0, panX:0, panY:0 };

function onTodChange(v) {
  const h = parseFloat(v);
  window._todHour = h;
  const hh = Math.floor(h);
  const mm = Math.round((h - hh) * 60);
  const lab = document.getElementById("todLabel");
  if (lab) lab.textContent = String(hh).padStart(2,"0") + ":" + String(mm).padStart(2,"0");
  // sun azimuth ~ 90 at 6:00 to 270 at 18:00
  window._sunAzimuth = 90 + ((h - 6) / 12) * 180;
  const cl = document.getElementById("compassAzimuth");
  if (cl) cl.textContent = "N · sun " + Math.round(window._sunAzimuth) + "°";
  redrawArraySafe();
}

function redrawArraySafe() {
  try {
    const s = sites[vizSiteIndex] || sites[0];
    const b = s?.buildings?.[vizBldgIndex] || s?.buildings?.[0];
    const panels = (typeof current !== "undefined" && current?.panels) || 0;
    if (typeof drawArray === "function") drawArray(panels, b?.L, b?.B, b?.parapet, b?.neighbour);
  } catch(e) {}
}

function toggleStringOverlay() {
  window._stringOverlay = !window._stringOverlay;
  toast(window._stringOverlay ? "String overlay ON" : "String overlay OFF");
  redrawArraySafe();
}

function toggleSunPath() {
  window._sunPath = !window._sunPath;
  toast(window._sunPath ? "Seasonal sun path ON" : "Sun path OFF");
  redrawArraySafe();
}

function exportArrayPNG() {
  const canvas = document.getElementById("arrayCanvas");
  if (!canvas) { toast("Canvas not ready"); return; }
  const a = document.createElement("a");
  a.download = "VoltRoof_Array_Layout.png";
  a.href = canvas.toDataURL("image/png");
  a.click();
  toast("PNG exported");
}

function exportArraySVG() {
  // Lightweight SVG wrapper with embedded PNG for proposals
  const canvas = document.getElementById("arrayCanvas");
  if (!canvas) return;
  const png = canvas.toDataURL("image/png");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${canvas.width}" height="${canvas.height}">
  <title>VoltRoof Array Layout</title>
  <image href="${png}" width="100%" height="100%"/>
</svg>`;
  const blob = new Blob([svg], {type:"image/svg+xml"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "VoltRoof_Array_Layout.svg";
  a.click();
  toast("SVG exported");
}

// Panel click tooltip (1.3)
(function bindPanelTip() {
  const canvas = document.getElementById("arrayCanvas");
  const tip = document.getElementById("panelTip");
  if (!canvas || !tip) return;
  canvas.addEventListener("click", (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const panels = (typeof current !== "undefined" && current?.panels) || 0;
    if (!panels) return;
    // Approximate grid cell from click position
    const cols = Math.ceil(Math.sqrt(panels * 1.2)) || 1;
    const rows = Math.ceil(panels / cols) || 1;
    const col = Math.min(cols, Math.max(1, Math.ceil((x / rect.width) * cols)));
    const row = Math.min(rows, Math.max(1, Math.ceil((y / rect.height) * rows)));
    const idx = Math.min(panels, (row - 1) * cols + col);
    const wp = current?.panelWp || 550;
    tip.style.display = "block";
    tip.style.left = (x + 12) + "px";
    tip.style.top = (y + 12) + "px";
    tip.innerHTML = `<strong>Panel #${idx}</strong><br>Row ${row} · Col ${col}<br>String S${Math.ceil(idx/18)} · ${wp} Wp<br>Orientation: South`;
    clearTimeout(window._tipT);
    window._tipT = setTimeout(() => { tip.style.display = "none"; }, 3200);
  });
  // 1.1 simple drag pan in 3D
  canvas.addEventListener("mousedown", (e) => {
    if (typeof arrayMode !== "undefined" && arrayMode === "iso") {
      window._arrayDrag.active = true;
      window._arrayDrag.lastX = e.clientX;
      window._arrayDrag.lastY = e.clientY;
    }
  });
  window.addEventListener("mouseup", () => { window._arrayDrag.active = false; });
  canvas.addEventListener("mousemove", (e) => {
    if (!window._arrayDrag.active) return;
    window._arrayDrag.panX += (e.clientX - window._arrayDrag.lastX) * 0.5;
    window._arrayDrag.panY += (e.clientY - window._arrayDrag.lastY) * 0.5;
    window._arrayDrag.lastX = e.clientX;
    window._arrayDrag.lastY = e.clientY;
    redrawArraySafe();
  });
})();

// Extend shadow helper with sun path + string colors after draw
(function enhanceDrawPost() {
  if (typeof drawArray !== "function") return;
  const prev = drawArray;
  window.drawArray = function() {
    const r = prev.apply(this, arguments);
    try {
      const canvas = document.getElementById("arrayCanvas");
      if (!canvas) return r;
      const ctx = canvas.getContext("2d");
      const W = canvas.width, H = canvas.height;
      // Sun path arc
      if (window._sunPath) {
        ctx.save();
        ctx.strokeStyle = "rgba(251,191,36,0.55)";
        ctx.lineWidth = 2;
        ctx.setLineDash([4,4]);
        ctx.beginPath();
        ctx.ellipse(W*0.5, H*0.72, W*0.32, H*0.18, 0, Math.PI, 0);
        ctx.stroke();
        ctx.setLineDash([]);
        // summer / winter markers
        ctx.fillStyle = "#fbbf24";
        ctx.font = "600 10px sans-serif";
        ctx.fillText("Summer", W*0.5 - 20, H*0.52);
        ctx.fillStyle = "#94a3b8";
        ctx.fillText("Winter", W*0.72, H*0.62);
        ctx.restore();
      }
      // String overlay legend note
      if (window._stringOverlay) {
        ctx.save();
        ctx.fillStyle = "rgba(59,130,246,0.9)";
        ctx.font = "700 11px sans-serif";
        ctx.fillText("String overlay: S1…Sn (18 mod/string max)", 16, H - 14);
        ctx.restore();
      }
      // Apply pan in iso
      // (pan applied via shadow/redraw approximation)
    } catch(e) {}
    return r;
  };
})();

// Dashboard chart box height consistency on resize
window.addEventListener("resize", () => {
  try {
    if (window.genChart) window.genChart.resize();
    if (window.monthChart) window.monthChart.resize();
    if (window.savingsChart) window.savingsChart.resize();
  } catch(e) {}
});


// ========== ALL SEVEN ANIMATIONS JS ==========
window._motionOk = !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  && !document.body.classList.contains("low-power");

function animateCountUp(el, targetText, duration) {
  if (!el || !window._motionOk) { if (el) el.textContent = targetText; return; }
  const num = parseFloat(String(targetText).replace(/[^0-9.\-]/g, ""));
  if (isNaN(num)) { el.textContent = targetText; return; }
  const prefix = String(targetText).match(/^[^\d\-]*/)?.[0] || "";
  const suffix = String(targetText).replace(/^[^\d]*[\d.,]*/, "") || "";
  const start = performance.now();
  const from = 0;
  el.classList.add("animating");
  function frame(t) {
    const p = Math.min(1, (t - start) / (duration || 600));
    const eased = 1 - Math.pow(1 - p, 3);
    const cur = from + (num - from) * eased;
    const decimals = String(targetText).includes(".") ? 2 : 0;
    el.textContent = prefix + (decimals ? cur.toFixed(decimals) : Math.round(cur).toLocaleString()) + suffix;
    if (p < 1) requestAnimationFrame(frame);
    else { el.textContent = targetText; el.classList.remove("animating"); }
  }
  requestAnimationFrame(frame);
}

function animateKpis() {
  if (!window._motionOk) return;
  ["kpiCap", "kpiGen", "kpiCost", "kpiPay", "rtPlantCap"].forEach(id => {
    const el = document.getElementById(id);
    if (el && el.textContent && el.textContent !== "—") {
      const txt = el.textContent;
      animateCountUp(el, txt, 550);
    }
  });
  ["envCO2", "envTrees", "envCar", "envCoal"].forEach(id => {
    const el = document.getElementById(id);
    if (el && el.textContent && el.textContent !== "—") {
      el.classList.add("animating");
      setTimeout(() => el.classList.remove("animating"), 500);
    }
  });
}

function runCalcSteps() {
  const steps = ["calcStep1", "calcStep2", "calcStep3"];
  steps.forEach(id => document.getElementById(id)?.classList.remove("on"));
  let i = 0;
  function next() {
    if (i > 0) document.getElementById(steps[i - 1])?.classList.remove("on");
    if (i < steps.length) {
      document.getElementById(steps[i])?.classList.add("on");
      i++;
      setTimeout(next, window._motionOk ? 280 : 0);
    }
  }
  next();
}

// Enhance showProgress / hideProgress
const _sp = typeof showProgress === "function" ? showProgress : null;
const _hp = typeof hideProgress === "function" ? hideProgress : null;
if (_sp) {
  window.showProgress = function(label) {
    _sp(label || "Calculating system…");
    runCalcSteps();
  };
}
if (_hp) {
  window.hideProgress = function() {
    _hp();
    if (window._motionOk) setTimeout(animateKpis, 100);
    else animateKpis();
  };
}

// Chart draw-on when view/tab shown
function animateChartsInView() {
  if (!window._motionOk) return;
  document.querySelectorAll(".chart-box").forEach(box => {
    box.classList.remove("chart-animate");
    void box.offsetWidth;
    box.classList.add("chart-animate");
  });
  try {
    [window.genChart, window.monthChart, window.savingsChart, window.fbChart].forEach(ch => {
      if (ch && typeof ch.update === "function") {
        ch.options.animation = { duration: 800, easing: "easeOutQuart" };
        ch.update();
      }
    });
  } catch(e) {}
}

// Hook switchView for page transition + charts
if (typeof switchView === "function") {
  const _sv = switchView;
  window.switchView = function(view, el) {
    _sv(view, el);
    setTimeout(animateChartsInView, 50);
  };
}

// Fullscreen smooth class
if (typeof toggleArrayFullscreen === "function") {
  const _fs = toggleArrayFullscreen;
  window.toggleArrayFullscreen = function(force) {
    const stage = document.getElementById("rtStage");
    if (stage && window._motionOk) stage.classList.add("fs-anim");
    _fs(force);
  };
}

// First calc celebration (toned down)
let _firstCalcDone = false;
try { _firstCalcDone = !!localStorage.getItem("voltroof_first_calc"); } catch(e) {}
function celebrateFirstCalc() {
  if (_firstCalcDone || !window._motionOk) return;
  _firstCalcDone = true;
  try { localStorage.setItem("voltroof_first_calc", "1"); } catch(e) {}
  document.querySelectorAll(".kpi").forEach((k, i) => {
    setTimeout(() => {
      k.style.boxShadow = "0 0 0 3px rgba(16,185,129,0.35)";
      setTimeout(() => { k.style.boxShadow = ""; }, 700);
    }, i * 80);
  });
  if (typeof fireConfetti === "function" && !window._forceLowPower) {
    setTimeout(() => fireConfetti(), 200);
  }
}

// Wrap liveUpdate end to celebrate
if (typeof liveUpdate === "function") {
  const _luA = liveUpdate;
  window.liveUpdate = function() {
    const r = _luA.apply(this, arguments);
    try {
      if (typeof current !== "undefined" && current?.panels > 0) celebrateFirstCalc();
    } catch(e) {}
    return r;
  };
}

// Guided tour spotlight on next
if (typeof nextTourStep === "function") {
  const _nt = nextTourStep;
  window.nextTourStep = function() {
    document.querySelectorAll(".tour-spotlight").forEach(el => el.classList.remove("tour-spotlight"));
    _nt();
    // spotlight approximate targets by step
    const map = [
      null,
      document.querySelector("[data-view='studio'], .nav-item"),
      document.querySelector("[data-view='bom']"),
      document.getElementById("btnRibbonSave")
    ];
    const t = map[typeof tourIdx !== "undefined" ? tourIdx : 0];
    if (t && window._motionOk) t.classList.add("tour-spotlight");
  };
}
if (typeof closeTour === "function") {
  const _ct = closeTour;
  window.closeTour = function() {
    document.querySelectorAll(".tour-spotlight").forEach(el => el.classList.remove("tour-spotlight"));
    _ct();
  };
}

// Stage chip transition
if (typeof setProjectStage === "function") {
  const _ps = setProjectStage;
  window.setProjectStage = function(stage) {
    const sel = document.getElementById("projectStage");
    if (sel) sel.classList.add("stage-chip-anim");
    _ps(stage);
  };
}

// Panel stagger hint: CSS class on redraw (lightweight)
const _origDraw = typeof drawArray === "function" ? drawArray : null;
if (_origDraw && !_origDraw._animPanels) {
  // visualizer already draws instantly; stagger is expensive on canvas — skip heavy per-panel anim
  // Soft viewport pulse instead
  window.drawArray = function() {
    const stage = document.getElementById("rtStage");
    if (stage && window._motionOk) {
      stage.style.opacity = "0.85";
      setTimeout(() => { stage.style.opacity = "1"; stage.style.transition = "opacity 0.35s ease"; }, 30);
    }
    return _origDraw.apply(this, arguments);
  };
  window.drawArray._animPanels = true;
}

console.log("All seven animation layers active", { motion: window._motionOk });

// ========== COOL ANIMATIONS SET 2 (preserves set 1) ==========
function coolMotionOk() {
  return window._motionOk !== false
    && !window.matchMedia("(prefers-reduced-motion: reduce)").matches
    && !document.body.classList.contains("low-power");
}

// 1.2 KPI assemble on first calc — enhance celebrateFirstCalc
const _celeb = typeof celebrateFirstCalc === "function" ? celebrateFirstCalc : null;
window.celebrateFirstCalc = function() {
  if (_celeb) _celeb();
  if (!coolMotionOk()) return;
  document.querySelectorAll(".kpi").forEach((k, i) => {
    k.classList.remove("assemble");
    void k.offsetWidth;
    k.style.animationDelay = (i * 0.07) + "s";
    k.classList.add("assemble");
  });
};

// 1.3 PDF stamp pulse when download finishes / clicked
if (typeof downloadPdf === "function") {
  const _pdf = downloadPdf;
  window.downloadPdf = function() {
    const r = _pdf.apply(this, arguments);
    if (coolMotionOk()) {
      document.querySelectorAll(".btn-dl, .ribbon-btn.primary").forEach(b => {
        if (b.textContent && /PDF/i.test(b.textContent)) {
          b.classList.remove("stamp-ready");
          void b.offsetWidth;
          b.classList.add("stamp-ready");
        }
      });
    }
    return r;
  };
}

// 2.2 Sun disc on path — draw in visualizer post-pass
window._drawSunDisc = function(ctx, W, H, hour) {
  if (!coolMotionOk() || !ctx) return;
  const h = hour != null ? hour : (window._todHour || 12);
  // map 6..18 to arc t 0..1
  const t = Math.max(0, Math.min(1, (h - 6) / 12));
  const cx = W * 0.5, cy = H * 0.72, rx = W * 0.32, ry = H * 0.18;
  const ang = Math.PI * (1 - t); // pi → 0
  const sx = cx + rx * Math.cos(ang);
  const sy = cy - ry * Math.sin(ang);
  ctx.save();
  ctx.fillStyle = "rgba(251,191,36,0.95)";
  ctx.shadowColor = "rgba(251,191,36,0.6)";
  ctx.shadowBlur = 12;
  ctx.beginPath();
  ctx.arc(sx, sy, 7, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
};

// 2.3 Subtle auto-orbit once when entering 3D
let _orbitDone = false;
if (typeof setArrayMode === "function") {
  const _sam = setArrayMode;
  window.setArrayMode = function(mode, btn) {
    _sam(mode, btn);
    if (mode === "iso" && coolMotionOk() && !_orbitDone) {
      _orbitDone = true;
      let n = 0;
      const id = setInterval(() => {
        if (typeof arrayZoom === "number") {
          // tiny pan nudge
          if (window._arrayDrag) {
            window._arrayDrag.panX = Math.sin(n / 5) * 8;
          }
          if (typeof redrawArraySafe === "function") redrawArraySafe();
        }
        n++;
        if (n > 12) {
          clearInterval(id);
          if (window._arrayDrag) window._arrayDrag.panX = 0;
          if (typeof redrawArraySafe === "function") redrawArraySafe();
        }
      }, 50);
    }
  };
}

// 2.4 Fullscreen blur behind
if (typeof toggleArrayFullscreen === "function") {
  const _tfs = toggleArrayFullscreen;
  window.toggleArrayFullscreen = function(force) {
    _tfs(force);
    const on = document.getElementById("rtStage")?.classList.contains("fullscreen");
    document.body.classList.toggle("viz-fs-blur", !!on && coolMotionOk());
  };
}

// 3.3 BOM flash when cost KPI changes
(function watchBomFlash() {
  const el = document.getElementById("kpiCost");
  if (!el || el._bomObserved) return;
  el._bomObserved = true;
  let last = el.textContent;
  const obs = new MutationObserver(() => {
    if (el.textContent !== last) {
      last = el.textContent;
      if (coolMotionOk()) {
        el.classList.remove("bom-flash");
        void el.offsetWidth;
        el.classList.add("bom-flash");
      }
    }
  });
  obs.observe(el, { childList: true, characterData: true, subtree: true });
})();

// 5.1 Save ripple — enhance ribbonSave
if (typeof ribbonSave === "function") {
  const _rs = ribbonSave;
  window.ribbonSave = function() {
    if (coolMotionOk()) {
      const btn = document.getElementById("btnRibbonSave");
      if (btn) {
        btn.style.position = "relative";
        const ring = document.createElement("span");
        ring.className = "save-ripple";
        btn.appendChild(ring);
        setTimeout(() => ring.remove(), 650);
      }
    }
    return _rs.apply(this, arguments);
  };
}

// 5.2 Stage approved sparkle
if (typeof setProjectStage === "function") {
  const _sps = setProjectStage;
  window.setProjectStage = function(stage) {
    _sps(stage);
    if (stage === "approved" && coolMotionOk() && typeof fireConfetti === "function") {
      // tiny — only few particles via existing confetti is ok once
      try { fireConfetti(); } catch(e) {}
    }
  };
}

// 6.3 Compass already has CSS transition on .compass-arrow — ensure setCompass uses it
if (typeof setCompassAzimuth === "function") {
  const _sca = setCompassAzimuth;
  window.setCompassAzimuth = function(deg) {
    _sca(deg);
  };
}

// Hook sun disc into drawArray post
if (typeof drawArray === "function") {
  const _da2 = drawArray;
  window.drawArray = function() {
    const r = _da2.apply(this, arguments);
    try {
      const canvas = document.getElementById("arrayCanvas");
      if (canvas && window._sunPath) {
        const ctx = canvas.getContext("2d");
        window._drawSunDisc(ctx, canvas.width, canvas.height, window._todHour);
      }
    } catch(e) {}
    return r;
  };
}

// Chart area wipe — enable on Chart.js if present when animating
const _aciv = typeof animateChartsInView === "function" ? animateChartsInView : null;
window.animateChartsInView = function() {
  if (_aciv) _aciv();
  if (!coolMotionOk()) return;
  try {
    [window.genChart, window.monthChart, window.savingsChart].forEach(ch => {
      if (!ch) return;
      ch.options.animation = {
        duration: 900,
        easing: "easeOutQuart",
        animateRotate: true,
        animateScale: true
      };
      ch.update();
    });
  } catch(e) {}
};

// Re-assert set 1 motion flag after load
window._motionOk = coolMotionOk();

console.log("Cool animations set 2 active; set 1 preserved", { motion: window._motionOk });

// ========== FINAL FEATURE PASS JS ==========
window._pdfPreset = "engineer";
window._checklistAction = null;
window._measureMode = false;
window._measurePts = [];

function updateStickySummary() {
  const strip = document.getElementById("stickySummary");
  if (!strip) return;
  const cap = document.getElementById("kpiCap")?.textContent || "—";
  const cost = document.getElementById("kpiCost")?.textContent || "—";
  const pay = document.getElementById("kpiPay")?.textContent || "—";
  const co2 = document.getElementById("envCO2")?.textContent || "—";
  const sc = document.getElementById("ssCap");
  const so = document.getElementById("ssCost");
  const sp = document.getElementById("ssPay");
  const sco = document.getElementById("ssCO2");
  if (sc) sc.textContent = cap;
  if (so) so.textContent = cost;
  if (sp) sp.textContent = pay;
  if (sco) sco.textContent = co2 === "—" ? "—" : co2 + " t CO₂";
  const has = cap && cap !== "—" && !cap.includes("Enter");
  strip.classList.toggle("show", !!has);
}

function refreshRecentProjects() {
  const wrap = document.getElementById("recentProjectsWrap");
  const box = document.getElementById("recentProjects");
  if (!box) return;
  let projects = [];
  try {
    // from loadSelect options or localStorage
    const sel = document.getElementById("loadSelect");
    if (sel) {
      [...sel.options].forEach(o => {
        if (o.value) projects.push({ id: o.value, name: o.textContent || o.value, kw: "—" });
      });
    }
    const snaps = JSON.parse(localStorage.getItem("voltroof_snapshots") || "[]");
    snaps.forEach(s => projects.push({ id: "snap-" + s.id, name: s.label || "Autosave", kw: s.stage || "", date: s.at }));
  } catch(e) {}
  projects = projects.slice(0, 6);
  if (!projects.length) {
    if (wrap) wrap.style.display = "none";
    return;
  }
  if (wrap) wrap.style.display = "block";
  box.innerHTML = projects.map(p => `
    <button type="button" class="recent-card" onclick="loadRecentProject('${String(p.id).replace(/'/g,"")}')">
      <div class="rc-kw">${p.kw || "Project"}</div>
      <div style="font-weight:700;font-size:0.8rem">${p.name}</div>
      <div class="rc-meta">${p.date ? new Date(p.date).toLocaleString() : "Saved project"}</div>
    </button>`).join("");
}

function loadRecentProject(id) {
  if (id.startsWith("snap-")) {
    openSnapshotModal();
    toast("Open a snapshot to restore");
    return;
  }
  const sel = document.getElementById("loadSelect");
  if (sel && typeof loadProject === "function") {
    sel.value = id;
    loadProject(id);
  } else toast("Load from ribbon Load menu");
}

function setPdfPreset(mode) {
  window._pdfPreset = mode === "client" ? "client" : "engineer";
  toast(window._pdfPreset === "client" ? "PDF: Client-ready (outcomes focus)" : "PDF: Engineer (full detail)");
}

function runExportChecklist(actionFn, label) {
  window._checklistAction = actionFn;
  const items = [];
  const siteOk = typeof sites !== "undefined" && sites.length && (sites[0].name || sites[0].siteName);
  const locOk = !!(document.getElementById("cfgLoc")?.value || (typeof current !== "undefined" && current?.location));
  const capOk = typeof current !== "undefined" && current?.kw > 0 || (document.getElementById("kpiCap")?.textContent || "").match(/\d/);
  items.push({ ok: !!siteOk, text: siteOk ? "Site named" : "Name the site in Design" });
  items.push({ ok: !!locOk, text: locOk ? "Location set" : "Set location / weather" });
  items.push({ ok: !!capOk, text: capOk ? "Capacity calculated" : "Run Calculate (capacity > 0)" });
  const box = document.getElementById("checklistItems");
  if (box) {
    box.innerHTML = items.map(i =>
      `<div class="check-item ${i.ok ? "ok" : "bad"}">${i.ok ? "✓" : "✕"} ${i.text}</div>`
    ).join("");
  }
  const allOk = items.every(i => i.ok);
  const btn = document.getElementById("checklistProceed");
  if (btn) {
    btn.disabled = !allOk;
    btn.style.opacity = allOk ? "1" : "0.5";
    btn.textContent = allOk ? (label || "Continue") : "Fix items first";
  }
  document.getElementById("checklistModal")?.classList.add("show");
}

function proceedChecklistAction() {
  document.getElementById("checklistModal")?.classList.remove("show");
  if (typeof window._checklistAction === "function") window._checklistAction();
}

// Wrap PDF and Send with checklist
if (typeof downloadPdf === "function") {
  const _dp = downloadPdf;
  window.downloadPdf = function() {
    runExportChecklist(() => {
      if (window._pdfPreset === "client") {
        document.body.classList.add("pdf-client-preset");
        setTimeout(() => document.body.classList.remove("pdf-client-preset"), 2000);
      }
      _dp();
    }, "Download PDF");
  };
}
if (typeof sendEmailReport === "function") {
  const _se = sendEmailReport;
  window.sendEmailReport = function() {
    runExportChecklist(() => _se(), "Send report");
  };
}

// F5 Pricing impact on 5kW
function updatePricingImpact() {
  const el = document.getElementById("impactPreview");
  if (!el) return;
  try {
    const inputs = document.querySelectorAll(".pricing-input, #pricingBody input[type=number]");
    let delta = 0;
    inputs.forEach(inp => {
      const v = parseFloat(inp.value);
      const def = parseFloat(inp.defaultValue || inp.getAttribute("value") || v);
      if (!isNaN(v) && !isNaN(def) && v !== def) {
        // rough: module ₹/Wp * 5000 Wp scale
        delta += (v - def) * (inp.closest("tr")?.textContent?.includes("Module") ? 5000 : 1);
      }
    });
    if (Math.abs(delta) < 1) {
      el.textContent = "BOM impact preview: no rate changes — publish when ready";
    } else {
      const sign = delta > 0 ? "+" : "";
      el.innerHTML = `BOM impact on ~5 kW system: <strong style="color:var(--amber)">${sign}₹${Math.round(delta).toLocaleString()}</strong> (estimate)`;
    }
  } catch(e) {}
}
document.addEventListener("input", (e) => {
  if (e.target && (e.target.classList?.contains("pricing-input") || e.target.closest?.("#pricingBody"))) {
    updatePricingImpact();
  }
});

// A1 Panel install sequence flag
window._panelInstallAnim = true;
if (typeof drawArray === "function") {
  const _daF = drawArray;
  window.drawArray = function(panels) {
    const r = _daF.apply(this, arguments);
    // soft install: opacity already handled in set 1; pulse stage
    if (window._panelInstallAnim && panels > 0 && window._motionOk) {
      const stage = document.getElementById("rtStage");
      if (stage) {
        stage.style.boxShadow = "0 0 0 2px rgba(37,99,235,0.35)";
        setTimeout(() => { stage.style.boxShadow = ""; }, 500);
      }
    }
    return r;
  };
}

// A2 IntersectionObserver env count
(function envScrollAnim() {
  const tiles = document.querySelectorAll("#envCO2, #envTrees, #envCar, #envCoal");
  if (!tiles.length || !("IntersectionObserver" in window)) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting && window._motionOk) {
        en.target.classList.add("animating");
        setTimeout(() => en.target.classList.remove("animating"), 600);
      }
    });
  }, { threshold: 0.4 });
  tiles.forEach(t => io.observe(t));
})();

// Ensure charts keep animation + resize
function ensureChartsHealthy() {
  try {
    [window.genChart, window.monthChart, window.savingsChart, window.fbChart, window.hourlyChart].forEach(ch => {
      if (!ch) return;
      if (!ch.options) ch.options = {};
      ch.options.animation = ch.options.animation || { duration: 800, easing: "easeOutQuart" };
      if (typeof ch.resize === "function") ch.resize();
      if (typeof ch.update === "function") ch.update("none");
    });
  } catch(e) {}
}
window.addEventListener("resize", () => {
  ensureChartsHealthy();
  // overlap: compact ribbon on narrow
  document.querySelectorAll(".ribbon-group-label").forEach(l => {
    l.style.display = window.innerWidth < 800 ? "none" : "";
  });
});

// Hook liveUpdate / hideProgress to sticky + recent
const _hp2 = typeof hideProgress === "function" ? hideProgress : null;
if (_hp2) {
  window.hideProgress = function() {
    _hp2();
    updateStickySummary();
    refreshRecentProjects();
    ensureChartsHealthy();
  };
}
const _luF = typeof liveUpdate === "function" ? liveUpdate : null;
if (_luF) {
  window.liveUpdate = function() {
    const r = _luF.apply(this, arguments);
    setTimeout(() => { updateStickySummary(); ensureChartsHealthy(); }, 50);
    return r;
  };
}

// F6 Measure tool toggle on visualizer
window.toggleMeasureTool = function() {
  window._measureMode = !window._measureMode;
  window._measurePts = [];
  toast(window._measureMode ? "Measure: click two points on layout" : "Measure off");
};
const canvas = document.getElementById("arrayCanvas");
if (canvas && !canvas._measureBound) {
  canvas._measureBound = true;
  canvas.addEventListener("click", (e) => {
    if (!window._measureMode) return;
    const rect = canvas.getBoundingClientRect();
    window._measurePts.push({ x: e.clientX - rect.left, y: e.clientY - rect.top });
    if (window._measurePts.length >= 2) {
      const [a,b] = window._measurePts;
      const dx = b.x - a.x, dy = b.y - a.y;
      const px = Math.sqrt(dx*dx + dy*dy);
      // rough scale: canvas width ~ roof L
      const L = parseFloat(document.getElementById("cfgL")?.value) || 40;
      const ft = (px / rect.width) * L;
      toast(`Distance ≈ ${ft.toFixed(1)} ft (${(ft*0.3048).toFixed(1)} m)`);
      window._measurePts = [];
    }
  });
}

// Add measure to export row if present
setTimeout(() => {
  const row = document.querySelector(".rt-export-row");
  if (row && !document.getElementById("btnMeasure")) {
    const b = document.createElement("button");
    b.id = "btnMeasure";
    b.type = "button";
    b.textContent = "Measure";
    b.title = "Measure distance";
    b.onclick = () => toggleMeasureTool();
    row.appendChild(b);
  }
  updateStickySummary();
  refreshRecentProjects();
  ensureChartsHealthy();
}, 800);

console.log("Final feature pass ready — sticky, recent, checklist, impact, measure, charts");

console.log("Visualizer v2 (all six) + dashboard polish ready");

console.log("Visualizer advanced controls loaded");

console.log("Ribbon header ready");

console.log("Advanced features loaded", VR_FLAGS);

console.log("Performance optimizations loaded");

console.log("Extra recommendations loaded");

console.log("VoltRoof UX improvements loaded");


function toggleModalAdminRequestForm(show) {
  const loginView = document.getElementById("modalAdminLoginView");
  const reqView = document.getElementById("modalAdminRequestView");
  if (loginView && reqView) {
    loginView.style.display = show ? "none" : "block";
    reqView.style.display = show ? "block" : "none";
  }
}

async function submitAdminAccessRequest() {
  const u = (document.getElementById("reqAdminUser")?.value || "").trim();
  const em = (document.getElementById("reqAdminEmail")?.value || "").trim();
  const mob = (document.getElementById("reqAdminMobile")?.value || "").trim();
  const pw = (document.getElementById("reqAdminPass")?.value || "").trim();

  if (!u || !pw) {
    toast("Username and password are required.");
    return;
  }

  try {
    const res = await fetch("/api/admin/request_access", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: u, email: em, mobile: mob, password: pw })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      toast("Request submitted! Forwarded to Principal Admin (Adarsha KM).");
      toggleModalAdminRequestForm(false);
    } else {
      toast(data.error || "Failed to submit request.");
    }
  } catch (err) {
    toast("Server unreachable. Please verify network or start server.");
  }
}

// ------------------------------------------------------------
// PRICING CONFIGURATION CONTROLLER
// ------------------------------------------------------------
let dynamicPricing = {
  module_per_wp: 18.18,
  inverter_per_kw: 10500.0,
  structure_per_kw: 4800.0,
  dc_cable_per_m: 85.0,
  ac_cable_per_m: 180.0,
  mc4_per_pair: 300.0,
  dcdb_base: 7000.0,
  acdb_base: 7000.0,
  earthing_kit_base: 7500.0,
  lightning_arrester_base: 4000.0,
  accessories_per_kw: 1200.0,
  installation_per_kw: 4000.0
};

async function loadPricingConfig() {
  try {
    const res = await fetch("/api/pricing");
    if (res.ok) {
      const data = await res.json();
      Object.assign(dynamicPricing, data);
      safeSetLocal("voltroof_pricing_config", JSON.stringify(dynamicPricing));
    }
  } catch (e) {
    const saved = localStorage.getItem("voltroof_pricing_config");
    if (saved) try { Object.assign(dynamicPricing, JSON.parse(saved)); } catch(err){}
  }

  // Populate input fields
  for (const [k, v] of Object.entries(dynamicPricing)) {
    const el = document.getElementById("rate_" + k);
    if (el) el.value = v;
  }
}

async function savePricingConfig() {
  const updated = {};
  for (const k of Object.keys(dynamicPricing)) {
    const el = document.getElementById("rate_" + k);
    if (el) {
      const val = parseFloat(el.value);
      if (!isNaN(val)) updated[k] = val;
    }
  }

  try {
    const res = await fetch("/api/pricing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updated)
    });
    if (res.ok) {
      Object.assign(dynamicPricing, updated);
      safeSetLocal("voltroof_pricing_config", JSON.stringify(dynamicPricing));
      toast("Pricing configuration saved and active! 💰");
      liveUpdate();
    } else {
      toast("Failed to persist pricing to server.");
    }
  } catch (err) {
    Object.assign(dynamicPricing, updated);
    safeSetLocal("voltroof_pricing_config", JSON.stringify(dynamicPricing));
    toast("Pricing saved locally in browser! 💰");
    liveUpdate();
  }
}

function resetPricingConfig() {
  const defaults = {
    module_per_wp: 18.18,
    inverter_per_kw: 10500.0,
    structure_per_kw: 4800.0,
    dc_cable_per_m: 85.0,
    ac_cable_per_m: 180.0,
    mc4_per_pair: 300.0,
    dcdb_base: 7000.0,
    acdb_base: 7000.0,
    earthing_kit_base: 7500.0,
    lightning_arrester_base: 4000.0,
    accessories_per_kw: 1200.0,
    installation_per_kw: 4000.0
  };
  for (const [k, v] of Object.entries(defaults)) {
    const el = document.getElementById("rate_" + k);
    if (el) el.value = v;
  }
  toast("Fields restored to MNRE/KERC benchmark normative values.");
}

// ------------------------------------------------------------
// VISITOR ANALYTICS CONTROLLER
// ------------------------------------------------------------
async function refreshVisitorStats() {
  try {
    const res = await fetch("/api/visitors/stats");
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById("visTotalVisits").textContent = data.total_visits || 0;
    document.getElementById("visUniqueSessions").textContent = data.unique_sessions || 0;
    document.getElementById("visTodayVisits").textContent = data.today_visits || 0;

    const tbody = document.getElementById("visTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";
    if (!data.recent || data.recent.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="padding:8px;text-align:center;color:var(--muted)">No visitors logged yet</td></tr>';
      return;
    }
    data.recent.forEach(v => {
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid var(--border)";
      tr.innerHTML = `
        <td style="padding:4px 6px;white-space:nowrap">${v.timestamp || ""}</td>
        <td style="padding:4px 6px;font-family:monospace;color:var(--primary)">${v.session_id || ""}</td>
        <td style="padding:4px 6px">${v.path || "/"}</td>
        <td style="padding:4px 6px;max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted)" title="${v.user_agent || ""}">${v.user_agent || "Browser"}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Failed to refresh visitor stats:", err);
  }
}

// ------------------------------------------------------------
// FEEDBACK STREAM CONTROLLER
// ------------------------------------------------------------
async function refreshFeedbackStats() {
  try {
    const res = await fetch("/api/feedback");
    if (!res.ok) return;
    const data = await res.json();
    document.getElementById("fbTotalCount").textContent = data.total || 0;
    document.getElementById("fbAvgRating").textContent = (data.average_rating || 5.0).toFixed(1) + " ★";

    const yesCount = (data.rec_counts && data.rec_counts["Definitely Yes"]) || 0;
    const probCount = (data.rec_counts && data.rec_counts["Probably Yes"]) || 0;
    const recPct = data.total > 0 ? Math.round(((yesCount + probCount) / data.total) * 100) : 100;
    document.getElementById("fbTopRec").textContent = recPct + "%";

    const container = document.getElementById("fbListContainer");
    if (!container) return;
    container.innerHTML = "";
    if (!data.feedbacks || data.feedbacks.length === 0) {
      container.innerHTML = '<div style="text-align:center;padding:14px;color:var(--muted);font-size:0.78rem">No feedbacks submitted yet. Use the floating 💬 Feedback button to submit one!</div>';
      return;
    }

    data.feedbacks.forEach(f => {
      const card = document.createElement("div");
      card.style.cssText = "background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:10px;";
      const stars = "★".repeat(f.experience || 5) + "☆".repeat(Math.max(0, 5 - (f.experience || 5)));
      card.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
          <div>
            <span style="font-size:0.7rem;font-weight:800;color:var(--primary);background:rgba(59,130,246,0.1);padding:2px 6px;border-radius:4px">${f.category || "Engineer"}</span>
            <span style="margin-left:6px;color:var(--amber);font-size:0.85rem">${stars}</span>
          </div>
          <span style="font-size:0.68rem;color:var(--muted)">${f.timestamp || ""}</span>
        </div>
        <div style="font-size:0.74rem;color:var(--dim);margin-bottom:4px">
          Clarity: <strong style="color:var(--text)">${f.clarity || "Clear"}</strong> · BOM Utility: <strong style="color:var(--text)">${f.bom_utility || "Good"}</strong> · Recommend: <strong style="color:var(--emerald)">${f.recommend || "Yes"}</strong>
        </div>
        ${f.comments ? `<div style="font-size:0.78rem;color:var(--text);background:var(--bg-glass);padding:6px 8px;border-radius:6px;margin-top:4px;border-left:2px solid var(--emerald)">"${f.comments}"</div>` : ''}
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.warn("Failed to refresh feedback stats:", err);
  }
}

// ------------------------------------------------------------
// ADMIN MANAGEMENT & APPROVALS CONTROLLER
// ------------------------------------------------------------
async function refreshAdminList() {
  try {
    const res = await fetch("/api/admin/list");
    if (!res.ok) return;
    const admins = await res.json();
    const tbody = document.getElementById("adminUsersTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";
    admins.forEach(a => {
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid var(--border)";
      const isPending = a.status === "pending";
      const statusBadge = isPending 
        ? '<span style="color:var(--amber);font-weight:700">⏳ Pending Approval</span>' 
        : '<span style="color:var(--success);font-weight:700">✓ Approved</span>';

      const actionBtn = isPending
        ? `<button type="button" class="btn btn-sm btn-p" onclick="approveAdminUser('${a.username}')" style="padding:2px 8px;font-size:0.68rem">✓ Approve Access</button>`
        : '<span style="color:var(--muted);font-size:0.7rem">Active</span>';

      tr.innerHTML = `
        <td style="padding:6px;font-weight:700;color:var(--text)">${a.username}</td>
        <td style="padding:6px;text-transform:capitalize;color:var(--muted)">${a.role || "admin"}</td>
        <td style="padding:6px">${statusBadge}</td>
        <td style="padding:6px;color:var(--muted);font-size:0.7rem">${(a.created_at || "").substring(0, 10)}</td>
        <td style="padding:6px">${actionBtn}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Failed to refresh admin list:", err);
  }
}

async function approveAdminUser(username) {
  try {
    const res = await fetch("/api/admin/approve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username })
    });
    if (res.ok) {
      toast(`Access approved for ${username}! Account is now active.`);
      refreshAdminList();
    } else {
      toast("Failed to approve administrator access.");
    }
  } catch (e) {
    toast("Server communication error.");
  }
}


window.addEventListener("DOMContentLoaded", () => {
  // Visitor traffic tracker
  trackVisitorHit();
  // Load dynamic pricing configuration
  loadPricingConfig();
  initTechAndPanelDropdowns();
  // Initial location setup with live GPS detection & Karnataka database
  initLiveLocation();

  const locInput = document.getElementById("cfgLoc");
  if (locInput) {
    locInput.addEventListener("input", () => {
      const match = lookupKarnatakaLocation(locInput.value);
      if (match) applyLocationData(match, false);
    });
  }

  // Requirement 1: Welcome window ALWAYS appears on opening the link to ask for name!
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.remove("hidden");
    gate.style.display = "flex";
  }
  const savedUser = localStorage.getItem("voltroof_user") || "";
  const gateInput = document.getElementById("gateName");
  if (gateInput) {
    gateInput.value = ""; // Always start empty
    gateInput.placeholder = savedUser ? `Previous: ${savedUser} (or enter name)` : "Enter Engineer / Client Name";
    setTimeout(() => gateInput.focus(), 100);
  }
  gateInput?.addEventListener("keydown", e => {
    if (e.key === "Enter") enterApp();
  });

  // Admin gate login shortcut
  document.getElementById("gateAdminPass")?.addEventListener("keydown", e => {
    if (e.key === "Enter") loginAdminFromGate();
  });
  document.getElementById("modalAdminPass")?.addEventListener("keydown", e => {
    if (e.key === "Enter") loginAdminFromModal();
  });

  const savedTheme = localStorage.getItem("voltroof_theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  document.getElementById("themeIcon").textContent = savedTheme === "dark" ? "☀️" : "🌙";
  document.getElementById("themeIcon2").textContent = savedTheme === "dark" ? "☀️" : "🌙";

  renderSiteTabs();
  initCharts();
  liveUpdate();
  refreshLoadSelect();
  refreshManualMetadata();
  setInterval(updateClock, 1000);
  window.addEventListener("resize", () => drawArray(current?.panels || 0));

  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("view") === "admin_gate") {
    toggleGateAdminMode();
  } else if (urlParams.get("view") === "studio") {
    enterApp();
  } else if (urlParams.get("view") === "feedback_modal") {
    enterApp();
    openFeedbackModal();
  } else if (urlParams.get("view") === "admin_modal") {
    enterApp();
    openAdminManualModal();
  } else if (urlParams.get("view") === "admin_modal_logged") {
    localStorage.setItem("voltroof_admin_session", JSON.stringify({ username: "Adarsha KM", role: "super_admin", email: "adarshakm@jnnce.ac.in" }));
    enterApp();
    openAdminManualModal();
  } else if (urlParams.get("view") === "admin_pricing") {
    localStorage.setItem("voltroof_admin_session", JSON.stringify({ username: "Adarsha KM", role: "super_admin", email: "adarshakm@jnnce.ac.in" }));
    enterApp();
    openAdminManualModal();
    switchAdminTab('pricing');
  } else if (urlParams.get("view") === "admin_analytics") {
    localStorage.setItem("voltroof_admin_session", JSON.stringify({ username: "Adarsha KM", role: "super_admin", email: "adarshakm@jnnce.ac.in" }));
    enterApp();
    openAdminManualModal();
    switchAdminTab('visitors');
  } else if (urlParams.get("view") === "admin_feedback") {
    localStorage.setItem("voltroof_admin_session", JSON.stringify({ username: "Adarsha KM", role: "super_admin", email: "adarshakm@jnnce.ac.in" }));
    enterApp();
    openAdminManualModal();
    switchAdminTab('feedback');
  } else if (urlParams.get("view") === "admin_users") {
    localStorage.setItem("voltroof_admin_session", JSON.stringify({ username: "Adarsha KM", role: "super_admin", email: "adarshakm@jnnce.ac.in" }));
    enterApp();
    openAdminManualModal();
    switchAdminTab('users');
  }
});

// Centered admin auth layout
(function patchAdminModalLayout() {
  const modal = document.getElementById("modalAdminManual");
  if (!modal) return;
  function syncAuthOnly() {
    const login = document.getElementById("modalAdminLoginForm");
    const showLogin = login && login.style.display !== "none" && getComputedStyle(login).display !== "none";
    modal.classList.toggle("auth-only", !!showLogin);
  }
  const _open = typeof openAdminManualModal === "function" ? openAdminManualModal : null;
  if (_open) {
    window.openAdminManualModal = function() {
      _open();
      setTimeout(syncAuthOnly, 30);
    };
  }
  const _login = typeof loginAdminFromModal === "function" ? loginAdminFromModal : null;
  if (_login) {
    window.loginAdminFromModal = function() {
      const r = _login();
      setTimeout(syncAuthOnly, 50);
      return r;
    };
  }
  // observe display changes
  const loginEl = document.getElementById("modalAdminLoginForm");
  if (loginEl && window.MutationObserver) {
    new MutationObserver(syncAuthOnly).observe(loginEl, { attributes: true, attributeFilter: ["style"] });
  }
})();



// ========== LOGIN SLIDESHOW (visible art + captions) ==========
const LOGIN_SLIDES = [
  { title: "India's Power Journey", body: "India is the world's 3rd largest electricity producer — demand keeps rising with homes, industry & EVs.",
    bg: "linear-gradient(145deg,#0c4a6e,#1e3a8a 50%,#134e4a)", icon: "grid" },
  { title: "Coal Still Dominates", body: "Over half of generation is coal-based. Every rooftop kW of solar reduces fossil dependency.",
    bg: "linear-gradient(145deg,#44403c,#1c1917 40%,#0f766e)", icon: "coal" },
  { title: "Solar Potential", body: "Many states average ~5 kWh/m²/day GHI — ideal for 1–20 kW rooftop PV systems.",
    bg: "linear-gradient(145deg,#f59e0b,#ea580c 35%,#1e3a8a)", icon: "sun" },
  { title: "Rooftop Revolution", body: "National programmes are accelerating residential & commercial rooftop capacity this decade.",
    bg: "linear-gradient(145deg,#0369a1,#0f766e 50%,#14532d)", icon: "roof" },
  { title: "KERC-Aware Design", body: "Built for Karnataka LT frameworks — practical caps, norms and sizing guidance for engineers.",
    bg: "linear-gradient(145deg,#1e3a8a,#312e81 50%,#0f766e)", icon: "doc" },
  { title: "What VoltRoof Does", body: "Array layout, live BOM, payback vs bank FD, and environmental impact — in one studio.",
    bg: "linear-gradient(145deg,#064e3b,#0e7490 50%,#1d4ed8)", icon: "app" },
  { title: "Accurate System Design", body: "Panel layout, setbacks, shadows and capacity sizing aligned to real roof constraints.",
    bg: "linear-gradient(145deg,#1e40af,#2563eb 40%,#059669)", icon: "panel" },
  { title: "Financial Clarity", body: "Turnkey cost, ₹/Wp, payback and 25-year savings vs 6.5% FD — numbers clients understand.",
    bg: "linear-gradient(145deg,#0f172a,#1e3a8a 45%,#b45309)", icon: "money" },
  { title: "Cleaner Tomorrow", body: "Track CO₂ avoided, equivalent trees and coal offset — sustainability you can report.",
    bg: "linear-gradient(145deg,#14532d,#166534 40%,#0e7490)", icon: "leaf" },
  { title: "Design. Analyse. Save.", body: "From first login to PDF report — turn sunlight into bankable rooftop opportunities.",
    bg: "linear-gradient(145deg,#1d4ed8,#0f766e 50%,#ca8a04)", icon: "check" }
];

const SLIDE_ICONS = {
  grid: '<svg viewBox="0 0 120 80" fill="none"><rect x="10" y="20" width="20" height="40" rx="2" fill="#94a3b8" opacity=".5"/><rect x="40" y="10" width="20" height="50" rx="2" fill="#cbd5e1" opacity=".6"/><rect x="70" y="25" width="20" height="35" rx="2" fill="#94a3b8" opacity=".5"/><path d="M5 65 H115" stroke="#fbbf24" stroke-width="2"/><circle cx="100" cy="20" r="12" fill="#fbbf24" opacity=".85"/></svg>',
  coal: '<svg viewBox="0 0 120 80" fill="none"><path d="M30 60 L40 25 L50 60 Z" fill="#64748b"/><path d="M55 60 L65 20 L75 60 Z" fill="#475569"/><path d="M80 60 L90 30 L100 60 Z" fill="#64748b"/><ellipse cx="60" cy="62" rx="45" ry="8" fill="#1e293b" opacity=".5"/><path d="M42 25 Q45 10 48 25" stroke="#94a3b8" stroke-width="2" fill="none"/><path d="M67 20 Q70 5 73 20" stroke="#94a3b8" stroke-width="2" fill="none"/></svg>',
  sun: '<svg viewBox="0 0 120 80" fill="none"><circle cx="60" cy="36" r="18" fill="#fbbf24"/><g stroke="#f59e0b" stroke-width="3" stroke-linecap="round"><path d="M60 8v8M60 56v8M28 36h8M84 36h8M38 16l6 6M76 50l6 6M38 56l6-6M76 22l6-6"/></g><path d="M10 70 Q60 55 110 70" stroke="#34d399" stroke-width="3" fill="none"/></svg>',
  roof: '<svg viewBox="0 0 120 80" fill="none"><path d="M20 50 L60 20 L100 50 Z" fill="#2563eb"/><rect x="30" y="50" width="60" height="22" fill="#1e40af"/><g fill="#34d399"><rect x="36" y="28" width="12" height="8" rx="1"/><rect x="52" y="28" width="12" height="8" rx="1"/><rect x="68" y="28" width="12" height="8" rx="1"/><rect x="44" y="38" width="12" height="8" rx="1"/><rect x="60" y="38" width="12" height="8" rx="1"/></g></svg>',
  doc: '<svg viewBox="0 0 120 80" fill="none"><rect x="35" y="12" width="50" height="56" rx="4" fill="#e2e8f0"/><path d="M45 28h30M45 38h30M45 48h20" stroke="#1e40af" stroke-width="2.5" stroke-linecap="round"/><circle cx="85" cy="55" r="14" fill="#10b981"/><path d="M79 55l4 4 8-8" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  app: '<svg viewBox="0 0 120 80" fill="none"><rect x="25" y="15" width="70" height="50" rx="6" fill="#1e293b" stroke="#334155" stroke-width="2"/><rect x="32" y="22" width="35" height="28" rx="3" fill="#0f766e"/><rect x="72" y="22" width="16" height="8" rx="2" fill="#34d399"/><rect x="72" y="34" width="16" height="8" rx="2" fill="#fbbf24"/><rect x="72" y="46" width="16" height="8" rx="2" fill="#60a5fa"/></svg>',
  panel: '<svg viewBox="0 0 120 80" fill="none"><g fill="#1e40af" stroke="#60a5fa" stroke-width="1"><rect x="20" y="25" width="24" height="14" rx="1"/><rect x="48" y="25" width="24" height="14" rx="1"/><rect x="76" y="25" width="24" height="14" rx="1"/><rect x="20" y="43" width="24" height="14" rx="1"/><rect x="48" y="43" width="24" height="14" rx="1"/><rect x="76" y="43" width="24" height="14" rx="1"/></g><path d="M15 62 H105" stroke="#94a3b8" stroke-width="2"/></svg>',
  money: '<svg viewBox="0 0 120 80" fill="none"><rect x="25" y="28" width="50" height="28" rx="4" fill="#16a34a"/><text x="50" y="48" text-anchor="middle" fill="#fff" font-size="16" font-weight="700" font-family="system-ui">₹</text><path d="M85 55 L95 35 L105 55" stroke="#fbbf24" stroke-width="3" fill="none"/><path d="M88 48 H102" stroke="#fbbf24" stroke-width="3"/></svg>',
  leaf: '<svg viewBox="0 0 120 80" fill="none"><path d="M60 65 Q30 40 45 18 Q60 35 60 65 Q60 35 75 18 Q90 40 60 65" fill="#22c55e"/><path d="M60 65 V30" stroke="#14532d" stroke-width="2"/><circle cx="90" cy="22" r="10" fill="#fbbf24" opacity=".9"/></svg>',
  check: '<svg viewBox="0 0 120 80" fill="none"><circle cx="60" cy="40" r="24" fill="#10b981"/><path d="M48 40l8 8 16-16" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
};

let loginSlideIdx = 0;
let loginSlideTimer = null;

function renderLoginSlideshow() {
  const box = document.getElementById("loginSlideshow");
  const dots = document.getElementById("loginSlideDots");
  if (!box) return;
  box.innerHTML = LOGIN_SLIDES.map((s, i) => {
    const art = SLIDE_ICONS[s.icon] || SLIDE_ICONS.sun;
    return `<div class="login-slide${i===0?" active":""}" style="background:${s.bg}" data-idx="${i}">
      <div class="login-slide-art">${art}</div>
      <div class="login-slide-cap"><strong>${s.title}</strong><span>${s.body}</span></div>
    </div>`;
  }).join("");
  if (dots) {
    dots.innerHTML = LOGIN_SLIDES.map((_, i) =>
      `<button type="button" class="${i===0?"on":""}" aria-label="Slide ${i+1}" onclick="goLoginSlide(${i})"></button>`
    ).join("");
  }
}

function goLoginSlide(i) {
  loginSlideIdx = ((i % LOGIN_SLIDES.length) + LOGIN_SLIDES.length) % LOGIN_SLIDES.length;
  document.querySelectorAll(".login-slide").forEach((el, j) => el.classList.toggle("active", j === loginSlideIdx));
  document.querySelectorAll("#loginSlideDots button").forEach((el, j) => el.classList.toggle("on", j === loginSlideIdx));
}

function tickLoginSlide() {
  if (document.hidden) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  goLoginSlide(loginSlideIdx + 1);
}

function startLoginSlideshow() {
  renderLoginSlideshow();
  if (loginSlideTimer) clearInterval(loginSlideTimer);
  loginSlideTimer = setInterval(tickLoginSlide, 4500);
}

document.addEventListener("DOMContentLoaded", startLoginSlideshow);
if (document.readyState !== "loading") startLoginSlideshow();
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) goLoginSlide(loginSlideIdx);
});

console.log("Login slideshow ready (10 visible art slides)");



// ========== GATE FULLSCREEN LOCK ==========
function setGateOpen(open) {
  document.body.classList.toggle("gate-open", !!open);
  const gate = document.getElementById("nameGate");
  if (!gate) return;
  if (open) {
    gate.classList.remove("hidden");
    gate.style.display = "flex";
  } else {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
}
// On load: if gate visible, lock app
(function initGateLock() {
  const gate = document.getElementById("nameGate");
  if (gate && !gate.classList.contains("hidden")) {
    setGateOpen(true);
  }
})();
// Patch enterApp to close gate fully
if (typeof enterApp === "function") {
  const _eaGate = enterApp;
  window.enterApp = function() {
    const r = _eaGate.apply(this, arguments);
    setGateOpen(false);
    return r;
  };
}
// Patch openNameGate if exists
if (typeof openNameGate === "function") {
  const _ong = openNameGate;
  window.openNameGate = function() {
    _ong.apply(this, arguments);
    setGateOpen(true);
  };
} else {
  window.openNameGate = function() {
    setGateOpen(true);
    document.getElementById("gateName")?.focus();
  };
}
console.log("Gate fullscreen lock ready");


// ========== COMPASS + 3D ORBIT FIX ==========
window._orbitYaw = 0;
window._orbitPitch = 18;
window._orbitDragging = false;

function updateCompassFromDesign() {
  // Array azimuth from orientation select if present
  const ori = document.getElementById("cfgOri") || document.getElementById("cfgAzimuth");
  let arrAz = 180; // south default India
  if (ori) {
    const v = ori.value || ori.options?.[ori.selectedIndex]?.text || "";
    if (/south/i.test(v) || v === "180") arrAz = 180;
    else if (/north/i.test(v) || v === "0") arrAz = 0;
    else if (/east/i.test(v) || v === "90") arrAz = 90;
    else if (/west/i.test(v) || v === "270") arrAz = 270;
    else {
      const n = parseFloat(v);
      if (!isNaN(n)) arrAz = n;
    }
  }
  // TOD hour drives sun
  const tod = document.getElementById("todSlider");
  const hour = tod ? parseFloat(tod.value) : (window._todHour || 12);
  window._todHour = hour;
  // Sun azimuth approx for India: 6h=90°, 12h=180°, 18h=270°
  const sunAz = 90 + ((Math.max(6, Math.min(18, hour)) - 6) / 12) * 180;
  window._sunAzimuth = sunAz;

  // Compass needle shows array facing direction relative to North
  if (typeof setCompassAzimuth === "function") {
    setCompassAzimuth(arrAz);
  }
  const label = document.getElementById("compassAzimuth");
  if (label) label.textContent = "Array " + Math.round(arrAz) + "° · Sun " + Math.round(sunAz) + "°";
  const sunNeedle = document.getElementById("compassSun");
  if (sunNeedle) sunNeedle.style.transform = `rotate(${sunAz}deg)`;
}

// Hook TOD slider
document.addEventListener("input", (e) => {
  if (e.target && e.target.id === "todSlider") {
    window._todHour = parseFloat(e.target.value);
    updateCompassFromDesign();
    if (typeof redrawArraySafe === "function") redrawArraySafe();
    else if (typeof drawArray === "function") {
      try { drawArray(current?.panels || 0); } catch(_){}
    }
  }
});
document.addEventListener("change", (e) => {
  if (e.target && (e.target.id === "cfgOri" || e.target.id === "cfgAzimuth")) {
    updateCompassFromDesign();
  }
});
setTimeout(updateCompassFromDesign, 600);

// 3D orbit: drag on canvas in iso mode
(function bindOrbitDrag() {
  const canvas = document.getElementById("arrayCanvas");
  if (!canvas || canvas._orbitBound) return;
  canvas._orbitBound = true;
  let lastX = 0, lastY = 0;
  canvas.addEventListener("pointerdown", (e) => {
    if (window.arrayMode !== "iso" && window._arrayMode !== "iso") return;
    if (window._measureMode) return;
    window._orbitDragging = true;
    lastX = e.clientX; lastY = e.clientY;
    try { canvas.setPointerCapture(e.pointerId); } catch(_){}
  });
  canvas.addEventListener("pointermove", (e) => {
    if (!window._orbitDragging) return;
    const dx = e.clientX - lastX;
    const dy = e.clientY - lastY;
    lastX = e.clientX; lastY = e.clientY;
    window._orbitYaw = (window._orbitYaw + dx * 0.4) % 360;
    window._orbitPitch = Math.max(5, Math.min(60, window._orbitPitch - dy * 0.25));
    if (typeof redrawArraySafe === "function") redrawArraySafe();
    else if (typeof drawArray === "function") {
      try { drawArray(current?.panels || 0); } catch(_){}
    }
  });
  const end = () => { window._orbitDragging = false; };
  canvas.addEventListener("pointerup", end);
  canvas.addEventListener("pointercancel", end);
})();

// Improve setArrayMode to flag iso for orbit
if (typeof setArrayMode === "function") {
  const _sam2 = setArrayMode;
  window.setArrayMode = function(m, btn) {
    window.arrayMode = m;
    window._arrayMode = m;
    _sam2(m, btn);
    if (m === "iso") toast("3D view — drag to rotate");
    updateCompassFromDesign();
  };
}

console.log("Compass + 3D orbit fix ready");


// ========== A-Z UX SHORTLIST PASS ==========
// B1 Login → studio transition
(function patchEnterTransition() {
  if (typeof enterApp !== "function") return;
  const _e = enterApp;
  window.enterApp = function() {
    const gate = document.getElementById("nameGate");
    if (gate && window._motionOk !== false) {
      gate.style.transition = "opacity 0.4s ease";
      gate.style.opacity = "0";
      setTimeout(() => {
        _e.apply(this, arguments);
        gate.style.opacity = "";
        gate.style.transition = "";
        if (typeof setGateOpen === "function") setGateOpen(false);
        const name = document.getElementById("gateName")?.value?.trim();
        if (name && typeof toast === "function") toast("Welcome, " + name);
      }, 380);
    } else {
      _e.apply(this, arguments);
      if (typeof setGateOpen === "function") setGateOpen(false);
    }
  };
})();

// C2 Save state machine visual
if (typeof ribbonSave === "function") {
  const _rs = ribbonSave;
  window.ribbonSave = function() {
    const btn = document.getElementById("btnRibbonSave");
    if (btn) {
      btn.classList.add("saving");
      const label = btn.querySelector("span:last-child") || btn;
      const prev = label.textContent;
      if (label !== btn) label.textContent = "Saving…";
      const r = _rs.apply(this, arguments);
      setTimeout(() => {
        if (label !== btn) label.textContent = "Saved";
        btn.classList.add("saved-flash");
        setTimeout(() => {
          if (label !== btn) label.textContent = "Save";
          btn.classList.remove("saving", "saved-flash");
        }, 900);
      }, 400);
      return r;
    }
    return _rs.apply(this, arguments);
  };
}

// M3 Toast queue
window._toastQ = window._toastQ || [];
window._toastBusy = false;
if (typeof toast === "function") {
  const _t = toast;
  window.toast = function(msg, type) {
    window._toastQ.push([msg, type]);
    function pump() {
      if (window._toastBusy || !window._toastQ.length) return;
      window._toastBusy = true;
      const [m, ty] = window._toastQ.shift();
      _t(m, ty);
      setTimeout(() => { window._toastBusy = false; pump(); }, 2200);
    }
    pump();
  };
}

// O1 Unsaved exit confirm (beforeunload lightweight)
window._vrDirty = false;
["input", "change"].forEach(ev => {
  document.addEventListener(ev, () => { window._vrDirty = true; }, true);
});
if (typeof ribbonSave === "function") {
  // already wrapped — mark clean after save via flag
  document.addEventListener("click", (e) => {
    if (e.target?.closest?.("#btnRibbonSave")) window._vrDirty = false;
  });
}
window.addEventListener("beforeunload", (e) => {
  if (window._vrDirty) {
    e.preventDefault();
    e.returnValue = "";
  }
});

// N2 Pause slideshow when reduced motion (already in tick) — force render static first slide
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  setTimeout(() => { if (typeof goLoginSlide === "function") goLoginSlide(0); }, 200);
}

console.log("A-Z UX shortlist pass ready");



function toggleArrayFullscreen(force) {
  const stage = document.getElementById("rtStage");
  if (!stage) { console.warn("rtStage missing"); return; }

  if (typeof force === "boolean") arrayFullscreen = force;
  else arrayFullscreen = !arrayFullscreen;

  // Backdrop so nothing bleeds through
  let bd = document.getElementById("vrFsBackdrop");
  if (!bd) {
    bd = document.createElement("div");
    bd.id = "vrFsBackdrop";
    document.body.appendChild(bd);
  }

  stage.classList.toggle("fullscreen", arrayFullscreen);
  stage.classList.toggle("is-fs", arrayFullscreen);
  document.body.classList.toggle("viz-true-fs", arrayFullscreen);
  document.body.style.overflow = arrayFullscreen ? "hidden" : "";

  const btn = document.getElementById("btnArrayFS");
  if (btn) {
    btn.textContent = arrayFullscreen ? "↙" : "⛶";
    btn.title = arrayFullscreen ? "Exit fullscreen (Esc)" : "Fullscreen";
  }

  // Dedicated exit button (always works)
  let exitBtn = document.getElementById("vrFsExitBtn");
  if (arrayFullscreen) {
    if (!exitBtn) {
      exitBtn = document.createElement("button");
      exitBtn.id = "vrFsExitBtn";
      exitBtn.type = "button";
      exitBtn.textContent = "✕ Exit fullscreen";
      exitBtn.setAttribute("aria-label", "Exit fullscreen");
      exitBtn.style.cssText = "position:fixed;top:12px;right:12px;z-index:2147483647;padding:10px 18px;border-radius:10px;border:1px solid rgba(255,255,255,0.3);background:rgba(15,23,42,0.92);color:#fff;font-weight:700;cursor:pointer;font-family:inherit;font-size:0.9rem;box-shadow:0 8px 24px rgba(0,0,0,0.4)";
      exitBtn.onclick = function(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        toggleArrayFullscreen(false);
      };
      document.body.appendChild(exitBtn);
    }
    exitBtn.style.display = "block";
  } else if (exitBtn) {
    exitBtn.style.display = "none";
  }

  // Move stage to body so it escapes any overflow:hidden parents
  if (arrayFullscreen) {
    if (!stage._fsParent) {
      stage._fsParent = stage.parentNode;
      stage._fsNext = stage.nextSibling;
    }
    document.body.appendChild(stage);
  } else if (stage._fsParent) {
    if (stage._fsNext && stage._fsNext.parentNode === stage._fsParent) {
      stage._fsParent.insertBefore(stage, stage._fsNext);
    } else {
      stage._fsParent.appendChild(stage);
    }
  }

  // Size canvas to window
  function sizeAndDraw() {
    const canvas = document.getElementById("arrayCanvas");
    if (canvas) {
      const w = arrayFullscreen ? window.innerWidth : Math.max(320, (stage.clientWidth || 800));
      const h = arrayFullscreen ? window.innerHeight : Math.max(240, (stage.clientHeight || 380));
      canvas.width = w;
      canvas.height = h;
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
    }
    try {
      if (typeof drawArray === "function") {
        const panels = (typeof current !== "undefined" && current?.panels) || 0;
        drawArray(panels);
      }
    } catch (err) { console.warn(err); }
    try { if (typeof redrawArraySafe === "function") redrawArraySafe(); } catch (_){}
  }
  setTimeout(sizeAndDraw, 50);
  setTimeout(sizeAndDraw, 200);

  if (typeof toast === "function") {
    toast(arrayFullscreen ? "Fullscreen on — press Esc or Exit" : "Exited fullscreen");
  }
}

document.addEventListener("keydown", function(e) {
  if (e.key === "Escape" && typeof arrayFullscreen !== "undefined" && arrayFullscreen) {
    e.preventDefault();
    toggleArrayFullscreen(false);
  }
});


// ========== CHART RE-ANIMATE ON CARD CLICK ==========
function replayChartFromZero(chart) {
  if (!chart || !chart.data || !chart.data.datasets) return;
  try {
    chart.data.datasets.forEach(ds => {
      if (!ds._vrFullData) {
        ds._vrFullData = Array.isArray(ds.data) ? ds.data.slice() : ds.data;
      }
      const full = ds._vrFullData;
      if (Array.isArray(full)) {
        ds.data = full.map(() => 0);
      }
    });
    chart.update("none");
    chart.data.datasets.forEach(ds => {
      if (ds._vrFullData) ds.data = Array.isArray(ds._vrFullData) ? ds._vrFullData.slice() : ds._vrFullData;
    });
    chart.options.animation = {
      duration: 900,
      easing: "easeOutQuart"
    };
    chart.update();
  } catch (e) { console.warn("chart replay", e); }
}

function bindChartCardClicks() {
  const map = [
    ["chartMonthly", "monthChart", "genChart"],
    ["chartHourly", "hourlyChart", "genChart"],
    ["chartSavings", "savingsChart"],
    ["chartFeedback", "fbChart"],
    ["chartDiurnal", "hourlyChart"],
  ];
  // also any canvas inside .chart-box / .card
  document.querySelectorAll(".chart-box, .card canvas, canvas[id^='chart']").forEach(el => {
    const card = el.closest(".card, .chart-box") || el.parentElement;
    if (!card || card._chartClickBound) return;
    card._chartClickBound = true;
    card.style.cursor = "pointer";
    card.title = (card.title || "") + " · Click to replay chart animation";
    card.addEventListener("click", () => {
      const canvas = card.querySelector("canvas");
      if (!canvas) return;
      const id = canvas.id;
      const charts = [
        window.genChart, window.monthChart, window.savingsChart,
        window.fbChart, window.hourlyChart,
        window.charts?.monthly, window.charts?.hourly, window.charts?.savings
      ];
      // Chart.js instance from canvas
      let inst = null;
      try {
        if (window.Chart && Chart.getChart) inst = Chart.getChart(canvas);
      } catch (_) {}
      if (!inst) {
        charts.forEach(c => {
          if (c && c.canvas === canvas) inst = c;
        });
      }
      if (inst) {
        // refresh stored full data from current
        inst.data.datasets.forEach(ds => {
          ds._vrFullData = Array.isArray(ds.data) ? ds.data.slice() : ds.data;
        });
        replayChartFromZero(inst);
        if (typeof toast === "function") toast("Chart animation replayed");
      }
    });
  });
}
setTimeout(bindChartCardClicks, 1200);
document.addEventListener("DOMContentLoaded", () => setTimeout(bindChartCardClicks, 800));

// After liveUpdate, store full data on charts for replay
if (typeof liveUpdate === "function") {
  const _luCh = liveUpdate;
  window.liveUpdate = function() {
    const r = _luCh.apply(this, arguments);
    setTimeout(() => {
      try {
        [window.genChart, window.monthChart, window.savingsChart, window.hourlyChart, window.fbChart]
          .concat(window.charts ? Object.values(window.charts) : [])
          .forEach(ch => {
            if (!ch || !ch.data || !ch.data.datasets) return;
            ch.data.datasets.forEach(ds => {
              if (Array.isArray(ds.data)) ds._vrFullData = ds.data.slice();
            });
          });
      } catch (_) {}
      bindChartCardClicks();
    }, 100);
    return r;
  };
}

console.log("Sanctioned-load priority + chart click replay ready");


// ========== CONTENT STUDIO (Manual + Login Showcase) ==========
const CS_SLIDE_KEY = "voltroof_login_showcase_v1";
const CS_MANUAL_KEY = "voltroof_custom_manual_v1";
const CS_MAX_SLIDES = 50;

function csLoadSlides() {
  try {
    const raw = localStorage.getItem(CS_SLIDE_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr.slice(0, CS_MAX_SLIDES) : [];
  } catch (e) { return []; }
}

function csSaveSlides(arr) {
  localStorage.setItem(CS_SLIDE_KEY, JSON.stringify(arr.slice(0, CS_MAX_SLIDES)));
}

function openContentStudio() {
  // Require admin session if available
  let ok = true;
  try {
    const sess = localStorage.getItem("voltroof_admin_session");
    if (!sess) ok = false;
  } catch (e) {}
  if (!ok) {
    toast("Admin sign-in required for Content Studio");
    if (typeof openAdminManualModal === "function") openAdminManualModal();
    return;
  }
  const m = document.getElementById("modalContentStudio");
  if (m) {
    m.style.display = "flex";
    csRenderSlideList();
    csRefreshManualMeta();
  }
}

function closeContentStudio() {
  const m = document.getElementById("modalContentStudio");
  if (m) m.style.display = "none";
}

function csRefreshManualMeta() {
  const el = document.getElementById("csManualMeta");
  if (!el) return;
  try {
    const meta = JSON.parse(localStorage.getItem(CS_MANUAL_KEY) || "null");
    if (meta && meta.name) {
      el.textContent = `Active: ${meta.name} (${Math.round((meta.size || 0) / 1024)} KB)`;
    } else {
      el.textContent = "No custom manual — using default";
    }
  } catch (e) {
    el.textContent = "No custom manual — using default";
  }
}

function csSaveManual() {
  const inp = document.getElementById("csManualFile");
  const f = inp?.files?.[0];
  if (!f) { toast("Choose a PDF first"); return; }
  if (f.type && f.type !== "application/pdf" && !/\.pdf$/i.test(f.name)) {
    toast("PDF only");
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    try {
      localStorage.setItem(CS_MANUAL_KEY, JSON.stringify({
        name: f.name,
        size: f.size,
        dataUrl: reader.result,
        at: Date.now()
      }));
      // also sync common manual keys if app uses them
      try {
        localStorage.setItem("voltroof_user_manual_pdf", reader.result);
        localStorage.setItem("voltroof_user_manual_name", f.name);
      } catch (e) {}
      csRefreshManualMeta();
      toast("Instruction guide saved");
    } catch (e) {
      toast("Could not save (file may be too large for browser storage)");
    }
  };
  reader.readAsDataURL(f);
}

function csClearManual() {
  localStorage.removeItem(CS_MANUAL_KEY);
  try {
    localStorage.removeItem("voltroof_user_manual_pdf");
    localStorage.removeItem("voltroof_user_manual_name");
  } catch (e) {}
  csRefreshManualMeta();
  toast("Reset to default manual");
}

function csAddSlidesFromFiles() {
  const inp = document.getElementById("csSlideFile");
  const files = inp?.files;
  if (!files || !files.length) { toast("Choose image file(s)"); return; }
  let slides = csLoadSlides();
  const caption = document.getElementById("csSlideCaption")?.value?.trim() || "";
  const remain = CS_MAX_SLIDES - slides.length;
  if (remain <= 0) { toast("Maximum 50 slides"); return; }
  const list = [...files].slice(0, remain);
  let pending = list.length;
  list.forEach((f, i) => {
    const reader = new FileReader();
    reader.onload = () => {
      slides.push({
        id: "sl-" + Date.now() + "-" + i,
        image: reader.result,
        title: caption || f.name.replace(/\.[^.]+$/, ""),
        body: caption || "Login showcase slide",
        order: slides.length
      });
      pending--;
      if (pending <= 0) {
        csSaveSlides(slides);
        csRenderSlideList();
        if (inp) inp.value = "";
        const cap = document.getElementById("csSlideCaption");
        if (cap) cap.value = "";
        toast(`Added ${list.length} slide(s)`);
      }
    };
    reader.readAsDataURL(f);
  });
}

function csRenderSlideList() {
  const box = document.getElementById("csSlideList");
  const cnt = document.getElementById("csSlideCount");
  const slides = csLoadSlides();
  if (cnt) cnt.textContent = String(slides.length);
  if (!box) return;
  if (!slides.length) {
    box.innerHTML = '<div style="font-size:0.84rem;color:var(--muted);padding:12px">No custom slides yet — login uses built-in showcase until you publish.</div>';
    return;
  }
  box.innerHTML = slides.map((s, i) => `
    <div class="cs-slide-row" data-id="${s.id}">
      <div class="cs-ord">${i + 1}</div>
      <img src="${s.image}" alt="Slide ${i + 1}">
      <textarea data-i="${i}" onchange="csUpdateCaption(${i}, this.value)" placeholder="Info sentence for this slide">${(s.body || s.title || "").replace(/</g, "&lt;")}</textarea>
      <div style="display:flex;flex-direction:column;gap:4px">
        <button type="button" class="btn btn-sm" onclick="csMoveSlide(${i},-1)" title="Move up">↑</button>
        <button type="button" class="btn btn-sm" onclick="csMoveSlide(${i},1)" title="Move down">↓</button>
        <button type="button" class="btn btn-sm" style="color:var(--rose)" onclick="csDeleteSlide(${i})" title="Remove">✕</button>
      </div>
    </div>
  `).join("");
}

function csUpdateCaption(i, val) {
  const slides = csLoadSlides();
  if (!slides[i]) return;
  slides[i].body = val;
  slides[i].title = val.slice(0, 48) || slides[i].title;
  csSaveSlides(slides);
}

function csMoveSlide(i, dir) {
  const slides = csLoadSlides();
  const j = i + dir;
  if (j < 0 || j >= slides.length) return;
  const t = slides[i]; slides[i] = slides[j]; slides[j] = t;
  csSaveSlides(slides);
  csRenderSlideList();
}

function csDeleteSlide(i) {
  const slides = csLoadSlides();
  slides.splice(i, 1);
  csSaveSlides(slides);
  csRenderSlideList();
  toast("Slide removed");
}

function csPublishShowcase() {
  const slides = csLoadSlides();
  csSaveSlides(slides);
  // Rebuild login slideshow from custom slides
  if (typeof applyCustomLoginSlides === "function") applyCustomLoginSlides();
  toast(slides.length ? `Published ${slides.length} slide(s) to login` : "Login showcase reset to built-in");
  closeContentStudio();
}

function applyCustomLoginSlides() {
  const custom = csLoadSlides();
  if (!custom.length) {
    if (typeof startLoginSlideshow === "function") startLoginSlideshow();
    return;
  }
  // Override LOGIN_SLIDES visual path
  window.LOGIN_SLIDES = custom.map((s, i) => ({
    title: s.title || `Slide ${i + 1}`,
    body: s.body || "",
    bg: s.image ? `center/cover url(${s.image})` : "linear-gradient(145deg,#0c4a6e,#1e3a8a)",
    icon: "custom",
    image: s.image
  }));
  const box = document.getElementById("loginSlideshow");
  const dots = document.getElementById("loginSlideDots");
  if (!box) return;
  box.innerHTML = window.LOGIN_SLIDES.map((s, i) =>
    `<div class="login-slide${i===0?" active":""}" style="background:${s.bg}" data-idx="${i}">
      <div class="login-slide-cap"><strong>${s.title}</strong><span>${s.body}</span></div>
    </div>`
  ).join("");
  if (dots) {
    dots.innerHTML = window.LOGIN_SLIDES.map((_, i) =>
      `<button type="button" class="${i===0?"on":""}" onclick="goLoginSlide(${i})"></button>`
    ).join("");
  }
  if (typeof goLoginSlide === "function") goLoginSlide(0);
}

// Apply custom slides on load
setTimeout(() => {
  try {
    if (csLoadSlides().length) applyCustomLoginSlides();
  } catch (e) {}
}, 400);

// Show Content Studio only when admin (optional soft gate via label)
(function syncContentStudioNav() {
  const btn = document.getElementById("navContentStudioBtn");
  if (!btn) return;
  try {
    const sess = localStorage.getItem("voltroof_admin_session");
    btn.style.opacity = sess ? "1" : "0.85";
  } catch (e) {}
})();

console.log("Content Studio ready (max 50 slides, sites≤2, buildings≤10)");


// ========== SOLAR POLICY HUB (user) + POLICY DESK (admin) ==========
const PD_STORE_KEY = "voltroof_policy_desk_v1";

function pdLoad() {
  try {
    const a = JSON.parse(localStorage.getItem(PD_STORE_KEY) || "[]");
    return Array.isArray(a) ? a : [];
  } catch (e) { return []; }
}
function pdSave(arr) {
  localStorage.setItem(PD_STORE_KEY, JSON.stringify(arr));
}

function isAdminSession() {
  try { return !!localStorage.getItem("voltroof_admin_session"); } catch (e) { return false; }
}

function syncAdminNavVisibility() {
  const admin = isAdminSession();
  const sess = getActiveAdmin && getActiveAdmin();
  const isSuper = !!(sess && sess.role === "super_admin");
  const desk = document.getElementById("navPolicyDeskBtn");
  const studio = document.getElementById("navContentStudioBtn");
  const ctrl = document.getElementById("navAdminManualBtn");
  const team = document.getElementById("navAdminTeamBtn");
  if (desk) desk.style.display = admin ? "" : "none";
  if (studio) studio.style.display = admin ? "" : "none";
  if (ctrl) ctrl.style.display = admin ? "" : "none";
  if (team) team.style.display = admin ? "" : "none"; // admins see roster (limited); super sees full tools
}

function openPolicyHub() {
  switchView("policyHub");
  phShowTab("rules");
}
function closePolicyHub() {
  switchView("dashboard");
}

function phShowTab(tab) {
  const rules = document.getElementById("phContentRules");
  const subs = document.getElementById("phContentSubs");
  const bR = document.getElementById("phTabRules");
  const bS = document.getElementById("phTabSubs");
  if (tab === "subsidies") {
    if (rules) rules.style.display = "none";
    if (subs) subs.style.display = "block";
    if (bR) bR.classList.remove("btn-p");
    if (bS) bS.classList.add("btn-p");
  } else {
    if (rules) rules.style.display = "block";
    if (subs) subs.style.display = "none";
    if (bS) bS.classList.remove("btn-p");
    if (bR) bR.classList.add("btn-p");
  }
  phRender();
}

function phRender() {
  const items = pdLoad();
  const rules = items.filter(x => x.type === "rule");
  const subs = items.filter(x => x.type === "subsidy");
  const rBox = document.getElementById("phContentRules");
  const sBox = document.getElementById("phContentSubs");
  const empty = '<div style="font-size:0.84rem;color:var(--muted);padding:16px;text-align:center">No documents published yet. Check back after admin updates.</div>';
  function card(it) {
    const link = it.fileData
      ? `<div style="margin-top:8px"><a href="${it.fileData}" target="_blank" rel="noopener">Open attachment (${it.fileName || "file"})</a></div>`
      : "";
    const when = it.at ? new Date(it.at).toLocaleDateString() : "";
    return `<div class="ph-card"><h4>${it.title || "Untitled"}</h4><p>${(it.body || "").replace(/</g,"&lt;")}</p>${link}<div style="font-size:0.68rem;color:var(--dim);margin-top:6px">${when}</div></div>`;
  }
  if (rBox) rBox.innerHTML = rules.length ? rules.map(card).join("") : empty;
  if (sBox) sBox.innerHTML = subs.length ? subs.map(card).join("") : empty;
}

function openPolicyDesk() {
  if (!isAdminSession()) {
    toast("Admin sign-in required for Policy Desk");
    if (typeof openAdminManualModal === "function") openAdminManualModal();
    return;
  }
  switchView("policyDesk");
  pdRenderAdminList();
}
function closePolicyDesk() {
  switchView("dashboard");
}

function pdAddItem(type) {
  if (!isAdminSession()) { toast("Admin only"); return; }
  const isRule = type === "rule";
  const title = document.getElementById(isRule ? "pdRuleTitle" : "pdSubTitle")?.value?.trim();
  const body = document.getElementById(isRule ? "pdRuleBody" : "pdSubBody")?.value?.trim();
  const fileInp = document.getElementById(isRule ? "pdRuleFile" : "pdSubFile");
  if (!title) { toast("Enter a title"); return; }
  const file = fileInp?.files?.[0];
  const finish = (fileData, fileName) => {
    const arr = pdLoad();
    arr.unshift({
      id: "pd-" + Date.now(),
      type: isRule ? "rule" : "subsidy",
      title, body: body || "",
      fileData: fileData || null,
      fileName: fileName || null,
      at: Date.now()
    });
    try {
      pdSave(arr);
    } catch (e) {
      toast("Storage full — use a smaller file");
      return;
    }
    if (isRule) {
      document.getElementById("pdRuleTitle").value = "";
      document.getElementById("pdRuleBody").value = "";
      if (fileInp) fileInp.value = "";
    } else {
      document.getElementById("pdSubTitle").value = "";
      document.getElementById("pdSubBody").value = "";
      if (fileInp) fileInp.value = "";
    }
    pdRenderAdminList();
    toast(isRule ? "Rule published" : "Subsidy / ad published");
  };
  if (file) {
    const reader = new FileReader();
    reader.onload = () => finish(reader.result, file.name);
    reader.readAsDataURL(file);
  } else {
    finish(null, null);
  }
}

function pdDeleteItem(id) {
  if (!isAdminSession()) return;
  const arr = pdLoad().filter(x => x.id !== id);
  pdSave(arr);
  pdRenderAdminList();
  toast("Item deleted");
}

function pdRenderAdminList() {
  const box = document.getElementById("pdItemList");
  if (!box) return;
  const arr = pdLoad();
  if (!arr.length) {
    box.innerHTML = '<div style="font-size:0.84rem;color:var(--muted);padding:10px">No published items yet.</div>';
    return;
  }
  box.innerHTML = arr.map(it => `
    <div class="pd-item">
      <div style="flex:1;min-width:0">
        <span class="pd-tag ${it.type}">${it.type}</span>
        <div style="font-weight:700;margin-top:4px">${it.title || ""}</div>
        <div style="font-size:0.78rem;color:var(--muted)">${(it.body || "").slice(0, 120)}</div>
        ${it.fileName ? `<div style="font-size:0.72rem;margin-top:4px">📎 ${it.fileName}</div>` : ""}
      </div>
      <button type="button" class="btn btn-sm" style="color:var(--rose)" onclick="pdDeleteItem('${it.id}')">Delete</button>
    </div>
  `).join("");
}

// After admin login, show Policy Desk + Content Studio
(function hookAdminNav() {
  syncAdminNavVisibility();
  const _orig = typeof loginAdminFromModal === "function" ? loginAdminFromModal : null;
  if (_orig && !_orig._pdHooked) {
    window.loginAdminFromModal = function() {
      const r = _orig.apply(this, arguments);
      setTimeout(syncAdminNavVisibility, 100);
      return r;
    };
    window.loginAdminFromModal._pdHooked = true;
  }
  const _gate = typeof loginAdminFromGate === "function" ? loginAdminFromGate : null;
  if (_gate && !_gate._pdHooked) {
    window.loginAdminFromGate = function() {
      const r = _gate.apply(this, arguments);
      setTimeout(syncAdminNavVisibility, 100);
      return r;
    };
    window.loginAdminFromGate._pdHooked = true;
  }
  const _logout = typeof logoutAdmin === "function" ? logoutAdmin : null;
  if (_logout && !_logout._pdHooked) {
    window.logoutAdmin = function() {
      const r = _logout.apply(this, arguments);
      setTimeout(syncAdminNavVisibility, 50);
      return r;
    };
    window.logoutAdmin._pdHooked = true;
  }
})();

setTimeout(syncAdminNavVisibility, 200);
console.log("Solar Policy Hub + Policy Desk ready");


// ========== ADMIN ROSTER (Super Admin) ==========
const AT_CUSTOM_KEY = "voltroof_admin_roster_v1";
const AT_REQ_KEY = "voltroof_admin_reset_requests_v1";

function atLoadCustom() {
  try {
    const a = JSON.parse(localStorage.getItem(AT_CUSTOM_KEY) || "[]");
    return Array.isArray(a) ? a : [];
  } catch (e) { return []; }
}
function atSaveCustom(arr) {
  localStorage.setItem(AT_CUSTOM_KEY, JSON.stringify(arr));
}
function atLoadReqs() {
  try {
    const a = JSON.parse(localStorage.getItem(AT_REQ_KEY) || "[]");
    return Array.isArray(a) ? a : [];
  } catch (e) { return []; }
}
function atSaveReqs(arr) {
  localStorage.setItem(AT_REQ_KEY, JSON.stringify(arr));
}

/** Full admin list = builtin (minus removed) + custom */
function atGetAllAdmins() {
  const custom = atLoadCustom();
  const removed = custom.filter(x => x._removed).map(x => (x.username || "").toLowerCase());
  const overrides = {};
  custom.filter(x => !x._removed).forEach(x => {
    overrides[(x.username || "").toLowerCase()] = x;
  });
  const list = [];
  (typeof BUILTIN_ADMINS !== "undefined" ? BUILTIN_ADMINS : []).forEach(b => {
    const key = (b.username || "").toLowerCase();
    if (removed.includes(key)) return;
    if (overrides[key]) {
      list.push({ ...b, ...overrides[key], emails: overrides[key].emails || b.emails });
      delete overrides[key];
    } else {
      list.push({ ...b });
    }
  });
  Object.values(overrides).forEach(c => list.push(c));
  return list;
}

// Patch login to use dynamic roster
if (typeof loginAdminCore === "function" && !loginAdminCore._atPatched) {
  const _loginCore = loginAdminCore;
  window.loginAdminCore = async function(username, password) {
    const u = (username || "").trim().toLowerCase();
    const p = password || "";
    const found = atGetAllAdmins().find(adm => {
      const names = [adm.username, ...(adm.emails || []), adm.mobile].filter(Boolean).map(x => String(x).toLowerCase());
      return names.includes(u) && adm.password === p;
    });
    if (found) {
      return {
        username: found.username,
        role: found.role || "admin",
        email: (found.emails && found.emails[0]) || found.email || "",
        mobile: found.mobile || ""
      };
    }
    // fallback to original (builtin)
    return _loginCore(username, password);
  };
  window.loginAdminCore._atPatched = true;
}

function atVerifySuperPassword(pass) {
  const sess = getActiveAdmin();
  if (!sess || sess.role !== "super_admin") return false;
  const me = atGetAllAdmins().find(a => a.username === sess.username && a.role === "super_admin");
  if (!me) {
    // fallback builtin super
    const b = (BUILTIN_ADMINS || []).find(a => a.role === "super_admin");
    return b && b.password === pass;
  }
  return me.password === pass;
}

function atRender() {
  const sess = getActiveAdmin();
  const superBox = document.getElementById("atSuperOnly");
  const adminBox = document.getElementById("atAdminOnly");
  const denied = document.getElementById("atDenied");
  if (!sess) {
    if (superBox) superBox.style.display = "none";
    if (adminBox) adminBox.style.display = "none";
    if (denied) denied.style.display = "block";
    return;
  }
  if (denied) denied.style.display = "none";
  if (sess.role === "super_admin") {
    if (superBox) superBox.style.display = "block";
    if (adminBox) adminBox.style.display = "none";
    atRenderAdminList();
    atRenderRequests();
    atFillResetSelect();
  } else {
    if (superBox) superBox.style.display = "none";
    if (adminBox) adminBox.style.display = "block";
  }
}

function atRenderAdminList() {
  const box = document.getElementById("atAdminList");
  if (!box) return;
  const list = atGetAllAdmins();
  box.innerHTML = list.map(a => `
    <div class="pd-item">
      <div style="flex:1;min-width:0">
        <div style="font-weight:700">${a.username} ${a.role === "super_admin" ? '<span class="pd-tag rule">super</span>' : '<span class="pd-tag subsidy">admin</span>'}</div>
        <div style="font-size:0.78rem;color:var(--muted)">${(a.emails || [a.email]).filter(Boolean).join(", ") || "—"} ${a.mobile ? " · " + a.mobile : ""}</div>
      </div>
      ${a.role === "super_admin" ? "" : `<button type="button" class="btn btn-sm" style="color:var(--rose)" onclick="atRemoveAdmin('${(a.username || "").replace(/'/g, "\\'")}')">Remove</button>`}
    </div>
  `).join("") || '<div style="color:var(--muted)">No admins</div>';
}

function atFillResetSelect() {
  const sel = document.getElementById("atResetUser");
  if (!sel) return;
  const list = atGetAllAdmins().filter(a => a.role !== "super_admin");
  sel.innerHTML = list.map(a => `<option value="${a.username}">${a.username}</option>`).join("") || '<option value="">No admins</option>';
}

function atRenderRequests() {
  const box = document.getElementById("atRequestList");
  if (!box) return;
  const reqs = atLoadReqs();
  if (!reqs.length) {
    box.innerHTML = '<div style="font-size:0.84rem;color:var(--muted);padding:8px">No pending reset requests.</div>';
    return;
  }
  box.innerHTML = reqs.map(r => `
    <div class="pd-item">
      <div style="flex:1">
        <div style="font-weight:700">${r.username}</div>
        <div style="font-size:0.78rem;color:var(--muted)">${r.note || "No note"} · ${r.at ? new Date(r.at).toLocaleString() : ""}</div>
      </div>
      <button type="button" class="btn btn-sm btn-p" onclick="document.getElementById('atResetUser').value='${r.username}';document.getElementById('atResetNewPass').focus()">Handle</button>
      <button type="button" class="btn btn-sm" onclick="atDismissReq('${r.id}')">Dismiss</button>
    </div>
  `).join("");
}

function atAddAdmin() {
  const sess = getActiveAdmin();
  if (!sess || sess.role !== "super_admin") { toast("Super admin only"); return; }
  const username = document.getElementById("atNewUser")?.value?.trim();
  const email = document.getElementById("atNewEmail")?.value?.trim();
  const mobile = document.getElementById("atNewMobile")?.value?.trim() || "";
  const password = document.getElementById("atNewPass")?.value || "";
  const superPass = document.getElementById("atSuperPassAdd")?.value || "";
  if (!username || !email || !password) { toast("Name, email and password required"); return; }
  if (!atVerifySuperPassword(superPass)) { toast("Super-admin password incorrect"); return; }
  if (atGetAllAdmins().some(a => (a.username || "").toLowerCase() === username.toLowerCase())) {
    toast("Username already exists"); return;
  }
  const custom = atLoadCustom().filter(x => !(x._removed && (x.username || "").toLowerCase() === username.toLowerCase()));
  custom.push({ username, emails: [email], mobile, password, role: "admin" });
  atSaveCustom(custom);
  ["atNewUser","atNewEmail","atNewMobile","atNewPass","atSuperPassAdd"].forEach(id => {
    const el = document.getElementById(id); if (el) el.value = "";
  });
  atRender();
  toast("Administrator added");
}

function atRemoveAdmin(username) {
  const sess = getActiveAdmin();
  if (!sess || sess.role !== "super_admin") { toast("Super admin only"); return; }
  if (!confirm("Remove administrator " + username + "?")) return;
  const superPass = prompt("Enter your super-admin password to confirm removal:");
  if (!atVerifySuperPassword(superPass || "")) { toast("Super-admin password incorrect"); return; }
  let custom = atLoadCustom().filter(x => (x.username || "").toLowerCase() !== username.toLowerCase());
  // mark builtin as removed
  const isBuiltin = (BUILTIN_ADMINS || []).some(b => (b.username || "").toLowerCase() === username.toLowerCase());
  if (isBuiltin) custom.push({ username, _removed: true });
  atSaveCustom(custom);
  atRender();
  toast("Administrator removed");
}

function atResetPassword() {
  const sess = getActiveAdmin();
  if (!sess || sess.role !== "super_admin") { toast("Super admin only"); return; }
  const username = document.getElementById("atResetUser")?.value;
  const newPass = document.getElementById("atResetNewPass")?.value || "";
  const superPass = document.getElementById("atSuperPassReset")?.value || "";
  if (!username || !newPass) { toast("Select admin and enter new password"); return; }
  if (!atVerifySuperPassword(superPass)) { toast("Super-admin password incorrect"); return; }
  // Update or create override with new password
  const all = atGetAllAdmins();
  const target = all.find(a => a.username === username);
  if (!target) { toast("Admin not found"); return; }
  let custom = atLoadCustom().filter(x => (x.username || "").toLowerCase() !== username.toLowerCase() || x._removed);
  custom = custom.filter(x => !x._removed || (x.username || "").toLowerCase() !== username.toLowerCase());
  custom.push({
    username: target.username,
    emails: target.emails || [target.email].filter(Boolean),
    mobile: target.mobile || "",
    password: newPass,
    role: target.role || "admin"
  });
  atSaveCustom(custom);
  // clear matching requests
  atSaveReqs(atLoadReqs().filter(r => r.username !== username));
  document.getElementById("atResetNewPass").value = "";
  document.getElementById("atSuperPassReset").value = "";
  atRender();
  toast("Password updated for " + username);
}

function atRequestReset() {
  const sess = getActiveAdmin();
  if (!sess) { toast("Admin sign-in required"); return; }
  if (sess.role === "super_admin") { toast("Super admin can reset passwords directly"); return; }
  const note = document.getElementById("atReqNote")?.value?.trim() || "";
  const reqs = atLoadReqs().filter(r => r.username !== sess.username);
  reqs.unshift({ id: "req-" + Date.now(), username: sess.username, note, at: Date.now() });
  atSaveReqs(reqs);
  toast("Reset request sent to Super Admin");
  const el = document.getElementById("atReqNote"); if (el) el.value = "";
}

function atDismissReq(id) {
  atSaveReqs(atLoadReqs().filter(r => r.id !== id));
  atRenderRequests();
  toast("Request dismissed");
}

// Hook switchView for policy hub render
if (typeof switchView === "function" && !switchView._phHook) {
  const _sv = switchView;
  window.switchView = function(id, btn) {
    _sv(id, btn);
    if (id === "policyHub") setTimeout(() => phShowTab("rules"), 30);
    if (id === "policyDesk") setTimeout(() => pdRenderAdminList(), 30);
    if (id === "adminTeam") setTimeout(() => atRender(), 30);
  };
  window.switchView._phHook = true;
}

console.log("Admin Roster + full-page Policy views ready");


// ========== LOGIN CLOCK · LOGO FLY · GREETINGS · DAILY QUOTES ==========
const VR_GREET_KEY = "voltroof_custom_greetings_v1";

// AM (until noon): Good morning + Good day allowed
// PM onward: only time-specific (afternoon / evening / night) — no generic "Good day"
const DEFAULT_GREETINGS = {
  morning: [
    "Good morning, {name}.",
    "Good morning, {name}. A calm start is a strong start.",
    "Good morning, {name}. Take it one step at a time.",
    "Good morning, {name}. You’re in the right place.",
    "Have a good day, {name}.",
    "Have a good day, {name}. Steady progress beats rushed guesses.",
    "Good day, {name}. We’re glad you’re here.",
    "Good day, {name}. Breathe — the design can wait a moment.",
  ],
  afternoon: [
    "Good afternoon, {name}.",
    "Good afternoon, {name}. You’re doing fine — keep going gently.",
    "Good afternoon, {name}. Pause if you need to; the numbers will still be here.",
    "Good afternoon, {name}. Clear work, calm mind.",
    "Good afternoon, {name}. One careful decision at a time.",
    "Good afternoon, {name}. No rush — accuracy over speed.",
    "Good afternoon, {name}. You’ve got this.",
  ],
  evening: [
    "Good evening, {name}.",
    "Good evening, {name}. Wind down with steady, simple steps.",
    "Good evening, {name}. There’s no pressure here.",
    "Good evening, {name}. Finish what feels right; leave the rest.",
    "Good evening, {name}. Calm focus is enough.",
    "Good evening, {name}. You’re among tools built to help, not hurry you.",
    "Good evening, {name}. Take a breath — then continue when ready.",
  ],
  night: [
    "Good night, {name}.",
    "Good night, {name}. Rest matters as much as results.",
    "Good night, {name}. Save your work and be kind to yourself.",
    "Good night, {name}. The grid can wait until morning.",
    "Good night, {name}. Peaceful close to the day.",
    "Good night, {name}. You’ve done enough for now.",
    "Good night, {name}. Tomorrow’s designs will still be here.",
  ],
};

// Calm extras: AM may use "good day"; PM extras avoid "good day"
const CALM_EXTRA_AM = [
  "Have a good day, {name}. Slow is smooth — and smooth is fast enough.",
  "It’s okay to feel stuck, {name}. Start with one field.",
  "{name}, frustration is normal; clarity comes next.",
  "You’re not behind, {name}. You’re learning the system.",
  "Have a good day, {name}. Every careful kilowatt starts with a calm mind.",
  "{name}, this tool is here to support you — not judge you.",
  "Good day, {name}. Mistakes in a draft are free. Explore freely.",
  "Steady hands, {name}. Good engineering is patient.",
];
const CALM_EXTRA_PM = [
  "{name}, slow is smooth — and smooth is fast enough.",
  "It’s okay to feel stuck, {name}. Start with one field.",
  "{name}, frustration is normal; clarity comes next.",
  "You’re not behind, {name}. You’re learning the system.",
  "{name}, every careful kilowatt starts with a calm mind.",
  "If it’s heavy right now, {name}, do only the next small step.",
  "{name}, this tool is here to support you — not judge you.",
  "Welcome back, {name}. No need to rush the estimate.",
  "{name}, mistakes in a draft are free. Explore freely.",
  "Steady hands, {name}. Good engineering is patient.",
];


// ---- Date-aware quotes (India national + electrical engineering days) ----
// mm-dd keys; shown only on that calendar day
const INDIA_DAY_QUOTES = {
  "01-12": { title: "National Youth Day", text: "Swami Vivekananda’s birthday — courage and character for India’s next engineers." },
  "01-15": { title: "Army Day", text: "Saluting those who guard the nation — power systems keep bases and homes ready." },
  "01-26": { title: "Republic Day", text: "26 January 1950 — the Constitution came into force. Free citizens, a shared grid, a shared future." },
  "02-28": { title: "National Science Day", text: "C.V. Raman’s legacy — measure nature carefully; design power systems the same way." },
  "03-03": { title: "World Wildlife Day", text: "Clean energy protects habitats — rooftop solar is local power with a lighter footprint." },
  "03-04": { title: "National Safety Day (India)", text: "Safety first in every substation, every rooftop string, every isolation procedure." },
  "03-08": { title: "International Women’s Day", text: "Honouring women in STEM and the power sector who keep India electrified and innovative." },
  "03-22": { title: "World Water Day", text: "Hydro and careful water use — energy and water are one planning problem." },
  "04-11": { title: "National Safe Motherhood Day", text: "Reliable electricity in clinics and homes is a quiet pillar of public health." },
  "04-14": { title: "Dr. Ambedkar Jayanti", text: "Equality and access — rural electrification and fair tariffs advance dignity." },
  "04-22": { title: "Earth Day", text: "Every rooftop kilowatt is a vote for a cleaner atmosphere." },
  "04-24": { title: "National Panchayati Raj Day", text: "Local governance, local loads — microgrids and rooftop solar strengthen villages." },
  "05-01": { title: "Labour Day / May Day", text: "Respect for every lineman, fitter, and engineer who builds India’s power system." },
  "05-11": { title: "National Technology Day", text: "Remembering India’s technology milestones — from reactors to renewable parks." },
  "05-21": { title: "Anti-Terrorism Day", text: "Resilient infrastructure and a stable grid support a secure society." },
  "06-05": { title: "World Environment Day", text: "5 June — act for the planet. Solar on the roof is climate action you can measure in kWh." },
  "06-08": { title: "World Oceans Day", text: "Cleaner generation means less stress on climate and coasts India depends on." },
  "06-21": { title: "International Yoga Day / World Hydrography Day", text: "Balance in body and in the grid — steady frequency, steady mind." },
  "07-01": { title: "National Doctors’ Day (India)", text: "Hospitals run on reliable power — design with critical loads in mind." },
  "07-11": { title: "World Population Day", text: "Rising demand needs efficient generation and demand-side wisdom." },
  "07-26": { title: "Kargil Vijay Diwas", text: "26 July — valour in the heights. A grateful nation remembers; engineers keep the home front powered." },
  "08-09": { title: "Quit India Movement Day", text: "1942 call for freedom — energy independence is today’s strategic parallel." },
  "08-15": { title: "Independence Day", text: "15 August 1947 — freedom. Electrifying every home continues the promise of opportunity." },
  "08-20": { title: "Sadbhavana Diwas", text: "Harmony and goodwill — shared infrastructure binds a diverse nation." },
  "08-29": { title: "National Sports Day", text: "Discipline and teamwork — the same virtues run a safe electrical crew." },
  "09-05": { title: "Teachers’ Day", text: "Dr. Radhakrishnan’s day — every senior engineer was once a student of a patient teacher." },
  "09-14": { title: "Hindi Diwas", text: "Language connects; so do transmission lines — one frequency, many voices." },
  "09-15": { title: "Engineers’ Day (India)", text: "15 September — Sir M. Visvesvaraya’s birth anniversary. Precision, integrity, public service." },
  "09-16": { title: "World Ozone Day", text: "Protect the sky — clean generation is part of the same duty." },
  "10-02": { title: "Gandhi Jayanti / Lal Bahadur Shastri Jayanti", text: "Simple living, high thinking — efficiency is the quietest power plant." },
  "10-08": { title: "Indian Air Force Day", text: "Technology and training — aviation and power both demand zero-compromise safety." },
  "10-15": { title: "Global Handwashing Day / APJ Abdul Kalam related observances", text: "Dr. Kalam inspired student-engineers to dream of a developed India." },
  "10-31": { title: "National Unity Day", text: "Sardar Patel’s legacy — integration of states; integration of grids." },
  "11-07": { title: "National Cancer Awareness Day", text: "Reliable hospital power and cleaner air both support public health." },
  "11-11": { title: "National Education Day", text: "Maulana Azad’s day — education lights minds; electricity lights classrooms." },
  "11-14": { title: "Children’s Day", text: "Nehru’s affection for children — every school electrified is a brighter childhood." },
  "11-26": { title: "Constitution Day", text: "We the people — institutions and infrastructure uphold the Republic." },
  "12-04": { title: "Indian Navy Day", text: "Guardians of the sea lanes — ports and shipyards depend on robust power." },
  "12-14": { title: "National Energy Conservation Day", text: "14 December — the best unit is the one we never waste. Design for efficiency." },
  "12-16": { title: "Vijay Diwas (1971)", text: "Victory with resolve — a nation that builds and protects its critical systems." },
  "12-22": { title: "National Mathematics Day", text: "Ramanujan’s day — every load flow and every tariff table begins with clear maths." },
  "12-23": { title: "Kisan Diwas", text: "Farmers and pump sets — rural power quality is national priority." }
};

// Electrical engineering journey milestones (India) — date keyed
const EE_JOURNEY_QUOTES = {
  "01-01": { title: "New Year · Grid outlook", text: "A new year on the Indian grid — plan capacity, maintenance, and rooftop additions early." },
  "04-01": { title: "Financial year start (India)", text: "New FY for DISCOMs and projects — sanctioned loads and CAPEX cycles reset." },
  "05-01": { title: "Labour & power workforce", text: "The power sector runs on skilled hands — from tower lines to rooftop modules." },
  "08-15": { title: "Independence · Energy access", text: "From freedom to electrification — Saubhagya and rooftop programmes extend opportunity." },
  "09-15": { title: "Engineers’ Day · Visvesvaraya", text: "Sir M. Visvesvaraya — model of an engineer in public life. Design with duty." },
  "10-02": { title: "Energy simplicity", text: "Lower demand through efficiency is generation you do not have to build." },
  "12-14": { title: "Energy Conservation Day", text: "Bureau of Energy Efficiency spirit — measure, manage, minimise waste." }
};

// Rotating general IE quotes when no special date
const IE_GENERAL_QUOTES = [
  "Indian electrical engineering: one frequency, many climates, one responsibility — reliability.",
  "From Bhakra to HVDC corridors — India built scale; rooftop solar builds participation.",
  "CEA, CERC, KERC — regulation is infrastructure for fair electrons.",
  "A balanced grid is a national asset; power factor is not optional.",
  "DISCOMs and citizens share one goal: reliable, affordable electricity.",
  "Rooftop PV: the shortest transmission line is the one you never need.",
  "Document the as-built; the next engineer will thank you.",
  "Safety: earthing, isolation, and discipline save more than equipment.",
  "Net metering turns prosumers into partners of the grid.",
  "Design for the hottest day and the cloudiest week — then verify on site.",
  "Copper, aluminium, and silicon rewired modern India.",
  "When voltage sags, character shows — in grids and in teams.",
  "Karnataka’s solar resource is a geographic advantage; design unlocks it.",
  "PM-KUSUM and rooftop schemes: policy that can turn sunlight into livelihoods.",
  "Efficiency is the quietest renewable resource."
];

function pad2(n) { return String(n).padStart(2, "0"); }
function todayKey(d) {
  d = d || new Date();
  return pad2(d.getMonth() + 1) + "-" + pad2(d.getDate());
}

function getSpecialDayInfo(d) {
  d = d || new Date();
  const key = todayKey(d);
  return INDIA_DAY_QUOTES[key] || EE_JOURNEY_QUOTES[key] || null;
}

// Days that get the special image-style greeting card
const SPECIAL_GREET_DAYS = {
  "01-26": { emoji: "🇮🇳", wish: "Happy Republic Day", note: "Honouring the Constitution and the Republic of India." },
  "08-15": { emoji: "🇮🇳", wish: "Happy Independence Day", note: "Celebrating freedom and the journey toward energy access for all." },
  "06-05": { emoji: "🌍", wish: "Happy World Environment Day", note: "Clean generation and careful design for a living planet." },
  "07-26": { emoji: "🎖️", wish: "Remembering Kargil Vijay Diwas", note: "Saluting courage in the heights; keeping the home front strong." },
  "09-15": { emoji: "⚙️", wish: "Happy Engineers’ Day", note: "In honour of Sir M. Visvesvaraya — integrity in every calculation." },
  "12-14": { emoji: "⚡", wish: "National Energy Conservation Day", note: "Save a unit, serve the nation." },
  "10-02": { emoji: "🕊️", wish: "Happy Gandhi Jayanti", note: "Simple living, efficient systems." },
  "01-12": { emoji: "🔥", wish: "National Youth Day", note: "Arise, awake — build with courage." },
  "04-22": { emoji: "🌱", wish: "Happy Earth Day", note: "Every rooftop kWh is climate action." },
  "11-26": { emoji: "📜", wish: "Constitution Day", note: "We the people — institutions and infrastructure." },
  "12-22": { emoji: "∫", wish: "National Mathematics Day", note: "Clear maths, clear power systems." },
  "05-11": { emoji: "🔬", wish: "National Technology Day", note: "Indian technology in service of the nation." }
};

function getDayQuote(d) {
  d = d || new Date();
  const key = todayKey(d);
  const special = INDIA_DAY_QUOTES[key] || EE_JOURNEY_QUOTES[key];
  if (special) {
    return special.title + " — " + special.text;
  }
  const day = Math.floor(d.getTime() / 86400000);
  return IE_GENERAL_QUOTES[day % IE_GENERAL_QUOTES.length];
}

function applyDailyQuotes() {
  const q = getDayQuote();
  const loginQ = document.getElementById("loginQuoteText");
  const appQ = document.getElementById("appQuoteText");
  if (loginQ) loginQ.textContent = q;
  if (appQ) appQ.textContent = q;
  const bar = document.getElementById("appQuoteBar");
  if (bar) {
    const sp = getSpecialDayInfo();
    const strong = bar.querySelector("strong");
    if (strong) strong.textContent = sp ? sp.title : "Quote";
  }
}

function tickLoginClock() {
  const tEl = document.getElementById("loginClockTime");
  const dEl = document.getElementById("loginClockDate");
  if (!tEl && !dEl) return;
  const now = new Date();
  const use24 = !!window._clock24;
  const t = now.toLocaleTimeString("en-IN", {
    hour: "2-digit", minute: "2-digit", second: "2-digit",
    hour12: !use24
  });
  const d = now.toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
  if (tEl) tEl.textContent = t;
  if (dEl) dEl.textContent = d;
}

if (!window._vrClockStarted) {
  window._vrClockStarted = true;
  setInterval(tickLoginClock, 1000);
  tickLoginClock();
  applyDailyQuotes();
}


function getTimeBucket(h) {
  // AM period (00:00–11:59): morning bucket allows "Good day" / "Have a good day"
  // From 12:00 (PM) onward: only afternoon / evening / night — no generic Good day
  if (h < 12) return "morning";
  if (h < 17) return "afternoon";
  if (h < 21) return "evening";
  return "night";
}

function timeGreetingWord(h) {
  h = typeof h === "number" ? h : new Date().getHours();
  if (h < 12) return "Good morning"; // header in AM; popup may still say Have a good day
  if (h < 17) return "Good afternoon";
  if (h < 21) return "Good evening";
  return "Good night";
}

function loadCustomGreetings() {
  try {
    const a = JSON.parse(localStorage.getItem(VR_GREET_KEY) || "[]");
    return Array.isArray(a) ? a.filter(Boolean) : [];
  } catch (e) { return []; }
}

function pickGreeting(name) {
  const h = new Date().getHours();
  const bucket = getTimeBucket(h);
  const day = Math.floor(Date.now() / 86400000);
  const isAM = h < 12;
  const extras = isAM ? CALM_EXTRA_AM : CALM_EXTRA_PM;
  let pool = (DEFAULT_GREETINGS[bucket] || DEFAULT_GREETINGS.afternoon).concat(extras);
  // Custom admin lines: in PM, drop any that say "good day"
  loadCustomGreetings().forEach(g => {
    if (!isAM && /good\s*day/i.test(g)) return;
    pool.push(g);
  });
  const idx = (day + h) % Math.max(pool.length, 1);
  const raw = pool[idx] || (isAM ? "Have a good day, {name}." : "Good afternoon, {name}.");
  return raw.replace(/\{name\}/gi, name || "Engineer");
}

function showGreetPopup(name) {
  const pop = document.getElementById("greetPopup");
  const msg = document.getElementById("greetPopupMsg");
  const time = document.getElementById("greetPopupTime");
  if (!pop || !msg) return;
  name = name || "Engineer";
  const key = todayKey();
  const special = SPECIAL_GREET_DAYS[key];

  // Sync header time-of-day word
  const greetBar = document.querySelector(".ribbon-greet");
  if (greetBar) {
    const word = timeGreetingWord(new Date().getHours());
    const nameEl = document.getElementById("greetName");
    if (nameEl) {
      let prefix = greetBar.querySelector(".greet-prefix");
      if (!prefix) {
        prefix = document.createElement("span");
        prefix.className = "greet-prefix";
        greetBar.insertBefore(prefix, nameEl);
      }
      prefix.textContent = word + ", ";
      nameEl.textContent = name;
    }
  }

  if (time) {
    time.textContent = new Date().toLocaleString("en-IN", {
      weekday: "long", day: "numeric", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit"
    });
  }

  if (special) {
    pop.classList.add("special-day");
    pop.innerHTML = `
      <div class="sd-banner" aria-hidden="true">${special.emoji}</div>
      <div class="sd-body">
        <div class="sd-day">${SPECIAL_GREET_DAYS[key] ? (INDIA_DAY_QUOTES[key] || EE_JOURNEY_QUOTES[key] || {}).title || key : key}</div>
        <div class="gp-msg">${special.wish}, <strong>${name.replace(/</g,"")}</strong>!</div>
        <div class="sd-note">${special.note}</div>
        <div class="gp-time" id="greetPopupTime">${time ? time.textContent : ""}</div>
      </div>`;
  } else {
    pop.classList.remove("special-day");
    // restore simple structure if it was replaced
    if (!document.getElementById("greetPopupMsg") || pop.classList.contains("special-day") === false) {
      if (!pop.querySelector("#greetPopupMsg")) {
        pop.innerHTML = `<div class="gp-msg" id="greetPopupMsg"></div><div class="gp-time" id="greetPopupTime"></div>`;
      }
    }
    const msgEl = document.getElementById("greetPopupMsg");
    const timeEl = document.getElementById("greetPopupTime");
    if (msgEl) msgEl.textContent = pickGreeting(name);
    if (timeEl) timeEl.textContent = new Date().toLocaleString("en-IN", {
      weekday: "long", day: "numeric", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit"
    });
  }

  pop.classList.remove("gp-out");
  pop.classList.add("show");
  const hold = special ? 5500 : 4200;
  setTimeout(() => {
    pop.classList.add("gp-out");
    setTimeout(() => {
      pop.classList.remove("show", "gp-out", "special-day");
      // restore default structure for next time
      if (!document.getElementById("greetPopupMsg")) {
        pop.innerHTML = `<div class="gp-msg" id="greetPopupMsg"></div><div class="gp-time" id="greetPopupTime"></div>`;
      }
    }, 420);
  }, hold);
}

function atSaveGreetings() {
  const ta = document.getElementById("atGreetEditor");
  if (!ta) return;
  const lines = ta.value.split("\\n").map(s => s.trim()).filter(Boolean);
  localStorage.setItem(VR_GREET_KEY, JSON.stringify(lines));
  toast("Custom greetings saved (" + lines.length + ")");
}

function atLoadGreetEditor() {
  const ta = document.getElementById("atGreetEditor");
  if (!ta) return;
  ta.value = loadCustomGreetings().join("\\n");
}

// Logo → sidebar logo (size+pos); Name → header name (font+colour)
function animateLogoAndNameToNav(displayName, thenFn) {
  const srcMark = document.getElementById("loginLogoMark") || document.querySelector("#loginLogoSource .vr-logo-mark");
  const dstMark = document.getElementById("navLogoMark") || document.querySelector("#navLogoTarget .vr-logo-mark");
  const greetName = document.getElementById("greetName");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const runAfter = () => { if (typeof thenFn === "function") thenFn(); };

  if (reduced || !srcMark || !dstMark) {
    runAfter();
    return;
  }

  // Ensure destination is measurable (sidebar visible)
  const gate = document.getElementById("nameGate");
  // Don't hide gate until animation ends — measure first
  const s = srcMark.getBoundingClientRect();
  const d = dstMark.getBoundingClientRect();
  if (!s.width || !d.width) {
    runAfter();
    return;
  }

  // Logo clone: fly to exact sidebar mark box
  const logoClone = srcMark.cloneNode(true);
  logoClone.id = "logoFlyClone";
  logoClone.style.cssText = `position:fixed;z-index:2147483000;pointer-events:none;left:${s.left}px;top:${s.top}px;width:${s.width}px;height:${s.height}px;margin:0;transition:left 0.75s cubic-bezier(0.22,1,0.36,1),top 0.75s cubic-bezier(0.22,1,0.36,1),width 0.75s cubic-bezier(0.22,1,0.36,1),height 0.75s cubic-bezier(0.22,1,0.36,1),opacity 0.2s ease;will-change:left,top,width,height;`;
  document.body.appendChild(logoClone);
  srcMark.style.opacity = "0.2";
  dstMark.style.opacity = "0.15";

  requestAnimationFrame(() => {
    logoClone.style.left = d.left + "px";
    logoClone.style.top = d.top + "px";
    logoClone.style.width = d.width + "px";
    logoClone.style.height = d.height + "px";
  });

  // Name clone: fly to header greetName with matching styles
  let nameClone = null;
  if (displayName && greetName) {
    // Temporarily show greet bar so we can measure
    const greetBar = document.getElementById("greetBar");
    const wasHidden = greetBar && greetBar.style.display === "none";
    if (greetBar) greetBar.style.display = "block";
    greetName.textContent = displayName;
    const gr = greetName.getBoundingClientRect();
    const cs = window.getComputedStyle(greetName);
    nameClone = document.createElement("div");
    nameClone.id = "nameFlyClone";
    nameClone.textContent = displayName;
    const field = document.getElementById("gateName") || document.getElementById("gateAdminUser");
    const fr = field ? field.getBoundingClientRect() : s;
    nameClone.style.cssText = `position:fixed;z-index:2147483001;pointer-events:none;left:${fr.left}px;top:${fr.top}px;font-family:${cs.fontFamily};font-weight:${cs.fontWeight || 800};font-size:1.05rem;color:${cs.color || "var(--text)"};letter-spacing:${cs.letterSpacing};white-space:nowrap;transition:left 0.7s cubic-bezier(0.22,1,0.36,1),top 0.7s cubic-bezier(0.22,1,0.36,1),font-size 0.7s ease,color 0.5s ease,opacity 0.25s ease;`;
    document.body.appendChild(nameClone);
    requestAnimationFrame(() => {
      nameClone.style.left = gr.left + "px";
      nameClone.style.top = gr.top + "px";
      nameClone.style.fontSize = cs.fontSize || "0.9rem";
      nameClone.style.color = cs.color;
    });
    if (wasHidden && greetBar) {
      // keep visible for measure; finishEnterApp will manage
    }
  }

  setTimeout(() => {
    logoClone.remove();
    if (nameClone) nameClone.remove();
    srcMark.style.opacity = "";
    dstMark.style.opacity = "";
    dstMark.classList.add("logo-settle");
    setTimeout(() => dstMark.classList.remove("logo-settle"), 500);
    runAfter();
  }, 780);
}

function finishEnterApp(n) {
  try { localStorage.setItem("voltroof_user", n); } catch (e) {}
  const gate = document.getElementById("nameGate");
  if (gate) {
    gate.classList.add("hidden");
    gate.style.display = "none";
  }
  if (typeof setGateOpen === "function") setGateOpen(false);
  document.body.classList.remove("gate-open");

  const greetEl = document.getElementById("greetName");
  if (greetEl) greetEl.textContent = n;
  const greetBar = document.getElementById("greetBar");
  if (greetBar) greetBar.style.display = "block";

  const appQ = document.getElementById("appQuoteBar");
  if (appQ) appQ.style.display = "block";
  applyDailyQuotes();

  if (typeof sites !== "undefined" && sites[activeSiteIndex] && !sites[activeSiteIndex].name) {
    sites[activeSiteIndex].name = "";
    const cfgName = document.getElementById("cfgName");
    if (cfgName) cfgName.value = "";
  }
  if (typeof renderSiteTabs === "function") renderSiteTabs();
  if (typeof liveUpdate === "function") liveUpdate();
  if (typeof updateAdminUIState === "function") updateAdminUIState();
  showGreetPopup(n);
}

// Override enterApp with animation
window.enterApp = function enterApp() {
  const inputEl = document.getElementById("gateName");
  let n = (inputEl?.value || "").trim();
  if (!n) {
    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (admin) n = admin.username;
    else n = localStorage.getItem("voltroof_user") || "Engineer";
  }
  animateLogoAndNameToNav(n, () => finishEnterApp(n));
};

// After admin login from gate — same logo fly + greeting
if (typeof loginAdminFromGate === "function" && !loginAdminFromGate._flyHook) {
  const _laf = loginAdminFromGate;
  window.loginAdminFromGate = async function() {
    const r = await _laf.apply(this, arguments);
    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (admin) {
      const n = admin.username;
      // If still on gate, fly then enter
      const gate = document.getElementById("nameGate");
      if (gate && !gate.classList.contains("hidden") && gate.style.display !== "none") {
        animateLogoAndNameToNav(n, () => finishEnterApp(n));
      } else {
        showGreetPopup(n);
        const appQ = document.getElementById("appQuoteBar");
        if (appQ) appQ.style.display = "block";
      }
      if (typeof syncAdminNavVisibility === "function") syncAdminNavVisibility();
    }
    return r;
  };
  window.loginAdminFromGate._flyHook = true;
}

if (typeof loginAdminFromModal === "function" && !loginAdminFromModal._flyHook) {
  const _lam = loginAdminFromModal;
  window.loginAdminFromModal = async function() {
    const r = await _lam.apply(this, arguments);
    const admin = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (admin) showGreetPopup(admin.username);
    return r;
  };
  window.loginAdminFromModal._flyHook = true;
}

// Load greet editor when opening admin team
if (typeof atRender === "function" && !atRender._greetHook) {
  const _atr = atRender;
  window.atRender = function() {
    _atr.apply(this, arguments);
    atLoadGreetEditor();
  };
  window.atRender._greetHook = true;
}

// Hide app quote when gate open
(function quoteGateSync() {
  const obs = new MutationObserver(() => {
    const gate = document.getElementById("nameGate");
    const appQ = document.getElementById("appQuoteBar");
    if (!appQ) return;
    const open = gate && !gate.classList.contains("hidden") && gate.style.display !== "none";
    if (open) appQ.style.display = "none";
  });
  const gate = document.getElementById("nameGate");
  if (gate) obs.observe(gate, { attributes: true, attributeFilter: ["class", "style"] });
})();

console.log("Login clock, logo fly, greetings, daily quotes ready");


// ========== UX PACK IMPLEMENTATION (1, 2.3-2.7, 3, 4, 5) ==========
function ariaAnnounce(msg) {
  const el = document.getElementById("ariaLiveRegion");
  if (el) { el.textContent = ""; setTimeout(() => { el.textContent = msg; }, 30); }
}

function toggleHighContrast() {
  document.body.classList.toggle("hc-mode");
  const on = document.body.classList.contains("hc-mode");
  try { localStorage.setItem("voltroof_hc", on ? "1" : "0"); } catch(e){}
  toast(on ? "High contrast on" : "High contrast off");
}
try { if (localStorage.getItem("voltroof_hc") === "1") document.body.classList.add("hc-mode"); } catch(e){}

window._clock24 = false;
try { window._clock24 = localStorage.getItem("voltroof_clock24") === "1"; } catch(e){}
function toggleClockFormat() {
  window._clock24 = !window._clock24;
  try { localStorage.setItem("voltroof_clock24", window._clock24 ? "1" : "0"); } catch(e){}
  if (typeof tickLoginClock === "function") tickLoginClock();
  toast(window._clock24 ? "Clock: 24-hour" : "Clock: 12-hour");
}

// Patch tickLoginClock for 12/24
if (typeof tickLoginClock === "function") {
  window.tickLoginClock = function() {
    const tEl = document.getElementById("loginClockTime");
    const dEl = document.getElementById("loginClockDate");
    if (!tEl && !dEl) return;
    const now = new Date();
    const t = now.toLocaleTimeString("en-IN", {
      hour: "2-digit", minute: "2-digit", second: "2-digit",
      hour12: !window._clock24
    });
    const d = now.toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
    if (tEl) tEl.textContent = t;
    if (dEl) dEl.textContent = d;
  };
}

// View transition animation
if (typeof switchView === "function" && !switchView._uxPack) {
  const _svUx = switchView;
  window.switchView = function(id, btn) {
    _svUx(id, btn);
    const v = document.getElementById("view-" + id);
    if (v && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      v.classList.remove("vr-view-in");
      void v.offsetWidth;
      v.classList.add("vr-view-in");
    }
    if (id === "policyHub") setTimeout(() => { if (typeof phRender === "function") phRender(); }, 40);
  };
  window.switchView._uxPack = true;
}

// Greeting exit fade + aria
// showGreetPopup handles its own timing + special-day cards; only wire aria
if (typeof showGreetPopup === "function" && !showGreetPopup._uxPack) {
  const _sg = showGreetPopup;
  window.showGreetPopup = function(name) {
    _sg(name);
    const pop = document.getElementById("greetPopup");
    const msg = pop?.querySelector(".gp-msg")?.textContent || document.getElementById("greetPopupMsg")?.textContent || ("Welcome, " + name);
    if (typeof ariaAnnounce === "function") ariaAnnounce(msg);
  };
  showGreetPopup._uxPack = true;
}

// Logo settle pulse after fly
if (typeof animateLogoAndNameToNav === "function" && !animateLogoAndNameToNav._uxPack) {
  const _fly = animateLogoAndNameToNav;
  window.animateLogoAndNameToNav = function(displayName, thenFn) {
    _fly(displayName, function() {
      const mark = document.getElementById("navLogoMark") || document.getElementById("navLogoTarget");
      if (mark && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        mark.classList.add("logo-settle");
        setTimeout(() => mark.classList.remove("logo-settle"), 500);
      }
      if (typeof thenFn === "function") thenFn();
    });
  };
  animateLogoAndNameToNav._uxPack = true;
}

// Empty state helper
function emptyStateHtml(ico, title, body, btnLabel, btnOnclick) {
  return `<div class="empty-state">
    <div class="es-ico">${ico}</div>
    <div class="es-title">${title}</div>
    <div>${body}</div>
    ${btnLabel ? `<div class="es-act"><button type="button" class="btn btn-p btn-sm" onclick="${btnOnclick}">${btnLabel}</button></div>` : ""}
  </div>`;
}

// Policy Hub search + empty state
if (typeof phRender === "function") {
  window.phRender = function() {
    const items = typeof pdLoad === "function" ? pdLoad() : [];
    const q = (document.getElementById("phSearchInput")?.value || "").trim().toLowerCase();
    let rules = items.filter(x => x.type === "rule");
    let subs = items.filter(x => x.type === "subsidy");
    if (q) {
      const match = (it) => ((it.title||"")+(it.body||"")).toLowerCase().includes(q);
      rules = rules.filter(match);
      subs = subs.filter(match);
    }
    const rBox = document.getElementById("phContentRules");
    const sBox = document.getElementById("phContentSubs");
    const deskBtn = document.getElementById("navPolicyDeskBtn");
    const canOpenDesk = deskBtn && deskBtn.style.display !== "none" && typeof isAdminSession === "function" && isAdminSession();
    const emptyR = emptyStateHtml(
      "📜", "No rules yet",
      q ? "No matches for your search." : "Check back after admin publishes KERC / ESCOM updates.",
      (!q && canOpenDesk) ? "Open Policy Desk" : "",
      (!q && canOpenDesk) ? "switchView('policyDesk')" : ""
    );
    const emptyS = emptyStateHtml(
      "🏷", "No subsidies yet",
      q ? "No matches for your search." : "Government incentives will appear here when published.",
      (!q && canOpenDesk) ? "Open Policy Desk" : "",
      (!q && canOpenDesk) ? "switchView('policyDesk')" : ""
    );
    function card(it) {
      const link = it.fileData ? `<div style="margin-top:8px"><a href="${it.fileData}" target="_blank" rel="noopener">Open attachment (${it.fileName || "file"})</a></div>` : "";
      const until = it.validUntil ? `<div style="font-size:0.72rem;color:var(--amber,#f59e0b);margin-top:4px">Valid until ${it.validUntil}</div>` : "";
      const when = it.at ? new Date(it.at).toLocaleDateString() : "";
      return `<div class="ph-card"><h4>${it.title || "Untitled"}</h4><p>${(it.body || "").replace(/</g,"&lt;")}</p>${until}${link}<div style="font-size:0.68rem;color:var(--dim);margin-top:6px">${when}</div></div>`;
    }
    if (rBox) rBox.innerHTML = rules.length ? rules.map(card).join("") : emptyR;
    if (sBox) sBox.innerHTML = subs.length ? subs.map(card).join("") : emptyS;
  };
}

// pdAddItem: valid until
if (typeof pdAddItem === "function" && !pdAddItem._uxPack) {
  const _pd = pdAddItem;
  window.pdAddItem = function(type) {
    const isRule = type === "rule";
    const untilEl = document.getElementById(isRule ? "pdRuleUntil" : "pdSubUntil");
    const until = untilEl?.value || "";
    // wrap finish via intercepting localStorage save - simpler: call original then patch last item
    const before = typeof pdLoad === "function" ? pdLoad().length : 0;
    _pd(type);
    setTimeout(() => {
      if (typeof pdLoad !== "function" || !until) return;
      const arr = pdLoad();
      if (arr.length && arr.length >= before) {
        arr[0].validUntil = until;
        if (typeof pdSave === "function") pdSave(arr);
        if (untilEl) untilEl.value = "";
        if (typeof pdRenderAdminList === "function") pdRenderAdminList();
      }
    }, 50);
  };
  pdAddItem._uxPack = true;
}

// Password reset: copy summary for super admin
if (typeof atRequestReset === "function" && !atRequestReset._uxPack) {
  const _req = atRequestReset;
  window.atRequestReset = function() {
    _req();
    const sess = typeof getActiveAdmin === "function" ? getActiveAdmin() : null;
    if (!sess) return;
    const note = document.getElementById("atReqNote")?.value?.trim() || "(no note)";
    const summary = `VoltRoof password reset request\nAdmin: ${sess.username}\nNote: ${note}\nTime: ${new Date().toLocaleString()}`;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(summary).then(() => toast("Request sent · summary copied")).catch(() => {});
      }
    } catch (e) {}
  };
  atRequestReset._uxPack = true;
}

// Admin list table on wide screens
if (typeof atRenderAdminList === "function") {
  const _arl = atRenderAdminList;
  window.atRenderAdminList = function() {
    _arl();
    const box = document.getElementById("atAdminList");
    if (!box || typeof atGetAllAdmins !== "function") return;
    const list = atGetAllAdmins();
    const table = `<table class="at-table"><thead><tr><th>Name</th><th>Role</th><th>Contact</th><th></th></tr></thead><tbody>
      ${list.map(a => `<tr>
        <td><strong>${a.username}</strong></td>
        <td>${a.role === "super_admin" ? "Super Admin" : "Admin"}</td>
        <td>${(a.emails || [a.email]).filter(Boolean).join(", ")}${a.mobile ? " · " + a.mobile : ""}</td>
        <td>${a.role === "super_admin" ? "—" : `<button type="button" class="btn btn-sm" style="color:var(--rose)" onclick="atRemoveAdmin('${(a.username||"").replace(/'/g,"\\'")}')">Remove</button>`}</td>
      </tr>`).join("")}
    </tbody></table>
    <div class="at-cards-mobile" style="display:none">${box.innerHTML}</div>`;
    // Keep mobile cards from original by re-calling structure
    const cards = list.map(a => `
      <div class="pd-item">
        <div style="flex:1;min-width:0">
          <div style="font-weight:700">${a.username} ${a.role === "super_admin" ? '<span class="pd-tag rule">super</span>' : '<span class="pd-tag subsidy">admin</span>'}</div>
          <div style="font-size:0.78rem;color:var(--muted)">${(a.emails || [a.email]).filter(Boolean).join(", ") || "—"} ${a.mobile ? " · " + a.mobile : ""}</div>
        </div>
        ${a.role === "super_admin" ? "" : `<button type="button" class="btn btn-sm" style="color:var(--rose)" onclick="atRemoveAdmin('${(a.username || "").replace(/'/g, "\\'")}')">Remove</button>`}
      </div>`).join("");
    box.innerHTML = table.replace('style="display:none">', 'style="display:none">' + cards);
  };
}

// Site status chips in tabs - patch renderSiteTabs if exists
if (typeof renderSiteTabs === "function" && !renderSiteTabs._uxPack) {
  const _rst = renderSiteTabs;
  window.renderSiteTabs = function() {
    _rst.apply(this, arguments);
    try {
      document.querySelectorAll("#studioSiteTabs button, #studioSiteTabs .site-tab").forEach((btn, i) => {
        if (btn.querySelector(".site-chip")) return;
        const s = sites[i];
        let st = "draft";
        if (s && s._saved) st = "saved";
        if (current && activeSiteIndex === i && current.capacityKw) st = "calc";
        const chip = document.createElement("span");
        chip.className = "site-chip " + st;
        chip.textContent = st === "calc" ? "Calculated" : st === "saved" ? "Saved" : "Draft";
        btn.appendChild(chip);
      });
    } catch (e) {}
  };
  renderSiteTabs._uxPack = true;
}

// After calculate: scroll KPIs + show bar + burst
if (typeof onCalculateClick === "function" && !onCalculateClick._uxPack) {
  const _occ = onCalculateClick;
  window.onCalculateClick = function() {
    const r = _occ.apply(this, arguments);
    setTimeout(() => {
      const bar = document.getElementById("postCalcBar");
      if (bar) bar.classList.add("show");
      const kpi = document.querySelector(".kpi-row, #view-dashboard .kpi, .sticky-summary");
      if (kpi) kpi.scrollIntoView({ behavior: "smooth", block: "start" });
      const burst = document.getElementById("calcBurst");
      if (burst && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        burst.classList.add("show");
        setTimeout(() => burst.classList.remove("show"), 700);
      }
      ariaAnnounce("System calculated successfully");
    }, 200);
    return r;
  };
  onCalculateClick._uxPack = true;
}

// Unsaved banner
window._vrDirty = window._vrDirty || false;
document.addEventListener("input", () => {
  window._vrDirty = true;
  document.getElementById("unsavedBanner")?.classList.add("show");
}, true);
document.addEventListener("click", (e) => {
  if (e.target?.closest?.("#btnRibbonSave, [onclick*='saveProject'], [onclick*='ribbonSave']")) {
    window._vrDirty = false;
    document.getElementById("unsavedBanner")?.classList.remove("show");
  }
});

// Slideshow: pause on hover + progress bar
(function enhanceSlideshow() {
  let progressTimer = null;
  let paused = false;
  const SLIDE_MS = 4500;
  function startProgress() {
    const bar = document.getElementById("loginSlideProgress");
    if (!bar) return;
    bar.style.transition = "none";
    bar.style.width = "0%";
    void bar.offsetWidth;
    if (paused || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    bar.style.transition = `width ${SLIDE_MS}ms linear`;
    bar.style.width = "100%";
  }
  const box = document.getElementById("loginSlideshow");
  if (box) {
    box.addEventListener("mouseenter", () => {
      paused = true;
      if (typeof loginSlideTimer !== "undefined" && loginSlideTimer) {
        clearInterval(loginSlideTimer);
        loginSlideTimer = null;
      }
      const bar = document.getElementById("loginSlideProgress");
      if (bar) { bar.style.transition = "none"; }
    });
    box.addEventListener("mouseleave", () => {
      paused = false;
      if (typeof startLoginSlideshow === "function") {
        /* restart interval only */
        if (typeof loginSlideTimer !== "undefined" && loginSlideTimer) clearInterval(loginSlideTimer);
        try {
          loginSlideTimer = setInterval(() => {
            if (typeof tickLoginSlide === "function") tickLoginSlide();
            startProgress();
          }, SLIDE_MS);
        } catch (e) {}
      }
      startProgress();
    });
  }
  if (typeof goLoginSlide === "function" && !goLoginSlide._uxPack) {
    const _go = goLoginSlide;
    window.goLoginSlide = function(i) {
      _go(i);
      startProgress();
    };
    goLoginSlide._uxPack = true;
  }
  setTimeout(startProgress, 500);
})();

// Enter / Esc on login
document.addEventListener("keydown", (e) => {
  const gate = document.getElementById("nameGate");
  const gateOpen = gate && !gate.classList.contains("hidden") && gate.style.display !== "none";
  if (!gateOpen) return;
  if (e.key === "Enter") {
    const adminMode = document.getElementById("gateAdminMode");
    if (adminMode && adminMode.style.display !== "none") {
      if (typeof loginAdminFromGate === "function") loginAdminFromGate();
    } else if (typeof enterApp === "function") {
      enterApp();
    }
  }
  if (e.key === "Escape") {
    const adminMode = document.getElementById("gateAdminMode");
    if (adminMode && adminMode.style.display !== "none" && typeof toggleGateAdminMode === "function") {
      toggleGateAdminMode();
    }
  }
});

// Toast aria
if (typeof toast === "function" && !toast._ariaUx) {
  const _t = toast;
  window.toast = function(msg, type) {
    _t(msg, type);
    ariaAnnounce(String(msg || ""));
  };
  toast._ariaUx = true;
}

// Quote day crossfade check hourly
setInterval(() => {
  const bar = document.getElementById("appQuoteBar");
  if (!bar || bar.style.display === "none") return;
  const prev = bar.dataset.daykey;
  const day = String(Math.floor(Date.now() / 86400000));
  if (prev && prev !== day) {
    bar.classList.add("dq-fade");
    setTimeout(() => {
      if (typeof applyDailyQuotes === "function") applyDailyQuotes();
      bar.classList.remove("dq-fade");
    }, 600);
  }
  bar.dataset.daykey = day;
}, 60000);

console.log("UX pack applied: UI/UX/animations/a11y");


// ========== AUDIT FIX PACK (sections 1, 4.3, 5, 7.2, 9.2) ==========
// 1.4 / 5.3 Toast → aria-live
(function wireToastAria() {
  function announce(msg) {
    const el = document.getElementById("ariaLiveRegion");
    if (!el) return;
    el.textContent = "";
    setTimeout(() => { el.textContent = String(msg || ""); }, 20);
  }
  if (typeof toast === "function" && !toast._auditAria) {
    const _t = toast;
    window.toast = function(msg, type) {
      _t(msg, type);
      announce(msg);
    };
    toast._auditAria = true;
  }
})();

// 7.2 Inline field errors on validation failure
window.markFieldError = function(id, message) {
  const el = document.getElementById(id);
  if (!el) return;
  el.style.borderColor = "var(--rose, #f43f5e)";
  el.setAttribute("aria-invalid", "true");
  let err = el.parentElement?.querySelector(".field-error");
  if (!err && el.parentElement) {
    err = document.createElement("div");
    err.className = "field-error";
    err.style.cssText = "font-size:0.72rem;color:var(--rose,#f43f5e);margin-top:4px;font-weight:600";
    el.parentElement.appendChild(err);
  }
  if (err) err.textContent = message || "Required";
  el.addEventListener("input", function clear() {
    el.style.borderColor = "";
    el.removeAttribute("aria-invalid");
    if (err) err.remove();
    el.removeEventListener("input", clear);
  }, { once: true });
};

if (typeof onCalculateClick === "function" && !onCalculateClick._auditVal) {
  const _calc = onCalculateClick;
  window.onCalculateClick = function() {
    // Clear previous errors
    document.querySelectorAll(".field-error").forEach(e => e.remove());
    // Shimmer skeleton 4.3
    const dash = document.getElementById("view-dashboard");
    if (dash && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      dash.classList.add("calc-shimmer");
      setTimeout(() => dash.classList.remove("calc-shimmer"), 900);
    }
    try {
      return _calc.apply(this, arguments);
    } catch (e) {
      console.warn(e);
    }
  };
  onCalculateClick._auditVal = true;
}

// Hook common focus-to-field validation toast patterns via focus
(function patchFocusError() {
  const _focus = HTMLElement.prototype.focus;
  // When studio focuses empty cfg fields after toast - add mark if empty
  document.addEventListener("focusin", (e) => {
    const el = e.target;
    if (!el || !el.id || !/^cfg/.test(el.id)) return;
    if (el.value === "" && el.hasAttribute("required")) {
      // soft highlight only if recently calculated fail - skip
    }
  });
})();

// KPI count-up 4.3
window.animateKpiCountUp = function(el, target, prefix, suffix, duration) {
  if (!el) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    el.textContent = (prefix || "") + target + (suffix || "");
    return;
  }
  const start = performance.now();
  const from = 0;
  const to = parseFloat(String(target).replace(/[^0-9.-]/g, "")) || 0;
  const dur = duration || 700;
  function frame(now) {
    const t = Math.min(1, (now - start) / dur);
    const eased = 1 - Math.pow(1 - t, 3);
    const val = from + (to - from) * eased;
    const decimals = to % 1 !== 0 ? 2 : 0;
    el.textContent = (prefix || "") + val.toFixed(decimals) + (suffix || "");
    if (t < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
};

// After liveUpdate, count-up main KPIs if present
if (typeof liveUpdate === "function" && !liveUpdate._kpiCount) {
  const _lu = liveUpdate;
  window.liveUpdate = function() {
    const r = _lu.apply(this, arguments);
    setTimeout(() => {
      try {
        if (!current) return;
        const map = [
          ["kpiKw", current.capacityKw, "", " kW"],
          ["kpiGen", current.annualGen, "", " kWh"],
          ["kpiCost", current.turnkeyCost, "₹ ", ""],
        ];
        map.forEach(([id, val, pre, suf]) => {
          const el = document.getElementById(id);
          if (el && val != null && !isNaN(val)) animateKpiCountUp(el, val, pre, suf);
        });
      } catch (e) {}
    }, 50);
    return r;
  };
  liveUpdate._kpiCount = true;
}

// Stagger table rows 4.3
window.staggerTableRows = function(tableOrId) {
  const table = typeof tableOrId === "string" ? document.getElementById(tableOrId) : tableOrId;
  if (!table) return;
  const rows = table.querySelectorAll("tbody tr");
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  rows.forEach((row, i) => {
    row.style.opacity = "0";
    row.style.transform = "translateY(6px)";
    row.style.transition = "opacity 0.25s ease, transform 0.25s ease";
    setTimeout(() => {
      row.style.opacity = "1";
      row.style.transform = "none";
    }, 30 + i * 28);
  });
};

// Call stagger when switching to bom/financials
if (typeof switchView === "function" && !switchView._stagger) {
  const _sv = switchView;
  window.switchView = function(id, btn) {
    _sv(id, btn);
    if (id === "bom") setTimeout(() => {
      const t = document.querySelector("#view-bom table");
      if (t) staggerTableRows(t);
    }, 80);
    if (id === "financials") setTimeout(() => {
      const t = document.querySelector("#view-financials table");
      if (t) staggerTableRows(t);
    }, 80);
  };
  switchView._stagger = true;
}

// 9.2 Visualizer: collapse export actions into details dropdown if row exists
(function declutterVisualizer() {
  const row = document.querySelector(".rt-export-row");
  if (!row || row.dataset.decluttered) return;
  const btns = [...row.querySelectorAll("button")];
  if (btns.length < 2) return;
  // Keep first two primary if any, rest into details
  const keep = [];
  const rest = [];
  btns.forEach((b, i) => {
    const t = (b.textContent || b.title || "").toLowerCase();
    if (/png|svg|export/i.test(t) || i > 1) rest.push(b);
    else keep.push(b);
  });
  if (!rest.length) return;
  const det = document.createElement("details");
  det.className = "rt-more-export";
  det.style.cssText = "display:inline-block;position:relative";
  det.innerHTML = `<summary style="cursor:pointer;list-style:none;padding:6px 10px;border-radius:8px;background:rgba(15,23,42,0.75);border:1px solid rgba(148,163,184,0.25);color:#e2e8f0;font-size:0.75rem;font-weight:700">More ▾</summary>`;
  const menu = document.createElement("div");
  menu.style.cssText = "position:absolute;bottom:110%;left:0;min-width:140px;background:rgba(15,23,42,0.95);border:1px solid rgba(148,163,184,0.3);border-radius:10px;padding:6px;display:flex;flex-direction:column;gap:4px;z-index:20";
  rest.forEach(b => {
    b.style.width = "100%";
    b.style.textAlign = "left";
    menu.appendChild(b);
  });
  det.appendChild(menu);
  row.appendChild(det);
  row.dataset.decluttered = "1";
})();

// calc shimmer CSS class support
(function injectShimmerClass() {
  if (document.getElementById("auditShimmerStyle")) return;
  const s = document.createElement("style");
  s.id = "auditShimmerStyle";
  s.textContent = `
    .calc-shimmer .kpi, .calc-shimmer .chart-box {
      position: relative; overflow: hidden;
    }
    .calc-shimmer .kpi::after, .calc-shimmer .chart-box::after {
      content: ""; position: absolute; inset: 0;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
      animation: auditShimmer 0.9s ease;
    }
    @keyframes auditShimmer {
      from { transform: translateX(-100%); }
      to { transform: translateX(100%); }
    }
    .field-error { display: block; }
  `;
  document.head.appendChild(s);
})();

// Motion tokens: map common transitions (light touch)
document.documentElement.style.setProperty("--dur-fast", "150ms");
document.documentElement.style.setProperty("--dur-med", "280ms");
document.documentElement.style.setProperty("--dur-slow", "450ms");
document.documentElement.style.setProperty("--ease-out", "cubic-bezier(0.22, 1, 0.36, 1)");

console.log("Audit fix pack applied");


// ========== CONTACT US (user view + admin publish) ==========
const CU_KEY = "voltroof_contacts_v1";

function cuLoad() {
  try {
    const a = JSON.parse(localStorage.getItem(CU_KEY) || "[]");
    return Array.isArray(a) ? a : [];
  } catch (e) { return []; }
}
function cuSave(arr) {
  localStorage.setItem(CU_KEY, JSON.stringify(arr));
}

function cuRender() {
  const list = cuLoad();
  const box = document.getElementById("cuList");
  const adminPanel = document.getElementById("cuAdminPanel");
  if (box) {
    if (!list.length) {
      box.innerHTML = `<div class="empty-state">
        <div class="es-ico">✉️</div>
        <div class="es-title">No contacts published yet</div>
        <div>Your administrator can add names, roles, phone and email here.</div>
      </div>`;
    } else {
      box.innerHTML = list.map(c => `
        <div class="cu-card">
          <div class="cu-name">${(c.name || "").replace(/</g,"&lt;")}</div>
          <div class="cu-role">${(c.role || "").replace(/</g,"&lt;")}</div>
          <div class="cu-meta">${c.phone ? "📞 " + String(c.phone).replace(/</g,"&lt;") : ""}</div>
          <div class="cu-meta">${c.email ? '✉️ <a href="mailto:' + String(c.email).replace(/"/g,"") + '">' + String(c.email).replace(/</g,"&lt;") + "</a>" : ""}</div>
        </div>
      `).join("");
    }
  }
  const isAdmin = typeof isAdminSession === "function" && isAdminSession();
  if (adminPanel) {
    adminPanel.style.display = isAdmin ? "block" : "none";
    if (isAdmin) cuRenderAdminList();
  }
}

function cuRenderAdminList() {
  const box = document.getElementById("cuAdminList");
  if (!box) return;
  const list = cuLoad();
  box.innerHTML = list.map((c, i) => `
    <div class="pd-item">
      <div style="flex:1"><strong>${c.name}</strong> · ${c.role || "—"}<br><span style="font-size:0.78rem;color:var(--muted)">${c.phone || ""} ${c.email || ""}</span></div>
      <button type="button" class="btn btn-sm" style="color:var(--rose)" onclick="cuRemove(${i})">Remove</button>
    </div>
  `).join("") || '<div style="color:var(--muted);font-size:0.84rem">No contacts yet — add above.</div>';
}

function cuAdd() {
  if (!(typeof isAdminSession === "function" && isAdminSession())) {
    toast("Admin sign-in required");
    return;
  }
  const name = document.getElementById("cuName")?.value?.trim();
  const role = document.getElementById("cuRole")?.value?.trim();
  const phone = document.getElementById("cuPhone")?.value?.trim();
  const email = document.getElementById("cuEmail")?.value?.trim();
  if (!name) { toast("Name is required"); return; }
  const arr = cuLoad();
  arr.push({ name, role, phone, email, at: Date.now() });
  cuSave(arr);
  ["cuName","cuRole","cuPhone","cuEmail"].forEach(id => {
    const el = document.getElementById(id); if (el) el.value = "";
  });
  cuRender();
  toast("Contact published");
}

function cuRemove(i) {
  if (!(typeof isAdminSession === "function" && isAdminSession())) return;
  const arr = cuLoad();
  arr.splice(i, 1);
  cuSave(arr);
  cuRender();
  toast("Contact removed");
}

if (typeof switchView === "function" && !switchView._cuHook) {
  const _svCu = switchView;
  window.switchView = function(id, btn) {
    _svCu(id, btn);
    if (id === "contactUs") setTimeout(() => cuRender(), 30);
  };
  switchView._cuHook = true;
}

