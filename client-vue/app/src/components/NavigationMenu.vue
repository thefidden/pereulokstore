<script setup lang = "ts">
    import { ref } from "vue";
    import { useRouter } from "vue-router";
    import { MEDIA } from "../conf.ts";

    const emits = defineEmits(['close'])

    const router = useRouter()
    const closingAnimation = ref(false)

    const pages = [
        { name: 'Комиксы', type: 'comics', image: `${MEDIA}/comics-page.jpg` },
        { name: 'Фигурки', type: 'shape', image: `${MEDIA}/shapes-page.jpg` },
        { name: 'Костюмы', type: 'suit', image: `${MEDIA}/suits-page.jpg` }
    ]

    function closeMenu() {
        closingAnimation.value = true
        setTimeout(() => emits('close'), 300)
    }

    function navigateTo(url: string) {
        closeMenu()
        router.push(url)
    }
</script>

<template>
    <Teleport to = 'body'>
        <div :class = "['menu', !closingAnimation ? 'menuFadeIn' : 'menuFadeOut']">
            <div v-for = "page in pages" class = 'pageButton' @click = "navigateTo(`/store?type=${page.type}`)">
                <img :src = "page.image" alt = ''/>
                <div class = 'pageName'>{{ page.name }}</div>
            </div>
        </div>

        <div :class = "['menuCloseArrow', !closingAnimation ? 'arrowFadeIn' : 'arrowFadeOut']" @click = "closeMenu">
            <svg width = "42" height = "23" viewBox = "0 0 42 23" fill = "none">
                <path
                    d = "M0.43934 9.98524C-0.146447 10.571 -0.146447 11.5208 0.43934 12.1066L9.98528 21.6525C10.5711 22.2383 11.5208 22.2383 12.1066 21.6525C12.6924 21.0667 12.6924 20.117 12.1066 19.5312L3.62132 11.0459L12.1066 2.56062C12.6924 1.97483 12.6924 1.02508 12.1066 0.439297C11.5208 -0.14649 10.5711 -0.14649 9.98528 0.439297L0.43934 9.98524ZM1.5 11.0459V12.5459H41.5V11.0459V9.5459H1.5V11.0459Z"
                    fill = "white"/>
            </svg>
        </div>

        <div :class = "['overlay', !closingAnimation ? 'overlayFadeIn' : 'overlayFadeOut']" @click = "closeMenu"></div>
    </Teleport>
</template>

<style scoped>
    .menu {
        position: fixed;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;

        opacity: 0;

        inset: 0;
        width: 605px;
        height: 100%;

        background-color: #7A89DC;
        z-index: 11;
        box-shadow: 0 0 50px 15px rgba(122, 137, 220, 0.4);

        border-radius: 0 100px 100px 0;
    }

    .pageButton {
        box-sizing: border-box;

        width: 400px;
        height: 190px;

        display: flex;
        align-items: center;
        justify-content: center;

        background-color: white;
        border-radius: 100px;
        border: 2px solid transparent;
        overflow: hidden;

        transition: transform 0.3s ease-out, border 0.3s ease-out, box-shadow 0.3s ease-out;
        will-change: transform, border, box-shadow;

        cursor: pointer;

        &:hover {
            transform: scale(1.05);
            border: 2px solid rgb(177, 217, 225);
            box-shadow: 0 0 30px 15px rgba(177, 217, 225, 0.3);

            img {
                transform: scale(1.05);
                filter: brightness(1);
            }
        }
    }

    .pageButton img {
        width: 100%;
        height: 100%;
        object-fit: cover;

        filter: brightness(0.9);

        transition: transform 0.3s ease-out, filter 0.3s ease-out;
        will-change: transform, filter;
    }

    .pageName {
        position: absolute;

        width: 190px;
        height: 50px;

        display: flex;
        align-items: center;
        justify-content: center;

        background-color: #7A89DC;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 24px;
        color: white;

        will-change: transform;

        user-select: none;
    }

    .menuCloseArrow {
        position: fixed;

        display: flex;
        justify-content: center;
        align-items: center;

        width: 70px;
        aspect-ratio: 1/1;
        padding: 10px;

        left: 705px;
        top: 50%;
        z-index: 12;

        transform: translateY(-50%);

        opacity: 0;
        background-color: var(--color-magenta);

        box-sizing: border-box;
        border: 2px solid white;
        border-radius: 100%;

        will-change: opacity, transform, filter, box-shadow, left;
        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;

        cursor: pointer;

        &:hover {
            transform: translateY(-50%) scale(1.1);
            box-shadow: 0 0 30px 15px rgba(177, 217, 225, 0.3);
        }
    }

    .overlay {
        position: fixed;

        inset: 0;
        width: 100%;
        height: 100%;

        background-color: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(3px);
        z-index: 10;
        opacity: 0;

        will-change: opacity;
    }

    .menuFadeIn { animation: MenuFadeIn 0.3s ease-out forwards }
    .menuFadeOut { animation: MenuFadeOut 0.3s ease-out forwards }
    .arrowFadeIn { animation: ArrowFadeIn 0.3s ease-out forwards }
    .arrowFadeOut { animation: ArrowFadeOut 0.3s ease-out forwards }
    .overlayFadeIn { animation: OverlayFadeIn 0.15s ease-out forwards }
    .overlayFadeOut { animation: OverlayFadeOut 0.15s ease-out forwards }

    @keyframes MenuFadeIn {
        from {
            opacity: 0;
            transform: translateX(-5%) scale(1.1);
            filter: blur(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0) scale(1);
            filter: blur(0);
        }
    }

    @keyframes MenuFadeOut {
        from {
            opacity: 1;
            transform: translateX(0) scale(1);
            filter: blur(0);
        }
        to {
            opacity: 0;
            transform: translateX(-5%) scale(1.1);
            filter: blur(30px);
        }
    }

    @keyframes ArrowFadeIn {
        from {
            opacity: 0;
            left: 655px;
            filter: blur(10px);
        }
        to {
            opacity: 1;
            left: 705px;
            filter: blur(0);
        }
    }

    @keyframes ArrowFadeOut {
        from {
            opacity: 1;
            left: 705px;
            filter: blur(0);
        }
        to {
            opacity: 0;
            left: 655px;
            filter: blur(10px);
            transform: translateY(-50%) scale(1.5);
        }
    }

    @keyframes OverlayFadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes OverlayFadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }
</style>