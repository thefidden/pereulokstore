<script setup lang="ts">
    import { storeToRefs } from "pinia";
    import { computed, ref } from "vue";

    import { useCart } from "../stores/CartStore.ts";
    import { useOrders } from "../stores/OrdersStore.ts";

    import CartItemCard from "../components/CartItemCard.vue";
    import Loader from "../components/Loader.vue";
    import OrderPaymentStatusBox from "../components/OrderPaymentStatusBox.vue";

    const state = history.state

    const cartStore = useCart()
    const { cart, loading: cartLoading } = storeToRefs(cartStore)

    const ordersStore = useOrders()
    const { loading: ordersLoading } = storeToRefs(ordersStore)
    const { create: createOrder } = ordersStore

    const totalPrice = computed(() => {
        return cart.value.reduce((accumulator, cartItem) => accumulator += cartItem.product.price * cartItem.amount, 0)
    })

    const orderPaymentStatusBoxVisible = ref(state?.orderId as boolean)
</script>

<template>
    <OrderPaymentStatusBox v-if="orderPaymentStatusBoxVisible"
                           :order-id="state?.orderId"
                           :payment-status="state?.paymentStatus"
                           @close="orderPaymentStatusBoxVisible = false"
    />

    <Loader v-if="cartLoading || ordersLoading"/>

    <div v-if="!cartLoading" class="cartPage">
        <div class="title">Корзина товаров</div>

        <div v-if="cart.length" class="cart">
            <div class="productsGrid">
                <CartItemCard v-for="(cartItem, index) in cart"
                              :cartItem="cartItem"
                              :animationDelay="0.3 + 0.1 * index"/>
            </div>

            <div class="totalPrice">Сумма: {{ totalPrice }}₽</div>

            <div class="buyButtonWrapper">
                <div class="buyButton" @click="createOrder">Оплатить</div>
            </div>
        </div>

        <div v-else class="noCartItems">Корзина пустая</div>
    </div>
</template>

<style scoped>
    .cartPage {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .title {
        display: flex;
        justify-content: center;
        align-items: center;

        width: 610px;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        user-select: none;

        will-change: opacity, filter, transform;
        animation: CartPageFadeIn 0.3s ease-out forwards;
    }

    .cart {
        display: grid;
        grid-template-areas:
            "products-grid products-grid"
            "price buy-button";
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .totalPrice {
        grid-area: price;
        justify-self: stretch;

        display: flex;
        justify-content: center;
        align-items: center;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        opacity: 0;
        user-select: none;

        will-change: opacity, filter, transform;
        animation: CartPageFadeIn 0.3s ease-out forwards;
    }

    .buyButtonWrapper {
        grid-area: buy-button;

        opacity: 0;
        will-change: background-color, color, transform, box-shadow, opacity, filter;
        animation: CartPageFadeIn 0.3s ease-out forwards;
    }

    .buyButton {
        grid-area: buy-button;
        justify-self: stretch;

        display: flex;
        justify-content: center;
        align-items: center;

        height: 70px;

        background-color: white;
        border-radius: 100px;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        user-select: none;
        cursor: pointer;

        transition: background-color ease-out,
        color 0.3s ease-out,
        transform 0.3s ease-out,
        box-shadow 0.3s ease-out;

        &:hover {
            background-color: var(--color-magenta);
            color: white;
            transform: scale(1.05);
            box-shadow: 0 0 30px 15px rgba(122, 137, 220, 0.3);
        }
    }

    .productsGrid {
        grid-area: products-grid;

        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;

        gap: 50px;
    }

    .noCartItems {
        display: flex;

        justify-content: center;
        align-items: center;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);
        text-transform: uppercase;

        width: 100%;
        min-height: 500px;
        border-radius: 100px;
        user-select: none;

        background-color: white;
        opacity: 0;

        will-change: transform, opacity, filter;
        animation: CartPageFadeIn 0.3s ease-out forwards;
    }

    @keyframes CartPageFadeIn {
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
</style>