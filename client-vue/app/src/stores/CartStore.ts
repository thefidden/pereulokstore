import { defineStore } from "pinia";
import { API, HOST } from "../conf.ts";
import type { CartItem } from "../interfaces/CartItemInterface.ts";
import type { Product } from "../interfaces/ProductInterface.ts";
import { getCookie } from "../utils.ts";

export const useCart = defineStore("cart", {
    state: () => ({
        cart: [] as Array<CartItem>,
        loading: false
    }),
    actions: {
        async fetch() {
            this.loading = true

            try {
                const response = await fetch(`${HOST}/api/carts/`, {
                    method: "GET",
                    credentials: "include"
                })
                const data = await response.json()
                for (const item of data) delete item.user
                this.cart = data
            }
            catch (e) {
                console.log("fetchCart error:", e)
                this.cart = []
            }
            finally {
                this.loading = false
            }
        },

        get(product: Product): CartItem | null {
            return this.cart.find((cartItem: CartItem) => cartItem.product.id === product.id) ?? null
        },

        async add(product: Product) {
            this.loading = true

            try {
                const response = await fetch(`${HOST}/api/carts/`, {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")!!
                    },
                    body: JSON.stringify({
                        productId: product.id
                    })
                })
                const cartItem: CartItem = await response.json()
                this.cart.push(cartItem)
            }
            catch (e) {
                console.log("addToCart error:", e)
            }
            finally {
                this.loading = false
            }
        },

        async update(cartItem: CartItem, amount: number) {
            this.loading = true

            try {
                const response = await fetch(`${API}/carts/${cartItem.id}/`, {
                    method: "PATCH",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")!!
                    },
                    body: JSON.stringify({
                        "amount": amount
                    })
                })
                const newItem = await response.json() as CartItem

                this.cart = this.cart.map((oldItem: CartItem) =>
                    oldItem.id !== newItem.id
                    ? oldItem
                    : newItem
                )
            }
            catch (e) {
                console.log("updateCartItem error:", e)
            }
            finally {
                this.loading = false
            }
        },

        async delete(cartItem: CartItem) {
            this.loading = true

            try {
                const response = await fetch(`${API}/carts/${cartItem.id}/`, {
                    method: "DELETE",
                    credentials: "include",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")!!
                    }
                })
                this.cart = this.cart.filter((item: CartItem) => item.id !== cartItem.id)
            }
            catch (e) {
                console.log("deleteCartItem error:", e)
            }
            finally {
                this.loading = false
            }
        },

        async empty() {
            this.loading = true
            const cart = this.cart

            try {
                this.cart.forEach((cartItem: CartItem) => this.delete(cartItem))
            }
            catch (e) {
                this.cart = cart
                console.log()
            }
            finally {
                this.loading = false
            }
        }
    }
})