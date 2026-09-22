"""Generate Mauna building concept prompts (v01) from the Terran building set.

Writes one <ASSET>_concept_v01.txt per building and jobs.tsv (prompt path, Terran reference image)
for the Codex batch runner. Style is the approved MAU-DIR-001 direction; the Terran concept is
attached only as a function/footprint reference.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

# id: (name, dimensions, gameplay purpose, Mauna subject)
BUILDINGS = {
    "BLD-CMD-002": ("Security Centre", "38 × 30 × 20", "colony security and surveillance",
        "A squat armoured strongroom built from a grounded bronze cargo hull cut in half, lying on its side on a stepped gunmetal plinth. A whole off-white salvaged block serves as the controlled-access gatehouse, joined by a thick clamp collar, with one large flush closed vault hatch. A solid block sensor head sits on a short tapered mast block on the roof. Narrow opaque slit viewports."),
    "BLD-HAB-001": ("Residential Block", "55 × 35 × 22", "high-density colonist housing",
        "A dense stack of repurposed bronze capsule cargo pods laid in two staggered tiers on a stepped plinth, each pod a dwelling, seated in thick gunmetal clamp collars. A long off-white salvaged corridor block links the pods along one side. Rows of narrow opaque slit windows on every pod, several flush closed airlock hatches, one solid tapered counterweight stack."),
    "BLD-HAB-002": ("Living Quarters", "32 × 22 × 15", "basic worker accommodation",
        "A compact dormitory made from one grounded bronze cargo-belly hull on short solid plinth blocks, with one smaller off-white salvaged module clamped to its end. A single flush closed airlock hatch, a band of narrow opaque slit windows, one verdigris patch plate."),
    "BLD-HAB-003": ("Pleasure Dome", "60 m diameter × 28", "morale and recreation",
        "A black-market bazaar dome: a wide low bronze dome made of many stepped verdigris and bronze plates, ringed by a thick gunmetal clamp band and a broad crimson stencil band. Opaque near-black glazing panels set into the dome in a ring (no visible interior). A welded off-white salvaged entry block with a large flush closed double hatch. Two short clamped cargo pods beside the entrance."),
    "BLD-LIF-001": ("Medical Centre", "42 × 30 × 18", "restore and support colony population",
        "A cleaner, calmer Mauna building: a smooth off-white salvaged hull section, the most intact piece of salvage in the colony, laid on a bronze plinth. A large flush closed ambulance hatch at one end, a thick gunmetal collar joining a bronze service capsule, and a flat off-white crescent emblem on a crimson roundel as the medical mark. Opaque slit windows."),
    "BLD-LIF-002": ("Air Processor", "50 × 30 × 28", "generate breathable atmosphere",
        "A bank of three huge squat thick-walled engine bells turned upward into intake stacks, each capped by a solid louvred gunmetal grille block, rising from a long bronze pressure-vessel body. Two large enclosed capsule pressure tanks clamped along one side in thick collars. Deep solid louvre blocks, no open fans."),
    "BLD-LIF-003": ("Environment Control", "48 × 34 × 24", "stabilise colony environmental systems",
        "A central bronze control capsule with an opaque slit viewport, flanked asymmetrically by a tall stack of thick solid heat-exchanger slabs on one side and two solid tapered vent towers on the other. Enclosed pipe trunks as raised ribs join everything to the plinth. One verdigris patch plate, one crimson stencil."),
    "BLD-LIF-004": ("Hydration Plant", "44 × 32 × 22", "extract and process colony water",
        "A cluster of four enclosed capsule water tanks of unequal sizes, two upright and two lying down, all seated in thick gunmetal clamp collars on a stepped plinth. A welded off-white salvaged pump-house block in the middle with a flush closed hatch. Enclosed pipe trunks as thick raised ribs. Verdigris staining concentrated around the tanks."),
    "BLD-LIF-005": ("Hydroponics Plant", "65 × 35 × 20", "produce food and support population",
        "A long greenhouse made of a split-open bronze freighter hull whose upper half is replaced by rows of flat opaque near-black glazing panels in thick bronze frames (no visible plants, no transparency). A spine of enclosed nutrient capsule tanks runs along one side in clamp collars. One off-white salvaged service block at the end."),
    "BLD-MIN-001": ("Basic Mine", "45 × 32 × 26", "extract common ore from the asteroid surface",
        "A salvaged engine turned into a drill: one thick-walled engine bell mounted pointing DOWN into the rock inside a solid tapered bronze drill housing, braced by a solid gunmetal buttress block (no open derrick). An enclosed ore conveyor tunnel as a solid box ramp leads to a small off-white salvaged processing bunker. One clamped ore capsule pod."),
    "BLD-MIN-002": ("Advanced Mine", "60 × 40 × 32", "increase ore extraction throughput",
        "Two unequal solid tapered drill housings, one bronze and one off-white salvage, each holding a downward-pointing engine-bell drill, joined by a thick clamp collar bridge. An enclosed box conveyor feeds a bronze processing capsule with a flush hatch and a slit viewport control cabin. Two clamped ore pods."),
    "BLD-MIN-003": ("Deep Bore Mine", "75 × 55 × 48", "reach deep high-value ore deposits",
        "A hero-scale bore: a massive vertical bronze drill shaft made from a stack of three huge clamp collars and hull rings of decreasing size, driven into a wide stepped gunmetal foundation. Four solid sloped buttress blocks brace it (no gantry). Enclosed box ore chutes descend to a rack of clamped ore capsule pods. A strong circular top view."),
    "BLD-MIN-004": ("Seismic Penetrator", "58 × 38 × 34", "specialised high-force extraction",
        "A brutal ram rig: a heavy solid gunmetal ram block hanging inside a closed bronze housing shaped like an upended ship's hull, with two thick enclosed shock-absorber cylinders either side. An off-white salvaged control block welded to the base. Crimson stencil warning chevrons as flat paint."),
    "BLD-STO-001": ("Ore Storage", "40 × 30 × 26", "store mined resources",
        "A cluster of three large upright capsule ore silos of unequal height in thick gunmetal clamp collars, sharing a solid sloped hopper base with an enclosed loading chute. One silo is off-white salvage, the others bronze with verdigris patches. A flush closed smuggler hatch at the base of the tallest silo."),
    "BLD-STO-002": ("Protected Storage Tower", "28 × 28 × 50", "secure valuable resources",
        "A tall armoured vault tower made of stacked bronze hull rings bound by four thick gunmetal clamp collars, tapering slightly toward a recessed solid top cap. One large flush closed vault hatch at the base and a second hidden flush hatch high on the side. A broad crimson stencil band with the crescent emblem. Clearly the place the Mauna keep contraband."),
    "BLD-STO-003": ("Ore Teleporter", "46 × 40 × 30", "late-game resource transfer",
        "A thick solid bronze transfer ring standing upright on a stepped plinth, its opening filled by a flat opaque dark disc (unlit, no glow), held by two solid tapered containment pylons of unequal size. An enclosed feed tunnel from a clamped ore capsule pod leads into the ring. One off-white salvaged control block."),
    "BLD-PWR-001": ("Solar Panel", "18 × 10 × 5", "provide early modular power",
        "A low, rugged array: two thick rigid near-black solar slabs of unequal size in heavy bronze frames, tilted on a solid gunmetal turntable block on a small plinth. A salvaged off-white converter box clamped to the base. Matte panels, no reflections."),
    "BLD-PWR-002": ("Solar Matrix", "75 × 45 × 22", "provide advanced solar power",
        "A central bronze conversion capsule on a heavy turntable, with five thick rigid near-black solar wings of mismatched lengths radiating on chunky solid root blocks, two of the wings in off-white salvaged frames. Solid radiator slabs on the hub. Deliberately asymmetric."),
    "BLD-PWR-003": ("Power Store", "38 × 30 × 24", "buffer colony energy",
        "A row of six enclosed capsule battery cells of two sizes lying in thick gunmetal clamp collars on a stepped plinth, with solid ceramic insulator blocks between them. A bronze cooling capsule with raised rib conduits at one end. Flat crimson stencils on each cell."),
    "BLD-PWR-004": ("Power Plant", "65 × 48 × 38", "generate the colony's primary power",
        "A salvaged starship reactor grounded as a power plant: a big bronze reactor sphere half-sunk into a stepped plinth, wrapped by two thick clamp collars, with a long off-white salvaged turbine hall welded to one side. Two short squat cooling stacks made from upturned engine bells capped with solid louvre blocks. Strong top view."),
    "BLD-PWR-005": ("High-Energy Generator", "58 × 48 × 42", "late-game high-output generation",
        "A contained core: a large solid bronze sphere held in the centre of three massive gunmetal clamp arms rising from a stepped plinth, the arms of unequal thickness. A flat dark opaque band around the sphere's equator (no glow). Two off-white salvaged capacitor blocks at the base."),
    "BLD-MFG-001": ("Weapons Factory", "70 × 50 × 32", "manufacture colony weapons and ordnance",
        "A long bronze factory hall built from a grounded cargo freighter hull, with two huge flush closed loading hatches along its side and a solid enclosed gantry beam housing on the roof. An armoured off-white salvaged magazine block clamped to one end. A concealed cupola turret on the roof as a security measure."),
    "BLD-MFG-002": ("Shipyard", "100 × 75 × 42", "construct small and medium ships",
        "A hangar made from the hollowed, grounded rear half of a huge bronze freighter, its open stern closed by enormous flush segmented hangar doors facing the launch path. A solid sloped launch ramp in front. A heavy solid gunmetal crane-housing block on the roof, a rack of clamped part pods along one side and an off-white salvaged fabrication block."),
    "BLD-MFG-003": ("Space Dock", "250 × 180 × 90", "construct capital ships",
        "Capital-ship infrastructure: two enormous parallel bronze hull spines on a vast stepped foundation, joined at intervals by massive gunmetal clamp collars forming a closed U-shaped cradle. Solid docking-clamp blocks line the inside faces. Off-white salvaged control towers of unequal height at each end. The cradle reads as big enough for a battleship."),
    "BLD-MFG-004": ("Construction Yard", "75 × 55 × 30", "support colony building construction",
        "A yard of solid material stacks: salvaged off-white hull plates and bronze plates stacked as solid blocks, a heavy solid tapered crane-tower block with a thick folded boom housing (no lattice), and a bronze drone-bay capsule with three flush closed bay hatches. A pod-transfer cradle holding one capsule."),
    "BLD-LOG-001": ("Landing Pad", "60 × 60 × 8", "receive shuttles, cargo and personnel",
        "A broad low octagonal gunmetal pad with a raised solid lip, its top painted with a huge flat crimson crescent emblem and landing markings. Solid sloped blast-deflector blocks at four corners, one off-white salvaged service kiosk block and two flush service sockets."),
    "BLD-LOG-002": ("Refuelling Depot", "55 × 38 × 24", "refuel colony ships",
        "A tank farm of three enclosed capsule fuel tanks of unequal sizes in thick clamp collars, beside a bronze pump house with a flush hatch. A solid folded refuelling boom housing lies along the top of the pump house (no hoses). Low solid crash-barrier blocks around the tanks. Crimson flat hazard stencils."),
    "BLD-LOG-003": ("Repair Facility", "85 × 60 × 35", "repair damaged ships and machinery",
        "A repair hangar made of a bronze hull arch closed at the back, with a wide open-fronted but roofed bay whose interior is a flat dark recess (no visible scaffolds). A heavy solid overhead crane-beam housing across the top. Two chunky solid manipulator-root blocks at the bay mouth and a rack of clamped spare-part pods."),
    "BLD-LOG-004": ("Cargo Depot", "60 × 45 × 24", "handle colony goods and trade",
        "A smuggler's warehouse: a low bronze hall with a row of flush closed loading hatches, surrounded by solid stacks of capsule cargo pods and off-white salvaged container blocks. One suspiciously large flush hatch in the floor apron. The crescent emblem stencilled over the main doors."),
    "BLD-DEF-001": ("Basic Turret", "18 × 18 × 15", "early anti-ship defence",
        "A concealed cupola turret: a thick bronze dome on a heavy gunmetal turntable ring on a stepped plinth, with one thick barrel shroud (not a thin barrel) protruding. An off-white salvaged ammunition block clamped to the base."),
    "BLD-DEF-002": ("Plasma Turret", "24 × 24 × 20", "heavy energy defence against ships",
        "A big bronze cupola on a heavy turntable, carrying one short wide emitter shroud whose muzzle is a flat opaque dark disc (no glow), flanked by two enclosed capsule capacitor tanks of unequal size in clamp collars. Solid louvre cooling blocks on the back of the cupola."),
    "BLD-DEF-003": ("Photon Turret", "22 × 22 × 21", "late-game precision anti-ship defence",
        "A taller cupola on a heavy turntable carrying two thick unequal emitter shrouds, one bronze and one salvaged off-white, with a solid block sensor head on top. Raised rib conduits run from the base to the emitters. Flat opaque dark lenses."),
    "BLD-DEF-004": ("Anti-Missile Pod", "14 × 14 × 12", "intercept incoming missiles",
        "A compact closed launcher: a thick bronze box pod with a flat face of sixteen closed hatch cells, on a heavy gimbal turntable, with a small solid block radar head on one side and a flush reload hatch on the back."),
    "BLD-DEF-005": ("Screen Generator", "34 × 34 × 28", "project a defensive colony screen",
        "A central solid bronze projector column capped by a thick flat dark disc (unlit), surrounded by three solid ring-shaped clamp collars stacked around it, and three short stabilising node blocks of unequal height on the plinth corners. One off-white salvaged capacitor block."),
    "BLD-DEF-006": ("Missile Silo", "26 × 26 × 18", "launch strategic missiles",
        "A low armoured silo built into a stepped gunmetal plinth, capped by a massive round bronze flush hatch split into two closed leaves with a crimson crescent stencil across them. A solid sunken blast trench on one side and an off-white salvaged service block."),
    "BLD-DEF-007": ("Satellite Silo", "30 × 30 × 22", "deploy orbital satellites",
        "A squat bronze launch drum on a stepped plinth with a closed segmented dome roof, a solid tapered guidance mast block beside it, and a pod-transfer cradle holding one enclosed capsule satellite pod ready for loading. One flush service hatch."),
    "BLD-DEF-008": ("Defensive Bunker", "25 × 20 × 10", "provide generic colony fortification",
        "A very low armoured bunker made of a half-buried bronze hull section with sloped solid armour skirts, a row of narrow closed firing-port slits and one flush entry hatch. A verdigris patch plate on the roof."),
    "BLD-SEN-001": ("Sensor Array", "38 × 34 × 40", "detect ships and threats",
        "A tall solid tapered bronze mast block on a heavy turntable, carrying one large thick-bowl dish with a heavy rim on a chunky block mount, plus two smaller block sensor heads at different heights. A salvaged off-white equipment cabin at the base with a slit viewport."),
    "BLD-SEN-002": ("Long Range Transmitter", "24 × 24 × 65", "long-distance communications",
        "A tall landmark tower made of a stack of bronze hull rings and clamp collars tapering upward, braced by four solid sloped buttress blocks at the base (no guy wires). A large thick-bowl dish on a chunky mount near the top and a solid block antenna crown. Broad crimson stencil bands."),
    "BLD-TEC-001": ("Gravity Nullifier", "48 × 48 × 44", "manipulate local gravity",
        "Exotic salvaged tech held down by overbuilt Mauna engineering: three thick concentric bronze rings standing at different angles, all physically joined to each other and to the plinth by heavy gunmetal clamp blocks (nothing floating), around a solid dark sphere. Four massive stabiliser blocks at the corners."),
    "BLD-TEC-002": ("Asteroid Engine", "180 × 120 × 90", "move an entire asteroid",
        "A colossal engine torn from a capital ship and sunk into the asteroid: one enormous thick-walled bronze thrust bell pointing up and back, closed by a solid dark exhaust plate, set into a massive stepped gunmetal anchor foundation with four huge solid anchor blocks. Enclosed fuel trunks as thick raised ribs lead to a rack of giant clamped fuel capsules. Unmistakable scale."),
    "BLD-TEC-003": ("Shield Generator", "42 × 42 × 34", "generate local protective shields",
        "A heavy bronze generator drum with four thick field-coil rings clamped around it at unequal spacing, a flat dark opaque core disc on top (no glow), and a bank of enclosed capsule capacitors in clamp collars along one side."),
    "BLD-TEC-004": ("Construction Droid Hub", "40 × 32 × 18", "deploy autonomous construction units",
        "A low bronze operations hub with a row of five flush closed droid-bay hatches of two sizes, a solid block control mast with a slit viewport, and two clamped material-dispenser capsule pods. An off-white salvaged charging block at one end."),
    "BLD-TEC-005": ("Teleportation Equipment", "50 × 44 × 30", "transfer personnel or matter",
        "A raised round bronze transfer pad with a flat dark opaque centre disc, framed by three solid tapered projector pylons of unequal height joined to the pad by thick clamp collars, and a protected off-white salvaged control block with a slit viewport. Low solid barrier blocks around the pad."),
}

STYLE = (
    "Mauna smuggler-salvage faction. Buildings are made from acquired and rebuilt hardware: grounded bronze "
    "ship hulls, capsule cargo pods and whole angular salvaged sections of off-white foreign plating, joined "
    "by thick gunmetal clamp collars, on stepped gunmetal plinths. Deliberately asymmetric. Large "
    "verdigris-oxidised stepped patch plates. Every building has at least one large flush closed hatch. The "
    "building's function-specific shape described above is the dominant form; add only the parts the "
    "description names. Palette: tarnished bronze and umber, verdigris secondary, off-white only on whole "
    "salvaged sections, gunmetal joints and plinths, near-black glazing, and a single controlled accent of "
    "deep crimson as small flat stencils. At most one small crescent-and-blade emblem from reference 2. Wear concentrates at collars and hatches. Avoid Terran hazard stripes, tarps, dangling "
    "cargo, clean luxury curves and all-over neon."
)

SAFETY = (
    "Isolated elevated orthographic-style three-quarter view, same camera as reference 1, complete building "
    "centred on a plain flat light-grey background. No ground shadow, no environment, no text, no watermark, "
    "no people, no vehicles. Build it to be scanned into 3D. These are hard constraints: solid enclosed "
    "volumes and a closed silhouette; no open lattice, truss, gantry framework, scaffold or derrick; no "
    "wires, cables, hoses, ropes, chains, railings, ladders or thin aerials; no floating parts; no holes or "
    "see-through gaps; no feature smaller than about 2% of the building's longest dimension; large planes "
    "with deep bold breaks, no fine greeble or rivets. Windows and energy surfaces are flat, opaque, "
    "near-black and unlit: no interiors, no screens, no reflections. Matte to satin only; no chrome, gloss or "
    "transparency. Flat even studio lighting, no rim light, no baked ambient occlusion, no glowing lights, "
    "energy effects or emissive surfaces. Stencils are flat paint, not raised geometry."
)

# Owner-requested re-rolls (2026-09-14): v01 copied the Exchange's layout. v01 files are kept as record.
REROLL = {
    "BLD-CMD-002": ("v02", "It must NOT look like the Exchange: no dome, no row of pods, no tapered tower. Its "
        "dominant form is a long, low, angular armoured block with a flat roof, clearly a fortress rather than a hall."),
    "BLD-LIF-001": ("v02", "It must NOT look like the Exchange: no bronze dome, no dish, no tapered tower, no row of "
        "pods. Its dominant form is the long smooth off-white salvaged hull section lying horizontally, mostly off-white "
        "rather than bronze, with the medical roundel as the main mark."),
    "BLD-LIF-003": ("v02", "It must NOT look like the Exchange: no dome anywhere. Its dominant form is the long "
        "horizontal bronze control capsule with the tall stacked heat-exchanger slabs clearly the largest mass."),
}

EXCHANGE = ROOT / "Concepts/Mauna/Buildings/MAU-BLD-CMD-001/MAU-BLD-CMD-001_concept_v01.png"
EMBLEM = ROOT / "Concepts/Mauna/Shared/MAU-EMB-001/MAU-emblem_ref_v01.png"


def terran_ref(asset: str) -> Path:
    return sorted((ROOT / "Concepts/Terran/Buildings" / asset).glob(f"{asset}_concept_v*.png"))[-1]


def main() -> None:
    jobs = []
    for asset, (name, dims, purpose, subject) in BUILDINGS.items():
        mau = f"MAU-{asset}"
        ver, extra = REROLL.get(asset, ("v01", ""))
        if extra:
            subject = f"{subject} {extra}"
        target = ROOT / f"Concepts/Mauna/Buildings/{mau}/{mau}_concept_{ver}.png"
        ref = terran_ref(asset)
        text = (
            "Use your image generation tool to create exactly ONE image. Three reference images are attached:\n"
            f"1. {EXCHANGE.name}: the approved Mauna Exchange. Match ONLY its materials, surface texture, palette, "
            "wear, rendering style and camera. Do NOT copy its composition: no dome, no row of three pods, no "
            "tapered tower, no dish and no crimson band unless the prompt below asks for them. This building must "
            "have its own distinct silhouette.\n"
            f"2. {EMBLEM.name}: the approved Mauna crescent-and-blade emblem.\n"
            f"3. {ref.name}: the Terran {name}. Use it ONLY to understand this building's function, footprint and "
            "main parts. Do NOT copy its Terran style, boxy panelling, off-white-and-black colour scheme, "
            "hazard stripes, railings, thin parts or glowing lights.\n"
            "Do not edit any repository file. When the image exists, copy the generated PNG to this exact path "
            "(create folders as needed), then reply with only the saved path:\n"
            f"{target}\n\nPROMPT:\n"
            f"Mauna {name}, {dims} metres, for {purpose}. {subject}\n\n{STYLE}\n\n{SAFETY}\n"
        )
        prompt = OUT / f"{mau}_concept_{ver}.txt"
        prompt.write_text(text, encoding="utf-8")
        jobs.append(f"{mau}\t{prompt.relative_to(ROOT).as_posix()}\t{ref.relative_to(ROOT).as_posix()}\t{ver}")
    # newline="\n": bash reads this file, and a Windows \r would end up inside the last column.
    (OUT / "jobs.tsv").write_text("\n".join(jobs) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(jobs)} prompts written")


if __name__ == "__main__":
    main()
