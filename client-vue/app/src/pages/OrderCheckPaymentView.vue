<script setup lang="ts">
    import { useRouter } from "vue-router";
    import { onMounted} from "vue";

    import { useOrders } from "../stores/OrdersStore.ts";
    import Loader from "../components/Loader.vue";
    import { useCart } from "../stores/CartStore.ts";

    const { orderId, bankOrderId } = defineProps<{
        orderId: string,
        bankOrderId: string
    }>()
    const router = useRouter()

    const ordersStore = useOrders()
    const cartStore = useCart()

    const { fetchPaymentStatus } = ordersStore
    const { empty: emptyCart } = cartStore

    onMounted(async () => {
        try {
            const status = await fetchPaymentStatus(orderId, bankOrderId)

            if (status === "successful") {
                await emptyCart()
                await router.replace({
                    path: "/orders",
                    state: {
                        orderId: orderId,
                        paymentStatus: status
                    }
                })
            }

            if (status === "failure") {
                await router.replace({
                    path: "/cart",
                    state: {
                        orderId: orderId,
                        paymentStatus: status
                    }
                })
            }
        }
        catch (e) {
            console.log(e)
        }
    })
</script>

<template>
    <Loader/>
</template>

<style scoped>

</style>