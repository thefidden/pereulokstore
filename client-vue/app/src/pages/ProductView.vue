<script setup lang="ts">
    import { computed, ref, watch } from "vue";
    import { storeToRefs } from "pinia";

    import { useProduct } from "../stores/ProductStore.ts";
    import { useCart } from "../stores/CartStore.ts";
    import Loader from "../components/Loader.vue";
    import { useUser } from "../stores/UserStore.ts";
    import type { CartItem } from "../interfaces/CartItemInterface.ts";

    const productStore = useProduct()
    const cartStore = useCart()

    const { product, loading: productLoading } = storeToRefs(productStore)
    const { loading: cartLoading } = storeToRefs(cartStore)

    const { get: getFromCart, add: addToCart, delete: deleteFromCart } = cartStore

    const productInCartHovered = ref(false)

    const cartItem = computed(() => getFromCart(product.value!!))
    const productInCartText = computed(() => !productInCartHovered.value ? "Товар в корзине" : "Удалить из корзины")
</script>

<template>
    <Loader v-if="productLoading || cartLoading"/>

    <div v-else class="productGrid">
        <div class="name">{{ product?.name }}</div>

        <div class="image">
            <img :src="product?.images?.[0]" alt=""/>
        </div>

        <div class="price">Цена: {{ product?.price }}₽</div>
        <div class="description">{{ product?.description }}</div>

        <div v-if="cartItem" class="productInCart"
             @click="deleteFromCart(cartItem)"
             @mouseenter="productInCartHovered = true"
             @mouseleave="productInCartHovered = false"
        >
            {{ productInCartText }}
        </div>

        <div v-else class="addToCart" @click="addToCart(product!!)">Добавить в корзину</div>
    </div>
</template>

<style scoped>
    .productGrid {
        display: grid;
        grid-gap: 30px;
        grid-template-columns: 4fr 3fr 3fr;
        grid-template-rows: 100px auto 100px;
        grid-template-areas:
                "image name name"
                "image description description"
                "image price add-to-cart";
    }

    .name {
        grid-area: name;
        opacity: 0;

        animation: fadeInScale 0.3s ease-out 0.3s forwards;
        will-change: transform, opacity, filter;
    }

    .price {
        grid-area: price;
        opacity: 0;

        animation: fadeInScale 0.3s ease-out 0.5s forwards;
        will-change: transform, opacity, filter;
    }

    .name, .price, .productInCart, .addToCart {
        display: flex;
        justify-content: center;
        align-items: center;

        background-color: white;
        border-radius: 100px;

        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);
        text-wrap: nowrap;
    }

    .image {
        grid-area: image;

        height: 600px;
        box-sizing: border-box;
        border-radius: 100px;
        overflow: hidden;

        border: 2px solid white;

        opacity: 0;

        animation: fadeInFromLeft 0.3s ease-out forwards;
        will-change: transform, opacity, filter;
    }

    .image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .description {
        grid-area: description;

        display: flex;
        justify-content: center;
        align-items: center;

        padding: 20px 100px;
        opacity: 0;

        background-color: white;
        border-radius: 100px;

        font-size: var(--font-size-regular);
        color: black;

        animation: fadeInScale 0.3s ease-out 0.4s forwards;
        will-change: transform, opacity, filter;
    }

    .productInCart, .addToCart {
        font-size: 32px;
        user-select: none;

        opacity: 0;
        cursor: pointer;

        animation: fadeInScale 0.3s ease-out 0.6s forwards;
        will-change: background-color, color, box-shadow, transform, opacity, filter;
        transition: background-color 0.3s ease-out, color 0.3s ease-out, box-shadow 0.3s ease-out;
    }

    .addToCart {
        background-color: var(--color-magenta);
        color: white;

        &:hover {
            background-color: white;
            color: var(--color-magenta);
            box-shadow: 0 0 30px 15px rgba(255, 255, 255, 0.5);
        }
    }

    .productInCart {
        &:hover {
            background-color: var(--color-magenta);
            color: white;
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);
        }
    }

    @keyframes fadeInFromLeft {
        from {
            transform: translateX(-20%) scale(1.2);
            opacity: 0;
            filter: blur(30px);
        }
        to {
            transform: translateX(0) scale(1);
            opacity: 1;
            filter: blur(0);
        }
    }

    @keyframes fadeInFromRight {
        from {
            transform: translateX(5%);
            opacity: 0;
            filter: blur(3px);
        }
        to {
            transform: translateX(0);
            opacity: 1;
            filter: blur(0);
        }
    }

    @keyframes fadeInScale {
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

    @keyframes rootFadeOut {
        to {
            opacity: 0;
            filter: blur(30px);
            transform: scale(2);
        }
    }
</style>