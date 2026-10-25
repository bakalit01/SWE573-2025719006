"""Fictional sample data for demos and tests.

Everything here is invented and labelled "Sample data" on screen. No real community, maker
or cultural knowledge is represented: real records are only added with documented consent.
"""

COMMUNITIES = [
    {
        "slug": "sample-riverbend",
        "name": "Riverbend (sample community)",
        "region": "River valley",
        "description": "A fictional community used to demonstrate the platform.",
    },
    {
        "slug": "sample-high-plateau",
        "name": "High Plateau (sample community)",
        "region": "Upland plateau",
        "description": "A fictional community used to demonstrate the platform.",
    },
    {
        "slug": "sample-coastal-dunes",
        "name": "Coastal Dunes (sample community)",
        "region": "Coastline",
        "description": "A fictional community used to demonstrate the platform.",
    },
    {
        "slug": "sample-northern-forest",
        "name": "Northern Forest (sample community)",
        "region": "Boreal forest",
        "description": "A fictional community used to demonstrate the platform.",
    },
]

# Each craft type carries its own attribute definitions (REQUIREMENTS §4.2).
CRAFT_TYPES = [
    {
        "slug": "textile",
        "name": "Textile",
        "description": "Woven, knotted or felted cloth.",
        "attributes": [
            ("loom_type", "Loom type", "choice", "", ["Backstrap", "Upright", "Floor", "None"]),
            ("fibre", "Fibre", "text", "", []),
            ("dye_source", "Dye source", "choice", "", ["Natural", "Synthetic", "Mixed", "Undyed"]),
            ("thread_count", "Threads per cm", "number", "per cm", []),
        ],
    },
    {
        "slug": "pottery",
        "name": "Pottery",
        "description": "Vessels and figures made from fired clay.",
        "attributes": [
            ("clay_source", "Clay source", "text", "", []),
            ("forming_method", "Forming method", "choice", "", ["Coil", "Pinch", "Slab", "Wheel"]),
            ("firing_method", "Firing method", "choice", "", ["Open pit", "Kiln", "Bonfire"]),
            ("vessel_form", "Vessel form", "choice", "", ["Jar", "Bowl", "Cup", "Plate"]),
        ],
    },
    {
        "slug": "beadwork",
        "name": "Beadwork",
        "description": "Decoration and objects made with beads.",
        "attributes": [
            (
                "bead_material",
                "Bead material",
                "multi_choice",
                "",
                ["Glass", "Shell", "Seed", "Bone"],
            ),
            ("bead_size", "Bead size", "number", "mm", []),
            ("stitch", "Stitch", "text", "", []),
            ("backing", "Backing material", "text", "", []),
        ],
    },
    {
        "slug": "basketry",
        "name": "Basketry",
        "description": "Containers woven from plant fibres.",
        "attributes": [
            ("plant_fibre", "Plant fibre", "text", "", []),
            ("weave", "Weave", "choice", "", ["Coiled", "Twined", "Plaited", "Wicker"]),
            ("harvest_season", "Harvest season", "text", "", []),
            ("watertight", "Watertight", "boolean", "", []),
        ],
    },
    {
        "slug": "carving",
        "name": "Carving",
        "description": "Objects shaped from wood, stone or bone.",
        "attributes": [
            ("carved_material", "Material", "text", "", []),
            ("tools", "Tools", "text", "", []),
            ("finish", "Finish", "text", "", []),
        ],
    },
    {
        "slug": "jewellery",
        "name": "Jewellery",
        "description": "Adornment made from metal, stone, shell and other materials.",
        "attributes": [
            ("metal", "Metal", "choice", "", ["Silver", "Copper", "Brass", "None"]),
            ("stones", "Stones", "text", "", []),
            ("metal_technique", "Metal technique", "choice", "", ["Cast", "Hammered", "Filigree"]),
        ],
    },
]

# (slug, title, type, community, visibility, materials, techniques, attributes, summary)
CRAFTS = [
    (
        "sample-backstrap-woven-sash",
        "Backstrap-woven sash",
        "textile",
        "sample-high-plateau",
        "public",
        ["Wool", "Plant dye"],
        ["Weaving"],
        {
            "loom_type": "Backstrap",
            "fibre": "Sheep wool",
            "dye_source": "Natural",
            "thread_count": 12,
        },
        "A narrow sash woven on a backstrap loom, with a repeating diamond band.",
    ),
    (
        "sample-felted-saddle-blanket",
        "Felted saddle blanket",
        "textile",
        "sample-high-plateau",
        "public",
        ["Wool"],
        ["Felting"],
        {"loom_type": "None", "fibre": "Wool", "dye_source": "Undyed"},
        "A thick felted blanket made by rolling and pressing wet wool.",
    ),
    (
        "sample-coil-built-storage-jar",
        "Coil-built storage jar",
        "pottery",
        "sample-riverbend",
        "public",
        ["River clay", "Mineral pigment"],
        ["Coiling", "Burnishing"],
        {
            "clay_source": "Riverbank",
            "forming_method": "Coil",
            "firing_method": "Open pit",
            "vessel_form": "Jar",
        },
        "A round-bodied jar built up from coils, burnished and fired in an open pit.",
    ),
    (
        "sample-pinch-pot-water-cup",
        "Pinch-pot water cup",
        "pottery",
        "sample-riverbend",
        "public",
        ["River clay"],
        ["Pinching"],
        {
            "clay_source": "Riverbank",
            "forming_method": "Pinch",
            "firing_method": "Bonfire",
            "vessel_form": "Cup",
        },
        "A small cup shaped by hand from a single ball of clay.",
    ),
    (
        "sample-beaded-shoulder-bag",
        "Beaded shoulder bag",
        "beadwork",
        "sample-northern-forest",
        "public",
        ["Glass beads", "Leather"],
        ["Appliqué beading"],
        {
            "bead_material": ["Glass", "Seed"],
            "bead_size": 2,
            "stitch": "Two-needle appliqué",
            "backing": "Smoked hide",
        },
        "A shoulder bag decorated with a floral beaded panel on smoked hide.",
    ),
    (
        "sample-shell-bead-necklace",
        "Shell-bead necklace",
        "beadwork",
        "sample-coastal-dunes",
        "members",
        ["Shell", "Plant fibre cord"],
        ["Drilling", "Stringing"],
        {"bead_material": ["Shell"], "bead_size": 6, "stitch": "Single strand", "backing": "None"},
        "A long necklace of hand-drilled shell discs. Shown to members only (sample).",
    ),
    (
        "sample-coiled-sedge-basket",
        "Coiled sedge basket",
        "basketry",
        "sample-coastal-dunes",
        "public",
        ["Sedge", "Bulrush"],
        ["Coiling"],
        {
            "plant_fibre": "Sedge root",
            "weave": "Coiled",
            "harvest_season": "Late summer",
            "watertight": True,
        },
        "A tightly coiled basket woven so closely it can hold water.",
    ),
    (
        "sample-twined-gathering-basket",
        "Twined gathering basket",
        "basketry",
        "sample-northern-forest",
        "public",
        ["Spruce root", "Bark"],
        ["Twining"],
        {
            "plant_fibre": "Spruce root",
            "weave": "Twined",
            "harvest_season": "Spring",
            "watertight": False,
        },
        "An open-twined basket used for gathering berries.",
    ),
    (
        "sample-carved-cedar-bowl",
        "Carved cedar bowl",
        "carving",
        "sample-northern-forest",
        "public",
        ["Cedar"],
        ["Adzing", "Knife carving"],
        {"carved_material": "Cedar wood", "tools": "Adze, crooked knife", "finish": "Oiled"},
        "A shallow serving bowl carved from a single block of cedar.",
    ),
    (
        "sample-soapstone-figure",
        "Soapstone animal figure",
        "carving",
        "sample-high-plateau",
        "members",
        ["Soapstone"],
        ["Knife carving", "Polishing"],
        {"carved_material": "Soapstone", "tools": "Files, knives", "finish": "Polished"},
        "A small polished figure of a resting animal. Shown to members only (sample).",
    ),
    (
        "sample-hammered-copper-cuff",
        "Hammered copper cuff",
        "jewellery",
        "sample-riverbend",
        "public",
        ["Copper"],
        ["Hammering"],
        {"metal": "Copper", "stones": "None", "metal_technique": "Hammered"},
        "A cuff bracelet shaped and textured with a round-faced hammer.",
    ),
    (
        "sample-silver-filigree-earrings",
        "Silver filigree earrings",
        "jewellery",
        "sample-coastal-dunes",
        "public",
        ["Silver"],
        ["Filigree"],
        {"metal": "Silver", "stones": "Small blue stones", "metal_technique": "Filigree"},
        "A pair of earrings made from fine twisted silver wire.",
    ),
]

DESCRIPTION = (
    "This is a fictional sample record created to demonstrate the platform. It does not "
    "describe a real object, maker or community.\n\n{summary}"
)
CULTURAL_CONTEXT = (
    "Real records include context written or approved by the community, such as how the "
    "craft is used and who may make or see it. Sample records leave this as an example."
)


# Extra detail per sample craft (feedback FB-01…FB-04). Places are broad, approximate sample
# locations, never real community sites; units vary on purpose to show international units.
SAMPLE_PLACE_NOTE = "Approximate sample location"

DETAILS = {
    "sample-backstrap-woven-sash": {
        "year_made": 2019,
        "place": ("Sample upland plateau", "", -15.8, -70.0),
        "size": (None, 9, 210, "cm"),  # (height, width, depth/length, unit): a long narrow sash
        "weight": (180, "g"),
        "traditional_measure": "About three arm-spans long",
        "materials": [
            ("Wool", "Sheep raised by the (sample) household", "Spun by hand on a drop spindle"),
            ("Plant dye", "Roots and leaves gathered nearby", "Mordanted with alum for red"),
        ],
        "techniques": [("Weaving", "Warp-faced weave on a backstrap loom tied to a post")],
        "process": "Wool is washed, spun and dyed. The warp is wound on stakes, tied to a "
        "post and to the weaver's waist, and the diamond band is picked up by hand.",
    },
    "sample-felted-saddle-blanket": {
        "year_made": 1985,
        "year_is_approximate": True,
        "place": ("Sample upland plateau", "", -16.4, -69.3),
        "size": (4, 90, 120, "cm"),
        "weight": (2.6, "kg"),
        "materials": [("Wool", "Mixed fleece", "Laid out in thin crossing layers")],
        "techniques": [("Felting", "Rolled in a reed mat with hot water and pressed for hours")],
        "process": "Layers of loose wool are wetted with hot water, rolled tightly inside a mat "
        "and pressed until the fibres lock into a dense felt.",
    },
    "sample-coil-built-storage-jar": {
        "year_made": 2021,
        "place": ("Sample river valley", "", 9.0, 38.7),
        "size": (34, 28, 28, "cm"),
        "weight": (4.1, "kg"),
        "materials": [
            ("River clay", "Dug from the riverbank in the dry season", "Mixed with sand as temper"),
            ("Mineral pigment", "Red earth", "Painted on as a slip before burnishing"),
        ],
        "techniques": [
            ("Coiling", "Rolled coils are pinched together and smoothed with a gourd scraper"),
            ("Burnishing", "Polished with a river pebble while leather-hard"),
        ],
        "process": "Clay is cleaned, tempered and rolled into coils that are built up in rings. "
        "The jar is scraped thin, slipped, burnished and fired in an open pit.",
    },
    "sample-pinch-pot-water-cup": {
        "year_made": 2023,
        "place": ("Sample river valley", "", 9.3, 38.9),
        "size": (9, 8, 8, "cm"),
        "weight": (210, "g"),
        "traditional_measure": "Fits in one palm",
        "materials": [("River clay", "Riverbank", "Used without temper for a fine wall")],
        "techniques": [("Pinching", "Opened with the thumb and thinned by turning in the hand")],
        "process": "A ball of clay is opened with the thumb and pinched evenly while turning, "
        "then dried slowly and fired in a bonfire.",
    },
    "sample-beaded-shoulder-bag": {
        "year_made": 2015,
        "place": ("Sample boreal forest", "", 54.0, -105.0),
        "size": (11, 9, 1.5, "in"),
        "weight": (14, "oz"),
        "materials": [
            ("Glass beads", "Traded seed beads", "Size 11 beads in six colours"),
            ("Leather", "Smoked hide", "Smoking gives colour and keeps it soft"),
        ],
        "techniques": [("Appliqué beading", "Beads strung on one thread, couched with a second")],
        "process": "The floral design is drawn on the hide, then beads are laid along the lines "
        "and stitched down every two or three beads with a second needle.",
    },
    "sample-shell-bead-necklace": {
        "year_made": 1960,
        "year_is_approximate": True,
        "place": ("Sample coastline", "", -33.9, 151.2),
        "precision": "approximate",
        "size": (None, None, 76, "cm"),
        "weight": (95, "g"),
        "materials": [
            ("Shell", "Collected on the shore", "Broken into blanks and ground into discs"),
            ("Plant fibre cord", "Twisted bark fibre", "Two-ply cord"),
        ],
        "techniques": [
            ("Drilling", "Pump drill with a stone point"),
            ("Stringing", "Discs graded by size from the centre outwards"),
        ],
        "process": "Shell blanks are ground flat on sandstone, drilled with a pump drill, strung "
        "and rolled together to an even edge.",
    },
    "sample-coiled-sedge-basket": {
        "year_made": 2008,
        "place": ("Sample coastline", "", 36.6, -121.9),
        "size": (14, 30, 30, "cm"),
        "weight": (520, "g"),
        "materials": [
            ("Sedge", "Root runners dug from sandy banks", "Split and soaked before use"),
            ("Bulrush", "Marsh edge", "Used as the foundation bundle"),
        ],
        "techniques": [("Coiling", "Sewn with an awl, about 8 stitches per centimetre")],
        "process": "A bundle of bulrush is wrapped and sewn in a spiral with split sedge so "
        "tightly that the basket holds water once the fibres swell.",
    },
    "sample-twined-gathering-basket": {
        "year_made": 2017,
        "place": ("Sample boreal forest", "", 61.2, -135.0),
        "size": (10, 12, 12, "in"),
        "weight": (1.1, "lb"),
        "traditional_measure": "Holds about one day's berry picking",
        "materials": [
            ("Spruce root", "Pulled from moss in spring", "Roasted, peeled and split"),
            ("Bark", "Birch", "Used for the rim"),
        ],
        "techniques": [("Twining", "Two wefts twisted around each warp, open weave for air")],
        "process": "Roots are roasted and split into fine strands, then twined over a warp "
        "starting from the centre of the base and finished with a bark rim.",
    },
    "sample-carved-cedar-bowl": {
        "year_made": 2012,
        "place": ("Sample boreal forest", "", 53.3, -132.1),
        "size": (90, 380, 240, "mm"),
        "weight": (1.3, "kg"),
        "materials": [("Cedar", "Windfall log", "Seasoned for a year before carving")],
        "techniques": [
            ("Adzing", "Bowl hollowed with an elbow adze"),
            ("Knife carving", "Rim and handles refined with a crooked knife"),
        ],
        "process": "A section of log is split, roughed out with an adze, hollowed, refined with "
        "a crooked knife and finished with oil.",
    },
    "sample-soapstone-figure": {
        "year_made": 1990,
        "year_is_approximate": True,
        "place": ("Sample upland plateau", "", -17.0, -68.5),
        "precision": "hidden",
        "size": (7, 12, 5, "cm"),
        "weight": (340, "g"),
        "traditional_measure": "Two finger-widths tall",
        "materials": [
            ("Soapstone", "Local outcrop (location kept private)", "Soft and easy to file")
        ],
        "techniques": [
            ("Knife carving", "Shape blocked out with knives and rasps"),
            ("Polishing", "Sanded wet, then rubbed with oil"),
        ],
        "process": "The figure is blocked out with knives, refined with files and polished wet "
        "until the stone takes a soft shine.",
    },
    "sample-hammered-copper-cuff": {
        "year_made": 2022,
        "place": ("Sample river valley", "", 9.6, 39.2),
        "size": (3.5, 6.5, 5.5, "cm"),
        "weight": (2.1, "oz"),
        "materials": [("Copper", "Recycled sheet", "Annealed in charcoal to soften")],
        "techniques": [("Hammering", "Textured with a round-faced hammer over a stake")],
        "process": "A copper strip is annealed, shaped around a stake, textured with a "
        "round-faced hammer and polished.",
    },
    "sample-silver-filigree-earrings": {
        "year_made": 2020,
        "place": ("Sample coastline", "", 38.4, 27.1),
        "size": (45, 20, 3, "mm"),
        "weight": (6.5, "g"),
        "materials": [
            ("Silver", "Recycled jewellery silver", "Drawn into fine wire and twisted"),
            ("Small blue stones", "Bought from a trader", "Set in bezels at the centre"),
        ],
        "techniques": [("Filigree", "Twisted wire scrolls soldered into a frame")],
        "process": "Silver wire is drawn, twisted and flattened, bent into scrolls, fitted into "
        "a frame and soldered with a small torch.",
    },
}
