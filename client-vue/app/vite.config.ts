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
        allowedHosts: true
    }
})
