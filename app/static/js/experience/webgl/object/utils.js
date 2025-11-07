import * as THREE from "three";

// ==================== Face division ====================

/*
            vertex0
              ⟋⟍
      edge0 ⟋    ⟍ edge2
          ⟋        ⟍
vertex1 ⟋____________⟍ vertex2
             edge1
*/

/**
 * Subdivises faces into smaller faces
 * @param {list} faces List of nine values, or list of list of nine values, each representing a face to subdivise
 * @param {int} n_divisions Number of division to process (/!\ Exponential)
 * @returns {list} List of values representing the faces
 */
export function subdiviseFaces(faces, n_divisions) {
    if (typeof faces[0] === "number") {
        faces = [faces];
    }

    for (let division = 0; division < n_divisions; division++) {
        let newFaces = [];
        faces.forEach((face) => {
            const vertices = computeVertices(face);
            const edges = computeEdges(vertices);
            const [newVertex, longestEdge] = computeDivision(edges);
            newFaces.push(
                ...computeNewFaces(vertices, newVertex, edges, longestEdge)
            );
        });
        faces = newFaces;
    }
    return faces;
}

/**
 * Computes the vertices from the provided list of values
 * @param {list} face List of nine values representing a face (ex: [v1.x, v1.y, v1.z, ..., v3.z])
 * @returns {list} List of three THREE.Vector3 vertices
 */
function computeVertices(face) {
    const vertex0 = new THREE.Vector3(face[0], face[1], face[2]);
    const vertex1 = new THREE.Vector3(face[3], face[4], face[5]);
    const vertex2 = new THREE.Vector3(face[6], face[7], face[8]);
    return [vertex0, vertex1, vertex2];
}

/**
 * Computes the edges from the provided list of vertices
 * @param {list} vertices List of three THREE.Vector3 vertices
 * @returns {list} List of three THREE.Vector3 edges
 */
function computeEdges(vertices) {
    const edge0 = {
        fromVertex: vertices[0],
        toVertex: vertices[1],
        edge: new THREE.Vector3(
            vertices[1].x - vertices[0].x,
            vertices[1].y - vertices[0].y,
            vertices[1].z - vertices[0].z
        ),
    };
    const edge1 = {
        fromVertex: vertices[1],
        toVertex: vertices[2],
        edge: new THREE.Vector3(
            vertices[2].x - vertices[1].x,
            vertices[2].y - vertices[1].y,
            vertices[2].z - vertices[1].z
        ),
    };
    const edge2 = {
        fromVertex: vertices[2],
        toVertex: vertices[0],
        edge: new THREE.Vector3(
            vertices[0].x - vertices[2].x,
            vertices[0].y - vertices[2].y,
            vertices[0].z - vertices[2].z
        ),
    };
    return [edge0, edge1, edge2];
}

/**
 * Creates a vertex in the middle of the longest of the provided edges
 * @param {list} edges List of three THREE.Vector3 edges
 * @returns {list} Returns both the newly created vertex and the splitted edge
 */
function computeDivision(edges) {
    const longestEdge = edges.reduce(
        (edge, previous) =>
            edge.edge.length() > previous.edge.length() ? edge : previous,
        { edge: new THREE.Vector3(0, 0, 0) }
    );

    const newVertex = new THREE.Vector3(
        (longestEdge.fromVertex.x + longestEdge.toVertex.x) / 2,
        (longestEdge.fromVertex.y + longestEdge.toVertex.y) / 2,
        (longestEdge.fromVertex.z + longestEdge.toVertex.z) / 2
    );
    return [newVertex, longestEdge];
}

/**
 * Splits the face in two
 * @param {list} vertices List of three THREE.Vector3 vertices
 * @param {THREE.Vector3} newVertex Newly created vertex
 * @param {list} edges List of three THREE.Vector3 edges
 * @param {THREE.Vector3} longestEdge Splitted edge
 * @returns {list} List of values representing the splitted faces
 */
function computeNewFaces(vertices, newVertex, edges, longestEdge) {
    switch (longestEdge) {
        case edges[0]:
            return [
                createNewFace(vertices[0], newVertex, vertices[2]),
                createNewFace(newVertex, vertices[1], vertices[2]),
            ];
        case edges[1]:
            return [
                createNewFace(vertices[0], vertices[1], newVertex),
                createNewFace(vertices[0], newVertex, vertices[2]),
            ];
        case edges[2]:
            return [
                createNewFace(vertices[0], vertices[1], newVertex),
                createNewFace(newVertex, vertices[1], vertices[2]),
            ];
    }
}

/**
 * Creates a face from three vertex
 * @param {THREE.Vector3} vertex1 First vertex of the face
 * @param {THREE.Vector3} vertex2 Second vertex of the face
 * @param {THREE.Vector3} vertex3 Third vertex of the face
 * @returns {list} List of values representing a face
 */
function createNewFace(vertex1, vertex2, vertex3) {
    return [
        ...[vertex1.x, vertex1.y, vertex1.z],
        ...[vertex2.x, vertex2.y, vertex2.z],
        ...[vertex3.x, vertex3.y, vertex3.z],
    ];
}

// ==================== UVs ====================

/**
 * Computes the UVs from the faces
 * @param {list} faces List of nine values, or list of list of nine values, each representing a face to compute the UVs of
 * @param {list} axis Ordered list of the two axis to compute the uvs on (ex: ["x", "y"])
 * @returns {list} List of the UVs
 */
export function computeUVs(faces, axis) {
    if (typeof faces[0] === "number") {
        faces = [faces];
    }

    const range = computeRange(faces, axis);

    const uvs = [];
    faces.forEach((face) => {
        uvs.push(...computeFaceUVs(face, axis, range));
    });

    return uvs;
}

/**
 * Computes the maximum range of the faces vertices
 * @param {list} faces List of nine values, or list of list of nine values, each representing a face to compute the range froms
 * @param {list} axis List of the two axis to compute the uvs on (ex: ["x", "y"])
 * @returns {number} Maximum range of the faces vertices
 */
function computeRange(faces, axis) {
    let ignoredAxis;
    if (!axis.includes("x")) ignoredAxis = 0;
    if (!axis.includes("y")) ignoredAxis = 1;
    if (!axis.includes("z")) ignoredAxis = 2;

    const flatFaces = faces.flat(Infinity);
    for (ignoredAxis; ignoredAxis < flatFaces.length; ignoredAxis += 3) {
        flatFaces[ignoredAxis] = 0;
    }

    return Math.max(-Math.min(...flatFaces), Math.max(...flatFaces));
}

/**
 * Computes the UVs from the face
 * @param {list} faces List of nine values, representing a face to compute the UVs of
 * @param {list} axis List of the two axis to compute the uvs on (ex: ["x", "y"])
 * @param {number} range Maximum range of the faces vertices
 * @returns List of eighteen coords representing the face UVs
 */
function computeFaceUVs(face, axis, range) {
    const getVertex = (i) => {
        return face.slice(i, i + 3);
    };
    const uvs = [];
    for (let i = 0; i < face.length; i += 3) {
        uvs.push(...computeVertexUVs(getVertex(i), axis, range));
    }

    return uvs;
}

/**
 * Compute the UVs for a vertex
 * @param {list} vertex List of three values representing a vertex
 * @param {list} axis List of the two axis to compute the uvs on (ex: ["x", "y"])
 * @param {number} range Maximum range of the UVs
 * @returns List of two coords representing the vertex UVs
 */
function computeVertexUVs(vertex, axis, range) {
    const getAxisIndex = (axis) => {
        return { x: 0, y: 1, z: 2 }[axis];
    };
    const computeUV = (index) => {
        return (vertex[index] + range) / (range * 2);
    };
    return [computeUV(getAxisIndex(axis[0])), computeUV(getAxisIndex(axis[1]))];
}
