import { createWebHistory, createRouter, type RouteLocationNormalized } from "vue-router";

import CartView from "./pages/CartView.vue";
import StoreView from "./pages/StoreView.vue";
import ProductView from "./pages/ProductView.vue";
import OrdersView from "./pages/OrdersView.vue";
import OrderCheckPaymentView from "./pages/OrderCheckPaymentView.vue";
import TestView from "./pages/TestView.vue";
import AboutView from "./pages/AboutView.vue";
import { useStore } from "./stores/StoreStore.ts";
import { useProduct } from "./stores/ProductStore.ts";


export default createRouter({
    history: createWebHistory(),

    routes: [
        { path: "/", name: "main", redirect: "/store?type=suit" },
        { path: "/about", name: "about", component: AboutView },
        {
            path: "/store",
            name: "store",
            component: StoreView,
            props: (route: RouteLocationNormalized) => ({ ...route.query, ...route.params }),
            beforeEnter: async (to: RouteLocationNormalized) => {
                const { fetch: fetchStore } = useStore()
                await fetchStore({
                    type: to.query.type as string,
                    name: to.query.name as string,
                    priceMin: parseInt(to.query.priceMin as string),
                    priceMax: parseInt(to.query.priceMax as string)
                })
            }
        },
        {
            path: "/products/:productUUID",
            name: "product",
            component: ProductView,
            beforeEnter: async (to: RouteLocationNormalized) => {
                const { fetch: fetchProduct } = useProduct()
                await fetchProduct(to.params.productUUID as string)
            }
        },
        { path: "/cart", name: "cart", component: CartView },
        { path: "/orders", name: "orders", component: OrdersView },
        {
            path: "/orders/:orderUUID/payment/check",
            name: "orderPaymentCheck",
            component: OrderCheckPaymentView,
            props: (route: RouteLocationNormalized) => ({
                orderId: route.params.orderUUID,
                bankOrderId: route.query.orderId
            })
        },
        { path: "/test", component: TestView }
    ]
})