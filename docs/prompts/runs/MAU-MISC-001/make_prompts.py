"""Generate Mauna prompts for missiles, satellites, environment kits and prop kits (17 assets)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

SHIP = "Ships/MAU-SHP-007/MAU-SHP-007_concept_v01.png"
BLD = "Buildings/MAU-BLD-CMD-001/MAU-BLD-CMD-001_concept_v01.png"

# id: (folder, name, size, purpose, subject, style reference)
ASSETS = {
    "MIS-ORD-001": ("Missiles", "Standard Missile", "5 x 0.8 m", "baseline ship or silo-launched ordnance",
        "A single Mauna guided missile shown horizontally. A thick bronze cylindrical body with a blunt salvaged off-white seeker nose clamped on by a gunmetal collar, a second collar at mid-body, and four short stubby solid fins of unequal size set in two pairs at the tail. The tail nozzle is a flat dark recessed plate. One small crimson emblem stencil. Crude but heavy.", SHIP),
    "MIS-ORD-002": ("Missiles", "Plasma Missile", "6 x 1.1 m", "advanced high-damage ordnance",
        "A single heavier Mauna guided missile shown horizontally. A fat bronze body swelling at mid-length into a thick verdigris containment band holding a flat, opaque, unlit dark warhead drum with no glow. A salvaged off-white seeker nose on a clamp collar, four short solid tail fins, and a flat dark recessed tail nozzle. Two crimson stencils.", SHIP),
    "MIS-ORD-003": ("Missiles", "Interceptor Missile", "2.5 x 0.35 m", "destroying incoming missiles",
        "A single small, slim Mauna interceptor missile shown horizontally. A narrow bronze tube with an off-white salvaged nose cone, one clamp collar, and oversized but thick solid control fins near the tail: chunky wedge fins, never thin blades. Flat dark recessed tail nozzle. One tiny crimson stencil.", SHIP),
    "SAT-ORB-001": ("Satellites", "Recon Satellite", "12 m span", "extending detection and intelligence",
        "A Mauna reconnaissance satellite: a compact bronze drum body with a salvaged off-white instrument block clamped to one side, two thick rigid near-black sensor panels of unequal size on chunky solid root blocks, and one blocky sensor head. Deliberately lopsided, with a counterweight block opposite the panels. Small crimson emblem.", SHIP),
    "SAT-ORB-002": ("Satellites", "Defence Satellite", "16 m span", "orbital defence",
        "A Mauna defence satellite: an armoured bronze drum body on a heavy gunmetal turntable ring carrying one concealed cupola turret with a thick barrel shroud. Two short rigid near-black power panels on solid roots, one blocky sensor head, one clamped off-white capsule magazine pod. Compact and militarised.", SHIP),
    "SAT-ORB-003": ("Satellites", "Communications Satellite", "14 m span", "colony communications",
        "A Mauna communications satellite: a bronze drum body carrying one large squat thick-bowl dish with a heavy rim on a blocky mount, plus one smaller dish at a different angle. Two rigid near-black panels on solid roots, one salvaged off-white equipment block clamped on. Asymmetric, with a visible counterweight.", SHIP),
    "ENV-INF-001": ("Environment", "Construction Pad Kit", "8-80 m", "seating buildings convincingly on rock",
        "A labelled kit sheet of isolated Mauna foundation modules in neat rows on a light-grey background, each drawn separately at consistent scale: stepped gunmetal plinth slabs in three sizes, corner and edge blocks, solid anchoring plates, shallow solid service trenches with flush covers, and a ramp block. Worn bronze and gunmetal, verdigris patches, one crimson stencil per module type. Short labels only.", BLD),
    "ENV-INF-002": ("Environment", "Road and Pipe Network", "2-100 m modules", "connecting colony buildings visually",
        "A labelled kit sheet of isolated Mauna connection modules in neat rows on a light-grey background: straight road slabs, a corner and a T-junction slab, a raised solid walkway block, enclosed pipe trunk sections as thick solid boxes with clamp collars, a pipe elbow, a pipe tee and a junction block. Every pipe is an enclosed solid trunk, never an open tube or a thin free-standing pipe. Short labels only.", BLD),
    "PRP-IND-001": ("Props", "Conveyor Module Kit", "3-20 m modules", "moving ore between mining assets",
        "A labelled kit sheet of isolated Mauna conveyor modules in neat rows on a light-grey background: enclosed straight conveyor box sections in two lengths, an inclined conveyor box, a corner junction box, a solid transfer tower block and a chute block. Every module is a closed solid box with clamp collars: no open belts, no frames, no visible rollers. Short labels only.", BLD),
    "PRP-IND-002": ("Props", "Ore Container Kit", "1-6 m", "populating mining and cargo areas",
        "A labelled kit sheet of isolated Mauna ore containers in neat rows on a light-grey background: enclosed capsule ore pods in three sizes, a square hopper bin, a low ore skip with thick solid walls, and two compact ore piles as solid rounded mounds. Bronze and off-white salvage, verdigris patches, crimson stencils. Short labels only.", BLD),
    "PRP-IND-003": ("Props", "Power Node Kit", "1-8 m", "distributing power around colonies visually",
        "A labelled kit sheet of isolated Mauna power modules in neat rows on a light-grey background: a transformer block, a capacitor capsule in a clamp collar, a substation cabinet, a junction block and a raised conduit rib section. All solid enclosed volumes; conduits are raised ribs on a base slab, never free-standing cables. Short labels only.", BLD),
    "PRP-IND-004": ("Props", "Industrial Pipe Kit", "0.3-4 m diameter", "dressing and connecting industrial assets",
        "A labelled kit sheet of isolated Mauna pipe modules in neat rows on a light-grey background: straight enclosed pipe trunks in three diameters, a 90-degree elbow, a tee, a valve block with a solid handwheel disc, a clamp-collar coupler and a capped end block. Thick-walled and solid, seated on small plinth blocks. Short labels only.", BLD),
    "PRP-IND-005": ("Props", "Tank and Vessel Kit", "2-18 m", "populating process-industry buildings",
        "A labelled kit sheet of isolated Mauna tanks in neat rows on a light-grey background: upright capsule pressure vessels in three sizes, two horizontal cylinders in clamp-collar cradles, a conical hopper body and a squat spherical tank. Bronze with verdigris, some off-white salvage, clamp collars, crimson stencils. Short labels only.", BLD),
    "PRP-IND-006": ("Props", "Cargo Crate Kit", "0.5-4 m", "populating logistics areas",
        "A labelled kit sheet of isolated Mauna cargo containers in neat rows on a light-grey background: stackable rectangular crates in three sizes, a flat pallet block, a sealed drum, a long capsule container and a stacked pair of crates. Worn bronze and off-white salvage with clamp bands and small crescent emblem stencils. Short labels only.", BLD),
    "PRP-IND-007": ("Props", "Antenna and Sensor Kit", "0.5-18 m", "coherent communications detail",
        "A labelled kit sheet of isolated Mauna sensor parts in neat rows on a light-grey background: squat thick-bowl dishes with heavy rims in three sizes on blocky mounts, a blocky radar head, a flat panel sensor block, a solid tapered mast base and an equipment box. Every dish is a thick solid bowl, never a thin curved sheet, and there are no thin aerials or rods. Short labels only.", BLD),
    "PRP-CON-001": ("Props", "Crane and Manipulator Kit", "5-45 m", "animating yards, docks and factories",
        "A labelled kit sheet of isolated Mauna lifting modules in neat rows on a light-grey background: a solid tapered crane tower block, an enclosed boom housing as one thick solid beam, a hinge and root block, a heavy hook-carriage block, a folded manipulator arm stowed as a solid segmented volume, and a turntable ring. Every part is a closed solid volume: no lattice, no trusses, no cables, no chains. Short labels only.", BLD),
    "PRP-CON-002": ("Props", "Construction and Scaffolding Kit", "2-30 m modules", "showing staged building construction",
        "A labelled kit sheet of isolated Mauna construction modules in neat rows on a light-grey background: a foundation slab, a partially built solid wall block, a half-finished hull section with exposed stepped plating, a solid temporary service cabin, a stack of building plates and a solid work-platform block with a low parapet. Scaffolding is expressed as solid stepped blocks and plate stacks, never as open frames, poles or planks. Short labels only.", BLD),
}

STYLE = (
    "Mauna smuggler-salvage faction: hardware acquired and rebuilt. Tarnished bronze and umber, "
    "verdigris-oxidised stepped patch plates, off-white only on whole salvaged sections, thick gunmetal "
    "clamp collars and plinths, near-black opaque glazing, and a single controlled accent of deep crimson "
    "as small flat stencils, with at most one small crescent-and-blade emblem from reference 2. Wear "
    "concentrates at collars and edges. Avoid Terran hazard stripes, tarps, dangling cargo, clean luxury "
    "curves and neon."
)

SAFETY = (
    "Isolated elevated orthographic-style three-quarter view, complete subject centred on a plain flat "
    "light-grey background, matching the rendering style and lighting of reference 1. No ground shadow, no "
    "environment, no watermark, no people, no vehicles. Build it to be scanned into 3D: solid enclosed "
    "volumes and closed silhouettes; no open lattice, truss, scaffold or frame; no wires, cables, ropes, "
    "chains, railings, ladders or thin aerials; no holes or see-through gaps; no feature smaller than about "
    "2% of the object's longest dimension; large planes with deep bold breaks, no fine greeble or rivets. "
    "Glass is flat, opaque and near-black. Matte to satin only; no chrome, gloss or transparency. Flat even "
    "studio lighting, no rim light, no baked ambient occlusion, no glowing lights or emissive surfaces. "
    "Stencils are flat paint, not raised geometry."
)


def main() -> None:
    jobs = []
    for asset, (folder, name, size, purpose, subject, ref1) in ASSETS.items():
        mau = f"MAU-{asset}"
        out = f"{folder}/{mau}/{mau}_concept_v01.png"
        terran = sorted((ROOT / f"Concepts/Terran/{folder}/{asset}").glob(f"{asset}_concept_v*.png"))[-1]
        text = (
            "Use your image generation tool to create exactly ONE image. Three reference images are attached:\n"
            f"1. {Path(ref1).name}: an approved Mauna asset. Match ONLY its materials, surface texture, "
            "palette, wear and rendering style. Do NOT copy its shape or composition.\n"
            "2. MAU-emblem_ref_v01.png: the approved Mauna crescent-and-blade emblem.\n"
            f"3. {terran.name}: the Terran {name}. Use it ONLY to understand what this asset is for and "
            "roughly how big its parts are. Do NOT copy its Terran style, colours, hazard stripes or thin parts.\n"
            "Do not edit any repository file. When the image exists, copy the generated PNG to this exact "
            "path (create folders as needed), then reply with only the saved path:\n"
            f"{(ROOT / 'Concepts/Mauna' / out)}\n\nPROMPT:\n"
            f"Mauna {name}, {size}, for {purpose}. {subject}\n\n{STYLE}\n\n{SAFETY}\n"
        )
        p = OUT / f"{mau}_concept_v01.txt"
        p.write_text(text, encoding="utf-8", newline="\n")
        jobs.append(f"{mau}\t{p.name}\t{out}\t{ref1}\t{terran.relative_to(ROOT).as_posix()}")
    (OUT / "jobs.tsv").write_text("\n".join(jobs) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(jobs)} prompts written")


if __name__ == "__main__":
    main()
