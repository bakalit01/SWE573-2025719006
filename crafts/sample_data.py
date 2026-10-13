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
            ("height", "Height", "number", "cm", []),
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
            "height": 34,
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
            "height": 9,
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
