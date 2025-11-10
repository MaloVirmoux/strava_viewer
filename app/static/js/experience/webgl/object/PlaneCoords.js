import * as THREE from "three";

/** Class used to create plane coords */
export default class PlaneCoords extends THREE.Plane {
    /**
     * Creates the Plane Coords
     * @param {THREE.Vector3} origin
     * @param {THREE.Vector3} horizontalAxis
     * @param {THREE.Vector3} verticalAxis
     */
    constructor(origin, horizontalAxis, verticalAxis) {
        super();
        this.origin = origin;

        this.setFromCoplanarPoints(
            this.origin,
            this.origin.clone().add(horizontalAxis),
            this.origin.clone().add(verticalAxis)
        );

        // prettier-ignore
        // Used to convert a vertex from the global coords to the plane local coords
        this.invertedAxesMatrix = new THREE.Matrix3(
            horizontalAxis.x, verticalAxis.x, this.normal.x, 
            horizontalAxis.y, verticalAxis.y, this.normal.y,
            horizontalAxis.z, verticalAxis.z, this.normal.z
        ).invert();
    }

    /**
     * Checks if the provided vertex is on the plane
     * @param {THREE.Vector3} vertex Vertex to check
     * @returns {boolean} True if the point is on the plane, false otherwise
     */
    contains(vertex) {
        return this.distanceToPoint(vertex) < 1e-10 ? true : false;
    }

    /**
     * Converts a vertex to the local coords system
     * @param {THREE.Vector3} vertex Vertex to convert
     * @returns {THREE.Vector2} Converted vertex
     */
    getLocalCoords(vertex) {
        if (!this.contains(vertex)) {
            return new THREE.Vector2();
        }
        const localCoords = vertex
            .clone()
            .sub(this.origin)
            .applyMatrix3(this.invertedAxesMatrix);
        return new THREE.Vector2(localCoords.x, localCoords.y);
    }
}
