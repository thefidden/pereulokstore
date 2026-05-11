<script setup lang="ts">
    import type { CartItem } from "../interfaces/CartItemInterface.ts";
    import ProductCard from "./ProductCard.vue";
    import { useCart } from "../stores/CartStore.ts";

    interface CartItemProps {
        cartItem: CartItem,
        animationDelay?: number,
        showButtons?: boolean
    }

    const {
        cartItem,
        animationDelay = 0,
        showButtons = true
    } = defineProps<CartItemProps>()

    const cart = useCart()
    const { update: updateCartItem, delete: deleteFromCart } = cart
</script>

<template>
    <div class="root" :style="`animation-delay: ${animationDelay}s`">
        <ProductCard :product="cartItem.product" :playAnimation="false"/>

        <div class="amountControl">
            <div v-if="showButtons" class="decreaseAmount" @click="
                 cartItem.amount - 1
                 ? updateCartItem(cartItem,cartItem.amount - 1)
                 : deleteFromCart(cartItem)
            ">
                <svg width="15" height="3" viewBox="0 0 15 3">
                    <line x1="1.5" y1="1.5" x2="13.5" y2="1.5" stroke-width="3"
                          stroke-linecap="round"/>
                </svg>
            </div>

            <div class="amount">Кол-во: {{ cartItem.amount }}</div>

            <div v-if="showButtons" class="increaseAmount" @click="updateCartItem(cartItem,cartItem.amount + 1)">
                <svg width="15" height="15" viewBox="0 0 15 15">
                    <line x1="7.5" y1="1.5" x2="7.5" y2="13.5" stroke-width="3"
                          stroke-linecap="round"/>
                    <line x1="1.5" y1="7.5" x2="13.5" y2="7.5" stroke-width="3"
                          stroke-linecap="round"/>
                </svg>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .root {
        display: flex;
        flex-direction: column;
        gap: 20px;

        opacity: 0;
        will-change: filter, opacity, transform;
        animation: SlideIn 0.3s ease-out forwards
    }

    .amount {
        display: flex;
        justify-content: center;
        align-items: center;

        width: 50%;
        height: 35px;

        border-radius: 100px;
        background-color: var(--color-magenta);
        color: white;
        user-select: none;
    }

    .amountControl {
        position: relative;

        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;

        gap: 10px;
    }

    .decreaseAmount, .increaseAmount {
        display: flex;
        justify-content: center;
        align-items: center;

        background-color: var(--color-magenta);
        stroke: white;

        width: 35px;
        aspect-ratio: 1/1;
        border-radius: 100%;

        transition: background-color 0.3s ease-out,
        stroke 0.3s ease-out,
        box-shadow 0.3s ease-out;
        will-change: background-color, stroke, box-shadow;

        &:hover {
            background-color: white;
            stroke: var(--color-magenta);
            box-shadow: 0 0 30px 15px rgba(255, 255, 255, 0.5);
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