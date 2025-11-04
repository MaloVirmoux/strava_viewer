import * as THREE from "three";

import CanvaSize from "./setup/CanvaSize";
import Scene from "./setup/Scene";
import Camera from "./setup/Camera";
import Renderer from "./setup/Renderer";
import Composer from "./setup/Composer";
import RenderPass from "./pass/RenderPass";

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

        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        const mesh = new THREE.Mesh(geometry, material);
        this.scene.add(mesh);

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
