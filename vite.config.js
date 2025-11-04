import { defineConfig } from "vite";

export default defineConfig({
    root: ".",
    base: "/",
    server: {
        port: 5173,
        open: "/app/templates/map.html", // ouvre automatiquement cette page
    },
});
