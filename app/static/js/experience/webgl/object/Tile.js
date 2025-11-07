import * as THREE from "three";
import { subdiviseFaces, computeUVs } from "./utils";

/** Class used to create a tile */
export default class Tile extends THREE.Mesh {
    /**
     * Creates the tile
     */
    constructor() {
        const geometry = new TileGeometry();
        const material = new TileMaterial();
        super(geometry, material);
    }
}

/* Doc
                                              ⮝                                                                                    ⮝
                                              ║  Coord Y                                                                            ║  Coord Y
                                             (2)                                                                                   (2)
                                       ██████ ║ ██████                                                                       ██████ ║ ██████
              Face 4 & 5            ███       ║       ███            Face 6 & 7                                           ███       ║       ███
                              ██████          ║          ██████                                                     ██████          ║          ██████
                           ███                ║                ███                                               ███                ║                ███
                     ██████       Face 0      ║                   ██████                                   ██████                   ║                   ██████
                  ███                         ║                         ███                             ███             Face 16     ║     Face 17             ███
               (1)┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈║┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈(3)                       (1)┈┈┈                         ║                         ┈┈┈(3)
               ███                            ║                   ┈┈┈┈┈┈   ███                       ███   ┈┈┈┈┈┈                   ║                   ┈┈┈┈┈┈   ███
               ███                            ║             ┈┈┈┈┈┈         ███   Face 8 & 9          ███         ┈┈┈┈┈┈             ║             ┈┈┈┈┈┈         ███
               ███      Face 1                ║       ┈┈┈┈┈┈               ███                       ███               ┈┈┈┈┈┈       ║       ┈┈┈┈┈┈               ███
               ███                            ║ ┈┈┈┈┈┈                     ███                       ███                     ┈┈┈┈┈┈ ║ ┈┈┈┈┈┈         Face 18     ███
            ═══███════════════════════════════╬════════════════════════════███═══➤  Coord X      ═══███═══════════════════════════(0)═══════════════════════════███═══➤  Coord X
               ███                     ┈┈┈┈┈┈ ║                            ███                       ███     Face 21         ┈┈┈┈┈┈ ║ ┈┈┈┈┈┈                     ███
               ███               ┈┈┈┈┈┈       ║           Face 2           ███                       ███               ┈┈┈┈┈┈       ║       ┈┈┈┈┈┈               ███
Face 14 & 15   ███         ┈┈┈┈┈┈             ║                            ███                       ███         ┈┈┈┈┈┈             ║             ┈┈┈┈┈┈         ███
               ███   ┈┈┈┈┈┈                   ║                            ███                       ███   ┈┈┈┈┈┈                   ║                   ┈┈┈┈┈┈   ███
               (6)┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈║┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈(4)                       (6)┈┈┈             Face 20     ║     Face 19             ┈┈┈(4)
                  ███                         ║                         ███                             ███                         ║                         ███
                     ██████                   ║ Face 3            ██████                                   ██████                   ║                   ██████
                           ███                ║                ███                                               ███                ║                ███
                              ██████          ║          ██████                                                     ██████          ║          ██████
            Face 12 & 13            ███       ║       ███            Face 10 & 11                                         ███       ║       ███
                                       ██████ ║ ██████                                                                       ██████ ║ ██████
                                             (5)                                                                                   (5)
                                              ║                                                                                     ║
*/

/** Class used to create a tile */
class TileGeometry extends THREE.BufferGeometry {
    /**
     * Creates the tile
     */
    constructor() {
        super();

        const COORD_X = Math.sqrt(3) / 2;
        const COORD_Y = 1;
        const COORD_Z = 1;

        const V1_FLOOR = [ - COORD_X,   COORD_Y / 2,       0]; // prettier-ignore
        const V2_FLOOR = [         0,   COORD_Y    ,       0]; // prettier-ignore
        const V3_FLOOR = [   COORD_X,   COORD_Y / 2,       0]; // prettier-ignore
        const V4_FLOOR = [   COORD_X, - COORD_Y / 2,       0]; // prettier-ignore
        const V5_FLOOR = [         0, - COORD_Y    ,       0]; // prettier-ignore
        const V6_FLOOR = [ - COORD_X, - COORD_Y / 2,       0]; // prettier-ignore
        const V0_ROOF_ = [         0,             0, COORD_Z]; // prettier-ignore
        const V1_ROOF_ = [ - COORD_X,   COORD_Y / 2, COORD_Z]; // prettier-ignore
        const V2_ROOF_ = [         0,   COORD_Y    , COORD_Z]; // prettier-ignore
        const V3_ROOF_ = [   COORD_X,   COORD_Y / 2, COORD_Z]; // prettier-ignore
        const V4_ROOF_ = [   COORD_X, - COORD_Y / 2, COORD_Z]; // prettier-ignore
        const V5_ROOF_ = [         0, - COORD_Y    , COORD_Z]; // prettier-ignore
        const V6_ROOF_ = [ - COORD_X, - COORD_Y / 2, COORD_Z]; // prettier-ignore

        const floorPositions = [
            [...V1_FLOOR, ...V2_FLOOR, ...V3_FLOOR], // Face 0 (Floor - Top)
            [...V6_FLOOR, ...V1_FLOOR, ...V3_FLOOR], // Face 1 (Floor - Middle #1)
            [...V6_FLOOR, ...V3_FLOOR, ...V4_FLOOR], // Face 2 (Floor - Middle #2)
            [...V6_FLOOR, ...V4_FLOOR, ...V5_FLOOR], // Face 3 (Floor - Bottom)
        ];
        const floorUVs = Array(floorPositions.length * 3).fill([NaN, NaN]);

        const wallsPositions = [
            [...V1_FLOOR, ...V1_ROOF_, ...V2_FLOOR], // Face 4 (Wall #1 - Bottom)
            [...V2_FLOOR, ...V1_ROOF_, ...V2_ROOF_], // Face 5 (Wall #1 - Top)
            [...V2_FLOOR, ...V2_ROOF_, ...V3_FLOOR], // Face 6 (Wall #2 - Bottom)
            [...V3_FLOOR, ...V2_ROOF_, ...V3_ROOF_], // Face 7 (Wall #2 - Top)
            [...V3_FLOOR, ...V3_ROOF_, ...V4_FLOOR], // Face 8 (Wall #3 - Bottom)
            [...V4_FLOOR, ...V3_ROOF_, ...V4_ROOF_], // Face 9 (Wall #3 - Top)
            [...V4_FLOOR, ...V4_ROOF_, ...V5_FLOOR], // Face 10 (Wall #4 - Bottom)
            [...V5_FLOOR, ...V4_ROOF_, ...V5_ROOF_], // Face 11 (Wall #4 - Top)
            [...V5_FLOOR, ...V5_ROOF_, ...V6_FLOOR], // Face 12 (Wall #5 - Bottom)
            [...V6_FLOOR, ...V5_ROOF_, ...V6_ROOF_], // Face 13 (Wall #5 - Top)
            [...V6_FLOOR, ...V6_ROOF_, ...V1_FLOOR], // Face 14 (Wall #6 - Bottom)
            [...V1_FLOOR, ...V6_ROOF_, ...V1_ROOF_], // Face 15 (Wall #6 - Top)
        ];
        const wallsUVs = Array(wallsPositions.length * 3).fill([NaN, NaN]);

        const draftRoofPositions = [
            [...V1_ROOF_, ...V0_ROOF_, ...V2_ROOF_], // Face 16 (Ceiling #1)
            [...V2_ROOF_, ...V0_ROOF_, ...V3_ROOF_], // Face 17 (Ceiling #2)
            [...V3_ROOF_, ...V0_ROOF_, ...V4_ROOF_], // Face 18 (Ceiling #3)
            [...V4_ROOF_, ...V0_ROOF_, ...V5_ROOF_], // Face 19 (Ceiling #4)
            [...V5_ROOF_, ...V0_ROOF_, ...V6_ROOF_], // Face 20 (Ceiling #5)
            [...V6_ROOF_, ...V0_ROOF_, ...V1_ROOF_], // Face 21 (Ceiling #6)
        ];
        const dividedRoofPositions = subdiviseFaces(draftRoofPositions, 10);
        const roofUVs = computeUVs(dividedRoofPositions, ["x", "y"]);

        this.setAttribute(
            "position",
            new THREE.Float32BufferAttribute(
                [
                    ...floorPositions.flat(Infinity),
                    ...wallsPositions.flat(Infinity),
                    ...dividedRoofPositions.flat(Infinity),
                ],
                3
            )
        );
        this.computeVertexNormals();

        this.setAttribute(
            "uv",
            new THREE.Float32BufferAttribute(
                [
                    ...floorUVs.flat(Infinity),
                    ...wallsUVs.flat(Infinity),
                    ...roofUVs.flat(Infinity),
                ],
                2
            )
        );
    }
}

/** Class used to create the material for the tiles */
class TileMaterial extends THREE.MeshStandardMaterial {
    /**
     * Creates the material
     */
    constructor() {
        const image = new Image();
        const texture = new THREE.Texture(image);
        image.addEventListener("load", () => {
            texture.needsUpdate = true;
        });
        image.src = "/app/static/img/height_map.jpg";
        super({
            color: 0xffffff,
            roughness: 0.4,
            displacementMap: texture,
            displacementScale: 0.2,
        });
    }
}
