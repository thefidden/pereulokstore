import { defineStore } from "pinia";

import type { Product } from "../interfaces/ProductInterface.ts";
import type { StoreFilters } from "../interfaces/StoreFiltersInterface.ts";


export const useStore = defineStore('store', {
    state: () => ({
        store: [] as Array<Product>,
        loading: false
    }),
    actions: {
        async fetch(filters: StoreFilters) {
            this.store = []
            this.loading = true

            const url = new URL(`/api/products/`, window.location.origin)

            if (filters.type) url.searchParams.append('type', filters.type)
            if (filters.name) url.searchParams.append('name', filters.name)
            if (filters.priceMin) url.searchParams.append('price_min', filters.priceMin.toString())
            if (filters.priceMax) url.searchParams.append('price_max', filters.priceMax.toString())

            try {
                const response = await fetch(url)
                this.store = await response.json()
            }
            catch (e) {
                console.log('fetchStore error:', e)
                this.store = []
            }
            finally {
                this.loading = false
            }
        }
    }
})