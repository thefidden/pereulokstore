import { defineStore } from "pinia";
import type { Order } from "../interfaces/OrderInterface.ts";
import { API } from "../conf.ts";
import type { OrderItem } from "../interfaces/OrderItemInterface.ts";
import { getCookie } from "../utils.ts";


export const useOrders = defineStore("orders", {
    state: () => ({
        orders: [] as Array<Order>,
        loading: false
    }),

    getters: {
        reversed: (state) => [...state.orders].reverse()
    },

    actions: {
        async fetch(): Promise<void> {
            this.loading = true

            try {
                const response = await fetch(`${API}/orders/`, {
                    method: "GET",
                    credentials: "include"
                })
                const data: Array<any> = await response.json()
                this.orders = data.map(order => (
                    {
                        id: order.id,
                        price: order.price,
                        status: order.status,
                        items: order.products.map((orderItem: any) => (
                            {
                                product: orderItem.product,
                                price: orderItem.price,
                                amount: orderItem.amount
                            } as OrderItem
                        ))
                    } as Order
                ))
            }
            catch (e) {
                console.log("fetchOrders error:", e)
                this.orders = []
            }
            finally {
                this.loading = false
            }
        },

        async create(): Promise<void> {
            this.loading = true

            try {
                const response = await fetch(`${API}/orders/`, {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")!!
                    }
                })
                const { order, formUrl } = await response.json()
                this.orders.push(
                    {
                        id: order.id,
                        price: order.price,
                        status: order.status,
                        items: order.products.map((orderItem: any) => (
                            {
                                product: orderItem.product,
                                price: orderItem.price,
                                amount: orderItem.amount
                            } as OrderItem
                        ))
                    } as Order
                )
                window.open(formUrl, '_blank')
            }
            catch (e) {
                console.log("createOrder error:", e)
            }
            finally {
                this.loading = false
            }
        },

        async fetchPaymentStatus(orderId: string, bankOrderId: string): Promise<'successful' | 'failure'> {
            this.loading = true

            try {
                const response = await fetch(`${API}/orders/${orderId}/payment/check/?bankOrderId=${bankOrderId}`, {
                    credentials: "include"
                })
                const { paymentStatus } = await response.json()
                return paymentStatus
            }
            catch (e) {
                console.log("checkOrderPaymentStatus error:", e)
                throw e
            }
            finally {
                this.loading = false
            }
        }
    }
})