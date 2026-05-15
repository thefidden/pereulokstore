import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import obfuscatorPlugin from "vite-plugin-javascript-obfuscator";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue()
    ],

    build: {
        rollupOptions: {
            plugins: [
                obfuscatorPlugin({
                    apply: "serve",
                    debugger: true,
                    options: {
                        compact: false,
                        controlFlowFlattening: true,
                        controlFlowFlatteningThreshold: 1,
                        numbersToExpressions: true,
                        simplify: false,
                        stringArrayShuffle: true,
                        splitStrings: true,
                        stringArrayThreshold: 1,
                        deadCodeInjection: true,
                        deadCodeInjectionThreshold: 1,
                        identifierNamesGenerator: 'hexadecimal'
                    }
                })
            ]
        }
    },

    server: {
        host: '0.0.0.0',
        port: 5173,
        allowedHosts: true,

        // DEV MODE:
        // http://127.0.0.1:5173  -> frontend
        // http://127.0.0.1:8000  -> backend
        //
        // Все запросы ниже
        // автоматически проксируются на Django backend.

        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            },

            '/media': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            },

            '/admin': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            },

            '/static': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            },

            '/silk': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            },
        }
    }
})
