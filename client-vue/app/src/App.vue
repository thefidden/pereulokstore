<script setup lang="ts">
    import Header from "./components/Header.vue";
    import { useUser } from "./stores/UserStore.ts";
    import { onMounted } from "vue";
    import { useCart } from "./stores/CartStore.ts";
    import { useOrders } from "./stores/OrdersStore.ts";

    const { fetch: fetchUser } = useUser()
    const { fetch: fetchCart } = useCart()
    const { fetch: fetchOrders } = useOrders()

    onMounted(() => {
        fetchUser()
        fetchCart()
        fetchOrders()
    })
</script>

<template>
    <div class="root">
        <Header/>
        <router-view/>
    </div>
</template>

<style scoped>
    .root {
        display: flex;
        flex-direction: column;

        max-width: 1440px;

        padding: 40px 0;
        margin: 0 auto;

        gap: 80px;

        font-family: 'Jost', serif;
    }
</style>
