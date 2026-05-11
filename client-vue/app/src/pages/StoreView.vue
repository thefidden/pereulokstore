<script setup lang = "ts">
    import { onBeforeRouteUpdate } from "vue-router";
    import { storeToRefs } from "pinia";
    import type { RouteLocationNormalized } from "vue-router";

    import { useStore } from "../stores/StoreStore.ts";
    import ProductCard from "../components/ProductCard.vue";
    import Loader from "../components/Loader.vue";
    import { useUser } from "../stores/UserStore.ts";

    const userStore = useUser()
    const storeStore = useStore()

    const { user, loading: userLoading } = storeToRefs(userStore)

    const { fetch: fetchStore } = storeStore
    const { store, loading: storeLoading } = storeToRefs(storeStore)

    onBeforeRouteUpdate(async (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
        await fetchStore({
            type: to.query.type as string,
            name: to.query.name as string,
            priceMin: parseInt(to.query.priceMin as string),
            priceMax: parseInt(to.query.priceMax as string)
        })
    })
</script>

<template>
    <Loader v-if = "userLoading || storeLoading"/>

    <div v-else class = 'productsGrid'>
        <ProductCard
            v-if = "store.length"
            v-for = "(product, index) in store"
            :product = "product"
            :animationDelay = "0.1 * index"
        />
        <div v-else class = 'noProducts'>Товары не найдены</div>
    </div>
</template>

<style scoped>
    .productsGrid {
        display: flex;
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;

        gap: 50px;
    }

    .noProducts {
        display: flex;

        justify-content: center;
        align-items: center;

        font-family: 'Jost', serif;
        font-size: 48px;
        font-weight: var(--font-weight-bold);
        color: var(--color-magenta);

        width: 100%;
        min-height: 500px;
        border-radius: 100px;
        user-select: none;
    }
</style>