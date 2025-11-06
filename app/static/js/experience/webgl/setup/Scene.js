import * as THREE from "three";

/** Class used to create the scene */
export default class Scene extends THREE.Scene {
    /** Creates the scene */
    constructor() {
        super();
        this.background = new THREE.Color("#ffffff");
    }
}
