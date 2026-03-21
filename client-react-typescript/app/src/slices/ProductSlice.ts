import { createSlice, createAsyncThunk } from "@reduxjs/toolkit"
import type { Product } from "../interfaces/ProductInterface.ts";
import { API } from "../conf.ts";

interface State {
    product: Product | null,
    loading: boolean
}

export const fetchProduct = createAsyncThunk(
    "product/fetchProduct",
    async (productId: string): Promise<Product> => {
        const response = await fetch(`${API}/products/${productId}/`)
        const { id, name, type, description, price, images } = await response.json()
        return {
            id: id,
            name: name,
            type: type,
            description: description,
            price: price,
            images: images
        } as Product
    }
)

export const ProductSlice = createSlice({
    name: "product",

    initialState: {
        product: null,
        loading: false
    } as State,

    reducers: {},

    extraReducers: (builder) => {
        builder
            .addCase(fetchProduct.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchProduct.fulfilled, (state, action) => {
                state.product = action.payload
                state.loading = false
            })
            .addCase(fetchProduct.rejected, (state) => {
                state.loading = false
            })
    }
})