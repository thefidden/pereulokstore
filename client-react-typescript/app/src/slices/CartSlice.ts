import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import type { CartItem } from '../interfaces/CartItemInterface.ts';
import { API } from '../conf.ts';
import type { Product } from '../interfaces/ProductInterface.ts';
import { getCookie } from '../utils.ts';
import type { RootState } from "../store.ts";

interface State {
    cart: Array<CartItem>,
    loading: boolean
}

export const fetchCart = createAsyncThunk(
    'cart/fetchCart',

    async (): Promise<Array<CartItem>> => {
        const response = await fetch(`${ API }/carts/`, {
            method: 'GET',
            credentials: 'include'
        })
        const data = await response.json()
        return data.map(({ user, ...rest }) => rest)
    }
)

export const addCartItem = createAsyncThunk(
    'cart/addItem',

    async (
        { product }: { product: Product }
    ): Promise<CartItem> => {
        const response = await fetch(`${ API }/carts/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')!
            },
            body: JSON.stringify({
                productId: product.id
            })
        })
        return await response.json() as CartItem
    }
)

export const updateCartItem = createAsyncThunk(
    'cart/updateItem',

    async (
        { cartItem, amount }: { cartItem: CartItem, amount: number }
    ): Promise<CartItem> => {
        const response = await fetch(`${ API }/carts/${ cartItem.id }/`, {
            method: 'PATCH',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')!
            },
            body: JSON.stringify({
                'amount': amount
            })
        })
        return await response.json() as CartItem
    }
)

export const deleteCartItem = createAsyncThunk(
    'cart/deleteItem',

    async (
        { cartItem }: { cartItem: CartItem }
    ): Promise<CartItem> => {
        const response = await fetch(`${ API }/carts/${ cartItem.id }/`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')!
            }
        })
        return cartItem
    }
)

export const emptyCart = createAsyncThunk(
    'cart/emptyCart',

    async (_, { dispatch, getState }) => {
        const { cart } = (getState() as RootState).cart

        await Promise.all(
            cart.map(cartItem =>
                dispatch(deleteCartItem({ cartItem }))
            )
        )
    }
)

export const CartSlice = createSlice({
    name: 'cart',

    initialState: {
        cart: [] as Array<CartItem>,
        loading: false
    } as State,

    reducers: {},

    extraReducers: (builder) => {
        builder
            // FETCH CART
            .addCase(fetchCart.pending, (state) => {
                state.loading = true
            })
            .addCase(fetchCart.fulfilled, (state, action) => {
                state.cart = action.payload
                state.loading = false
            })
            .addCase(fetchCart.rejected, (state) => {
                state.cart = []
                state.loading = false
            })

            // ADD ITEM
            .addCase(addCartItem.pending, (state) => {
                state.loading = true
            })
            .addCase(addCartItem.fulfilled, (state, action) => {
                state.cart.push(action.payload)
                state.loading = false
            })
            .addCase(addCartItem.rejected, (state) => {
                state.loading = false
            })

            // UPDATE ITEM
            .addCase(updateCartItem.pending, (state) => {
                state.loading = true
            })
            .addCase(updateCartItem.fulfilled, (state, action) => {
                const newItem = action.payload
                state.cart = state.cart.map((oldItem: CartItem) =>
                    oldItem.id !== newItem.id
                        ? oldItem
                        : newItem
                )
                state.loading = false
            })
            .addCase(updateCartItem.rejected, (state) => {
                state.loading = false
            })

            // DELETE ITEM
            .addCase(deleteCartItem.pending, (state) => {
                state.loading = true
            })
            .addCase(deleteCartItem.fulfilled, (state, action) => {
                const deletedItem = action.payload
                state.cart = state.cart.filter((item: CartItem) =>
                    item.id !== deletedItem.id
                )
                state.loading = false
            })
            .addCase(deleteCartItem.rejected, (state) => {
                state.loading = false
            })

            // EMPTY CART
            .addCase(emptyCart.pending, (state) => {
                state.loading = true
            })
            .addCase(emptyCart.fulfilled, (state) => {
                state.loading = false
            })
            .addCase(emptyCart.rejected, (state) => {
                state.loading = false
            })
    }
})

export const cartReducer = CartSlice.reducer