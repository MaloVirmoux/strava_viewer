import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

import CanvaSize from "./setup/CanvaSize";
import Scene from "./setup/Scene";
import Camera from "./setup/Camera";
import Renderer from "./setup/Renderer";
import Composer from "./setup/Composer";
import RenderPass from "./pass/RenderPass";
import Tile from "./object/Tile";

/** Class used to create the render */
export default class Render {
    /**
     * Creates the render
     * @param {Element} container HTML Element to display the scene in
     */
    constructor(container) {
        this.container = container;

        this.canvaSize = new CanvaSize();
        this.scene = new Scene();
        this.camera = new Camera(this.canvaSize);
        this.scene.add(this.camera);

        this.controls = new OrbitControls(this.camera, this.container);

        const pointLight1 = new THREE.PointLight(0xff9000, 50);
        pointLight1.position.set(3, 2, 3);
        const pointLight2 = new THREE.PointLight(0x0090ff, 50);
        pointLight2.position.set(-3, 2, 3);
        const pointLight3 = new THREE.PointLight(0x90ff90, 50);
        pointLight3.position.set(0, -3, 3);
        const pointLightHelper1 = new THREE.PointLightHelper(pointLight1, 1);
        const pointLightHelper2 = new THREE.PointLightHelper(pointLight2, 1);
        const pointLightHelper3 = new THREE.PointLightHelper(pointLight3, 1);
        this.scene.add(
            pointLight1,
            pointLightHelper1,
            pointLight2,
            pointLightHelper2,
            pointLight3,
            pointLightHelper3
        );

        const axisHelper = new THREE.AxesHelper(3);
        const tile = new Tile();
        this.scene.add(tile, axisHelper);
        console.log(tile);

        this.renderer = new Renderer(this.canvaSize, this.container);
        this.composer = new Composer(this.canvaSize, this.renderer);
        this.renderPass = new RenderPass(this.scene, this.camera);
        this.composer.addPass(this.renderPass);

        this.createListener();
    }

    /** Creates the listeners to update the render */
    createListener() {
        window.addEventListener("resize", () => {
            this.canvaSize.update();
            this.camera.update(this.canvaSize);
            this.renderer.update(this.canvaSize);
            this.composer.update(this.canvaSize);
        });
    }

    /** Updates the render */
    update() {
        this.composer.render();
    }
}
