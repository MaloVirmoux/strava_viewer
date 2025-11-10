import * as THREE from "three";
import { params } from "../../params";
import { computeUVs, subdiviseFaces, verticesToPositions } from "./utils";

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

/* Schema of the hexagon 
                                     ⮝                                                                  ⮝
                                     ║  Coord Y                                                          ║  Coord Y
                                    (2)                                                                 (2)
              Face 4 & 5      ██████ ║ ██████      Face 6 & 7                                     ██████ ║ ██████
                           ███       ║       ███                                               ███       ║       ███
                     ██████          ║          ██████                                   ██████          ║          ██████
                  ███        Face 0  ║                ███                             ███        Face 16 ║ Face 17        ███
               (1)┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈║┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈(3)                       (1)┈┈┈┈┈┈             ║             ┈┈┈┈┈┈(3)
               ███                   ║             ┈┈┈┈┈┈███                       ███      ┈┈┈          ║          ┈┈┈      ███
               ███      Face 1       ║       ┈┈┈┈┈┈      ███   Face 8 & 9          ███         ┈┈┈┈┈┈    ║    ┈┈┈┈┈┈         ███
               ███                   ║ ┈┈┈┈┈┈            ███                       ███               ┈┈┈ ║ ┈┈┈       Face 18 ███
            ═══███═══════════════════╬═══════════════════███═══➤  Coord X      ═══███══════════════════(0)══════════════════███═══➤  Coord X
               ███            ┈┈┈┈┈┈ ║                   ███                       ███ Face 22       ┈┈┈ ║ ┈┈┈               ███
Face 14 & 15   ███      ┈┈┈┈┈┈       ║       Face 2      ███                       ███         ┈┈┈┈┈┈    ║    ┈┈┈┈┈┈         ███
               ███┈┈┈┈┈┈             ║                   ███                       ███      ┈┈┈          ║          ┈┈┈      ███
               (6)┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈║┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈(4)                       (6)┈┈┈┈┈┈             ║             ┈┈┈┈┈┈(4)
                  ███                ║  Face 3        ███                             ███        Face 21 ║ Face 20         ███
                     ██████          ║          ██████                                   ██████          ║           ██████
                           ███       ║       ███                                               ███       ║       ███
            Face 12 & 13      ██████ ║ ██████      Face 10 & 11                                   ██████ ║ ██████
                                    (5)                                                                 (5)
                                     ║                                                                   ║
*/

/** Class used to create a tile */
class TileGeometry extends THREE.BufferGeometry {
    /**
     * Creates the tile
     */
    constructor() {
        super();

        const COORD_Y = params.tile.size,
            COORD_X = (COORD_Y * Math.sqrt(3)) / 2,
            COORD_Z = params.tile.height;

        // prettier-ignore
        const V1_FLOOR = new THREE.Vector3(- COORD_X,   COORD_Y / 2,       0),
              V2_FLOOR = new THREE.Vector3(        0,   COORD_Y    ,       0),
              V3_FLOOR = new THREE.Vector3(  COORD_X,   COORD_Y / 2,       0),
              V4_FLOOR = new THREE.Vector3(  COORD_X, - COORD_Y / 2,       0),
              V5_FLOOR = new THREE.Vector3(        0, - COORD_Y    ,       0),
              V6_FLOOR = new THREE.Vector3(- COORD_X, - COORD_Y / 2,       0),
              V0_ROOF_ = new THREE.Vector3(        0,             0, COORD_Z),
              V1_ROOF_ = new THREE.Vector3(- COORD_X,   COORD_Y / 2, COORD_Z),
              V2_ROOF_ = new THREE.Vector3(        0,   COORD_Y    , COORD_Z),
              V3_ROOF_ = new THREE.Vector3(  COORD_X,   COORD_Y / 2, COORD_Z),
              V4_ROOF_ = new THREE.Vector3(  COORD_X, - COORD_Y / 2, COORD_Z),
              V5_ROOF_ = new THREE.Vector3(        0, - COORD_Y    , COORD_Z),
              V6_ROOF_ = new THREE.Vector3(- COORD_X, - COORD_Y / 2, COORD_Z);

        const floorVertices = [
            [V1_FLOOR, V2_FLOOR, V3_FLOOR], // Face 0 (Floor - Top)
            [V6_FLOOR, V1_FLOOR, V3_FLOOR], // Face 1 (Floor - Middle #1)
            [V6_FLOOR, V3_FLOOR, V4_FLOOR], // Face 2 (Floor - Middle #2)
            [V6_FLOOR, V4_FLOOR, V5_FLOOR], // Face 3 (Floor - Bottom)
        ];
        const floorUVs = Array(floorVertices.length * 3).fill([NaN, NaN]);

        const wallsVertices = [
            [V1_FLOOR, V1_ROOF_, V2_FLOOR], // Face 4 (Wall #1 - Bottom)
            [V2_FLOOR, V1_ROOF_, V2_ROOF_], // Face 5 (Wall #1 - Top)
            [V2_FLOOR, V2_ROOF_, V3_FLOOR], // Face 6 (Wall #2 - Bottom)
            [V3_FLOOR, V2_ROOF_, V3_ROOF_], // Face 7 (Wall #2 - Top)
            [V3_FLOOR, V3_ROOF_, V4_FLOOR], // Face 8 (Wall #3 - Bottom)
            [V4_FLOOR, V3_ROOF_, V4_ROOF_], // Face 9 (Wall #3 - Top)
            [V4_FLOOR, V4_ROOF_, V5_FLOOR], // Face 10 (Wall #4 - Bottom)
            [V5_FLOOR, V4_ROOF_, V5_ROOF_], // Face 11 (Wall #4 - Top)
            [V5_FLOOR, V5_ROOF_, V6_FLOOR], // Face 12 (Wall #5 - Bottom)
            [V6_FLOOR, V5_ROOF_, V6_ROOF_], // Face 13 (Wall #5 - Top)
            [V6_FLOOR, V6_ROOF_, V1_FLOOR], // Face 14 (Wall #6 - Bottom)
            [V1_FLOOR, V6_ROOF_, V1_ROOF_], // Face 15 (Wall #6 - Top)
        ];
        const wallsUVs = Array(wallsVertices.length * 3).fill([NaN, NaN]);

        let roofVertices = [
            [V1_ROOF_, V0_ROOF_, V2_ROOF_], // Face 16 (Ceiling #1)
            [V2_ROOF_, V0_ROOF_, V3_ROOF_], // Face 17 (Ceiling #2)
            [V3_ROOF_, V0_ROOF_, V4_ROOF_], // Face 18 (Ceiling #3)
            [V4_ROOF_, V0_ROOF_, V5_ROOF_], // Face 19 (Ceiling #4)
            [V5_ROOF_, V0_ROOF_, V6_ROOF_], // Face 20 (Ceiling #5)
            [V6_ROOF_, V0_ROOF_, V1_ROOF_], // Face 21 (Ceiling #6)
        ];
        roofVertices = subdiviseFaces(roofVertices, params.tile.division);
        const ORIGIN_ROOF = new THREE.Vector3(0, 0, COORD_Z),
            HORIZONTAL_ROOF_AXIS = new THREE.Vector3(1, 0, 0),
            VERTICAL_ROOF_AXIS = new THREE.Vector3(0, 1, 0);
        const roofUVs = computeUVs(
            roofVertices,
            ORIGIN_ROOF,
            HORIZONTAL_ROOF_AXIS,
            VERTICAL_ROOF_AXIS
        );

        this.setAttribute(
            "position",
            new THREE.Float32BufferAttribute(
                [
                    ...verticesToPositions(floorVertices),
                    ...verticesToPositions(wallsVertices),
                    ...verticesToPositions(roofVertices),
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
        // image.src = "/app/static/img/height_map.jpg";
        image.src = "/app/static/img/uv_test.jpg";
        super({
            color: "#ffffff",
            roughness: 0.4,
            // wireframe: true,
            map: texture,
            // displacementMap: texture,
            // displacementScale: 0.2,
        });
    }
}
