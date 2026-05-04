<script setup lang = "ts">

</script>

<template>
    <Teleport to = "body">
        <div class = 'root'>
            <div class = 'loadingAnimation'></div>
        </div>
    </Teleport>
</template>

<style scoped>
    .root {
        position: fixed;

        display: flex;
        align-items: center;
        justify-content: center;

        inset: 0;
        width: 100%;
        height: 100%;
        z-index: 20;

        background-color: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(3px);
        opacity: 1;
    }

    .loadingAnimation {
        width: 70px;
        height: 70px;
        z-index: 21;

        border-radius: 50%;
        background: var(--color-magenta);

        animation: pulse 1.2s ease-in-out infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(0.8);
            opacity: 0.5;
            filter: blur(10px);
        }
        50% {
            transform: scale(1.2);
            opacity: 1;
            filter: blur(0);
        }
        100% {
            transform: scale(0.8);
            opacity: 0.5;
            filter: blur(10px);
        }
    }
</style>