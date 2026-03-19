<script setup lang="ts">
    import { useOrders } from "../stores/OrdersStore.ts";
    import { storeToRefs } from "pinia";
    import { ref, watch } from "vue";
    import Loader from "../components/Loader.vue";
    import ProductCard from "../components/ProductCard.vue";
    import { useRoute } from "vue-router";
    import OrderPaymentStatusBox from "../components/OrderPaymentStatusBox.vue";

    const route = useRoute()
    const state = history.state

    const ordersStore = useOrders()
    const { orders, loading: ordersLoading, reversed: ordersReversed } = storeToRefs(ordersStore)

    const orderPaymentStatusBoxVisible = ref(state?.orderId as boolean)

    const orderStatusTranslation = {
        pending_payment: "Ожидает оплаты",
        paid: "Оплачен",
        pending_assembly: "Собирается",
        assembled: "Собран",
        pending_pickup: "Готов к выдаче",
        picked_up: "Выдан покупателю",
        finished: "Завершен",
        cancelled: "Отменен"
    }

    watch(orders, () => console.log(orders.value))
</script>

<template>
    <OrderPaymentStatusBox v-if="orderPaymentStatusBoxVisible"
                           :order-id="state?.orderId"
                           :payment-status="state?.paymentStatus"
                           @close="orderPaymentStatusBoxVisible = false"
    />

    <Loader v-if="ordersLoading"/>

    <div v-else class="orders">
        <div class="title">Список заказов</div>

        <div v-if="orders.length" v-for="order in ordersReversed" class="order">
            <div class="orderId">Заказ: {{ order.id }}</div>
            <div class="orderPrice">Сумма: {{ order.price }}₽</div>
            <div class="orderStatus">Статус: {{ orderStatusTranslation[order.status] }}</div>

            <div class="orderProductsGrid">
                <ProductCard v-for="(orderItem, index) in order.items"
                             :product="orderItem.product"
                             :playAnimation="true"
                             :animationName="'slideIn'"
                             :animationDelay="0.3 + 0.1 * index"
                />
            </div>
        </div>

        <div v-else class="noOrders">ЗАКАЗЫ НЕ ОБНАРУЖЕНЫ</div>
    </div>
</template>

<style scoped>
    .orders {
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

        will-change: transform, opacity, filter;
        animation: OrdersPageFadeIn 0.3s ease-out forwards;
    }

    .orders {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .order {
        display: grid;
        grid-template-areas:
            "id _"
            "products-grid products-grid"
            "status price";
        grid-template-columns: 1fr 1fr;

        gap: 20px;

        width: 100%;
        min-height: 100px;
        box-sizing: border-box;
    }

    .orderId {
        grid-area: id;
        border-radius: 100px;
    }

    .orderPrice {
        grid-area: price;
        border-radius: 100px;
    }

    .orderStatus {
        grid-area: status;
        border-radius: 100px;
    }

    .orderId, .orderPrice, .orderStatus {
        display: flex;
        justify-content: center;
        align-items: center;

        padding: 20px 40px;

        background-color: var(--color-magenta);

        font-family: 'Jost', serif;
        font-size: 32px;
        font-weight: var(--font-weight-bold);
        color: white;
        text-wrap: nowrap;

        user-select: none;
        opacity: 0;

        will-change: transform, opacity, filter;
        animation: OrdersPageFadeIn 0.3s ease-out forwards;
    }

    .orderProductsGrid {
        grid-area: products-grid;

        display: flex;
        flex-wrap: wrap;
        justify-content: center;

        gap: 50px;

        box-sizing: border-box;
    }

    .noOrders {
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
        animation: OrdersPageFadeIn 0.3s ease-out forwards;
    }

    @keyframes OrdersPageFadeIn {
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