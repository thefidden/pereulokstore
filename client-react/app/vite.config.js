import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react'
import obfuscator from "vite-plugin-javascript-obfuscator"

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        obfuscator(
            {
            compact: true,

            controlFlowFlattening: true,
            controlFlowFlatteningThreshold: 1,

            deadCodeInjection: true,
            deadCodeInjectionThreshold: 1,

            stringArray: true,
            stringArrayEncoding: ['base64'],
            rotateStringArray: true,

            selfDefending: true,
            identifierNamesGenerator: 'hexadecimal',

            domainLock: true,
            domainLockRedirectUrl: 'www.example.com'
        })
    ],
    server: {
        allowedHosts: true
    }
})
