import { ConfigEnv, UserConfigExport, defineConfig, loadEnv } from "vite";

// import { VitePWA } from "vite-plugin-pwa";
import { resolve } from "path";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default ({ mode }: ConfigEnv): UserConfigExport => {
    const env = loadEnv(mode, ".");
    return defineConfig({
        plugins: [
            vue(),
            // VitePWA({
            //     registerType: "autoUpdate",
            //     includeAssets: [
            //         "favicon.ico",
            //         "apple-touch-icon.png",
            //         "masked-icon.svg"
            //     ],
            //     manifest: {
            //         id: "/",
            //         categories: ["work"],
            //         name: "ts bot dashboard",
            //         short_name: "Статистика бота ТС",
            //         description: "Статистика телеграм бота Торгового Сбора",
            //         theme_color: "#ffffff",
            //         start_url: "/",
            //         icons: [
            //             {
            //                 src: "pwa-192x192.png",
            //                 sizes: "192x192",
            //                 type: "image/png"
            //             },
            //             {
            //                 src: "pwa-512x512.png",
            //                 sizes: "512x512",
            //                 type: "image/png"
            //             },
            //             {
            //                 src: "pwa-512x512.png",
            //                 sizes: "512x512",
            //                 type: "image/png",
            //                 purpose: "any maskable"
            //             }
            //         ]
            //     }
            // })
        ],
        server: {
            https: false,
            proxy: {
                "/api": {
                    target: env.VITE_PROXY_TARGET,
                    changeOrigin: true
                }
            },
            host: env.VITE_HOST,
            port: parseInt(env.VITE_PORT)
        },
        build: {
            target: "modules",
            outDir: "dist",
            manifest: false,
            minify: "esbuild",
            emptyOutDir: true,
            sourcemap: false,
            cssCodeSplit: false,
            chunkSizeWarningLimit: 2 << 19
        },
        resolve: {
            alias: [
                {
                    find: "@",
                    replacement: resolve(__dirname, "src")
                }
            ]
        }
    });
};
