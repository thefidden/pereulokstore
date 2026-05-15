<script setup lang = "ts">

</script>

<template>
    <div/>
</template>

<style scoped>
    div {
        position: fixed;

        inset: 0;
        width: 100%;
        height: 100%;

        background-color: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(3px);
        z-index: 10;
        opacity: 0;

        will-change: opacity;
        animation: ${closingAnimation ? "overlayFadeOut 0.15s ease-out forwards" : "overlayFadeIn 0.15s ease-out forwards"};

        @keyframes overlayFadeIn {
            to {
                opacity: 1;
            }
        }

        @keyframes overlayFadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
    }
</style>