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
    ("yoruk", "Yörük", "Taurus Mountains and Aegean and Mediterranean coasts, Türkiye"),
    ("syriac-tur-abdin", "Syriac (Süryani) community", "Tur Abdin, Mardin Province, Türkiye"),
    ("ainu", "Ainu", "Hokkaido, Japan"),
    ("guna", "Guna (Kuna)", "Guna Yala (San Blas Islands), Panama"),
    ("wayuu", "Wayuu", "La Guajira peninsula, Colombia and Venezuela"),
    ("shipibo-conibo", "Shipibo-Conibo", "Ucayali River, Peruvian Amazon"),
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
    # ---- Türkiye ----
    {
        "slug": "yoruk-kilim",
        "title": "Yörük kilim",
        "type": "textile",
        "community": "yoruk",
        "summary": "A flat-woven Yörük kilim in slit tapestry, woven in two halves and joined "
        "in the middle.",
        "description": "Kilims are flat-woven rugs with no pile: the wool weft carries the "
        "design and hides the warp. Anatolian kilims are among the best known, and most are "
        "slit-woven. Yörük kilims share the motifs, patterns and colours of other Anatolian "
        "weavings. On the Isparta example, the row of rhombic motifs is a 'nazarlık', an "
        "amulet against the evil eye, and the zigzag borders are 'suyolu', running water, a "
        "symbol of fertility.",
        "process": "Coloured wool weft is woven back and forth over a wool warp, one colour "
        "area at a time. Where two colours meet along a vertical line, a small slit is left "
        "between them (slit tapestry). Wide pieces were woven in narrow parts on small "
        "nomadic looms and sewn together.",
        "cultural_context": "The Yörük are a Turkish subgroup of Oghuz descent living mainly "
        "in the mountains of Anatolia, some of them historically nomadic: they went up to "
        "the mountains in summer and down to the coastal plains in winter. Kilims were "
        "light and portable, suited to life on the move. Researchers note that weaving has "
        "largely disappeared as nomads settled and tourism offered other income.",
        "maker": "Unnamed Yörük weavers",
        "place": ("Isparta, western Taurus Mountains", "Türkiye", 37.76, 30.55),
        "materials": [
            ("Wool", "Sheep raised by the weavers' families", "Spun and dyed for weft and warp"),
        ],
        "techniques": [
            ("Slit tapestry weaving", "Weft-faced flat weave with slits between colour areas"),
            ("Joining panels", "Woven in two halves and sewn together in the middle"),
        ],
        "attributes": {"fibre": "Wool (weft and warp)"},
        "images": [
            (
                "Istanbul Former Mint Kilim exposition Yörük kilim, woven in two parts and put "
                "together (horizontally) in the middle in 2003 05.jpg",
                "A Yörük kilim with rows of red, blue, green and yellow hexagonal motifs",
                "Yörük kilim, woven in two parts and joined in the middle. Kilim exhibition, "
                "Istanbul",
                "",
            ),
            (
                "Istanbul Former Mint Kilim exposition Yörük kilim, woven in two parts and put "
                "together (horizontally) in the middle Detail in 2003 06.jpg",
                "Close-up of a hexagonal motif in red, blue, green and yellow wool",
                "Detail of the hexagonal motif",
                "",
            ),
            (
                "Isparta museum Large ‘kilim’ 021.jpg",
                "A long Yörük kilim with a row of rhombic motifs and zigzag borders",
                "Yörük slit-tapestry kilim with 'nazarlık' motifs. Isparta Museum",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Kilim", "https://en.wikipedia.org/wiki/Kilim"),
            ("Wikipedia: Yörüks", "https://en.wikipedia.org/wiki/Y%C3%B6r%C3%BCks"),
            (
                "Weaving in the life of Antalya Yörüks (journal article)",
                "https://bulprengpe.enu.kz/index.php/main/article/view/272",
            ),
        ],
    },
    {
        "slug": "yoruk-black-goat-hair-tent",
        "title": "Yörük black tent (kara çadır)",
        "type": "textile",
        "community": "yoruk",
        "summary": "A nomad's tent woven from black goat hair, furnished with kilims, bags and "
        "household goods, shown at the Antalya Museum.",
        "description": "The 'kara çadır' (black tent), or 'kıl çadır' (goat-hair tent), is "
        "typical of Yörük nomads and semi-nomads. Goat hair repels water, so the cloth keeps "
        "out the rain, while its loose weave lets air through in the heat. Inside, woven "
        "bags, kilims and cushions furnish the tent.",
        "process": "Goat hair is spun into a strong, dark yarn and woven into cloth, which "
        "is stretched over wooden poles and held with ropes.",
        "cultural_context": "For most of the year the nomadic Yörüks lived in these dark "
        "tents, moving between summer pastures in the mountains and winter camps on the "
        "coast. The Sarıkeçili, about 200 families around Antalya and Mersin, are described "
        "as the last Yörüks keeping the nomadic way of life.",
        "maker": "Yörük nomads (museum reconstruction)",
        "place": ("Antalya", "Türkiye", 36.89, 30.70),
        "materials": [
            ("Goat hair", "Black goats kept by the nomads", "Spun into a strong yarn; sheds water"),
            ("Wood", "Mountain forests", "Tent poles"),
            ("Wool", "Sheep", "Kilims, bags and cushions inside the tent"),
        ],
        "techniques": [
            ("Weaving", "Goat-hair yarn woven into tent cloth"),
        ],
        "attributes": {"fibre": "Goat hair", "dye_source": "Undyed"},
        "images": [
            (
                "Antalya Museum nomads tent 4900.jpg",
                "A black goat-hair tent with an open front, furnished with kilims, bags and "
                "gourds, in a museum",
                "Yörük black tent and its interior. Antalya Museum",
                "",
            ),
            (
                "Antalya Museum nomads tent 4907.jpg",
                "The same black tent seen from another side, with woven bags and pots inside",
                "Another view of the tent",
                "",
            ),
            (
                "Antalya Museum nomads tent 4908.jpg",
                "Inside the tent: woven bags, a low table with fruit and tea glasses on kilims",
                "Inside the tent: woven bags and kilims",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Yörüks", "https://en.wikipedia.org/wiki/Y%C3%B6r%C3%BCks"),
            (
                "A Part of Yürük Life Style: Tents (Zeitschrift für die Welt der Türken)",
                "https://dieweltdertuerken.org/index.php/ZfWT/article/view/253",
            ),
        ],
    },
    {
        "slug": "dosemealti-carpet",
        "title": "Döşemealtı carpet",
        "type": "textile",
        "community": "yoruk",
        "summary": "A 20th-century knotted-pile carpet from Döşemealtı, north of Antalya, in "
        "the Antalya Museum.",
        "description": "Döşemealtı carpets come from the Döşemealtı area just north of "
        "Antalya. Original Döşemealtı rugs were made by nomadic or semi-nomadic Yörük "
        "tribes. Most examples in the Antalya Museum date from the early or mid 20th "
        "century.",
        "process": "Unlike a kilim, a carpet has a pile: short lengths of coloured wool are "
        "knotted around the warp threads row by row, with rows of weft in between, and the "
        "pile is then trimmed level.",
        "cultural_context": "Yörük rugs were light and portable, suited to nomadic life; "
        "demand fell as migration ended. The Antalya Museum's ethnographic section shows "
        "Döşemealtı carpets among other regional weavings.",
        "maker": "Yörük weavers of Döşemealtı (unnamed)",
        "period": "20th century",
        "place": ("Döşemealtı, Antalya", "Türkiye", 37.03, 30.60),
        "materials": [("Wool", "Local sheep", "Spun, dyed and knotted as pile")],
        "techniques": [("Pile knotting", "Wool knotted around the warp and trimmed")],
        "attributes": {"fibre": "Wool"},
        "images": [
            (
                "Antalya museum Döşemealtı carpet, 20th century 4895.jpg",
                "Detail of a Döşemealtı carpet with a red field, blue and white border and "
                "stepped motifs",
                "Döşemealtı carpet, 20th century. Antalya Museum",
                "",
            ),
            (
                "Antalya museum A Döşemealtı carpet, “New”, Toplu 4900.jpg",
                "A newer Döşemealtı carpet in the 'Toplu' pattern",
                "A newer Döşemealtı carpet, 'Toplu' pattern. Antalya Museum",
                "",
            ),
        ],
        "sources": [
            (
                "Antalya Archaeological Museum: Döşemealtı rugs on display (Jozan)",
                "https://www.jozan.net/antalya-archaeological-museum-dosemealti-rugs-on-display/",
            ),
            (
                "Weaving in the life of Antalya Yörüks (journal article)",
                "https://bulprengpe.enu.kz/index.php/main/article/view/272",
            ),
        ],
    },
    {
        "slug": "midyat-telkari-silver-filigree",
        "title": "Midyat telkari (silver filigree)",
        "type": "jewellery",
        "community": "syriac-tur-abdin",
        "summary": "A silver filigree brooch from Midyat, made of fine silver wire curled and "
        "soldered into an openwork elephant.",
        "description": "Telkari is a form of filigree in silver and gold wire specific to "
        "Midyat in Mardin Province, developed from the 15th century. Midyat's silver is "
        "described as Syriac silver craft: handmade filigree ornaments. Craftsmen in the "
        "region still make fine pieces today.",
        "process": "Fine, pliable silver wire is curled, twisted and plaited into shapes, "
        "framed with thicker wire for strength, and joined where the wires touch with "
        "solder and a flux such as borax. Openwork filigree like this has no backing sheet.",
        "cultural_context": "Midyat is a historic centre of the Assyrians in Turkey and was "
        "long seen as the capital of Tur Abdin, the heartland of Syriac Christianity. The "
        "Midyat Telkari Museum opened in December 2023 in an 1850 house built by an "
        "Assyrian family.",
        "maker": "Midyat telkari silversmith (unnamed)",
        "place": ("Midyat, Mardin", "Türkiye", 37.4167, 41.3697),
        "materials": [
            ("Silver wire", "Drawn into very fine threads", "Curled and soldered into openwork"),
        ],
        "techniques": [
            ("Filigree (telkari)", "Wire curled, twisted and soldered without a backing"),
        ],
        "attributes": {"metal": "Silver", "metal_technique": "Filigree"},
        "images": [
            (
                "Midyat Silver Jewelry 1310249 Nevit.jpg",
                "A silver filigree brooch in the shape of an elephant, made of curled wire",
                "Silver filigree from Midyat",
                "",
            ),
            (
                "T.C. Midyat Beleiyesi Telkari Müzesi.jpg",
                "Stone façade of the Midyat Telkari Museum with its sign above the door",
                "Midyat Telkari Museum",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Midyat", "https://en.wikipedia.org/wiki/Midyat"),
            ("Wikipedia: Filigree", "https://en.wikipedia.org/wiki/Filigree"),
        ],
    },
    # ---- Other regions ----
    {
        "slug": "ainu-attus-robe",
        "title": "Ainu attus robe",
        "type": "textile",
        "community": "ainu",
        "summary": "A 19th-century Ainu coat woven from elm-bark fibre (attus), in the Tokyo "
        "National Museum.",
        "description": "Attus (also attush) is cloth woven by the Ainu of Hokkaido from tree "
        "bark fibre, called ohyo. It is water-resistant and light, and is used mainly for "
        "traditional Ainu robes. Nibutani in Biratori has produced attus since at least the "
        "18th century, and Nibutani attus was recognised as a Traditional Craft of Japan in "
        "2013.",
        "process": "Inner bark is stripped mainly from lobed elm (Ulmus laciniata) or "
        "Japanese lime, boiled, and dried into ohyo fibre, which is spun by hand into "
        "twisted yarn. The yarn is woven on an Ainu backstrap loom, and seams are sewn with "
        "ohyo.",
        "cultural_context": "This coat has dark appliqué bands along the collar, front and "
        "hems. Attus is still woven in Nibutani today.",
        "maker": "Unrecorded Ainu weaver",
        "period": "19th century",
        "place": ("Hokkaido", "Japan", 43.2, 142.8),
        "materials": [
            (
                "Elm bark fibre (ohyo)",
                "Inner bark of lobed elm or Japanese lime",
                "Boiled, dried and spun into yarn",
            ),
            ("Cotton cloth", "", "Dark bands sewn along the edges"),
        ],
        "techniques": [
            ("Backstrap weaving", "Ohyo yarn woven on an Ainu backstrap loom"),
            ("Appliqué", "Dark cloth bands sewn along the collar and hems"),
        ],
        "attributes": {
            "loom_type": "Backstrap",
            "fibre": "Elm bark fibre (ohyo)",
        },
        "images": [
            (
                "Coat, Ainu, Hokkaido, 1800s AD, attus (bast fiber) - Tokyo National Museum - "
                "Ueno Park, Tokyo, Japan - DSC09077.jpg",
                "A golden-brown attus coat with dark appliqué bands along the collar and hems",
                "Ainu attus coat, 19th century. Tokyo National Museum",
                "",
            ),
            (
                "Attus Cloth.jpg",
                "A roll of striped attus cloth on display",
                "A roll of attus cloth. Upopoy National Ainu Museum",
                "",
            ),
            (
                "Ainu monogatari takekuma 08.jpg",
                "Line drawings of the tools used to weave attus",
                "Tools for weaving attus, from 'Ainu Monogatari' (1918)",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Ainu bark cloth", "https://en.wikipedia.org/wiki/Ainu_bark_cloth"),
        ],
    },
    {
        "slug": "guna-mola",
        "title": "Guna mola (blouse panel)",
        "type": "textile",
        "community": "guna",
        "summary": "A mola blouse panel from the San Blas Islands, made in layered cotton by "
        "reverse appliqué, in the Honolulu Museum of Art.",
        "description": "A mola is a handmade textile that forms part of the traditional "
        "clothing of Guna women in Panama. In the Guna language, 'mola' means shirt or "
        "clothing. A mola panel forms the front or back of a blouse, and the two panels are "
        "often sold as a pair. Designs range from geometric patterns to flowers, sea "
        "animals, birds and modern graphics.",
        "process": "Several layers of cotton cloth in different colours are sewn together. "
        "The maker cuts away parts of each layer and turns the edges under, so the design "
        "appears in the colours below (reverse appliqué).",
        "cultural_context": "Molas are made by women. The art likely began as geometric body "
        "painting and moved to cloth after Spanish contact. Molas are credited with "
        "strengthening the Guna's push for autonomy in Guna Yala.",
        "maker": "Guna women of Wichubuala island (unnamed)",
        "period": "20th century",
        "place": ("Wichubuala, Guna Yala (San Blas Islands)", "Panama", 9.55, -78.90),
        "materials": [("Cotton cloth", "Several layers in different colours", "Cut and stitched")],
        "techniques": [
            ("Reverse appliqué", "Layers cut away to reveal colours below, edges hand-sewn"),
            ("Appliqué", "Small pieces sewn on top for details"),
        ],
        "attributes": {"loom_type": "None", "fibre": "Cotton"},
        "images": [
            (
                "Mola (blouse panel), Cuna (Kuna) Indians, Honolulu Museum of Art, 3739.1.JPG",
                "A red mola panel with two large stylised rays and fish outlined in black, "
                "orange and yellow",
                "Mola blouse panel from Wichubuala island, 20th century. Honolulu Museum of Art",
                "",
            ),
            (
                "Turtle in Mola blouse, Kuna peoples, San Blas Islands, Panama, 20th century, "
                "cotton, polyester - Fernbank Museum of Natural History - DSC09997 "
                "(cropped).JPG",
                "Close-up of a mola with a red turtle covered in small coloured squares",
                "Turtle mola, 20th century. Fernbank Museum of Natural History",
                "",
            ),
            (
                "Mola by Kuna women, Playon Chico.jpg",
                "A Guna woman holding a mola in front of many molas for sale",
                "Molas by Guna women, Playón Chico",
                "",
            ),
        ],
        "sources": [
            ("Wikipedia: Mola (art form)", "https://en.wikipedia.org/wiki/Mola_(art_form)"),
        ],
    },
    {
        "slug": "wayuu-mochila",
        "title": "Wayuu mochila bag",
        "type": "textile",
        "community": "wayuu",
        "summary": "Crocheted Wayuu mochila bags with kanaas designs, from La Guajira.",
        "description": "The mochila is the Wayuu's best-known weaving: a shoulder bag "
        "crocheted by one woman, with designs called kanaas that depict society, daily "
        "life, nature and the Wayuu world view. More complex designs make a bag more "
        "valuable. Wayuu women also weave chinchorros (hammocks), backpacks, mats and "
        "sandals.",
        "process": "Each bag is crocheted by a single Wayuu woman and takes twenty to thirty "
        "days, depending on the pattern. Traditionally the yarn was maguey cactus fibre.",
        "cultural_context": "In Wayuu tradition, the spider Waleker taught Wayuu women to "
        "weave. Girls learn weaving from elder women during their seclusion at puberty, and "
        "weaving is one of the most important tasks for a Wayuu woman. Mochilas are now "
        "sold in Colombia and abroad.",
        "maker": "Wayuu women (unnamed)",
        "period": "Contemporary",
        "place": ("Riohacha, La Guajira", "Colombia", 11.54, -72.91),
        "materials": [("Yarn", "Traditionally maguey cactus fibre", "Crocheted in colour bands")],
        "techniques": [("Crochet", "One woman crochets the whole bag, 20–30 days per bag")],
        "attributes": {"loom_type": "None", "fibre": "Maguey fibre (traditional)"},
        "images": [
            (
                "Mochilas wayuu.png",
                "Several brightly coloured crocheted Wayuu mochila bags",
                "Mochilas handcrafted by the Wayuu",
                "",
            ),
            (
                "Artesanas Wayú.jpg",
                "A Wayuu woman crocheting a mochila with a geometric design on the Riohacha "
                "seafront",
                "Wayuu artisan crocheting a mochila, Riohacha",
                "",
            ),
            (
                "Mochilas Wayuu, Museo del Oro Tayrona. Santa Marta.jpg",
                "Rows of colourful Wayuu mochilas laid out under a building's overhang",
                "Wayuu mochilas outside the Museo del Oro Tayrona, Santa Marta",
                "",
            ),
        ],
        "sources": [
            (
                "Colombia: The Art of Weaving – The Wayuu People (Comboni Missionaries)",
                "https://combonimissionaries.ie/2018/02/09/colombia-the-art-of-weaving-the-wayuu-people/",
            ),
        ],
    },
    {
        "slug": "shipibo-conibo-ceramic-vessel",
        "title": "Shipibo-Conibo ceramic vessel",
        "type": "pottery",
        "community": "shipibo-conibo",
        "summary": "A coil-built Shipibo-Conibo vessel painted with kené designs, made in 1968, "
        "in the Museum of the Americas, Madrid.",
        "description": "Shipibo-Conibo communities along Peru's Ucayali River have made "
        "polychrome pottery for over 1,200 years. Only women make the pots, which are among "
        "the largest and thinnest coil-built vessels of any Indigenous group in the "
        "Americas. The painted designs, called kené, also appear on Shipibo textiles.",
        "process": "The walls are built up in coils, each section dried in the sun, then "
        "scraped and polished. A white or red slip is applied, and kené designs are painted "
        "with small brushes. The pot is fired covered with ashes inside a metal pot over a "
        "fire, then sealed with resin for a glossy finish.",
        "cultural_context": "Kené reflects Shipibo cosmology, and each woman's patterns are "
        "shaped by her dreams and visions. A chomo is a vessel for storing liquids such as "
        "water and masato.",
        "maker": "Shipibo-Conibo potter (unnamed)",
        "year": 1968,
        "place": ("Ucayali River, near Pucallpa", "Peru", -8.38, -74.55),
        "materials": [
            ("Clay", "Riverbanks of the Ucayali", "Coiled into thin walls"),
            ("Slip and natural pigments", "White and red clays", "Painted kené designs"),
            ("Resin", "Forest trees", "Seals the fired surface"),
        ],
        "techniques": [
            ("Coiling", "Walls built in coils, sun-dried, scraped and polished"),
            ("Kené painting", "Geometric designs painted with fine brushes"),
        ],
        "attributes": {"forming_method": "Coil", "vessel_form": "Jar"},
        "images": [
            (
                "Shipibo vessel.jpg",
                "A cream-coloured Shipibo-Conibo vessel with a face on the neck and dark kené "
                "line designs",
                "Shipibo vessel, 1968. Museum of the Americas, Madrid",
                "",
            ),
            (
                "Art textile par Sara Flores.jpg",
                "Black and white kené design on cloth by the Shipibo artist Sara Flores",
                "Kené on cloth by Sara Flores: the same designs painted on pottery",
                "",
            ),
        ],
        "sources": [
            (
                "Shipibo-Conibo ceramic vessel (Lam Museum of Anthropology, Wake Forest)",
                "https://lammuseum.wfu.edu/?p=10417",
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
    "yoruk-kilim": ["wool", "kilim", "Anatolia", "nomadic"],
    "yoruk-black-goat-hair-tent": ["goat hair", "nomadic", "Anatolia"],
    "dosemealti-carpet": ["wool", "carpet", "Anatolia"],
    "midyat-telkari-silver-filigree": ["silver", "filigree", "jewellery", "Mesopotamia"],
    "ainu-attus-robe": ["bark fibre", "clothing", "woven"],
    "guna-mola": ["cotton", "reverse appliqué", "clothing"],
    "wayuu-mochila": ["crochet", "bag", "La Guajira"],
    "shipibo-conibo-ceramic-vessel": ["hand-coiled", "painted", "kené"],
}
