import * as THREE from "three";
import PlaneCoords from "./PlaneCoords";

// ==================== Face division ====================

/**
 * Subdivises faces into smaller faces
 * @param {list<list<THREE.Vector3>>} faces List of three vertices, or list of list of three vertices, each representing a face to subdivise
 * @param {number} nDivisions Number of division to process (/!\ Exponential, each level multiplies by four the number of faces, <= 5 recommended)
 * @returns {list<list<THREE.Vector3>>} List of list of three vertices representing the faces
 */
export function subdiviseFaces(faces, nDivisions) {
    if (faces[0].isVector3) {
        faces = [faces];
    }

    for (let division = 0; division < nDivisions; division++) {
        let newFaces = [];
        faces.forEach((face) => {
            newFaces.push(...subdiviseFace(face));
        });
        faces = newFaces;
    }
    return faces;
}

/**
 * Subdivises a face into four smaller faces
 * @param {list<THREE.Vector3>} face List of three vertices representing a face to subdivise
 * @returns {list<list<THREE.Vector3>>} List of list of three vertices representing the four faces
 */
function subdiviseFace(face) {
    const middleVertices01 = getMiddle(face[0], face[1]),
        middleVertices12 = getMiddle(face[1], face[2]),
        middleVertices20 = getMiddle(face[2], face[0]);

    return [
        [face[0], middleVertices01, middleVertices20],
        [face[1], middleVertices12, middleVertices01],
        [face[2], middleVertices20, middleVertices12],
        [middleVertices01, middleVertices12, middleVertices20],
    ];
}

// export function subdiviseFacesEdge(faces, nDivisions) {
//     if (typeof faces[0] === "number") {
//         faces = [faces];
//     }

//     for (let division = 0; division < nDivisions; division++) {
//         let newFaces = [];
//         faces.forEach((face) => {
//             newFaces.push(...subdiviseFace(face));
//         });
//         faces = newFaces;
//     }
//     return faces;
// }

/**
 * Returns the vertex in the middle of two others vertices
 * @param {THREE.Vector3} vertex0 First vertex to compute the middle from
 * @param {THREE.Vector3} vertex1 Second vertex to compute the middle from
 * @returns {THREE.Vector3} Vertex in the middle of the above vertices
 */
function getMiddle(vertex0, vertex1) {
    return vertex0.clone().lerp(vertex1, 0.5);
}

/**
 * Converts a list of vertices into a list of positions
 * @param {list<THREE.Vector3>} vertices Nested list of vertices
 * @returns {list} Flat list of positions
 */
export function verticesToPositions(vertices) {
    return vertices
        .flat(Infinity)
        .map((vertex) => vertex.toArray())
        .flat(Infinity);
}

// ==================== UVs ====================

/**
 * Computes the UVs from the faces
 * @param {list<list<THREE.Vector3>>} faces List of nine vertices, or list of list of nine vertices, each representing a face to compute the UVs of
 * @param {THREE.Vector3} origin Vertex being the origin of the faces
 * @param {THREE.Vector3} horizontalAxis Horizontal axis to compute the UVs on
 * @param {THREE.Vector3} verticalAxis Vertical axis to compute the UVs on
 * @returns {list<number>} List of the UVs
 */
export function computeUVs(faces, origin, horizontalAxis, verticalAxis) {
    if (faces[0].isVector3) {
        faces = [faces];
    }

    const planeCoords = new PlaneCoords(origin, horizontalAxis, verticalAxis);
    const range = computeRange(faces, planeCoords);

    const uvs = [];
    faces.forEach((face) => {
        uvs.push(...computeFaceUVs(face, planeCoords, range));
    });
    return uvs;
}

/**
 * Computes the maximum range of the faces vertices
 * @param {list<list<THREE.Vector3>>} faces List of list of nine vertices, each representing a face to compute the range from
 * @param {PlaneCoords} planeCoords Plane coords to compute the UVs on
 * @returns {number} Maximum range of the faces vertices
 */
function computeRange(faces, planeCoords) {
    const vertices = faces
        .flat(Infinity)
        .map((vertex) => planeCoords.getLocalCoords(vertex));
    const ranges = vertices.map((vertex) => vertex.toArray()).flat(Infinity);

    return Math.max(-Math.min(...ranges), Math.max(...ranges));
}

/**
 * Computes the UVs from the face
 * @param {list<THREE.Vector3>} face List of nine vertices representing a face to compute the UVs of
 * @param {PlaneCoords} planeCoords Plane coords to compute the UVs on
 * @param {number} range Maximum range of the faces vertices
 * @returns List of eighteen coords representing the face UVs
 */
function computeFaceUVs(face, planeCoords, range) {
    const uvs = [];
    face.forEach((vertex) => {
        uvs.push(...computeVertexUVs(vertex, planeCoords, range));
    });
    return uvs;
}

/**
 * Compute the UVs for a vertex
 * @param {THREE.Vector3} vertex List of three values representing a vertex
 * @param {PlaneCoords} planeCoords Plane coords to compute the UVs on
 * @param {number} range Maximum range of the faces vertices
 * @returns List of two coords representing the vertex UVs
 */
function computeVertexUVs(vertex, planeCoords, range) {
    const localCoords = planeCoords.getLocalCoords(vertex);
    return [
        (localCoords.x + range) / (range * 2),
        (localCoords.y + range) / (range * 2),
    ];
}
