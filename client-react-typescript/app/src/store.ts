import { configureStore } from "@reduxjs/toolkit"
import { userReducer } from "./slices/UserSlice.ts"

export const store = configureStore({
    reducer: {
        user: userReducer
    }
})