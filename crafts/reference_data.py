"""Real-world reference records: Indigenous crafts documented in public sources.

Each record describes a publicly documented, non-restricted craft tradition and a specific
object or scene photographed for Wikimedia Commons, which hosts only freely licensed or
public-domain files. The craft page shows each photo's author and license (read from
Commons) and links to the file page. Text is summarised from the sources listed per record.
Makers are named only when the source names them.

If a community asks for a record to be changed or removed, that request takes precedence.
"""

COMMUNITIES = [
    ("dine-navajo", "Diné (Navajo)", "Navajo Nation, southwestern United States"),
    ("acoma-pueblo", "Acoma Pueblo", "New Mexico, United States"),
    ("inuit", "Inuit", "Canadian Arctic"),
    ("maasai", "Maasai", "Southern Kenya and northern Tanzania"),
    ("pomo", "Pomo", "Northern California, United States"),
    ("haida", "Haida", "Haida Gwaii, British Columbia, Canada"),
    ("sami", "Sámi", "Sápmi: northern Norway, Sweden, Finland and Russia"),
    ("maori", "Māori", "Aotearoa New Zealand"),
]

NARA_CREDIT = "U.S. National Archives (NARA), 1933 · Public domain"

CRAFTS = [
    {
        "slug": "dine-navajo-rug-on-an-upright-loom",
        "title": "Diné (Navajo) rug on an upright loom",
        "type": "textile",
        "community": "dine-navajo",
        "summary": "A Navajo weaver at work on a rug, photographed at the Southern Navajo "
        "Agency in 1933.",
        "description": "Navajo (Diné) weaving produces rugs and blankets in a flat tapestry "
        "weave, similar to a kilim but without slits, on a continuous warp. Regional "
        "styles developed around trading posts: Two Grey Hills is known for four-fold "
        "symmetrical geometric designs in natural wool colours, and Ganado for patterns "
        "dominated by red with black and white.",
        "process": "Wool from the family's sheep is sheared, carded and spun by hand. The "
        "warp is strung on an upright loom, a frame with no moving parts, and the weaver "
        "sits on the floor in front of it, building up the design colour by colour in "
        "tapestry weave.",
        "cultural_context": "Navajo weavers have used wool from Navajo-Churro sheep, a breed "
        "descended from the Iberian Churra, since the late 17th century. Weaving became an "
        "important source of income through trading posts, and the Navajo Arts and Crafts "
        "Guild was formed in 1941.",
        "maker": "Unnamed Diné weaver (photographed 1933)",
        "year": 1933,
        "place": ("Southern Navajo Agency, Arizona", "United States", 35.74, -109.07),
        "materials": [
            (
                "Wool",
                "Navajo-Churro sheep raised by Navajo families",
                "Hand-carded and spun into yarn",
            ),
            (
                "Natural and aniline dyes",
                "Plants such as rabbitbrush; aniline dyes from the 1880s",
                "Used to colour the weft yarn",
            ),
        ],
        "techniques": [
            ("Spinning", "Wool spun into yarn by hand before weaving"),
            ("Tapestry weaving", "Flat, slit-free tapestry weave on a continuous warp"),
        ],
        "attributes": {"loom_type": "Upright", "fibre": "Sheep's wool (Navajo-Churro)"},
        "images": [
            (
                "Navajo Indian rug weaver with partially completed rug in loom. Southern Navajo "
                "Agency, 1933 - NARA - 298601.jpg",
                "A Navajo weaver seated in front of an upright loom with a partly woven rug",
                "Weaver with a partly completed rug on the loom, 1933",
                NARA_CREDIT,
            ),
            (
                "Spinning wool into yarn to be used in Navajo rug weaving. Southern Navajo "
                "Agency, 1933 - NARA - 298599.jpg",
                "A woman spinning wool into yarn for rug weaving",
                "Spinning wool into yarn for weaving, 1933",
                NARA_CREDIT,
            ),
            (
                "Navajos raise the sheep which supply wool from which they weave blankets and "
                "rugs. Southern Navajo Agency, 1933 - NARA - 298597.jpg",
                "A flock of sheep raised by Navajo families for wool",
                "Sheep that supply the wool, 1933",
                NARA_CREDIT,
            ),
        ],
        "sources": [
            ("Wikipedia: Navajo weaving", "https://en.wikipedia.org/wiki/Navajo_weaving"),
        ],
    },
    {
        "slug": "acoma-pueblo-water-pot",
        "title": "Acoma Pueblo water pot",
        "type": "pottery",
        "community": "acoma-pueblo",
        "summary": "An earthenware water pot decorated with slip, made at Acoma Pueblo around "
        "1889–1903, now in the de Young Museum, San Francisco.",
        "description": "Acoma potters are known for thin-walled vessels painted with "
        "geometric patterns, thunderbirds and rainbows. Water pots like this one were "
        "made to carry and store water.",
        "process": "Potters dig a dense local clay, dry it and strengthen it by mixing in "
        "ground-up pottery shards. The pot is shaped, then painted using the spike of a "
        "yucca plant as a brush. Before firing, the potter taps the pot and listens for a "
        "ring: a pot that doesn't ring would crack in the fire, so it is ground into shards "
        "for the next batch of clay.",
        "cultural_context": "Acoma Pueblo, on a mesa in New Mexico, is one of the oldest "
        "continuously inhabited communities in North America. Pottery remains a living "
        "tradition there.",
        "maker": "Unrecorded Acoma potter",
        "period": "c. 1889–1903",
        "place": ("Acoma Pueblo, New Mexico", "United States", 34.8964, -107.5819),
        "materials": [
            ("Clay", "Dense clay dug near Acoma", "Dried before use"),
            ("Ground potsherds", "Broken pots", "Mixed into the clay as temper"),
            ("Slip and paint", "Mineral and plant pigments", "Painted with a yucca-spike brush"),
        ],
        "techniques": [
            ("Hand building", "Shaped by hand, without a wheel"),
            ("Painting", "Designs applied with a chewed yucca spike"),
        ],
        "attributes": {
            "clay_source": "Local clay near Acoma, tempered with ground shards",
            "vessel_form": "Jar",
        },
        "images": [
            (
                "Water pot, Acoma Pueblo, c. 1889-1903, earthenware decorated with slip - De "
                "Young Museum - DSC00772 (cropped).JPG",
                "Round earthenware water pot with dark painted geometric designs on a pale slip",
                "Water pot, Acoma Pueblo, c. 1889–1903. de Young Museum, San Francisco",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Acoma Pueblo", "https://en.wikipedia.org/wiki/Acoma_Pueblo"),
            ("Wikipedia: Pueblo pottery", "https://en.wikipedia.org/wiki/Pueblo_pottery"),
        ],
    },
    {
        "slug": "inuit-stone-sculpture",
        "title": "Inuit stone sculpture",
        "type": "carving",
        "community": "inuit",
        "summary": "A carved stone sculpture from the Canadian Arctic, shown in the Arctic Museum.",
        "description": "Inuit stone carvings are made mainly from soapstone, serpentinite "
        "and argillite, relatively soft stones. Carvers often depict animals and "
        "traditional beliefs.",
        "process": "The shape is roughed out with an axe and refined with files. Most "
        "carvers prefer hand tools to power tools. The surface is then polished for hours "
        "with waterproof sandpaper.",
        "cultural_context": "Contemporary Inuit stone carving grew from 1951, when James "
        "Houston encouraged carvers in Kinngait (Cape Dorset). The West Baffin Eskimo "
        "Cooperative, founded there in 1959, became the main buyer of their work.",
        "maker": "Unrecorded Inuit carver",
        "place": ("Canadian Arctic", "Canada", None, None),
        "materials": [
            (
                "Soft stone",
                "Soapstone, serpentinite or argillite from Arctic quarries",
                "Soft enough to shape with hand tools",
            ),
        ],
        "techniques": [
            ("Stone carving", "Roughed out with an axe, refined with files"),
            ("Polishing", "Hours of polishing with waterproof sandpaper"),
        ],
        "attributes": {
            "carved_material": "Stone (soapstone / serpentinite / argillite)",
            "tools": "Axe, files, waterproof sandpaper",
        },
        "images": [
            (
                "Inuit sculpture, Canada - Arctic Museum.jpg",
                "Carved stone sculpture by an Inuit artist displayed in a museum case",
                "Inuit sculpture, Canada. Arctic Museum",
                "",
            ),
        ],
        "sources": [("Wikipedia: Inuit art", "https://en.wikipedia.org/wiki/Inuit_art")],
    },
    {
        "slug": "maasai-beaded-jewellery",
        "title": "Maasai beaded jewellery",
        "type": "beadwork",
        "community": "maasai",
        "summary": "Beaded necklaces and collars on display at a Maasai market in Kenya.",
        "description": "Maasai jewellery uses brightly coloured glass beads strung on wire "
        "and sewn to hide. Pieces such as wide collars, necklaces and earrings show a "
        "wearer's gender, relationship status and age.",
        "process": "Beads are threaded onto wire or thread and arranged in bands of colour, "
        "then shaped into flat collars or sewn onto hide straps.",
        "cultural_context": "The Maasai live in southern Kenya and northern Tanzania. Beaded "
        "jewellery is worn every day and at ceremonies, and is also sold at markets.",
        "maker": "Maasai beadworkers (unnamed)",
        "period": "Contemporary",
        "place": ("Southern Kenya and northern Tanzania", "Kenya / Tanzania", None, None),
        "materials": [
            ("Glass beads", "Traded glass seed beads", "Arranged in bands of strong colour"),
            ("Wire", "Metal wire", "Gives collars their flat, round shape"),
            ("Leather", "Animal hide", "Backing for some pieces"),
        ],
        "techniques": [("Beading", "Beads strung on wire or sewn to hide")],
        "attributes": {"bead_material": ["Glass"], "backing": "Wire or animal hide"},
        "images": [
            (
                "The Maasai Market Jewelry.jpg",
                "Rows of colourful beaded Maasai necklaces and collars at a market stall",
                "Beaded jewellery at a Maasai market",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Maasai people", "https://en.wikipedia.org/wiki/Maasai_people"),
            (
                "Art Institute of Chicago: Beaded necklace (Maasai), 2024.369",
                "https://www.artic.edu/artworks/271734/beaded-necklace",
            ),
        ],
    },
    {
        "slug": "pomo-coiled-dowry-basket-jenny-hughes",
        "title": "Pomo coiled dowry basket by Jenny Hughes",
        "type": "basketry",
        "community": "pomo",
        "summary": "A coiled basket by Pomo weaver Jenny Hughes, made as a girl's dowry "
        "basket, in the Brooklyn Museum.",
        "description": "Pomo weavers are renowned for fine coiled and twined baskets made "
        "for cooking, storage and ceremony. Their feather baskets, often covered in red "
        "woodpecker feathers with beads and abalone pendants, are especially prized.",
        "process": "A foundation of plant rods is wrapped and stitched in a tight spiral "
        "(coiling), or flexible strands are twisted around upright rods (twining). Feathers, "
        "shell and beads can be worked into the surface.",
        "cultural_context": "Pomo homelands lie along the Northern California coast and "
        "inland to Clear Lake and the Russian River valley. Basket weaving was women's work, "
        "and baskets were made for daily use and for ceremonies.",
        "maker": "Jenny Hughes (Pomo)",
        "place": ("Clear Lake, California", "United States", 39.03, -122.78),
        "materials": [
            ("Sedge root", "Gathered from sandy riverbanks", "Used for the stitching"),
            ("Willow", "Willow shoots", "Used as the foundation rods"),
            ("Bulrush root", "Marsh edges", "Gives dark designs"),
        ],
        "techniques": [("Coiling", "Foundation rods wrapped and stitched in a tight spiral")],
        "attributes": {"plant_fibre": "Sedge root, willow, bulrush root", "weave": "Coiled"},
        "images": [
            (
                "WLA brooklynmuseum Jenny Hughes Pomo Girls Coiled Dowry Basket.jpg",
                "Round coiled basket with dark geometric bands, made by Jenny Hughes",
                "Jenny Hughes, Pomo girl's coiled dowry basket. Brooklyn Museum",
                "",
            ),
            (
                "Pomo Basket Bowl.jpg",
                "A round Pomo basket bowl with woven geometric designs",
                "Pomo basket bowl",
                "",
            ),
        ],
        "sources": [("Wikipedia: Pomo", "https://en.wikipedia.org/wiki/Pomo")],
    },
    {
        "slug": "haida-bentwood-box",
        "title": "Haida bentwood box",
        "type": "carving",
        "community": "haida",
        "summary": "A carved and painted bentwood box made from a single steamed and bent "
        "board, in the Royal Ontario Museum.",
        "description": "Bentwood boxes are made by First Nations of the Northwest Coast, "
        "including the Haida, Tlingit, Tsimshian, Gitxsan and Coast Salish. Some are plain "
        "storage boxes; others, like this one, are carved and painted.",
        "process": "Each box is usually formed from one piece of wood that is steamed until "
        "it bends, folded into four sides and closed at the last corner. A base and lid are "
        "fitted, and the sides can be carved and painted.",
        "cultural_context": "Bentwood boxes were used to store food and clothing, and for "
        "burial. Today many are made for collectors and sold through museums and galleries, "
        "or commissioned directly from artists.",
        "maker": "Unrecorded Haida artist",
        "place": ("Haida Gwaii, British Columbia", "Canada", 53.25, -132.08),
        "materials": [("Wood", "Traditionally cedar", "A single board, steamed so it can bend")],
        "techniques": [
            ("Steam bending", "One board steamed and bent into four sides"),
            ("Carving and painting", "Sides carved and painted in Northwest Coast style"),
        ],
        "attributes": {
            "carved_material": "Wood (single steamed and bent board)",
            "finish": "Carved and painted",
        },
        "images": [
            (
                "Haida bentwood box - Royal Ontario Museum (26648772868).jpg",
                "Carved and painted Haida bentwood box on display in a museum",
                "Haida bentwood box. Royal Ontario Museum, Toronto",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Bentwood", "https://en.wikipedia.org/wiki/Bentwood"),
            ("Wikipedia: Northwest Coast art", "https://en.wikipedia.org/wiki/Northwest_Coast_art"),
        ],
    },
    {
        "slug": "sami-guksi-drinking-cup",
        "title": "Sámi guksi drinking cup",
        "type": "carving",
        "community": "sami",
        "summary": "A guksi, the Sámi drinking cup carved from birch burl, shown with a "
        "Sámi knife.",
        "description": "A guksi (also kuksa or kåsa) is a drinking cup made as duodji, Sámi "
        "handicraft. Cups carved from birch burl last longer than those from plain birch, "
        "and a well-made one can last a lifetime.",
        "process": "A birch burl is roughly shaped, then dried slowly and carefully so it "
        "doesn't crack, and finally carved to its finished form following local traditions.",
        "cultural_context": "Traditionally a guksi is rinsed only with clean water and dried "
        "with a cloth, never washed with detergent. It is often given as a gift.",
        "maker": "Sámi duodji maker (unnamed)",
        "place": ("Sápmi", "Norway / Sweden / Finland / Russia", None, None),
        "materials": [("Birch burl", "Burls from birch trees", "Dried slowly to prevent cracks")],
        "techniques": [("Knife carving", "Shaped by hand with a knife after slow drying")],
        "attributes": {"carved_material": "Birch burl", "tools": "Knife"},
        "images": [
            (
                "Duodji guksi drinking cup kåsa niibi knife kniv.JPG",
                "A carved wooden guksi drinking cup next to a Sámi knife",
                "Duodji: guksi drinking cup and niibi (knife)",
                "",
            ),
            (
                "Kuksa, Inari, Suomi - Finland 2013-03-10.jpg",
                "A wooden kuksa cup photographed in Inari, Finland",
                "Kuksa in Inari, Finland",
                "",
            ),
        ],
        "sources": [("Wikipedia: Guksi", "https://en.wikipedia.org/wiki/Guksi")],
    },
    {
        "slug": "maori-kete-harakeke-basket",
        "title": "Māori kete (harakeke basket)",
        "type": "basketry",
        "community": "maori",
        "summary": "A kete woven from harakeke (New Zealand flax), with a 1918 photograph of "
        "Māori women weaving kete at Rangiahua.",
        "description": "Kete are traditionally woven from harakeke (New Zealand flax) leaves; "
        "sedge, nīkau palm and cabbage-tree leaves are sometimes used. Most are about the "
        "size of a large handbag and are used to carry food and other things. Small kete "
        "serve as gift containers, and decorated kete whakairo are often displayed.",
        "process": "Harakeke leaves are cut and prepared into strips, then plaited by hand "
        "into the body and handles of the kete.",
        "cultural_context": "Traditionally a finished kete is given away. Weaving was done by "
        "women, and the skills were passed down within families.",
        "maker": "Unrecorded Māori weaver",
        "place": ("Aotearoa New Zealand", "New Zealand", None, None),
        "materials": [
            (
                "Harakeke (New Zealand flax)",
                "Leaves of the flax plant",
                "Prepared into strips for plaiting",
            )
        ],
        "techniques": [("Plaiting", "Strips plaited by hand into the bag and handles")],
        "attributes": {"plant_fibre": "Harakeke (New Zealand flax)", "weave": "Plaited"},
        "images": [
            (
                "Kete (AM 1999.98.1-1).jpg",
                "A woven harakeke kete basket with handles",
                "Kete, Auckland Museum (AM 1999.98.1)",
                "",
            ),
            (
                "Group of Maori women weaving flax baskets (kete), at Rangiahua, 1918. ATLIB "
                "297992.png",
                "Historic photograph of a group of Māori women weaving flax baskets",
                "Māori women weaving kete at Rangiahua, 1918",
                "",
            ),
        ],
        "sources": [("Wikipedia: Kete (basket)", "https://en.wikipedia.org/wiki/Kete_(basket)")],
    },
    {
        "slug": "navajo-squash-blossom-necklace",
        "title": "Navajo squash blossom necklace",
        "type": "jewellery",
        "community": "dine-navajo",
        "summary": "A silver squash blossom necklace with its crescent-shaped naja pendant, "
        "one of the most important forms of Navajo jewellery.",
        "description": "Navajo silversmithing began in the 19th century, when Atsidi Sani "
        '("Old Smith") learned the craft from a Mexican smith. The squash blossom '
        "necklace, with blossom-shaped beads and a central naja pendant, became one of the "
        "best-known Navajo jewellery forms.",
        "process": "Early smiths melted silver from coins and other objects, later using "
        "sheet silver and wire. Designs were stamped and engraved with improvised and later "
        "commercial tools, and pieces were sand-cast from about 1875. Turquoise was first "
        "set in silver around 1880.",
        "cultural_context": "Silver jewellery is worn and traded as wealth and adornment and "
        "remains a living art among Navajo silversmiths.",
        "maker": "Unrecorded Navajo silversmith",
        "place": ("Navajo Nation", "United States", 35.68, -109.05),
        "materials": [
            (
                "Silver",
                "Historically melted coins; later sheet silver and wire",
                "Formed into beads, blossoms and the naja",
            ),
            ("Turquoise", "Southwestern mines", "Set in silver from about 1880"),
        ],
        "techniques": [
            ("Stamping", "Designs struck into the silver with metal stamps"),
            ("Sand casting", "Molten silver poured into carved moulds, from about 1875"),
        ],
        "attributes": {
            "metal": "Silver",
            "stones": "Turquoise (in many pieces)",
            "metal_technique": "Cast",
        },
        "images": [
            (
                "Navajo Squash Blossom Necklace.gif",
                "Silver squash blossom necklace with a crescent pendant",
                "Navajo squash blossom necklace",
                "",
            ),
        ],
        "sources": [
            (
                "Wikipedia: Native American jewelry",
                "https://en.wikipedia.org/wiki/Native_American_jewelry",
            ),
        ],
    },
]


# Starter tags for the reference records (users add their own; these are only descriptive).
TAGS = {
    "dine-navajo-rug-on-an-upright-loom": ["wool", "loom weaving", "geometric design"],
    "acoma-pueblo-water-pot": ["hand-coiled", "painted", "water vessel"],
    "inuit-stone-sculpture": ["soapstone", "sculpture", "Arctic"],
    "maasai-beaded-jewellery": ["beads", "adornment", "East Africa"],
    "pomo-coiled-dowry-basket-jenny-hughes": ["coiled", "museum collection", "California"],
    "haida-bentwood-box": ["cedar", "painted", "Northwest Coast"],
    "sami-guksi-drinking-cup": ["birch burl", "drinking cup", "Sápmi"],
    "maori-kete-harakeke-basket": ["harakeke", "woven", "Aotearoa"],
    "navajo-squash-blossom-necklace": ["silver", "turquoise", "jewellery"],
}
