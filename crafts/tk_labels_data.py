"""The managed list of Traditional Knowledge (TK) and Biocultural (BC) labels (US-26).

Names and codes follow the Local Contexts labels (https://localcontexts.org/labels/).
The explanations are short summaries written for this site, not Local Contexts' template
text; admins can reword them, retire labels or add a community's own in the admin.
Used by migration 0010 and by `crafts.seeding.ensure_tk_labels`.
"""

TK = "https://localcontexts.org/labels/traditional-knowledge-labels/"
BC = "https://localcontexts.org/labels/biocultural-labels/"

# (code, name, category, explanation)
TK_LABELS = [
    (
        "TK A",
        "TK Attribution",
        "provenance",
        "The community asks that anyone using this material credit the people and community "
        "named here as its source and custodians.",
    ),
    (
        "TK CL",
        "TK Clan",
        "provenance",
        "This material belongs to, or is shared according to the protocols of, a particular clan.",
    ),
    (
        "TK F",
        "TK Family",
        "provenance",
        "This material belongs to, or is shared according to the protocols of, a particular "
        "family.",
    ),
    (
        "TK MC",
        "TK Multiple Communities",
        "provenance",
        "Several communities hold responsibility for this material, and its use should "
        "respect all of them.",
    ),
    (
        "TK CV",
        "TK Community Voice",
        "provenance",
        "The community wants its own voice and perspective on this material to be heard; its "
        "description may differ from earlier records.",
    ),
    (
        "TK CR",
        "TK Creative",
        "provenance",
        "This material comes from a community's creative practice; the creators and their "
        "community should be acknowledged.",
    ),
    (
        "TK V",
        "TK Verified",
        "protocol",
        "The community has confirmed that this material is shared appropriately and that the "
        "record respects its protocols.",
    ),
    (
        "TK NV",
        "TK Non-Verified",
        "protocol",
        "The community has concerns about how this material is described or shared; treat "
        "the record with care until it is reviewed.",
    ),
    (
        "TK S",
        "TK Seasonal",
        "protocol",
        "This material, or the knowledge in it, has seasonal conditions: some uses or "
        "tellings belong to certain times of year.",
    ),
    (
        "TK WG",
        "TK Women General",
        "protocol",
        "This material is usually shared among women; the community asks others to respect "
        "this when viewing or using it.",
    ),
    (
        "TK MG",
        "TK Men General",
        "protocol",
        "This material is usually shared among men; the community asks others to respect "
        "this when viewing or using it.",
    ),
    (
        "TK WR",
        "TK Women Restricted",
        "protocol",
        "This material is restricted to women under the community's protocols.",
    ),
    (
        "TK MR",
        "TK Men Restricted",
        "protocol",
        "This material is restricted to men under the community's protocols.",
    ),
    (
        "TK CS",
        "TK Culturally Sensitive",
        "protocol",
        "This material is culturally sensitive. View and use it respectfully, and contact the "
        "community before reusing it.",
    ),
    (
        "TK SS",
        "TK Secret / Sacred",
        "protocol",
        "This material includes secret or sacred knowledge that is not usually open to the "
        "public. Do not copy or share it.",
    ),
    (
        "TK OC",
        "TK Open to Commercialization",
        "permission",
        "The community is open to commercial uses of this material, made with its agreement "
        "and on fair terms.",
    ),
    (
        "TK NC",
        "TK Non-Commercial",
        "permission",
        "This material may not be used for commercial purposes.",
    ),
    (
        "TK CO",
        "TK Community Use Only",
        "permission",
        "This material is meant for use within the community; outside use needs the "
        "community's permission.",
    ),
    (
        "TK O",
        "TK Outreach",
        "permission",
        "The community shares this material for education and outreach, such as teaching "
        "and public awareness.",
    ),
    (
        "TK CB",
        "TK Open to Collaboration",
        "permission",
        "The community welcomes collaboration on this material, such as research or "
        "exhibitions; contact it first.",
    ),
]

BC_LABELS = [
    (
        "BC P",
        "BC Provenance",
        "provenance",
        "Plants, animals, places or other natural resources in this record come from the "
        "lands and waters of the community named here.",
    ),
    (
        "BC MC",
        "BC Multiple Communities",
        "provenance",
        "Several communities hold rights and responsibilities for the natural resources in "
        "this record.",
    ),
    (
        "BC CL",
        "BC Clan",
        "provenance",
        "A particular clan holds rights and responsibilities for the natural resources in "
        "this record.",
    ),
    (
        "BC CV",
        "BC Consent Verified",
        "protocol",
        "The community has given consent for these natural resources and related knowledge "
        "to be used as described.",
    ),
    (
        "BC CNV",
        "BC Consent Non-Verified",
        "protocol",
        "The community's consent for using these natural resources has not been confirmed.",
    ),
    (
        "BC R",
        "BC Research Use",
        "permission",
        "These natural resources and related knowledge may be used for research, with "
        "acknowledgement of the community.",
    ),
    (
        "BC O",
        "BC Outreach",
        "permission",
        "These natural resources and related knowledge may be used for education and outreach.",
    ),
    (
        "BC NC",
        "BC Non-Commercial",
        "permission",
        "These natural resources and related knowledge may not be used commercially.",
    ),
    (
        "BC CB",
        "BC Open to Collaboration",
        "permission",
        "The community welcomes collaboration on research about these natural resources; "
        "contact it first.",
    ),
    (
        "BC OC",
        "BC Open to Commercialization",
        "permission",
        "The community is open to commercial uses of these natural resources, made with its "
        "agreement and on fair terms.",
    ),
]
