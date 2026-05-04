import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import type { Product } from '../interfaces/ProductInterface.ts';
import type { StoreFilters } from '../interfaces/StoreFiltersInterface.ts';
import { API } from '../conf.ts';

interface State {
    store: Array<Product>,
    loading: boolean
}

export const fetchStore = createAsyncThunk(
    'store/fetchStore',
    async (
        { filters }: { filters: StoreFilters }
    ): Promise<Array<Product>> => {
        const url = new URL(`${API}/products/`)

        if (filters.type) url.searchParams.append('type', filters.type)
        if (filters.name) url.searchParams.append('name', filters.name)
        if (filters.priceMin) url.searchParams.append('price_min', filters.priceMin.toString())
        if (filters.priceMax) url.searchParams.append('price_max', filters.priceMax.toString())

        const response = await fetch(url)
        return await response.json()
    }
)

export const StoreSlice = createSlice({
    name: 'store',

    initialState: {
        store: [] as Array<Product>,
        loading: false
    } as State,

    reducers: {},

    extraReducers: (builder) => {
        builder
            // FETCH STORE
            .addCase(fetchStore.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchStore.fulfilled, (state, action) => {
                state.store = action.payload
                state.loading = false
            })
            .addCase(fetchStore.rejected, (state) => {
                state.store = []
                state.loading = false
            })
    }
})

export const storeReducer = StoreSlice.reducer