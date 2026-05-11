<script setup lang = "ts">
    import {useRouter} from "vue-router";
    import {HOST} from "../conf.ts";
    import {computed} from "vue";
    import type {Product} from "../interfaces/ProductInterface.ts";

    interface ProductCardProps {
        product: Product,
        playAnimation?: boolean,
        animationName?: string,
        animationDelay?: number
    }

    const router = useRouter()
    const {
        product,
        playAnimation = true,
        animationName = 'fadeIn',
        animationDelay = 0
    } = defineProps<ProductCardProps>()
</script>

<template>
    <div :class = "['root', playAnimation ? animationName : '']" :style = "`animation-delay: ${animationDelay}s`">
        <div class = "card" @click = "router.push(`/products/${product.id}`)">
            <div class = 'imageFrame'>
                <img :src = 'HOST + product.images[0]' alt = ''/>
            </div>
            <div class = 'name'>{{ product.name }}</div>
            <div class = 'price'>{{ product.price }}₽</div>
        </div>
    </div>
</template>

<style scoped>
    .root {
        will-change: filter, opacity, transform;
    }

    .fadeIn {
        opacity: 0;

        animation-name: FadeIn;
        animation-duration: 0.3s;
        animation-timing-function: ease-out;
        animation-fill-mode: forwards;
    }

    .slideIn {
        opacity: 0;

        animation-name: SlideIn;
        animation-duration: 0.3s;
        animation-timing-function: ease-out;
        animation-fill-mode: forwards;
    }

    .card {
        box-sizing: border-box;
        width: 295px;
        height: 400px;

        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;

        background-color: #7A89DC;
        border-radius: 100px;
        padding: 10px;
        cursor: pointer;

        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out;
        will-change: transform, box-shadow;

        &:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);

            img {
                transform: scale(1.05);
            }
        }
    }

    .imageFrame {
        width: 100%;
        height: 80%;

        border-radius: 100px;
        overflow: hidden;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;

            transition: transform 0.3s ease-out;
            will-change: transform;
        }
    }

    .name, .price {
        font-family: "Jost", serif;
        font-size: 24px;
        color: white;
        user-select: none;
    }

    @keyframes FadeIn {
        from {
            filter: blur(30px);
            opacity: 0;
            transform: scale(1.2);
        }
        to {
            filter: blur(0);
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes SlideIn {
        from {
            filter: blur(30px);
            opacity: 0;
            transform: translateX(-20%);
        }
        to {
            filter: blur(0);
            opacity: 1;
            transform: translateX(0);
        }
    }
</style>