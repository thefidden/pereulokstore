import { defineStore } from "pinia";

import { HOST } from "../conf.ts";
import type { Product } from "../interfaces/ProductInterface.ts";


export const useProduct = defineStore("product", {
    state: () => ({
        product: null as Product | null,
        loading: false
    }),
    actions: {
        async fetch(productId: string) {
            this.loading = true

            try {
                const response = await fetch(`${HOST}/api/products/${productId}/`)
                const { id, name, type, description, price, images } = await response.json()
                this.product = { id, name, type, description, price, images }
            }
            catch (e) {
                this.product = null
                console.log("fetchProduct error:", e)
            }
            finally {
                this.loading = false
            }
        }
    }
})