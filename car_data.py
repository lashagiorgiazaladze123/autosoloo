# Comprehensive Car Database
CAR_MAKES_MODELS = {
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "e-tron", "RS3", "RS4", "RS5", "RS6", "RS7", "S3", "S4", "S5", "S6", "S7", "S8"],
    "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i3", "i4", "i8", "iX", "M2", "M3", "M4", "M5", "M8"],
    "Mercedes-Benz": ["A-Class", "B-Class", "C-Class", "CLA", "CLS", "E-Class", "G-Class", "GLA", "GLB", "GLC", "GLE", "GLS", "S-Class", "V-Class", "AMG GT", "EQA", "EQB", "EQC", "EQE", "EQS"],
    "Toyota": ["Corolla", "Camry", "RAV4", "Highlander", "4Runner", "Tacoma", "Tundra", "Land Cruiser", "Prius", "Avalon", "Sienna", "Supra", "86", "C-HR", "Venza", "Yaris", "Mirai"],
    "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Pilot", "Odyssey", "Ridgeline", "Passport", "Fit", "Insight", "Clarity", "NSX", "Jazz"],
    "Ford": ["Fiesta", "Focus", "Fusion", "Mustang", "Explorer", "Escape", "Edge", "Expedition", "F-150", "Ranger", "Bronco", "Maverick", "Transit", "EcoSport", "Mustang Mach-E"],
    "Chevrolet": ["Spark", "Sonic", "Cruze", "Malibu", "Camaro", "Corvette", "Trax", "Equinox", "Blazer", "Traverse", "Tahoe", "Suburban", "Silverado", "Colorado", "Bolt"],
    "Volkswagen": ["Polo", "Golf", "Jetta", "Passat", "Arteon", "Tiguan", "Atlas", "Touareg", "T-Roc", "T-Cross", "ID.3", "ID.4", "ID.Buzz"],
    "Nissan": ["Versa", "Sentra", "Altima", "Maxima", "370Z", "GT-R", "Kicks", "Rogue", "Murano", "Pathfinder", "Armada", "Frontier", "Titan", "Leaf"],
    "Hyundai": ["Accent", "Elantra", "Sonata", "Azera", "Veloster", "Kona", "Tucson", "Santa Fe", "Palisade", "Venue", "Ioniq", "Ioniq 5", "Ioniq 6"],
    "Kia": ["Rio", "Forte", "K5", "Stinger", "Soul", "Seltos", "Sportage", "Sorento", "Telluride", "Carnival", "Niro", "EV6"],
    "Mazda": ["Mazda2", "Mazda3", "Mazda6", "MX-5 Miata", "CX-3", "CX-30", "CX-5", "CX-50", "CX-9", "CX-90"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "Crosstrek", "Ascent", "BRZ", "WRX", "Solterra"],
    "Lexus": ["IS", "ES", "GS", "LS", "RC", "LC", "UX", "NX", "RX", "GX", "LX", "RZ"],
    "Porsche": ["718", "911", "Panamera", "Cayenne", "Macan", "Taycan"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck", "Roadster"],
    "Volvo": ["S60", "S90", "V60", "V90", "XC40", "XC60", "XC90", "C40"],
    "Jaguar": ["XE", "XF", "XJ", "F-Type", "E-Pace", "F-Pace", "I-Pace"],
    "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Range Rover", "Range Rover Sport", "Range Rover Evoque", "Range Rover Velar"],
    "Jeep": ["Renegade", "Compass", "Cherokee", "Grand Cherokee", "Wrangler", "Gladiator", "Wagoneer", "Grand Wagoneer"],
    "Dodge": ["Charger", "Challenger", "Durango", "Journey"],
    "Ram": ["1500", "2500", "3500", "ProMaster"],
    "Chrysler": ["300", "Pacifica", "Voyager"],
    "Acura": ["ILX", "TLX", "RLX", "NSX", "RDX", "MDX"],
    "Infiniti": ["Q50", "Q60", "QX50", "QX55", "QX60", "QX80"],
    "Genesis": ["G70", "G80", "G90", "GV60", "GV70", "GV80"],
    "Mini": ["Cooper", "Countryman", "Clubman", "Convertible"],
    "Fiat": ["500", "500X", "500L", "Tipo", "Panda"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale"],
    "Maserati": ["Ghibli", "Quattroporte", "Levante", "GranTurismo", "MC20"],
    "Ferrari": ["Roma", "Portofino", "F8", "SF90", "812", "296"],
    "Lamborghini": ["Huracan", "Aventador", "Urus"],
    "Bentley": ["Continental GT", "Flying Spur", "Bentayga"],
    "Rolls-Royce": ["Ghost", "Wraith", "Dawn", "Phantom", "Cullinan"],
    "Aston Martin": ["DB11", "DBS", "Vantage", "DBX"],
    "McLaren": ["GT", "Artura", "720S", "765LT"],
    "Bugatti": ["Chiron", "Divo"],
    "Peugeot": ["208", "308", "508", "2008", "3008", "5008"],
    "Renault": ["Clio", "Megane", "Captur", "Kadjar", "Koleos", "Talisman"],
    "Citroën": ["C3", "C4", "C5", "Berlingo"],
    "Skoda": ["Fabia", "Octavia", "Superb", "Kodiaq", "Karoq", "Kamiq"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Tarraco", "Arona"],
    "Mitsubishi": ["Mirage", "Outlander", "Eclipse Cross", "Pajero"],
    "Suzuki": ["Swift", "Vitara", "S-Cross", "Jimny"],
}

ENGINE_LITERS = ["1.0L", "1.2L", "1.4L", "1.5L", "1.6L", "1.8L", "2.0L", "2.2L", "2.4L", "2.5L", "3.0L", "3.5L", "3.6L", "4.0L", "4.6L", "5.0L", "5.7L", "6.0L", "6.2L", "Electric"]

ENGINE_CYLINDERS = ["3 cylinders", "4 cylinders", "5 cylinders", "6 cylinders", "8 cylinders", "10 cylinders", "12 cylinders", "16 cylinders", "Electric Motor", "Hybrid", "Rotary"]

YEARS = list(range(2025, 1979, -1))  # 2025 down to 1980

CATEGORIES = ["Sedan", "SUV", "Coupe", "Hatchback", "Convertible", "Wagon", "Pickup Truck", "Van", "Sports Car", "Luxury"]

GEARBOX_OPTIONS = ["Manual", "Automatic", "Semi-Automatic", "CVT", "DSG"]

STEERING_OPTIONS = ["Left-hand drive", "Right-hand drive"]

DRIVE_OPTIONS = ["Front-wheel drive (FWD)", "Rear-wheel drive (RWD)", "All-wheel drive (AWD)", "Four-wheel drive (4WD)"]

DOORS_OPTIONS = ["2", "3", "4", "5", ">5"]

COLORS = [
    "White", "Black", "Silver", "Gray", "Red", "Blue", "Green", "Yellow", 
    "Orange", "Brown", "Beige", "Gold", "Purple", "Pink", "Burgundy", 
    "Navy", "Teal", "Charcoal", "Pearl White", "Metallic Gray"
]

INTERIOR_MATERIALS = ["Cloth", "Leather", "Synthetic Leather", "Alcantara", "Suede", "Vinyl"]

INTERIOR_COLORS = ["Black", "Gray", "Beige", "Tan", "Brown", "White", "Red", "Blue"]

FUEL_TYPES = ["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid", "Hydrogen", "CNG", "LPG"]
